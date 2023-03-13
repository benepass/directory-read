from chalicelib.config import capture_monitored_exception, get_benepass_connection
from chalicelib.domain.fields.datetime import date_utc_now
from chalicelib.services.unit_of_work import UnitOfWork, atomicness
from chalicelib.utils.buffer import bufferize


class ExtractorException(Exception):
    pass


@atomicness
def extract_benepass(uow: UnitOfWork):
    employer_name, _, token = get_benepass_connection()

    result = list(uow.merge.fetch_all(token, "hris/v1/employees"))
    with bufferize(result) as buffer:
        error_metadata = uow.files.upload_to(
            buffer, key=f"{employer_name}/{date_utc_now()}/roster.json"
        )

        if error_metadata:
            capture_monitored_exception(ExtractorException("Error"))
