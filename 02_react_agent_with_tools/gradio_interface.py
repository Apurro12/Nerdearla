import gradio as gr
from agent import chat, chat_async

demo = gr.ChatInterface(fn=chat)
demo.launch()