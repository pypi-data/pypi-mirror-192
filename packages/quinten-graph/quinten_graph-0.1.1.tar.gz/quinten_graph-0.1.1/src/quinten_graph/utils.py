"""
This sub-module useful functions that do not belong to "settings" or "plotting" modules:
The following functions are available:
    - dfs_insight: quick overview of several datasets
    - non_outlier_indices_IQR: outlier detection
    - data_preparation: function to clean the sandbox dataset "datasetchurn.csv"

"""

import numpy as np
import pandas as pd

def dfs_insight(df_dict):
    """give general information on dfs of a list: shape, columns, % of NaN, duplicates
    -input: a dict of dataframes with their name as key

    -output:
        1) print a df with df-wise information: name_df, shape, % NaN, # duplicated rows
        2) print a df per df in the input dict: each printed df contains column-wise info:
        # dupplicated entries, avg_nan rate per column
    """
    from IPython.core.display import display

    class color:
        PURPLE = "\033[95m"
        CYAN = "\033[96m"
        DARKCYAN = "\033[36m"
        BLUE = "\033[94m"
        GREEN = "\033[92m"
        YELLOW = "\033[93m"
        RED = "\033[91m"
        BOLD = "\033[1m"
        UNDERLINE = "\033[4m"
        END = "\033[0m"


    # 1 dict that will contain the series describing the datasets (df-wise info) (1 series per df)
    dict_indic_series=dict()
    # columns of the series
    indic_columns=["name_df", "shape", "% NaN", "# duplicated rows"]
    # 1 dict to keep the dfs with column_wise info
    df_cols_display_dict = {}

    for name, df in df_dict.items():
        # compute general indicators on each df
        shape = df.shape
        avg_nan = "{:.2%}".format(df.isna().mean().mean())
        nb_dupli_rows = df.duplicated().value_counts().filter([True]).values
        if not nb_dupli_rows.size > 0:
            nb_dupli_rows = 0
        else:
            nb_dupli_rows = int(nb_dupli_rows)
        # make a series with these indicators and add the indicators names as index
        dict_indic_series[name] = pd.Series(
            [name, shape, avg_nan, nb_dupli_rows], index=indic_columns
        )
        # concat all series into a df 
        dfs_display = pd.concat([ser for ser in dict_indic_series.values()], ignore_index=True, axis=1).T

        # making a df for columns indicators (1 df per df), the column of the described df are the index
        df_cols_display = pd.DataFrame(index=df.columns)
        # adding the dtype
        df_cols_display["dtype"] = df.dtypes
        # computing the number of dupplicated entries per column
        try:
            nb_dupli_entries = df.apply(
                lambda col: col.duplicated().value_counts()
            ).loc[True]
            # if there is no dupplicated entries, we get NaN, we have to replace it by 0
            nb_dupli_entries.fillna(0, inplace=True)
            df_cols_display["# dupplicated entries"] = nb_dupli_entries.values
        except KeyError:
            nb_dupli_entries = 0
            df_cols_display["# dupplicated entries"] = nb_dupli_entries

        # computing the avg of NaN per column
        avg_nan_col = df.isna().mean()
        avg_nan_col = pd.Series(
            ["{:.2%}".format(val) for val in avg_nan_col], index=avg_nan_col.index
        )
        df_cols_display["avg_nan_col"] = avg_nan_col.values

        # adding the df to the dict for further displaying
        df_cols_display_dict[name] = df_cols_display

    # printig the general df with df-wise info
    print(color.BOLD, color.UNDERLINE, "df-wise information", color.END)
    print(dfs_display, "\n")
    # printing 1 df per df with column-wise-info
    print(color.BOLD, color.UNDERLINE, "column-wise information", color.END)
    for name, df in df_cols_display_dict.items():
        print(color.BOLD, name, color.END)
        print(df)
        print("\nfirst 3 rows\n")
        display(df_dict[name].head(3))
        print("-" * 70)

def non_outlier_indices_IQR(df):
    """ Returns boolean mask flagging all non outliers with the IQR method. 
    input:
    - df with numeric columns to be considered for outlier detection
    output:
    - list of boolean flagging rows that have no outlier
    https://stackoverflow.com/questions/46245035/pandas-dataframe-remove-outliers"""
    Q1 = df.quantile(0.25)
    Q3 = df.quantile(0.75)
    IQR = Q3 - Q1
    nonOutlierList  = ~((df < (Q1 - 1.5 * IQR)) | (df > (Q3 + 1.5 * IQR)))
    return nonOutlierList 

# functions to clean the sandbox data (datasetchurn)

def _drop_columns(df):
    df.drop("id_client",
    axis=1, inplace= True)
    df.drop("branche",
    axis= 1, inplace= True)  # we drop branche for sake of simplicity
    return df

def _clean_churn(df):
    # drop missing values
    df.dropna(subset=[ 'churn' ], inplace = True)
    CHURN_mapping = { "oui":1,"non": 0}
    df["churn"] = df["churn"].map(CHURN_mapping)
    return df


def _impute_na(df):
    # replace empty values by Nan
    df = df.replace(r'^\s*$',np.nan,
        regex=True)
    return df


def _clean_interet_compte_epargne_total(df):
    df["interet_compte_epargne_total"]=pd.to_numeric( df["interet_compte_epargne_total"] )
    return df

def _clean_compte_epargne(df):
    # when compte_epargne is unknown, replace by oui
    df.loc[(df["cartes_bancaires"]=="medium")& (df["compte_epargne"].isnull()),'compte_epargne']= "oui"
    df.loc[(df["cartes_bancaires"]== "premium")& (df["compte_epargne"].isnull()), 'compte_epargne']="oui"
    return df

def _clean_var_i(df):
    # remove correlated variables
    for i in range( 1,18 ) :
        df.drop("var_"+ str(i), axis=1, inplace= True)
    for i in range( 21,37):
        df.drop("var_"+str(i),axis = 1, inplace=True)
    # transform remaining vars into differences
    df["diff_var_0_19"] = df["var_0"]-df["var_19"]
    df["diff_var_0_20"] = df["var_0"]-df["var_20"]
    df["diff_var_20_38"] = df["var_20"]- df["var_38"]
    df["diff_var_0_38"] = df["var_0"]-df["var_38"]
    return df
        
def data_preparation(df):
    """ voilà un script bien plus clair"""
    # drop useless columns 
    df = _drop_columns(df)
    
    # clean churn column (outcome)
    df = _clean_churn(df)
    
    # impute empty values 
    df = _impute_na(df)
    
    # clean interet_compte_epargne_total column
    df = _clean_interet_compte_epargne_total(df)
    
    # clean compte_epargne column
    df = _clean_compte_epargne(df)
    
    # clean var_i columns 
    df = _clean_var_i(df)
    
    return df