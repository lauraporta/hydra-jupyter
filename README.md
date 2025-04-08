# hydra-jupyter

`hydra-jupyter` is a lightweight Python interface for controlling [Hydra](https://github.com/ojack/hydra) visuals directly from Jupyter notebooks. It enables sending NumPy arrays as textures to Hydra, writing code snippets with cell magics, and controlling Hydra sessions without writing JavaScript manually.

## Installation

Clone this repository and install in editable mode:

```bash
git clone https://github.com/lauraporta/hydra-jupyter.git
cd hydra-jupyter
pip install .
```

## Quickstart

### 1. Start a session

```python
from hydra_jupyter import HydraSession

session = HydraSession()
```
The default hydra scrpt will be `src(s0).out(o0);`.

### 2. Send an array

```python
import numpy as np

# Example: simple gradient
gradient = np.tile(np.linspace(0, 1, 256), (256, 1))
session.send_array(gradient, source_id=0) # This will become your s0
```

### 3. Write Hydra code in a notebook cell

First, load the extension:

```python
%load_ext hydra_jupyter.magic
```

Then use the magic:

```python
%%hydra
src(s0)
  .kaleid(5)
  .rotate(0.1)
  .out(o0)
```

### 4. Send animated stack

```python
def make_3d_pulsing_gradient(size=256, n_frames=30):
    x = np.linspace(-1, 1, size)
    y = np.linspace(-1, 1, size)
    xx, yy = np.meshgrid(x, y)
    radius = np.sqrt(xx**2 + yy**2)
    stack = []
    for i in range(n_frames):
        scale = 1 + 0.5 * np.sin(2 * np.pi * i / n_frames)
        pulse = np.clip(1 - radius * scale, 0, 1)
        stack.append(pulse)
    return np.stack(stack)

frames = make_3d_pulsing_gradient()
session.send_array(frames, frame_rate=15, source_id=0)
```

## Features

- Send 2D or 3D NumPy arrays as textures
- Reuse persistent Hydra sessions
- Write Hydra code with `%%hydra` cell magic


## Contributing

Contributions are welcome! If you have suggestions for improvements or new features, please open an issue or submit a pull request.
