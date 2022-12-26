import argparse
import json
import logging
import os
import sys
from types import SimpleNamespace as Namespace
# Add the directory of parent of file to sys path
sys.path.append(os.path.abspath('../../../'))
from utils.log_trace_util import log_trace_decorator
import utils.etl_util as etlu
import utils.misc_util as miscu

RETURN_SUCCESS = 0
RETURN_FAILURE = 1
APP = 'EtlData utility'


def main(argv):
    try:
        # Parse command line arguments.
        # Args are command line arguments
        args, process_name, process_type, process_config = _interpret_args(argv)

        # Create real path of log_path.
        std_filename = "etldata.log"
        logging_dir = os.path.realpath(f'{args.log_path}')
        if not os.path.exists(logging_dir):
            os.makedirs(logging_dir)
        # Change defalut logging level so only events of this level and above will be logged
        logging.basicConfig(filename=os.path.join(logging_dir, std_filename), filemode='a',
                            format='%(asctime)s - %(message)s', level=logging.INFO
                            )
        logging.info('')
        logging.info(f'Entering {APP}')

        # Preparation step.
        mapping_args = miscu.convert_namespace_to_dict(args)
        mapping_conf = miscu.convert_namespace_to_dict(process_config)

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
    with open(os.path.join(current_path, f'../config/{process_name}.json')) as file_config:
        mapping_config = json.load(file_config, object_hook=lambda d: Namespace(**d))
        if process_type == 'extraction':
            process_config = vars(mapping_config.extraction)
        elif process_type == 'transformation':
            process_config = vars(mapping_config.transformation)
        # Feature_args are dictionary of info in command line
        # Feature_args add arguments from json like input, output,mapping path to instruct terminal inputs
        feature_args = vars(mapping_config.feature_args)
        # Add necessary arguments to <arg_parser> instance, using static JSON-based configuration.
        if feature_args:
            for key, value in feature_args.items():
                if isinstance(value, Namespace):
                    # Vars function returns a dict
                    value = vars(value)
                arg_parser.add_argument(key, dest=value['dest'], help=value['help'], required=value['required'])
    return arg_parser.parse_args(argv), process_name, process_type, process_config


@log_trace_decorator
def run_extraction(args, config):

    # --------------------------------
    # Input section
    # --------------------------------

    # Prepare additional input parameters and update appropriate configuration section.
    # Inject 'path' and 'description' into <input> config section.
    # Args are command input
    input_update_with = {'path': miscu.eval_elem_mapping(args, 'input_path'), 'description': config['description']}
    input_config = miscu.eval_elem_mapping(config, 'input')
    # First create read dic in input key in config, then update with path and description
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

    # Implement and complete this section with the following steps:
    # Prepare additional mapping parameters and update appropriate configuration section.
    # Inject 'path' and 'description' into <output> config section.
    # Run write ETL feature.
    output_update_with = {'path': miscu.eval_elem_mapping(args, 'output_path'),
                          'description': config['description']}
    output_config = miscu.eval_elem_mapping(config, 'output')
    output_write_config = miscu.eval_update_mapping(output_config, 'write', output_update_with)
    # Run write ETL feature.
    etlu.write_feature(output_write_config, df_target)
    return df_target


@log_trace_decorator
def run_transformation(args, config):
    # --------------------------------
    # Input section
    # --------------------------------

    # Prepare additional input parameters and update appropriate configuration section.
    # Inject 'path' and 'description' into <input> config section.
    # Args are command input
    input_update_with = {'path': miscu.eval_elem_mapping(args, 'input_path'), 'description': config['description']}
    input_config = miscu.eval_elem_mapping(config, 'input')
    # First create read dic in input key in config, then update with path and description
    input_read_config = miscu.eval_update_mapping(input_config, "read", input_update_with)

    # Run read ETL feature.
    df_target = etlu.read_feature(input_read_config)
    # Engage plugin from <input> config section, if available.
    input_plugin = miscu.eval_elem_mapping(input_config, "plugin")
    if input_plugin:
        df_target = input_plugin(df_target)

    # --------------------------------
    # Transformation section
    # --------------------------------

    # Prepare additional mapping parameters and update appropriate configuration section.
    # Inject 'path' and 'description' into <aggregate> config section.
    trans_update_with = {'description': config['description']}
    trans_config = miscu.eval_elem_mapping(config, 'aggregate')
    trans_write_config = miscu.eval_update_mapping(trans_config, 'agg', trans_update_with)
    # Run write ETL feature.
    df_target = etlu.aggregate_feature(trans_write_config, df_target)
    # --------------------------------
    # Output section
    # --------------------------------

    # Implement and complete this section with the following steps:
    # Prepare additional mapping parameters and update appropriate configuration section.
    # Inject 'path' and 'description' into <output> config section.
    # Run write ETL feature.
    output_update_with = {'path': miscu.eval_elem_mapping(args, 'output_path'), 'description': config['description']}
    output_config = miscu.eval_elem_mapping(config, 'output')
    output_write_config = miscu.eval_update_mapping(output_config, 'write', output_update_with)
    # Run write ETL feature.
    etlu.write_feature(output_write_config, df_target)
    
    return


if __name__ == '__main__':
    # Call main process.
    main(sys.argv[1:])
    
