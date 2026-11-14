# DocuAgent Architecture

```mermaid
flowchart TD
    A["User selects Python Project"] --> B["Streamlit Web Interface"]
    B --> C["LangGraph Workflow"]
    C --> D["Information Extraction Agent"]
    D --> E["Documentation Planning Agent"]
    E --> F["Documentation Generation Agent"]
    F --> G["Documentation Validation Agent"]
    G --> H{"Validation Result"}
    H -->|PASS| I["Final Technical Documentation"]
    H -->|Review Required| J["Validation Report"]
    I --> K["Markdown Output"]
    J --> L["Improvement Suggestions"]
    E -.-> M["Ollama - Qwen 2.5 Coder 7B"]
    F -.-> M
    G -.-> M