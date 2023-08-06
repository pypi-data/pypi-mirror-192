import pandas as pd

def from_file(file):
    data = pd.read_csv(
        file,
        sep='\t',
        encoding='latin-1',
        index_col=False,
        dtype='str',
        keep_default_na=False,
        na_values=[],
    )
    return data
def to_file(file, data):
    if type(data) is not pd.DataFrame:
        raise TypeError()
    data.to_csv(
        file, 
        sep='\t',
        index=False,
    )