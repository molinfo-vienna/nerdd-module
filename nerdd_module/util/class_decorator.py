__all__ = ["class_decorator"]


def class_decorator(f):
    def result_decorator(*args, **kwargs):
        # Case 1: first argument is a class -> decorator is used without arguments
        #
        # Example:
        #
        # @my_decorator
        # class F:
        #     ...
        if len(args) > 0 and isinstance(args[0], type):
            return f(args[0], *args[1:], **kwargs)

        # Case 2: first argument is a not a class --> decorator is used with arguments
        #
        # Example:
        #
        # @my_decorator(42)
        # class F:
        #     ...
        def inner(cls):
            assert isinstance(cls, type), "Decorator must be used with a class"
            return f(cls, *args, **kwargs)

        return inner

    return result_decorator
