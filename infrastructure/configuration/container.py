from threading import local

class Container:
    _registrations = {}
    _singletons = {}
    _scoped_storage = local()
    _initialized = False

    class Lifetime:
        SINGLETON = "singleton"
        SCOPED = "scoped"
        TRANSIENT = "transient"

    @classmethod
    def _ensure_initialized(cls):
        if not cls._initialized:
            import infrastructure.configuration
            cls._initialized = True

    @classmethod
    def register(cls, interface, implementation, lifetime="transient"):
        cls._registrations[(interface, None)] = (implementation, lifetime)

    @classmethod
    def resolve(cls, interface, key=None):
        cls._ensure_initialized()
        reg_key = (interface, key)
        if reg_key not in cls._registrations:
            raise Exception(f"No hay implementación registrada para {interface} con key={key}")
        implementation, lifetime = cls._registrations[reg_key]
        try:
            if lifetime == cls.Lifetime.SINGLETON:
                if interface not in cls._singletons:
                    cls._singletons[interface] = implementation()
                return cls._singletons[interface]
            elif lifetime == cls.Lifetime.SCOPED:
                if not hasattr(cls._scoped_storage, "instances"):
                    cls._scoped_storage.instances = {}
                if interface not in cls._scoped_storage.instances:
                    cls._scoped_storage.instances[interface] = implementation()
                return cls._scoped_storage.instances[interface]
            else:  # TRANSIENT
                return implementation()
        except Exception as e:
            raise Exception(f"Error al resolver {interface}: {str(e)}")

    @classmethod
    def clear(cls):
        cls._singletons.clear()
        if hasattr(cls._scoped_storage, "instances"):
            cls._scoped_storage.instances.clear()