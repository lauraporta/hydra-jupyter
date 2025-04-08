from IPython.display import HTML, display

from .session import get_active_session


def _hydra_magic(line, cell):
    session = get_active_session()
    if session:
        session.run(cell)
    else:
        js = f"""
        <script>
        if (!window.hydra) {{
            window.hydra = new Hydra({{ detectAudio: false }});
        }}
        solid().out(o0);
        {cell}
        </script>
        """
        display(HTML(js))


def load_ipython_extension(ipython):
    ipython.register_magic_function(
        _hydra_magic, magic_kind="cell", magic_name="hydra"
    )
