import pandas as pd
import json


def respone_to_df(respone):
    """
    Tar emot en json och omvnadlar den till en pandas dataframe som sedan returneras
    """
    data = respone.read()
    formated_data = json.loads(data)
    df = pd.DataFrame(formated_data)
    return df
    
    
    
def rename_dr(df, rename_dict):
    """Tar emot en dictionary där key är det nuvarande namnet på kolumnen och value är det nya namnet på kolumnen.

    Args:
        df (pandas.DataFrame): dataframe vars columner ska byta namn
        rename_dict (dict): dictionary med key som är det nuvarande namnet på kolumnen och value som är det nya namnet på kolumnen
    """
    return df.rename(columns=rename_dict, inplace=True)


def extract_date_from_dataframe(df):
    """Tar emot en dataframe och extraherar datum och time_start och skapar en ny variabel med datumet.

    Args:
        df (pandas.DataFrame): dataframe vars datum ska ta ut
    """
    # bryter ut datum från time_start
    date_df = df['time_start'].str.split('T').str[0]
    # skapar en variabel med valt datum
    date = date_df[0]
    
    return date

def create_time_column(df):
    """Tar emot pandas dataframe och skapar en ny kolumn med tid utan sekunder och tar bort time_start, time_end och EXR

    Args:
        df (pandas.DataFrame): dataframe vars tid ska tas ut och läggas i ny kolumn
    """
    # bryter ut tid från time_start
    df['Tid'] = df['time_start'].str.split('T').str[1].str.split('+').str[0]
    ## tar bort sekunder från tiden
    df['Tid'] = df['Tid'].str[:5]
    ## tar bort onödiga columner
    df.drop(columns=['time_start', 'time_end', 'EXR'], inplace=True)
    return df


def df_to_html(df):
    """Tar emot en pandas dataframe och gör om den till en html tabell

    Args:
        df (pandas.DataFrame): dataframe som ska göras om till html tabell
    """
    # gör om dataframen till en html tabell
    df_html = df.to_html(classes="table table-striped table-hover table-bordered table-sm", index=False)
    return df_html