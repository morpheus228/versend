class DuplicateAccountError(Exception):
    """An account with this id/phone number/username already exists"""


class AccountNotFoundError(Exception):
    """Account with the given ID does not exist"""


class InvalidAccountData(Exception):
    """Invalid Account Data"""