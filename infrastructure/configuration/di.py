from functools import wraps
from infrastructure.configuration.container import Container

def inject_dependencies(*dependencies):
    def decorator(view_cls):
        orig_init = view_cls.__init__
        @wraps(orig_init)
        def __init__(self, *args, **kwargs):
            for dep in dependencies:
                dep_instance = Container.resolve(dep)
                setattr(self, dep.__name__.lower(), dep_instance)
            orig_init(self, *args, **kwargs)
        view_cls.__init__ = __init__
        return view_cls
    return decorator