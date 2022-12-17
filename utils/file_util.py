import logging
import pandas as pd
import os
import utils.datastorage as ds
from utils.log_trace_util import log_trace_decorator


class FileDataStorage(ds.DataStorage):
    def __init__(self, description):
        super().__init__(description)

    @log_trace_decorator
    def read(self, path, file_type='excel', separator=',', skip_rows=0, use_cols=None, sheet_name=0):
        """
        Read file, along with validating provided path.
        :param path: str; Fully qualified file name to read
        :param file_type: str, default='Excel'; Read type with possible values of 'csv' or 'excel'
        :param separator: str, default=','; Values separator
        :param skip_rows: int, default=0; Number of rows to skip
        :param use_cols: int, default=None; A list of columns to read (all others are discarded)
        :param sheet_name: int or str; default=0; A sheet name or index to read
        :return: pd.DataFrame; Resulted dataframe
        """
        df_target = None
        # Check whether the path is a file path
        if self.validate_path(path, False):
            if file_type.lower() == 'csv':
                # Read csv based file.
                df_target = pd.read_csv(path, sep=separator, skiprows=skip_rows, usecols=use_cols)
            elif file_type.lower() == 'excel':
                # Read Excel based file.
                if len((pd.ExcelFile(path)).sheet_names) > 1:
                    df_target = pd.read_excel(path, sep=separator, skiprows=skip_rows, usecol=use_cols, sheet_name=sheet_name)
                else:
                    df_target = pd.read_excel(path, usecols=use_cols)

        logging.info(f'{self._description} records <{len(df_target.index)}> were read from <{path}>')
        return df_target

    @log_trace_decorator
    def write(self, df, path, columns_wt, file_type='excel', separator=',', mode='new', header=True):
        """
        Write file, along with validating provided path.
        :param df: pd.DataFrame; content to write from
        :param path: str; Fully qualified file name to write
        :param columns_wt: list, default=df.columns; Columns to write
        :param file_type: str, default='Excel'; Read type with possible values of 'csv' or 'excel'
        :param separator: str, default=','; Values separator
        :param mode: str, default='new'; Overwrite or add new name
        :param header: bool, default=True; Whether to write out column names
        :return: str; Resulted file path
        """
        
        if os.path.dirname(path) == '':
            path = './' + path
        # Check whether the path of directory is valid
        if self.validate_path(os.path.dirname(path), True):
            # Write to csv
            if file_type.lower() == 'csv':
                path = os.path.splitext(path)[0]+'.csv'
                # create a new path if it overwrites exisiting path
                if mode == 'new':
                    path = self.path_new_mode(path)
                elif mode == 'overwrite':
                    path = path
                else:
                    logging.error(f'Invalid second input')
                    raise ValueError(f'Second paramenter should be new or overwrite')
                df.to_csv(path, columns=columns_wt, sep=separator, header=header)
                
            # Write to excel
            elif file_type.lower() == 'excel':
                path = os.path.splitext(path)[0]+'.xlsx'
                if mode == 'new':
                    path = self.path_new_mode(path)
                elif mode == 'overwrite':
                    path = path
                else:
                    logging.error(f'Invalid second input')
                    raise ValueError(f'Second paramenter should be new or overwrite')
                df.to_excel(path, columns=columns_wt,  header=header)

        logging.info(f'{self._description} records <{len(df.index)}> were write to <{path}>')
        return path
#remove it from staticmethod works
    @staticmethod
    @log_trace_decorator
    def validate_path(path, is_dir):
        """
        Validate provided path to support for directory validation
        :param path: Fully qualified file path
        :param is_dir: bool; Whether the path is a directory or file
        :return: bool; Resulted validation; either true or raise an exception
        """
        # if we need to check validity of a directory
        if not is_dir:
            if not os.path.isfile(path):
                logging.error(f'Provided file path is invalid: <{path}>')
                raise FileNotFoundError(f'Provided file path is invalid: <{path}>')
        # if we need to check validity of a directory
        elif is_dir:
            if not os.path.isdir(path):
                logging.error(f'Provided directory path is invalid: <{path}>')
                raise FileNotFoundError(f'Provided directory path is invalid: <{path}>')
        else:
            logging.error(f'Invalid second input')
            raise ValueError(f'Second paramenter should be True for directory and False for File')
        return True
    @staticmethod
    @log_trace_decorator
    def path_new_mode(path):
        """
        Find if given file name already exists and if so, construct appropriate suffix
        for the file name and use it when creating new file
        :param path: str; Fully qualified file name to read
        :return: str; New path
        """
        if os.path.exists(path):
            # Split path to be two parts separated by .
            name, ext = os.path.splitext(path)
            i = 1       
            while os.path.exists("{name}_{uid}{ext}".format(name=name, uid=i, ext=ext)):
                i += 1
            new_path = "{name}_{uid}{ext}".format(name=name, uid=i, ext=ext)
        else:
            new_path = path
        return new_path
