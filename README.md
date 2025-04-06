# hydra-jupyter

Control [Hydra](https://hydra.ojack.xyz/) (livecoding visuals) directly from a Jupyter notebook.
This package lets you send Hydra code to the browser, preview visuals in the notebook, and eventually manipulate textures with Python.

---

## ✨ Features

- 📽️ Run Hydra code from a Jupyter notebook
- 🧼 Apply custom CSS styles to clean up the notebook display
- 🧪 Future support for sending Python-generated textures (2D/3D arrays)

---

## 💡 Motivation

Hydra is a powerful tool for livecoded visuals, but it's mainly used through a text editor and a browser.
This package brings Hydra into Jupyter notebooks, allowing:

- quick prototyping,
- integration with data analysis or ML workflows,
- and a more seamless experience for creative coders working in Python.

---

## 🚀 Getting Started

Clone the repo and install locally:

```bash
git clone https://github.com/your-username/hydra-jupyter.git
cd hydra-jupyter
pip install -e .
```

Use it in your notebook:

```python
from hydra_jupyter import initialize_hydra, set_all_css, run_hydra

# Set up Hydra and clean notebook styles
initialize_hydra()
set_all_css()

# Run a visual sketch
run_hydra("osc(1, .4, 1).luma().kaleid().out()")
```

---

## 🤝 Contributing

Contributions are welcome!

If you have an idea, suggestion, or bug report, feel free to [open an issue](https://github.com/your-username/hydra-jupyter/issues).
Whether it's a small fix or a big feature, we'd love to hear from you.
