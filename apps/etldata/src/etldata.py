import argparse
import json
import logging
import os
import sys
from types import SimpleNamespace as Namespace
import sys
# Add the directory of parent of file to sys path
sys.path.append(os.path.join(os.path.abspath(os.path.dirname(__file__)), '../../../'))
import utils.convert_util as convertu

import fall2022py.utils.etl_util as etlu
import fall2022py.utils.misc_util as miscu


RETURN_SUCCESS = 0
RETURN_FAILURE = 1
APP = 'EtlData utility'


def main(argv):
    try:
        # Parse command line arguments.
        args, process_name, process_type, process_config = _interpret_args(argv)

        # Initialize standard logging \ destination file handlers.
        # Change log file directory
        std_filename = os.path.join(os.path.dirname(os.path.abspath('etldata.py')), "opendata.log")
        # Add logging level
        logging.basicConfig(filename=std_filename, level=logging.INFO, filemode='a', format='%(asctime)s - %(message)s')
        logging.info('')
        logging.info(f'Entering {APP}')
        #  Convert from Namespace to dict (args, feature_config).
        mapping_args = convertu.namespace_to_dict(args)
        mapping_conf = convertu.namespace_to_dict(feature_config)

        # Workflow steps.
        if process_type == 'extraction':
            run_extraction(mapping_args, mapping_conf)
        elif process_type == 'transformation':
            run_transformation(mapping_args, mapping_conf)
        else:
            logging.warning(f'Incorrect feature type: [{process_type}]')

        logging.info(f'Leaving {APP}')
        return RETURN_SUCCESS
    except FileNotFoundError as nf_error:
        logging.error(f'Leaving {APP} incomplete with errors')
        return f'ERROR: {str(nf_error)}'
    except KeyError as key_error:
        logging.error(f'Leaving {APP} incomplete with errors')
        return f'ERROR: {key_error.args[0]}'
    except Exception as gen_exc:
        logging.error(f'Leaving {APP} incomplete with errors')
        raise gen_exc


def _interpret_args(argv):
    """
    Read, parse, and interpret given command line arguments.
    Also, define default value.
    :param argv: Given argument parameters.
    :return: Full mapping of arguments, including all default values.
    """
    arg_parser = argparse.ArgumentParser(APP)
    arg_parser.add_argument('-log', dest='log_path', help='Fully qualified logging file')
    arg_parser.add_argument('-process', dest='process', help='Process type', required=True)

    # Extract and interpret rest of the arguments, using static config file, based on given specific feature.
    process_arg = argv[argv.index('-process') + 1]
    process_args = process_arg.rsplit('_', 1)
    process_name = process_args[0]
    process_type = process_args[1]
    current_path = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
    print(os.path.dirname(__file__))
    with open(os.path.join(current_path, f'../config/{process_name}.json')) as file_config:
        mapping_config = json.load(file_config, object_hook=lambda d: Namespace(**d))
        if process_type == 'extraction':
            process_config = vars(mapping_config.extraction)
        elif process_type == 'transformation':
            process_config = vars(mapping_config.transformation)

        feature_args = vars(mapping_config.feature_args)
        # Add necessary arguments to <arg_parser> instance, using static JSON-based configuration.
        if feature_args:
            for key, value in feature_args.items():
                if isinstance(value, Namespace):
                    # Vars function returns a dict
                    value = vars(value)
                arg_parser.add_argument(key, dest=value['dest'], help=value['help'], required=value['required'])
    # parse_args return a namespace
    return arg_parser.parse_args(argv), process_name, feature_type, feature_config


def run_extraction(args, config):

    # --------------------------------
    # Input section
    # --------------------------------

    # Prepare additional input parameters and update appropriate configuration section.
    # Inject 'path' and 'description' into <input> config section.
    input_update_with = {'path': miscu.eval_elem_mapping(args, 'input_path'), 'description': config['description']}
    input_config = miscu.eval_elem_mapping(config, 'input')
    input_read_config = miscu.eval_update_mapping(input_config, "read", input_update_with)

    # Run read ETL feature.
    df_target = etlu.read_feature(input_read_config)

    # Engage plugin from <input> config section, if available.
    input_plugin = miscu.eval_elem_mapping(input_config, "plugin")
    if input_plugin:
        df_target = input_plugin(df_target)

    # --------------------------------
    # Mapping section
    # --------------------------------

    # Prepare additional mapping parameters and update appropriate configuration section.
    # Inject 'path' and 'description' into <mapping> config section.
    mapping_update_with = {'path': miscu.eval_elem_mapping(args, 'mapping_path'), 'description': config['description']}
    mapping_config = miscu.eval_elem_mapping(config, 'mapping')
    mapping_read_config = miscu.eval_update_mapping(mapping_config, 'read', mapping_update_with)

    # Run mapping ETL feature.
    df_target = etlu.mapping_feature(df_target, mapping_config)

    # --------------------------------
    # Output section
    # --------------------------------

    # TODO: Implement and complete this section with the following steps:

    # TODO: Prepare additional mapping parameters and update appropriate configuration section.

    # TODO: Inject 'path' and 'description' into <output> config section.

    # TODO: Run write ETL feature.

    return df_target


def run_transformation(args, conf):
    pass


if __name__ == '__main__':
    # Call main process.
    sys.exit(main(sys.argv[1:]))
