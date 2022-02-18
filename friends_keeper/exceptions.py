"""Exception raised on the application."""


class FriendsKeeperError(BaseException):
    """General Friends keeper exception error.

    Args:
        BaseException (BaseException): Python's base exception.
    """

    pass


class ConfigurationError(FriendsKeeperError):
    """Raised when there is wrong configuration.

    Args:
        FriendsKeeperError (friends_keeper.exceptions.FriendsKeeperError): General Friends keeper exception.
    """

    pass


class DatabaseError(ConfigurationError):
    """Raised when there is some kind of issue with the database.

    Args:
        FriendsKeeperError (friends_keeper.exceptions.FriendsKeeperError): General Friends keeper exception.
    """

    pass


class NotifierError(FriendsKeeperError):
    """Raised when an error occurs while processing any notifier.

    Args:
        FriendsKeeperError (friends_keeper.exceptions.FriendsKeeperError): General Friends keeper exception.
    """

    pass


class WrongNotifierError(NotifierError):
    """Raised when not supported notifier is selected.

    Args:
        FriendsKeeperError (friends_keeper.exceptions.NotifierError): General Friends keeper  notifier exception.
    """

    pass
