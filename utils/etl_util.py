import pandas as pd
import datetime
import utils.file_util as fileu
import utils.misc_util as miscu


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


def read_feature(config):
    """
    ETL feature to read a file, based on provided ETL configuration section
    This is a composite feature, since it can call apply_dtype_feature, if appropriate config section exists
    :param config: dict; Provided configuration mapping
    :return: pd.DataFrame; Resulted dataframe
    """   
    FileData = fileu.FileDataStorage(miscu.eval_elem_mapping(config, 'description'))
    df_target = FileData.read(path=miscu.eval_elem_mapping(config, 'path'),
                              file_type=miscu.eval_elem_mapping(config, 'file_type', default_value='excel'),
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


def write_feature(config, df_target):
    """
    ETL feature to write a file, based on provided ETL configuration section
    :param config: dict; Provided configuration mapping
    :param df_target : pd.DataFrame; dataframe to write from
    :return: path
    """
    df_target = df_target.rename(columns=miscu.eval_elem_mapping(config, 'col_rename', default_value={}))
    FileData = fileu.FileDataStorage(miscu.eval_elem_mapping(config, 'description'))
    path = FileData.write(df=df_target,
                          path=miscu.eval_elem_mapping(config, 'path'),
                          columns_wt=miscu.eval_elem_mapping(config, 'columns', default_value=list(df_target.columns)),
                          file_type=miscu.eval_elem_mapping(config, 'file_type', default_value='excel'),
                          separator=miscu.eval_elem_mapping(config, 'separator', default_value=','),
                          mode=miscu.eval_elem_mapping(config, 'mode', default_value='new'),
                          header=miscu.eval_elem_mapping(config, 'header', default_value=True))
    return path