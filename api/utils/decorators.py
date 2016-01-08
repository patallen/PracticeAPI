def use_schema(schema, many=False):
    def wrap(f):
        def wrapped_function(*args, **kwargs):
            obj, status = f(*args, **kwargs)
            return schema(many=many).dump(obj).data, status
        return wrapped_function
    return wrap
