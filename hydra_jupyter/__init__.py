from importlib.metadata import PackageNotFoundError, version

try:
    __version__ = version("hydra-jupyter")
except PackageNotFoundError:
    # package is not installed
    pass
