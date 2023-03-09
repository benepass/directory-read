from mage_ai.data_preparation.repo_manager import get_repo_path
from mage_ai.io.config import ConfigFileLoader
from mage_ai.io.s3 import S3
import pandas as pd
from os import path
from datetime import date

if 'data_exporter' not in globals():
    from mage_ai.data_preparation.decorators import data_exporter

from mage_ai.data_preparation.shared.secrets import get_secret_value

print(get_secret_value('aws_access_key_id'))

@data_exporter
def export_data_to_s3(validation_response, **kwargs) -> None:

    EMPLOYER_SHORT_UUID = kwargs["EMPLOYER_SHORT_UUID"]
    
    
    config_path = path.join(get_repo_path(), 'io_config.yaml')
    config_profile = 'default'

    bucket_name = 'directory-read-prod-mvp'
    object_key = f'{EMPLOYER_SHORT_UUID}/errored_rows/{date.today()}.csv'

    errored_rows = validation_response.get('errored_rows')

    df = pd.DataFrame(errored_rows)

    S3.with_config(ConfigFileLoader(config_path, config_profile)).export(
        df,
        bucket_name,
        object_key,
    )

    return df
