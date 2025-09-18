import gradio as gr
from decoupled_yield import run_agent

demo = gr.ChatInterface(fn=run_agent)
demo.launch()