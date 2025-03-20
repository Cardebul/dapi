def generate_validator(model, create=False):
    import inspect

    from app.serializers import serializers

    classes = inspect.getmembers(serializers, lambda x: inspect.isclass(x) and (x.__module__ == serializers.__name__))
    for _, cls in classes:
        if not (meta := getattr(cls, 'Meta', None)): continue
        if not ((getattr(meta, 'model', None) is model) and (getattr(meta, 'create', False) is create)): continue
        return cls
    raise Exception('not found')