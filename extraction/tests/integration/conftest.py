from logging import getLogger

import pytest

from chalicelib.config import get_app_name, get_log_level
from chalicelib.services.unit_of_work import UnitOfWork


@pytest.fixture
def fake_logger():
    logger = getLogger(get_app_name())
    logger.setLevel(get_log_level())
    return logger


@pytest.fixture
def make_uow(fake_logger):
    def _factory(logger=fake_logger, **kwargs):
        return UnitOfWork(logger=logger, **kwargs)

    return _factory


@pytest.fixture
def uow(make_uow):
    return make_uow()
