from typing import Tuple

from chalice.app import Chalice, CloudWatchEvent, Cron

from chalicelib import config, middlewares
from chalicelib.presenters.custom import CustomPresenter
from chalicelib.services.handlers.extractors import extract_benepass
from chalicelib.services.unit_of_work import UnitOfWork


def bootstrap() -> Tuple[Chalice, UnitOfWork]:
    config.init_app_monitoring()

    app: Chalice = Chalice(app_name=config.get_app_name())
    app.debug = config.is_debug()

    app.log.setLevel(config.get_log_level())
    app.register_blueprint(middlewares.middlewares)

    uow: UnitOfWork = UnitOfWork(logger=app.log)

    return app, uow


app, uow = bootstrap()


EVERY_MIDNIGHT = Cron(0, 0, "*", "*", "?", "*")


@app.schedule(name="extract", expression=EVERY_MIDNIGHT)
def extract(event: CloudWatchEvent) -> dict:
    extract_benepass(uow)
    return CustomPresenter(ok=True).to_dict()
