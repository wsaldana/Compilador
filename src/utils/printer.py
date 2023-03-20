def print_return(msg):
    def decorator(func):
        def wrapper(*args, **kwargs):
            result = func(*args, **kwargs)
            print(msg, ": ", result)
            return result
        return wrapper
    return decorator
