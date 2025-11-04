
class InviteCodeNotFoundError(Exception):
    pass

class ExpiredInviteCodeError(Exception):
    pass

class UserAlreadyExistsError(Exception):
    pass

class UserNotFoundError(Exception):
    pass

class InvalidPasswordError(Exception):
    pass

class InvalidTokenError(Exception):
    pass