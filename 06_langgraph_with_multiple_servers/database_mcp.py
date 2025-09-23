
from mcp.server.fastmcp import FastMCP
import dotenv
import json 
import sqlite3
import pandas as pd
import io
from PIL import Image
import gradio as gr
import base64
import logging 
from langchain_community.llms import OpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from matplotlib import pyplot as plt
from typing import Any


logging.basicConfig(level=logging.INFO)
logging.info("Starting setup")

dotenv.load_dotenv()

mcp = FastMCP("database")

@mcp.tool()
def extract_data_from_database() -> str:
    """
    Get the instructions on how to extract data from a database.

    Args:
        database_id: the id of the database
    """
    return json.dumps({"steps": [
        "First of all always execute the tool get_database_schema, "
        "Once you have the schema use the tool transform_natural_languaje_to_sql",
        "Once you have the corresponding sql use the tool execute_sql_query"]})

@mcp.tool()
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

@mcp.tool()
def get_database_schema():
    """
    Get the database schema information.
    """
    return json.dumps({
        "user_info": {
            "columns": ["user_id INTEGER", "age INTEGER", "gender TEXT", "name TEXT", "lastname TEXT"]
        },
        "sell_info": {
            "columns": ["user_id INTEGER", "item_id INTEGER", "date INTEGER", "value INTEGER"]
        },
        "items_info": {
            "columns": ["item_id INTEGER", "item_name TEXT", "category TEXT"]
        }
    })

@mcp.tool()
def transform_natural_languaje_to_sql(user_question: str) -> str:
    llm = OpenAI(temperature=0)
    
    prompt_template = """
    Given the following user question about data, convert it to a valid SQL query.
    If you do joins, always explicite the table names before the column.
    Before generating the SQL, first get the database schema using the tool 'get_database_schema'.

    User question: {question}
    
    SQL Query (return only the SQL, no explanation):
    """

    
    prompt = PromptTemplate(template=prompt_template, input_variables=["question"])
    llm_chain = LLMChain(llm=llm, prompt=prompt)
    sql_query = llm_chain.run(question=prompt)

    return sql_query

mcp.run(transport="streamable-http")
#mcp.run(transport="stdio")