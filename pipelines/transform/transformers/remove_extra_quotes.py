import pandas as pd


@transformer
def transform(data: pd.DataFrame):
    df = data.replace('"', "", regex=True)
    return df
