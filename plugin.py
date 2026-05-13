import gradio as gr
from plugins import WAN2GPPlugin
import os
import base64

class CanvasEditorPlugin(WAN2GPPlugin):
    def __init__(self):
        super().__init__()
        self.name = "Canvas Editor"
        self.version = "1.1.0"
        self.description = "Un potente canvas per disegnare, modificare e inviare immagini al Reference Image in Wan2GP."

    def setup_ui(self):
        self.add_tab(
            tab_id="canvas_editor_tab",
            label="Canvas Editor",
            component_constructor=self.create_canvas_ui,
            position=2
        )

    def create_canvas_ui(self):
        plugin_dir = os.path.dirname(os.path.abspath(__file__))
        html_path = os.path.join(plugin_dir, "dist", "index.html")
        
        iframe_html = ""
        try:
             import html
             with open(html_path, "r", encoding="utf-8") as f:
                 html_content = f.read()
             escaped_html = html.escape(html_content, quote=True)
             iframe_html = f'<iframe srcdoc="{escaped_html}" width="100%" height="900px" style="border: none; border-radius: 8px; overflow: hidden; background: #000;"></iframe>'
        except Exception as e:
             iframe_html = f"<p>Error loading canvas UI from {html_path}: {str(e)}</p>"

        with gr.Blocks() as demo:
            gr.Markdown("### Wan2GP Canvas Editor by Fred Campzilla")
            gr.HTML(iframe_html)
            
        return demo
