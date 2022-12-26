import pandas as pd
import datetime
import utils.file_util as fileu
import utils.misc_util as miscu
from utils.log_trace_util import log_trace_decorator
import logging
import numpy as np
import matplotlib

@log_trace_decorator
def apply_dtype_feature(df, config):
    """
    ETL feature to apply data types to dataframe columns and limit columns to ones specified
    :param df: pd.DataFrame; Provided dataframe
    :param config: dict; Provided feature configuration
    :return: df_target: pd.DataFrame; Resulted dataframe
    Sample:
    "apply_dtype": {
        "INSURANCE_CODE": "str",
        "INSURANCE_AMOUNT": "float",
        "CLIENT_TYPE": "int"
    }
    """
    
    if config and isinstance(config, dict):
        for column_key, type_value in config.items():
            if column_key in df:
                # str type.
                if type_value is str or type_value == 'str':
                    df[column_key] = df[column_key].fillna('')
                    df[column_key] = df[column_key].astype(str)
                # int type.
                elif type_value is int or type_value == 'int':
                    df[column_key] = df[column_key].fillna(0)
                    df[column_key] = df[column_key].astype(int)
                # float type.
                elif type_value is float or type_value == 'float':
                    df[column_key] = df[column_key].fillna(0.0)
                    df[column_key] = df[column_key].astype(float)
                # datetime.date type
                elif type_value is datetime.date or type_value == 'date':
                    df[column_key] = pd.to_datetime(df[column_key], format="%d/%m/%Y")
            else:
                raise KeyError(f'Column <{column_key}> is missing from given dataframe')
        # Limit dataframe to specified columns.
        df = df[list(config.keys())]
    return df


@log_trace_decorator
def mapping_feature(df, config):
    """
    ETL feature to merge given dataframe with extracted mapping dataframe
    :param df: pd.DataFrame; Provided dataframe
    :param config: dict; Provided feature configuration
    :return: df_target: pd.DataFrame; Resulted dataframe
    """
    
    df_mapping = read_feature(config['read'])
    df_target = pd.merge(df, df_mapping, how='left', 
                         left_on=miscu.eval_elem_mapping(config, 'left_on'),
                         right_on=miscu.eval_elem_mapping(config, 'right_on'))                    
    return df_target


@log_trace_decorator
def read_feature(config):
    """
    ETL feature to read a file, based on provided ETL configuration section
    This is a composite feature, since it can call apply_dtype_feature, if appropriate config section exists
    :param config: dict; Provided configuration mapping
    :return: pd.DataFrame; Resulted dataframe
    """   
    filedata = fileu.FileDataStorage(miscu.eval_elem_mapping(config, 'description'))
    df_target = filedata.read(path=miscu.eval_elem_mapping(config, 'path'),
                              file_type=miscu.eval_elem_mapping(config, 'file_type', default_value='csv'),
                              separator=miscu.eval_elem_mapping(config, 'separator', default_value=','),
                              skip_rows=miscu.eval_elem_mapping(config, 'skip_rows', default_value=0),
                              use_cols=miscu.eval_elem_mapping(config, 'use_cols', default_value=None),
                              sheet_name=miscu.eval_elem_mapping(config, 'sheet_name', default_value=0))
    
    df_target.columns = df_target.columns.str.strip()
    # Call apply_dtype_feature, if appropriate config section exists
    apply_dtype_config = miscu.eval_elem_mapping(config, 'apply_dtype')
    if apply_dtype_config:
        df_target = apply_dtype_feature(df_target, apply_dtype_config)
    return df_target


