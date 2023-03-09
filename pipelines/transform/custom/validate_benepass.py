import json

import pandas as pd

if "custom" not in globals():
    from mage_ai.data_preparation.decorators import custom
if "test" not in globals():
    from mage_ai.data_preparation.decorators import test

from directory_read.custom.data_contracts.oneschema.validators import (
    validate_data_contract,
)


@custom
def transform_custom(df: pd.DataFrame, **kwargs):
    has_elections = kwargs["has_elections"]
    has_deductions = kwargs["has_deductions"]

    df["has_elections"] = has_elections
    df["has_deductions"] = has_deductions
    return validate_data_contract(json.loads(df.to_json(orient="records")))


@test
def test_output(output, *args) -> None:
    """
    Template code for testing the output of the block.
    """
    assert output is not None, "The output is undefined"
