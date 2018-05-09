class ValidationError(ValueError):
    """
    Use to validate user data
    """
    pass


class UserNotActivatedError(ValueError):
    """
    Use to make sure user is activated
    """
    pass