@log_trace_decorator
def write_feature(config, df_target):
    """
    ETL feature to write a file, based on provided ETL configuration section
    :param config: dict; Provided configuration mapping
    :param df_target : pd.DataFrame; dataframe to write from
    :return: path
    """
    
    # Rename and reorder columns
    df_target = rearrange_feature(df_target, config)
    # Add static columns
    col_static = miscu.eval_elem_mapping(config, 'assign_static', default_value={})
    for k,v in col_static.items():
        df_target[k] = v
    filedata = fileu.FileDataStorage(miscu.eval_elem_mapping(config, 'description'))
    path = filedata.write(df=df_target,
                          path=miscu.eval_elem_mapping(config, 'path'),
                          columns_wt=miscu.eval_elem_mapping(config, 'columns', default_value=list(df_target.columns)),
                          file_type=miscu.eval_elem_mapping(config, 'file_type', default_value='csv'),
                          separator=miscu.eval_elem_mapping(config, 'separator', default_value=','),
                          mode=miscu.eval_elem_mapping(config, 'mode', default_value='new'),
                          header=miscu.eval_elem_mapping(config, 'header', default_value=True))
    return path


@log_trace_decorator
def rearrange_feature(df, config):
    """
    ETL feature to rename and reorder columns of given dataframe.
    :param df: pd.DataFrame; Provided dataframe
    :param config: dict; Provided feature configuration
    :return: df_target: pd.DataFrame; Resulted dataframe
    """
    # Rename columns
    col_rename = miscu.eval_elem_mapping(config, 'col_rename', default_value={})
    # Delete pairs in col_rename if name has been changed
    for k, v in col_rename.items():
        if v in df.columns:
            del col_rename[k]
    # Raise exeption if columns renamed is not defined
    try:
        df_target = df.rename(columns=col_rename)
    except KeyError:
        raise KeyError(f"The <{col_rename}> is not in the dataframe.")

    # Reorder
    reorder = miscu.eval_elem_mapping(config, 'col_reorder', default_value=list(df_target.columns))
    if not all(x in df_target.columns for x in reorder):
        raise KeyError(f'Column <{reorder}> is not a subset of given dataframe')
    df_target = df_target[reorder]
    return df_target


@log_trace_decorator
def aggregate_feature(config, df_target):
    """
    ETL feature to aggregate, based on provided ETL configuration section
    Transformation can be either pivot and groupby
    :param config: dict; Provided configuration mapping
    :param df_target : pd.DataFrame; dataframe to write from
    :return: df_target: pd.DataFrame; Resulted dataframe
    """
     
    # Aggregation can be pivot or groupby
    agg = miscu.eval_elem_mapping(config, 'type')

    if agg == "pivot":
        df_target = df_target.pivot(index=miscu.eval_elem_mapping(config, 'index', default_value=None),
                                    columns=miscu.eval_elem_mapping(config, 'columns', default_value=None),
                                    values=miscu.eval_elem_mapping(config, 'values', default_value=None))
        # Flatten multi-index columns                            
        df_target.columns = df_target.columns.get_level_values(1)
        # Change column names
        df_target.columns = [f"Dept_{i}" for i in df_target.columns]

    elif agg == "groupby":
        col = miscu.eval_elem_mapping(config, 'agg_column', default_value=None)
        funcs = miscu.eval_elem_mapping(config, 'aggfunc', default_value=None)
        # Map function applys eval to multiple config functions
        # Raise exceptions if functions are not defined
        try:
            func_list = list(map(eval, funcs))
        except AttributeError:
            raise AttributeError(f"The <{funcs}> is not defined.")

        df_target = df_target.groupby(by=miscu.eval_elem_mapping(config, 'group_by', default_value=None),
                                      as_index=False)[[col]].agg(func_list)
        # Combine column names in multiple levels                              
        df_target.columns = ['_'.join(col).strip() for col in df_target.columns.values]   

    else:
        logging.error(f"The aggregation type: <{agg}> is not defined.")
        raise AttributeError(f'Type should be pivot or groupby')     
                           
    return df_target


@log_trace_decorator
def plot_feature(config, df_target):
    """
    ETL feature to plot, based on dataframe passed by
    Plotting specifies x and y features
    :param config: dict; Provided configuration plot feature
    :param df_target : pd.DataFrame; dataframe to write from
    :return: df_target: pd.DataFrame; Resulted dataframe
    """
    x = miscu.eval_elem_mapping(config, 'plot_x', default_value=None)
    y = miscu.eval_elem_mapping(config, 'plot_x', default_value=None)
    fig = df_target.plot(x,y).get_figure()
    fig.savefig("sales_mean_median.png")
    return df_target
