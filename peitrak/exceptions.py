class ServerError(Exception):
    CODE=1000

class InsufficientBalance(Exception):
    CODE=1001

class InvalidAccount(Exception):
    CODE=1002

class InvalidPin(Exception):
    CODE=1003

class InvalidDestination(InvalidAccount):
    CODE=1004

ERRORS = [
    ServerError,
    InsufficientBalance,
    InvalidAccount,
    InvalidPin,
    InvalidDestination
]
