import os
import pandas as pd
from pathlib import Path
import httpx
from lxml.html import fromstring
from jellyfish import jaro_winkler_similarity as jw

URL_DISTRICTS = "https://web.archive.org/web/20120116131947/http://dolr.nic.in/Hyperlink/distlistnew.htm"


def date_format(df: pd.DataFrame, column: str) -> pd.DataFrame:
    """
    Helper function to standarize date values in a column

    Args:
        - df: dataframe
        - column: name of the column

    Returns: dataframe with the selected column with date format
    """
    df.loc[:, column] = pd.to_datetime(df.loc[:, column], format="mixed")
    return df


def clean_text(text: str):
    new_text = text.replace(" - ", "").strip()
    new_text = new_text.replace("\n", " ")
    return new_text


def get_official_names(url=URL_DISTRICTS) -> list:
    """
    Helper function to fetch official district names
    """
    parser = fromstring(httpx.get(URL_DISTRICTS).text)
    xpath = parser.xpath('//a[@name="orissa"]/following-sibling::ul[1]')[0]
    official_names = [clean_text(child.text) for child in xpath.getchildren()]
    official_names.extend(["Bhubaneswar", "Rourkela"])
    return official_names


def match_names(raw_name: str, lst_compare: list, threshold: float) -> str:
    """
    Helper function to match a raw name of a district with the most closest name
    with a minimum similarity score.

    Args:
        - raw_name: raw name of the district
        - lst_compare: list with all possible district names
        - threshold: minimum score allowed to consider a match

    Returns: the closest name of the district
    """
    best_match = max(lst_compare, key=lambda x: jw(raw_name, x))
    similarity = jw(raw_name, best_match)
    if similarity > threshold:
        return best_match
    else:
        return raw_name


def clean_district_names(df: pd.DataFrame, column: str) -> pd.DataFrame:
    """
    Helper function to standarize district names based on an official record

    Args:
        - df: dataframe
        - column: name of the column

    Returns: dataframe with the selected column with corrected district names
    """
    official_names = get_official_names()
    unique_values = df.loc[:, column].unique()
    matched_names = {
        name: match_names(name, official_names, 0.8) for name in unique_values
    }
    df.loc[:, column] = df.loc[:, column].replace(matched_names)
    return df

def categorize_grievances(df: pd.DataFrame, column: str) -> pd.DataFrame:
    '''
    Helper function to categorize grievances text
        Args:
        - df: dataframe
        - column: name of the column

    Returns: dataframe with the new categorization column
    '''
    dict_categorize = {
        'Hostel conditions are very poor, water supply is irregular.' : 'Poor water supply',
        'Stipend not credited for the last three months.' : 'Stipend not credited',
        'Students are asked to arrange their own materials for practice.' : 'Students arrange own materials',
        'Trainer has not come to the institute for the past two weeks.' : 'Trainer absence',
        'Internet not working in the computer lab for over a month.' : 'Internet not working',
        'Electricity is not available during class hours.' : 'Lack of electricity',
        'No practical classes being conducted for welding program.' : 'No practical classes',
        'Grievance was registered last month, no action yet.' : 'No action, past month',
        'Lab equipment is broken and no replacement has been provided.' : 'Broken lab equipment',
        'Only one instructor for three different trades.' : 'Unique instructor'
    }

    df.loc[:, f'cat_{column}'] = df.loc[:,column].replace(dict_categorize)
    return df

def handle_duplicates(
    df: pd.DataFrame, cols_id: list, how: str, agg_var: str
) -> pd.DataFrame:
    """
    Helper function to handle duplicates from a DataFrame by indicating a list
    of columns that uniquely identifies the data

    Args:
        - df : dataframe
        - cols_id : columns that uniquely identifies the data
        - how : type of handle for duplicates
            'sum' : sum the values of the aggregate variable
            'max' : keeps the maximum value of the aggregate variable
            'mean' : keeps the average value of the aggregate variable

    Return: pd.DataFrame
    """
    df[agg_var] = pd.to_numeric(df[agg_var], errors="coerce").fillna(0)
    return df.groupby(by=cols_id)[agg_var].aggregate(how).reset_index()

def gen_ids(lst_uniques: list, id_name: str) -> pd.DataFrame:
    '''
    Function to create a pd.DataFrame with official districts names
    '''
    tuple_list = [(str(ix+1).zfill(4), name) for ix, name in enumerate(lst_uniques)]
    df = pd.DataFrame(tuple_list)
    df.columns = [id_name, 'name']
    return pd.DataFrame(df)

def clean_grievances(path: Path) -> pd.DataFrame:
    """
    Function to load and clean data from citizens complaints

    Args:
        - path: Path object where the file is located

    Returns: pd.Dataframe
    """
    df = pd.read_json(path)
    df = date_format(df, "submission_date")
    df['year'] = pd.to_datetime(df['submission_date']).dt.year
    df = clean_district_names(df, "district_name")

    cols_id = ["district_name", "submission_date", "grievance_text", "submitted_by", "year"]
    df = handle_duplicates(df, cols_id, how="max", agg_var="resolved")
    districts = gen_ids(get_official_names(), 'did')
    df = pd.merge(df, districts, how='left', left_on= 'district_name', right_on='name').drop(columns = ['name'])
    df = categorize_grievances(df , 'grievance_text')
    return df


def clean_iti_enrollments(path: Path) -> pd.DataFrame:
    """
    Function to load and clean data from Industrial Training Institutes (ITIs)

    Args:
        - path: Path object where the file is located

    Returns: pd.Dataframe
    """
    df = pd.read_csv(path)
    df = clean_district_names(df, "district")
    cols_id = ["year", "district", "institute_name", "program", "gender"]
    df = handle_duplicates(df, cols_id, how="sum", agg_var="enrolled")
    
    # Generating districts id
    districts = gen_ids(get_official_names(), 'did')
    df = pd.merge(df, districts, how='left', left_on= 'district', right_on='name').drop(columns = ['name'])
    
    # Generating iti id
    itis = gen_ids(df['institute_name'].unique(), 'iid')
    df = pd.merge(df, itis, how='left', left_on= 'institute_name', right_on='name').drop(columns = ['name'])
    return df

def main():
    path_g = Path('data/raw/grievances.json')
    path_i = Path('data/raw/iti_enrollments.csv')

    df_g ,df_i = clean_grievances(path_g), clean_iti_enrollments(path_i)
    districts = gen_ids(get_official_names(), 'did')
    itis = gen_ids(df_i['institute_name'].unique(), 'iid')

    path_clean = Path('data/clean')
    if not path_clean.exists():
        os.mkdir(path_clean)

    df_g.to_csv(Path('data/clean/grievances.csv'), index = False)
    df_i.to_csv(Path('data/clean/iti_enrollments.csv'), index = False)
    districts.to_csv(Path('data/clean/districts.csv'), index = False)
    itis.to_csv(Path('data/clean/itis.csv'), index = False)

if __name__ == "__main__":
    main()