# AI Developer Guidelines: PyroTrace

## 1. Strict Documentation Adherence
*   **Architecture Mandate:** You must strictly follow the system structures, hardware constraints, and offline data flows explicitly defined in `architecture.md`. Do not suggest, implement, or hallucinate cloud-based workarounds.
*   **Design Mandate:** You must strictly adhere to the UI/UX guidelines, color schemes, and visualization constraints outlined in `design.md`. Maintain the required dark-themed Streamlit and Plotly aesthetics without deviation.

## 2. File Protection & Retention
*   **Zero Deletion Policy:** Under no circumstances are you permitted to delete, remove, or suggest the removal of any `.md` (Markdown) files in this repository. 
*   **Documentation Preservation:** All documentation files, including project plans and folder structures, are critical for project alignment and must be preserved exactly as they are. You may read them for context, but you cannot delete them.

## 3. Implementation Guardrails
*   **Performance:** Ensure all Python logic remains optimized to handle the rolling 60-second Pandas dataframe without causing memory leaks or execution lag.
*   **Scope:** Do not introduce heavy, enterprise-grade dependencies (like full Bayesian AI models) unless specifically instructed to upgrade the existing scikit-learn Isolation Forest setup.