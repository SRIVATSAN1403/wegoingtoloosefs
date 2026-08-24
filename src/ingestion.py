import json
import logging
import random
import sys
import time
import threading
from typing import Dict, Any, Optional
import pandas as pd

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(name)s: %(message)s")
logger = logging.getLogger("PyroTrace.Ingestion")

try:
    import serial
    import serial.tools.list_ports
    HAS_PYSERIAL = True
except ImportError:
    HAS_PYSERIAL = False
    logger.warning("pyserial module not found. Operating in simulation fallback mode.")


class SerialIngestor:
    """
    PyroTrace Edge Telemetry Ingestor.
    Reads JSON telemetry over serial (target COM15) or generates mock telemetry
    if hardware is disconnected. Maintains a rolling 60-second Pandas DataFrame buffer.
    """

    def __init__(self, port: str = "COM15", baudrate: int = 115200, window_seconds: int = 60):
        self.port = port
        self.baudrate = baudrate
        self.window_seconds = window_seconds
        
        # Thread safety & state control
        self._lock = threading.Lock()
        self._running = False
        self._thread: Optional[threading.Thread] = None
        self._use_simulation = False
        self._serial_conn = None
        
        # Fault injection state for testing/demo
        self._active_fault_mode = 0  # 0: Normal, 1: Thermal Spike, 2: Fan Failure, 3: CPU Load Surge
        self._step_counter = 0

        # Buffer columns: timestamp (Unix or relative seconds), temp (°C), rpm (RPM), cpu_load (%), fault_mode
        self.columns = ["timestamp", "temp", "rpm", "cpu_load", "fault_mode", "datetime"]
        self._buffer = pd.DataFrame(columns=self.columns)

    def is_port_available(self, target_port: str) -> bool:
        """Check if target COM port exists on system."""
        if not HAS_PYSERIAL:
            return False
        ports = [p.device for p in serial.tools.list_ports.comports()]
        return target_port in ports

    def start(self) -> None:
        """Start background ingestion thread."""
        if self._running:
            logger.info("Ingestor already running.")
            return

        self._running = True
        self._thread = threading.Thread(target=self._ingestion_loop, daemon=True)
        self._thread.start()
        logger.info(f"Started telemetry ingestion pipeline on port={self.port}, window={self.window_seconds}s.")

    def stop(self) -> None:
        """Stop background ingestion thread."""
        self._running = False
        if self._thread and self._thread.is_alive():
            self._thread.join(timeout=2.0)
        if self._serial_conn and self._serial_conn.is_open:
            try:
                self._serial_conn.close()
            except Exception as e:
                logger.error(f"Error closing serial port: {e}")
        logger.info("Stopped telemetry ingestion pipeline.")

    def set_fault_mode(self, mode: int) -> None:
        """Inject a fault mode manually into the ingestion stream (0: Normal, 1: Temp, 2: Fan, 3: CPU)."""
        with self._lock:
            self._active_fault_mode = mode
            logger.info(f"Ingestor fault mode set to: {mode}")

    def get_buffer(self) -> pd.DataFrame:
        """Retrieve a thread-safe copy of the 60-second rolling buffer DataFrame."""
        with self._lock:
            return self._buffer.copy()

    def get_latest_sample(self) -> Optional[Dict[str, Any]]:
        """Get the single most recent telemetry payload."""
        with self._lock:
            if not self._buffer.empty:
                return self._buffer.iloc[-1].to_dict()
            return None

    def is_hardware_connected(self) -> bool:
        """Returns True if physically connected to serial port, False if using simulation fallback."""
        return not self._use_simulation and (self._serial_conn is not None and self._serial_conn.is_open)

    def _try_connect_serial(self) -> bool:
        """Attempt to open hardware serial port."""
        if not HAS_PYSERIAL:
            return False

        try:
            if self.is_port_available(self.port):
                self._serial_conn = serial.Serial(self.port, self.baudrate, timeout=1.0)
                logger.info(f"Successfully connected to hardware Serial port {self.port} at {self.baudrate} baud.")
                self._use_simulation = False
                return True
            else:
                logger.info(f"Target port {self.port} not found on system. Falling back to edge simulation engine.")
                self._use_simulation = True
                return False
        except Exception as e:
            logger.warning(f"Could not connect to serial port {self.port}: {e}. Using simulation mode.")
            self._use_simulation = True
            return False

    def _generate_mock_payload(self) -> Dict[str, Any]:
        """Generate high-fidelity hardware sensor telemetry when physical ESP32 is absent."""
        self._step_counter += 1
        now_ts = time.time()

        temp = 35.0 + random.uniform(-1.0, 1.0)
        rpm = 3200 + random.randint(-35, 35)
        cpu_load = 25.0 + random.uniform(-2.0, 2.0)

        # Apply fault dynamics
        mode = self._active_fault_mode
        if mode == 1:
            # Thermal spike
            temp += min(50.0, (self._step_counter % 60) * 1.8)
            cpu_load += 10.0
        elif mode == 2:
            # Fan bearing failure: RPM drops -> Temp increases
            rpm = max(400, 3200 - ((self._step_counter % 60) * 75))
            if rpm < 1500:
                temp += (1500 - rpm) * 0.025
        elif mode == 3:
            # CPU Load Surge: CPU 90-100% -> Temp spikes
            cpu_load = min(100.0, 88.0 + random.uniform(0, 10))
            temp += 22.0 + random.uniform(-1.0, 1.0)
            rpm += 550

        return {
            "timestamp": round(now_ts, 2),
            "temp": round(temp, 1),
            "rpm": int(rpm),
            "cpu_load": round(cpu_load, 1),
            "fault_mode": mode,
            "datetime": pd.to_datetime(now_ts, unit="s")
        }

    def _process_payload(self, data: Dict[str, Any]) -> None:
        """Append sample to rolling DataFrame buffer and prune rows older than window_seconds."""
        now_ts = data.get("timestamp", time.time())
        if "datetime" not in data:
            data["datetime"] = pd.to_datetime(now_ts, unit="s")

        with self._lock:
            # Create single row DataFrame
            new_row = pd.DataFrame([data])
            self._buffer = pd.concat([self._buffer, new_row], ignore_index=True)

            # Keep buffer strictly within rolling window_seconds
            cutoff_ts = now_ts - self.window_seconds
            self._buffer = self._buffer[self._buffer["timestamp"] >= cutoff_ts].reset_index(drop=True)

            # Cap max length to 120 samples as upper bound safeguard for memory stability
            if len(self._buffer) > 120:
                self._buffer = self._buffer.iloc[-120:].reset_index(drop=True)

    def _ingestion_loop(self) -> None:
        """Main background thread loop for serial or simulation ingestion."""
        self._try_connect_serial()

        while self._running:
            try:
                if not self._use_simulation and self._serial_conn and self._serial_conn.is_open:
                    line = self._serial_conn.readline().decode("utf-8", errors="ignore").strip()
                    if line:
                        try:
                            payload = json.loads(line)
                            payload["datetime"] = pd.to_datetime(payload.get("timestamp", time.time()), unit="s")
                            self._process_payload(payload)
                        except json.JSONDecodeError:
                            logger.debug(f"Skipping unparseable serial line: {line}")
                    else:
                        time.sleep(0.05)
                else:
                    # Simulation mode telemetry stream (1 Hz)
                    payload = self._generate_mock_payload()
                    self._process_payload(payload)
                    time.sleep(1.0)
            except Exception as e:
                logger.error(f"Error in ingestion thread loop: {e}")
                time.sleep(1.0)


# Quick verification script if run directly
if __name__ == "__main__":
    print("Testing PyroTrace Telemetry Ingestor (Phase 1 & 2)...")
    ingestor = SerialIngestor(port="COM15", window_seconds=60)
    ingestor.start()

    print("Ingesting telemetry data for 5 seconds...")
    time.sleep(5)

    buffer_df = ingestor.get_buffer()
    print(f"Buffer Row Count: {len(buffer_df)}")
    print("Sample Telemetry Buffer:")
    print(buffer_df.tail())

    ingestor.stop()
    print("Ingestion test completed cleanly.")
