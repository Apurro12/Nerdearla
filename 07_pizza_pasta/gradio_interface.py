import gradio as gr
from utils import run_agent_with_stop

demo = gr.ChatInterface(fn=run_agent_with_stop)
demo.launch()