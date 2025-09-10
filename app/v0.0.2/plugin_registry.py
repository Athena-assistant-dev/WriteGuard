# plugin_registry.py – centralized WriteGuard plugin registration

from typing import Callable, Dict

# Plugin function type signature
PluginFunc = Callable[[str], None]

# Registry dictionary
plugins: Dict[str, PluginFunc] = {}

def register_plugin(extension: str):
    """
    Decorator to register a plugin by file extension.
    Usage:
        @register_plugin(".json")
        def my_handler(path):
            ...
    """
    def decorator(func: PluginFunc) -> PluginFunc:
        plugins[extension.lower()] = func
        return func
    return decorator

def run_plugin_for(filepath: str):
    """Invoke plugin if file extension matches."""
    for ext, handler in plugins.items():
        if filepath.lower().endswith(ext):
            handler(filepath)
            return True
    return False