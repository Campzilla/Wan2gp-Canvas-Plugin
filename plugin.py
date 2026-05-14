import gradio as gr
import os

from shared.utils.plugins import WAN2GPPlugin

class CanvasEditorPlugin(WAN2GPPlugin):
    def __init__(self):
        super().__init__()
        self.name = "Canvas Editor"
        self.version = "1.2.0"
        self.description = "Un potente canvas per disegnare, modificare e inviare immagini al Reference Image in Wan2GP."

    def setup_ui(self):
        self.add_tab("canvas_editor_tab", "🎨 Canvas Editor", self.create_canvas_ui, position=5)

    def create_canvas_ui(self):
        import html
        import os
        
        plugin_dir = os.path.dirname(os.path.abspath(__file__))
        html_path = os.path.join(plugin_dir, "index.html")
        
        with open(html_path, "r", encoding="utf-8") as f:
            html_content = f.read()
            
        escaped_html = html.escape(html_content, quote=True).replace('\n', '&#10;').replace('\r', '&#13;')
        
        iframe_code = f"""
        <div style="width: 100%; height: 850px; background: #f8fafc; border-radius: 12px; overflow: hidden; border: 1px solid #e2e8f0;">
            <iframe srcdoc="{escaped_html}" sandbox="allow-scripts allow-same-origin allow-downloads allow-forms allow-popups" allow="clipboard-read; clipboard-write; display-capture" style="width: 100%; height: 100%; border: none;"></iframe>
        </div>
        """
        
        with gr.Blocks() as demo:
            gr.HTML(iframe_code)
        return demo
