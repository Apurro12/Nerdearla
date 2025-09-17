# Simple Response Application

This application creates a Gradio chat interface that converts natural language questions into SQL queries and visualizes the results.

## Application Flow

```mermaid
flowchart TD
    A[User Input via Gradio Chat] --> B[chat_with_plot function]
    B --> C[setup_llm]
    C --> D[Create OpenAI LLM with prompt template]
    D --> E[Generate SQL Query from user question]
    E --> F[execute_sql_query]
    F --> G{SQL Execution Success?}
    G -->|No| H[Create Error Visualization]
    G -->|Yes| I[create_visualization]
    I --> J{Data Processing}
    J -->|Single Row| K[Return String Format]
    J -->|Empty Data| L[Create 'No Data' Plot]
    J -->|Multiple Rows with Numeric Data| M[Create Bar Chart]
    J -->|Other Data| N[Create Table Text Plot]
    H --> O[Return Error Image]
    K --> P[Return Result + Query]
    L --> Q[Return Plot Image + Query]
    M --> Q
    N --> Q
    O --> R[Display in Gradio Interface]
    P --> R
    Q --> R

    style A fill:#e1f5fe
    style R fill:#c8e6c9
    style G fill:#fff3e0
    style J fill:#fff3e0
```

## Database Schema

```mermaid
erDiagram
    user_info {
        INTEGER user_id
        INTEGER age
        TEXT gender
        TEXT name
        TEXT lastname
    }
    
    sell_info {
        INTEGER user_id
        INTEGER item_id
        INTEGER date
        INTEGER value
    }
    
    items_info {
        INTEGER item_id
        TEXT item_name
        TEXT category
    }
    
    user_info ||--o{ sell_info : "user_id"
    items_info ||--o{ sell_info : "item_id"
```

## Function Dependencies

```mermaid
graph LR
    A[main.py] --> B[setup_llm]
    A --> C[execute_sql_query]
    A --> D[create_visualization]
    A --> E[chat_with_plot]
    
    E --> B
    E --> C
    E --> D
    
    B --> F[OpenAI LLM]
    B --> G[PromptTemplate]
    B --> H[LLMChain]
    
    C --> I[SQLite Connection]
    C --> J[Pandas DataFrame]
    
    D --> K[Matplotlib Plotting]
    D --> L[PIL Image Processing]
    D --> M[Gradio Image Component]
    
    E --> N[Gradio ChatInterface]
```