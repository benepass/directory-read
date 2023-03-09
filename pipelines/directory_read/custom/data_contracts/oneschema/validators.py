
import requests
from typing import Tuple

import requests
from mage_ai.data_preparation.shared.secrets import get_secret_value

def make_validation_request(contract_key:str,data:dict):
    return requests.post(
        "https://api.oneschema.co/v1/validate-json-rows",
        headers={"x-api-key": get_secret_value("one_schema_api_key")},
        json={"template_key": contract_key, "rows": data},
    )

def validate_data_contract(data: dict):
    roster_response = make_validation_request('roster-contract', data)
    assert roster_response.status_code == 200,  roster_response.json()
    assert roster_response.json().get('error_rows') or  roster_response.json().get('rows'), "Response content is not valid"
    return _parse_validation_response(data, roster_response.json())


def _parse_validation_response(data: dict, response_data: dict) -> Tuple[dict, dict]:
    errored_indexes_and_rows = []

    # deal with all the rows that errored
    for validation_error_row in response_data.get("error_rows", []):
        errors = validation_error_row.get("errors")
        row_index = validation_error_row.get("index")
        errored_row = {**data[row_index]}


        for error_key, error_content in errors.items():
            errored_row[error_key] = f"Error reason: {error_content['message']}"

        errored_indexes_and_rows.append((row_index, errored_row))

    # now find all the rows that didn't error 
    errored_indexes = [i for i, _ in errored_indexes_and_rows]
    success_rows = [d for i, d in enumerate(data) if i not in errored_indexes]
    errored_rows = [e for _, e in errored_indexes_and_rows]

    return {'success_rows':success_rows, 'errored_rows': errored_rows} 