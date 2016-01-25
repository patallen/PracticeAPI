def use_schema(schema, many=False):
    def wrap(f):
        def wrapped_function(*args, **kwargs):
            obj, status = f(*args, **kwargs)
            return schema(many=many).dump(obj).data, status
        return wrapped_function
    return wrap


def use_class_schema(many=False):
    def wrap(f):
        def wrapped_function(*args, **kwargs):
            schema = args[0].schema
            schema.many = many
            obj, status = f(*args, **kwargs)
            return schema.dump(obj).data, status
        return wrapped_function
    return wrap
