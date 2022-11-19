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

RETURN_SUCCESS = 0
RETURN_FAILURE = 1
APP = 'EtlData utility'


def main(argv):
    try:
        # Parse command line arguments.
        args, process_name, feature_type, feature_config = _interpret_args(argv)

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
        if feature_type == 'extraction':
            run_extraction(mapping_args, mapping_conf)
        elif feature_type == 'transformation':
            run_transformation(mapping_args, mapping_conf)
        else:
            logging.warning(f'Incorrect feature type: [{feature_type}]')

        logging.info(f'Leaving {APP}')
        return RETURN_SUCCESS
    except FileNotFoundError as nf_error:
        logging.info(f'Leaving {APP} incomplete with errors')
        return f'ERROR: {str(nf_error)}'
    except KeyError as key_error:
        logging.info(f'Leaving {APP} incomplete with errors')
        return f'ERROR: {key_error.args[0]}'
    except Exception as gen_exc:
        logging.info(f'Leaving {APP} incomplete with errors')
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
    feature_type = process_args[1]
    current_path = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
    print(os.path.dirname(__file__))
    with open(os.path.join(current_path, f'../config/{process_name}.json')) as file_config:
        mapping_config = json.load(file_config, object_hook=lambda d: Namespace(**d))
        if feature_type == 'extraction':
            feature_config = vars(mapping_config.extraction)
        elif feature_type == 'transformation':
            feature_config = vars(mapping_config.transformation)

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


def run_extraction(args, conf):
    pass


def run_transformation(args, conf):
    pass


if __name__ == '__main__':
    # Call main process.
    sys.exit(main(sys.argv[1:]))
