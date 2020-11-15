def validation_classes(validation_classes):
    def decorator(func):
        func.validation_classes = validation_classes
        return func

    return decorator
