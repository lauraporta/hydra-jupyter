import base64
import json
from io import BytesIO

import numpy as np
from IPython.display import HTML, Javascript, display
from PIL import Image


def initialize_hydra(detect_audio: bool = True):
    """Initialize Hydra in the notebook.

    Parameters
    ----------
    detect_audio : bool, optional
        Whether to detect audio input, by default True
    """
    audio = str(detect_audio).lower()
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


def set_all_css():
    """
    Set all CSS to transparent and remove shadows. This is useful for live 
    coding and other visualizations that require a clean background.
    """
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

        /* Manual syntax highlighting overrides */
        .cm-keyword     { color: #ff79c6 !important; font-weight: bold; }
        .cm-number      { color: #bd93f9 !important; }
        .cm-string      { color: #f1fa8c !important; }
        .cm-variable    { color: #8be9fd !important; }
        .cm-def         { color: #50fa7b !important; }
        .cm-comment     { color: #6272a4 !important; font-style: italic; }
        .cm-builtin     { color: #ffb86c !important; }
        .cm-operator    { color: #ff5555 !important; }
        .cm-property    { color: #66d9ef !important; }

        /* Black shadow on white text */
        .cm-content * {
        color: white !important;
        text-shadow:
            0 0 4px black,
            0 0 8px black,
            0 0 16px black,
            0 0 24px black;
        }

        /* Scrollbar styling */
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


def run_hydra(hydra_code: str):
    """Run a Hydra code snippet in the notebook.

    Parameters
    ----------
    hydra_code : str
        The Hydra code to run.
    """

    js = f"""
    <script>
    if (!window.hydra) {{
      window.hydra = new Hydra({{ detectAudio: true }});
    }}
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


def send_2D_array_to_hydra(
    array_2d: np.ndarray, hydra_code: str = "src(s0).out(o0);"
):
    """
    Send a 2D array to Hydra and run the provided code.
    This function converts the 2D array to an image, encodes it in base64,
    and injects it into the Hydra environment.

    ⚠️ Currently not working.

    Parameters
    ----------
    array_2d : np.ndarray
        The 2D array to send to Hydra.
    hydra_code : str, optional
        The Hydra code to run, by default "src(s0).out(o0);"
    """

    # Prepare image
    image = Image.fromarray(array_2d.astype(np.uint8))
    buffer = BytesIO()
    image.save(buffer, format="PNG")
    img_b64 = base64.b64encode(buffer.getvalue()).decode("utf-8")
    data_url = f"data:image/png;base64,{img_b64}"

    # Inject JS
    js_code = f"""
    if (!window.hydra) {{
      window.hydra = new Hydra({{ detectAudio: false }});
    }}

    s0.initImage("{data_url}", () => {{
      {hydra_code}
    }});

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
      }}
    }}, 300);
    """
    display(Javascript(js_code))


def send_3D_array_to_hydra(
    array_3d: np.ndarray, frame_rate: float = 10, hydra_code: str = ""
):
    """
    Send a 3D array to Hydra and run the provided code.
    This function converts each 2D slice of the 3D array to an image, encodes
    it in base64, and injects it into the Hydra environment.

    ⚠️ Currently not working.

    Parameters
    ----------
    array_3d : np.ndarray
        The 3D array to send to Hydra.
    frame_rate : float, optional
        The frame rate for the animation in frames per second, by default 10
    hydra_code : str, optional
        The Hydra code to run, by default ""
    """
    frames = []
    for i in range(array_3d.shape[0]):
        img = Image.fromarray(array_3d[i].astype(np.uint8))
        buffer = BytesIO()
        img.save(buffer, format="PNG")
        img_b64 = base64.b64encode(buffer.getvalue()).decode("utf-8")
        frames.append(f"data:image/png;base64,{img_b64}")

    js = f"""
    if (!window.hydra) {{
      window.hydra = new Hydra({{ detectAudio: false }});
    }}

    let frameIndex = 0;
    const frames = {json.dumps(frames)};
    const img = new Image();
    img.crossOrigin = "anonymous";

    function updateHydraTexture() {{
      s0.init({{ src: img }});
    }}

    img.onload = updateHydraTexture;
    img.src = frames[0];

    {hydra_code or "src(s0).out(o0);"}

    function updateFrame() {{
      frameIndex = (frameIndex + 1) % frames.length;
      img.onload = updateHydraTexture;
      img.src = frames[frameIndex];
    }}

    setInterval(updateFrame, {int(1000 / frame_rate)});

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
      }}
    }}, 300);
    """
    display(Javascript(js))
