import time

def type_control(*a_args, **a_kwargs):
    def decorator(fct):
        def modified_function(*args, **kwargs):
            
            if len(a_args) != len(args):
                raise TypeError(f"Number of positional args doesn't match with function {fct.__name__}")

            for i, arg in enumerate(args):
                if a_args[i] is not type(args[i]):
                    raise TypeError(f"Positional argument {i+1} of {fct.__name__} is {type(args[i]).__name__} instead of {a_args[i].__name__}")

            for key in kwargs:
                if a_kwargs[key] is not type(kwargs[key]):
                    raise TypeError(f"Argument {key} of {fct.__name__} is {type(kwargs[key]).__name__} instead of {a_kwargs[key].__name__}")
            
            return fct(*args, **kwargs)
        return modified_function
    return decorator

def timer(fct):
    def modified_function(*args, **kwargs):
        t0 = time.time()
        result = fct(*args, **kwargs)
        print(f"{fct.__name__} took {time.time() - t0}s to run")
        return result
    return modified_function