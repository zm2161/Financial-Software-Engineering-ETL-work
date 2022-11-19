from types import SimpleNamespace as Namespace
import argparse
def namespace_to_dict(args):
    """
    convert a namespace to dict recursively so we get all levels to be dict
    Params
    ---
    args: namespace/ dict/ argparse.Namespace
    Return
    ---
    dict
    """
    if isinstance(args,Namespace) or isinstance(args, argparse.Namespace):
        return namespace_to_dict(vars(args))

    elif isinstance(args,dict):
        for k,v in args.items():
            args[k]=namespace_to_dict(v)
        return args
    else:
        return {}

    