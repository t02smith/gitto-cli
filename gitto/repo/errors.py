# REPO DOESN'T EXISTS

class RepoNotInitialisedError(FileNotFoundError):
    pass


class RepoNotInitialisedOnRemoteError(RepoNotInitialisedError):
    pass


# REPO ALREADY EXISTS

class RepoAlreadyInitialised(FileExistsError):
    pass


class RepoAlreadyInitialisedOnRemote(RepoAlreadyInitialised):
    pass


# GENERAL

class RepoError(RuntimeError):
    pass