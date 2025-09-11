import os
import importlib.util
import traceback

PLUGIN_FOLDER = os.path.dirname(__file__)
LOADED_PLUGINS = {}

def safe_import_plugin(module_name, module_path):
    try:
        spec = importlib.util.spec_from_file_location(module_name, module_path)
        if spec and spec.loader:
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            return module
    except Exception as e:
        print(f"[PLUGIN LOADER] Error loading plugin {module_name}: {e}\n{traceback.format_exc()}")
    return None

from plugins.base_plugin import WritePlugin

def load_plugins():
    if not os.path.exists(PLUGIN_FOLDER):
        print(f"[PLUGIN LOADER] Plugin folder not found: {PLUGIN_FOLDER}")
        return

    for filename in os.listdir(PLUGIN_FOLDER):
        if filename.endswith(".py") and not filename.startswith("_") and filename != "plugin_loader.py":
            module_name = filename[:-3]
            module_path = os.path.join(PLUGIN_FOLDER, filename)
            module = safe_import_plugin(module_name, module_path)
            if module:
                for item_name in dir(module):
                    item = getattr(module, item_name)
                    if isinstance(item, type) and issubclass(item, WritePlugin) and item is not WritePlugin:
                        LOADED_PLUGINS[module_name] = item()
                        print(f"[PLUGIN LOADER] Loaded plugin class: {item_name}")
                        break

def validate_with_plugins(file_path, content):
    file_ext = os.path.splitext(file_path)[-1].lower()
    for name, plugin in LOADED_PLUGINS.items():
        if hasattr(plugin, "validate"):
            if not hasattr(plugin, "extensions") or file_ext in plugin.extensions:
                try:
                    plugin.validate(file_path, content)
                except Exception as e:
                    raise ValueError(f"[PLUGIN VALIDATOR] {name}: {e}")

def post_write_with_plugins(file_path, old_content, new_content):
    file_ext = os.path.splitext(file_path)[-1].lower()
    for name, plugin in LOADED_PLUGINS.items():
        if hasattr(plugin, "post_write"):
            if not hasattr(plugin, "extensions") or file_ext in plugin.extensions:
                try:
                    plugin.post_write(file_path, old_content, new_content)
                except Exception as e:
                    print(f"[PLUGIN POST-WRITE] Warning from {name}: {e}")

def get_plugin(name):
    return LOADED_PLUGINS.get(name)

def reload_plugins():
    LOADED_PLUGINS.clear()
    load_plugins()

# Auto-load on import
load_plugins()

if __name__ == "__main__":
    print("[PLUGIN LOADER] Running plugin system test...")
    test_file = "sample_test.json"
    test_content = '{"server": {"host": "localhost", "port": 8080}}'
    try:
        validate_with_plugins(test_file, test_content)
        print("[PLUGIN LOADER] Validation plugins ran successfully.")
    except Exception as e:
        print(f"[PLUGIN LOADER] Validation failed: {e}")