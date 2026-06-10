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
        self.request_component("image_start")
        self.request_component("main_tabs")
        self.request_component("image_start_row")
        self.request_component("image_prompt_type_radio")
        
        # Components for Inject Reference Images > Conditional Images
        self.request_component("image_refs")
        self.request_component("image_refs_row")
        self.request_component("video_prompt_type_image_refs")

        # Try to apply the safe preprocess patch at setup time
        try:
            self._apply_safe_radio_patch()
        except Exception as e:
            print(f"Canvas Editor Plugin: Initial safety patch deferred: {e}")

        self.add_tab("canvas_editor_tab", "🎨 Canvas Editor", self.create_canvas_ui, position=5)

    def _apply_safe_radio_patch(self):
        if hasattr(self, "image_prompt_type_radio") and self.image_prompt_type_radio is not None:
            # Check if already patched to prevent recursion
            if getattr(self.image_prompt_type_radio, "_is_safe_patched", False):
                return
            original_preprocess = self.image_prompt_type_radio.preprocess
            def safe_preprocess(x):
                try:
                    choices = getattr(self.image_prompt_type_radio, "choices", []) or []
                    choice_vals = [c[1] if (isinstance(c, (list, tuple)) and len(c) > 1) else c for c in choices]
                    choice_vals = [c for c in choice_vals if c is not None]
                    if x is not None and x not in choice_vals:
                        print(f"Canvas Editor Plugin Safe-Radio: Intercepted invalid value '{x}' not in choices {choice_vals}. Sanitizing to prevent Gradio crash.")
                        if choice_vals:
                            valid_vals = [v for v in choice_vals if v != '']
                            if valid_vals:
                                return valid_vals[0]
                            return choice_vals[0]
                        return None
                except Exception as e:
                    print(f"Canvas Editor Plugin Safe-Radio error checking: {e}")
                return original_preprocess(x)
            self.image_prompt_type_radio.preprocess = safe_preprocess
            self.image_prompt_type_radio._is_safe_patched = True
            print("Canvas Editor Plugin Safe-Radio: Successfully applied safety patch to image_prompt_type_radio.")

    def set_reference_image(self, b64_str):
        import base64
        import io
        import re
        from PIL import Image

        # Apply safety patch on-demand when sending reference images to prevent any choice validation crash
        try:
            self._apply_safe_radio_patch()
        except Exception as patch_err:
            print(f"Canvas Editor Plugin: Fallback safety patch failed: {patch_err}")

        # default updates dict
        updates = {}
        if hasattr(self, "outputs_list") and self.outputs_list:
            for comp in self.outputs_list:
                updates[comp] = gr.update()
        else:
            for comp in getattr(self, "outputs_list", []) or []:
                if comp is not None:
                    updates[comp] = gr.update()

        if not b64_str:
            return updates
        
        try:
            image_data = re.sub('^data:image/.+;base64,', '', b64_str)
            image = Image.open(io.BytesIO(base64.b64decode(image_data)))
            
            # Select Video Generation tab
            if getattr(self, "main_tabs", None) is not None:
                updates[self.main_tabs] = gr.update(selected="video_gen")
                
            # Specify the image_refs as the specific output
            if getattr(self, "image_refs", None) is not None:
                updates[self.image_refs] = [(image, "Canvas Editor")]
                print("Canvas Editor Plugin: Successfully sent canvas image to 'image_refs'")
                # Show the image ref row
                if getattr(self, "image_refs_row", None) is not None:
                    updates[self.image_refs_row] = gr.update(visible=True)
                
                # Switch the dropdown "Inject Reference Images" to "I" (People / Objects)
                if getattr(self, "video_prompt_type_image_refs", None) is not None:
                    updates[self.video_prompt_type_image_refs] = gr.update(value="I")

            else:
                # Fallback if image_refs is not found (shouldn't happen on latest Wan2GP)
                if getattr(self, "image_start", None) is not None:
                    comp_class = self.image_start.__class__.__name__
                    if comp_class == "Gallery" or isinstance(self.image_start, gr.Gallery):
                        updates[self.image_start] = [(image, "Canvas Editor")]
                    else:
                        updates[self.image_start] = image
                    if getattr(self, "image_start_row", None) is not None:
                        updates[self.image_start_row] = gr.update(visible=True)
                    print("Canvas Editor Plugin: No image_refs found. Updating standard self.image_start (Fallback Box)")

            gr.Info("Image successfully sent to Reference Images (People / Objects)!")
            return updates
        except Exception as e:
            gr.Warning(f"Failed to process image: {e}")
            return updates

    def create_canvas_ui(self):
        import html
        import os
        import gc
        
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
        
        js = """
        function() {
            window.addEventListener('message', (event) => {
                if (event.data && event.data.type === 'WAN2GP_SEND_TO_REFERENCE') {
                    const b64 = event.data.image;
                    const textarea = document.querySelector('#canvas_editor_hidden_b64 textarea');
                    if (textarea) {
                        textarea.value = b64;
                        textarea.dispatchEvent(new Event('input', { bubbles: true }));
                        
                        setTimeout(() => {
                            const btn = document.querySelector('#canvas_editor_hidden_btn');
                            if (btn) btn.click();
                        }, 150);
                    }
                }
            });
        }
        """
        
        with gr.Blocks() as demo:
            gr.HTML(iframe_code)
            
            # Setup hidden data bridges to pass JS events to Python Gradio app natively
            hidden_b64 = gr.Textbox(elem_id="canvas_editor_hidden_b64", visible=False)
            hidden_btn = gr.Button("Hidden Send", elem_id="canvas_editor_hidden_btn", visible=False)
            
            # Injecting javascript listener via demo load functionality
            demo.load(fn=None, js=js)
            
            # Apply safe radio patch when building the tab context
            try:
                self._apply_safe_radio_patch()
            except Exception as e:
                print(f"Canvas Editor Plugin: Tab initialization safety patch: {e}")

            # Define specific components to update
            outputs_list = []
            
            # Combine requested output components that are not None
            cand_attrs = [
                getattr(self, "image_start", None),
                getattr(self, "main_tabs", None),
                getattr(self, "image_start_row", None),
                getattr(self, "image_prompt_type_radio", None),
                getattr(self, "image_refs", None),
                getattr(self, "image_refs_row", None),
                getattr(self, "video_prompt_type_image_refs", None),
            ]
            
            for comp in cand_attrs:
                if comp is not None and comp not in outputs_list:
                    outputs_list.append(comp)

            self.outputs_list = outputs_list
            
            hidden_btn.click(
                fn=self.set_reference_image,
                inputs=[hidden_b64],
                outputs=outputs_list,
                show_progress="hidden"
            )
            
        return demo
