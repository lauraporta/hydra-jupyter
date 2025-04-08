import base64
import json
from io import BytesIO

import numpy as np
from IPython.display import HTML, Javascript, display
from PIL import Image

_active_session = None


def set_active_session(session):
    global _active_session
    _active_session = session


def get_active_session():
    return _active_session


class HydraSession:
    def __init__(
        self, hydra_code="src(s0).out(o0);", detect_audio=True, style_css=True
    ):
        self.hydra_code = hydra_code
        self.detect_audio = detect_audio

        self.initialize_hydra()
        if style_css:
            self.set_all_css()
        self.run(hydra_code)
        set_active_session(self)

    def initialize_hydra(self):
        audio = str(self.detect_audio).lower()
        js = f"""
        <script src="https://unpkg.com/hydra-synth"></script>
        <script>
        if (!window.hydra) {{
            window.hydra = new Hydra({{ detectAudio: {audio} }});
            console.log("✅ Hydra initialized");
        }}
        </script>
        """
        display(HTML(js))

    def set_all_css(self):
        js = """
        <script>
        function applyLiveCodingStyles() {
            const style = document.createElement('style');
            style.innerHTML = `

            html, body,
            .jp-Notebook,
            .jp-NotebookPanel,
            .jp-NotebookPanel-notebook,
            .jp-WindowedPanel,
            .jp-WindowedPanel-outer,
            .jp-WindowedPanel-inner,
            .jp-WindowedPanel-viewport {
                background: transparent !important;
                box-shadow: none !important;
            }

            .jp-Notebook .jp-Cell {
                background: transparent !important;
                padding: 0.5em !important;
                margin-bottom: 0.3em !important;
                box-shadow: none !important;
                border: none !important;
            }

            .jp-OutputArea-output,
            .jp-CodeCell .jp-InputArea,
            .jp-MarkdownCell .jp-Cell-inputWrapper,
            .jp-InputArea-editor,
            .cm-scroller,
            .cm-content {
                background: transparent !important;
                box-shadow: none !important;
            }

            :root {
                --jp-cell-padding: 0px !important;
                --jp-notebook-padding: 0px !important;
                --jp-layout-color0: transparent !important;
                --jp-layout-color1: transparent !important;
                --jp-layout-color2: transparent !important;
            }

            .CodeMirror {
                font-family: 'Fira Code', monospace;
                font-size: 1.1em;
                color: white;
            }

            .cm-keyword     { color: #ff79c6 !important; font-weight: bold; }
            .cm-number      { color: #bd93f9 !important; }
            .cm-string      { color: #f1fa8c !important; }
            .cm-variable    { color: #8be9fd !important; }
            .cm-def         { color: #50fa7b !important; }
            .cm-comment     { color: #6272a4 !important; font-style: italic; }
            .cm-builtin     { color: #ffb86c !important; }
            .cm-operator    { color: #ff5555 !important; }
            .cm-property    { color: #66d9ef !important; }

            .cm-content * {
                color: white !important;
                text-shadow:
                    0 0 4px black,
                    0 0 8px black,
                    0 0 16px black,
                    0 0 24px black;
            }

            ::-webkit-scrollbar {
                width: 8px;
                height: 8px;
            }
            ::-webkit-scrollbar-thumb {
                background-color: rgba(255, 255, 255, 0.2);
                border-radius: 4px;
            }
            ::-webkit-scrollbar-track {
                background: transparent;
            }
            `;
            document.head.appendChild(style);
        }

        applyLiveCodingStyles();
        </script>
        """
        display(HTML(js))

    def run(self, hydra_code: str):
        self.hydra_code = hydra_code
        js = f"""
        <script>
        if (!window.hydra) {{
            window.hydra = new Hydra({{ detectAudio: true }});
        }}

        solid().out(o0);  // reset
        {hydra_code}

        setTimeout(() => {{
            const hydraCanvas = document.querySelector('canvas');
            if (hydraCanvas) {{
                hydraCanvas.style.position = 'fixed';
                hydraCanvas.style.top = '0';
                hydraCanvas.style.left = '0';
                hydraCanvas.style.width = '100vw';
                hydraCanvas.style.height = '100vh';
                hydraCanvas.style.zIndex = '-1';
                hydraCanvas.style.pointerEvents = 'none';
                console.log("✅ Hydra canvas styled");
            }}
        }}, 300);
        </script>
        """
        display(HTML(js))

    def send_array(
        self, array: np.ndarray, frame_rate: int = 15, source_id: int = 0
    ):
        """
        Send a NumPy array (2D or 3D stack) to Hydra.

        Parameters
        ----------
        array : np.ndarray
            A 2D array (H, W) or 3D stack (T, H, W)
        frame_rate : int
            Animation frame rate if array is 3D
        source_id : int
            Which Hydra source to write to (0–3)
        """

        def to_b64(frame: np.ndarray) -> str:
            buffer = BytesIO()
            img = Image.fromarray(frame, mode="L")
            img.save(buffer, format="PNG")
            return base64.b64encode(buffer.getvalue()).decode("utf-8")

        # Normalize and convert to uint8 if needed
        if array.dtype != np.uint8:
            array = (array * 255).clip(0, 255).astype(np.uint8)

        if array.ndim == 2:
            self.send_frame(to_b64(array), source_id=source_id)

        elif array.ndim == 3:
            frames_b64 = [to_b64(frame) for frame in array]
            self.send_frames(
                frames_b64, frame_rate=frame_rate, source_id=source_id
            )

        else:
            raise ValueError("Expected 2D (H, W) or 3D (T, H, W) NumPy array")

    def send_frame(self, image_b64: str, source_id: int = 0):
        source_var = f"s{source_id}"
        js = f"""
        const img = new Image();
        img.crossOrigin = "anonymous";
        img.onload = () => {{
            {source_var}.init({{ src: img }});
        }};
        img.src = "data:image/png;base64,{image_b64}";
        """
        display(Javascript(js))

    def send_frames(
        self, image_b64_list: list, frame_rate: int = 15, source_id: int = 0
    ):
        source_var = f"s{source_id}"
        js = f"""
        if (window._hydraInterval) {{
            clearInterval(window._hydraInterval);
        }}

        const frames = {
            json.dumps(
                ["data:image/png;base64," + b64 for b64 in image_b64_list]
            )
        };
        let frameIndex = 0;
        const img = new Image();
        img.crossOrigin = "anonymous";

        function updateHydraTexture() {{
            {source_var}.init({{ src: img }});
        }}

        img.onload = updateHydraTexture;
        img.src = frames[0];

        window._hydraInterval = setInterval(() => {{
            frameIndex = (frameIndex + 1) % frames.length;
            img.src = frames[frameIndex];
        }}, {int(1000 / frame_rate)});
        """
        display(Javascript(js))
