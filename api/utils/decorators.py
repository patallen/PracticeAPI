def use_schema(schema, many=False):
    def wrap(f):
        def wrapped_function(*args, **kwargs):
            print(many)
            return schema(many=many).dump(f(*args, **kwargs)).data
        return wrapped_function
    return wrap
