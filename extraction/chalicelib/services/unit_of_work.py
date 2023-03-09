from logging import Logger


class UnitOfWork:
    def __init__(self, logger: Logger):
        self.logger = logger
