import gradio as gr
from agent import run_agent_with_stop

demo = gr.ChatInterface(fn=run_agent_with_stop)
demo.launch()