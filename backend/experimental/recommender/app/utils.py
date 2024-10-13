import pandas as pd


def read_csv(path:str, use_cols:list[str]=['Video name', 'label']) -> pd.DataFrame: 
    df = pd.read_csv(path, index_col=False, use_cols=use_cols)
    return df