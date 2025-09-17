import gradio as gr
import matplotlib.pyplot as plt
import pandas as pd
import sqlite3
import io
from PIL import Image
from langchain_community.llms import OpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
import logging

logging.basicConfig(level=logging.INFO)

logging.info("Starting setup")

def setup_llm():
    llm = OpenAI(temperature=0)
    
    prompt_template = """
    Given the following user question about data, convert it to a valid SQL query.
    If you do joins, always explicite the table names before the column

    Database schemas
    - Table: user_info
    - schema columns: user_id INTEGER , age INTEGER, gender TEXT, name TEXT, lastname TEXT

    - Table: sell_info
    - schema columns: user_id INTEGER , item_id INTEGER , date INTEGER, value INTEGER

    - Table: items_info
    - schema columns: item_id INTEGER , item_name TEXT, category TEXT

    User question: {question}
    
    SQL Query (return only the SQL, no explanation):
    """
    
    prompt = PromptTemplate(template=prompt_template, input_variables=["question"])
    return LLMChain(llm=llm, prompt=prompt)

def execute_sql_query(sql_query, db_path="data.db"):
    try:
        conn = sqlite3.connect(db_path)
        df = pd.read_sql_query(sql_query, conn)
        logging.info(f"SQL Query executed successfully: {df}")
        conn.close()
        return df, None
    except Exception as e:
        logging.error(f"Error executing SQL Query: {e}")
        return None, str(e)

def create_visualization(df, query_type):
    plt.close()

    if (len(df) == 1):
        return df.to_string()

    if df.empty:
        plt.text(0.5, 0.5, 'No data found', ha='center', va='center')
        plt.title("No Results")
    else:
        if len(df.columns) >= 2 and df.dtypes.iloc[1] in ['int64', 'float64']:
            df.plot(x=df.columns[0], y=df.columns[1], kind='bar')
            plt.title("Query Results")
            plt.xticks(rotation=45)
        else:
            plt.text(0.1, 0.5, df.to_string(), fontfamily='monospace', fontsize=8)
            plt.title("Query Results (Table)")
            plt.axis('off')
    
    plt.tight_layout()
    fig = plt.gcf()
    
    buf = io.BytesIO()
    fig.savefig(buf, format='png', dpi=100, bbox_inches='tight')
    buf.seek(0)
    
    pil_img = Image.open(buf)
    return gr.Image(pil_img)

def chat_with_plot(message, history):
    try:
        llm_chain = setup_llm()
        
        sql_query = llm_chain.run(question=message)
        logging.info(f"Generated SQL Query: {sql_query}")
        sql_query = sql_query.strip()
        
        df, error = execute_sql_query(sql_query)
        
        if error:
            plt.close()
            plt.text(0.5, 0.5, f'SQL Error: {error}', ha='center', va='center')
            plt.title("Error")
            fig = plt.gcf()
            buf = io.BytesIO()
            fig.savefig(buf, format='png')
            buf.seek(0)
            pil_img = Image.open(buf)
            return gr.Image(pil_img)
        
        result_img = create_visualization(df, message)
        return [result_img,f"Query: \n {sql_query}"]
        
    except Exception as e:
        plt.close()
        plt.text(0.5, 0.5, f'Error: {str(e)}', ha='center', va='center')
        plt.title("Error")
        fig = plt.gcf()
        buf = io.BytesIO()
        fig.savefig(buf, format='png')
        buf.seek(0)
        pil_img = Image.open(buf)
        return gr.Image(pil_img)

demo = gr.ChatInterface(fn=chat_with_plot)
demo.launch()