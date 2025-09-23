import gradio as gr
from agent import chat_async

demo = gr.ChatInterface(fn=chat_async)
demo.launch()