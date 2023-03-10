import io

import pandas as pd
import requests

if "data_loader" not in globals():
    from mage_ai.data_preparation.decorators import data_loader
if "test" not in globals():
    from mage_ai.data_preparation.decorators import test

from mage_ai.data_preparation.shared.secrets import get_secret_value


@data_loader
def load_data_from_api(*args, **kwargs):
    """
    Template for loading data from API
    """
    url = "https://api.merge.dev/api/hris/v1/employees"
    response = requests.get(
        url,
        headers={
            "Authorization": f'Bearer {get_secret_value("bp_merge_api_key")}',
            "X-Account-Token": get_secret_value("bp_act_token"),
        },
    )

    return pd.json_normalize(response.json().get("results", []))


@test
def test_output(output, *args) -> None:
    """
    Template code for testing the output of the block.
    """
    assert output is not None, "The output is undefined"
