import importlib


def import_class(class_path):
    class_path_parts = class_path.split('.')
    module_path = '.'.join(class_path_parts[0:-1])
    class_name = class_path_parts[-1]
    module = importlib.import_module(module_path)

    return getattr(module, class_name)
