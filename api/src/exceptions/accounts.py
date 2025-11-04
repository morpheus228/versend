class DuplicateAccountError(Exception):
    """An account with this id/phone number/username already exists"""

    def __init__(self, message: str = None):
        if message is None:
            message = "An account with this id/phone number/username already exists"
            
        super().__init__(message)


class AccountNotFoundError(Exception):
    """Account with the given ID does not exist"""
    def __init__(self, message: str = None):
        if message is None:
            message = "Account with the given ID does not exist"
            
        super().__init__(message)


class InvalidAccountData(Exception):
    """Invalid Account Data"""
    def __init__(self, message: str = None):
        if message is None:
            message = "Invalid Account Data"
            
        super().__init__(message)

