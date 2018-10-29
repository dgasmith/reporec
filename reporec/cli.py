"""
A command line interface to create reporec data.
"""
import os
import json
import yaml
import argparse

import pandas as pd

import reporec

# Options
parser = argparse.ArgumentParser(description='A CLI for the Repository Record.')
parser.add_argument("config_file", help="A configuration file to use.")
parser.add_argument("--dir", default="rrdata", type=str, help="Folder to add the data to.")


def read_config_file(fname):
    """Reads a JSON or YAML file.
    """
    if fname.endswith(".yaml") or fname.endswith(".yml"):
        rfunc = yaml.load
    elif fname.endswith(".json"):
        rfunc = json.load
    else:
        raise TypeError("Did not understand file type {}.".format(fname))

    with open(fname, "r") as handle:
        ret = rfunc(handle)

    return ret


def main():

    args = vars(parser.parse_args())

    # Handle paths
    config_path = os.path.join(os.getcwd(), args["config_file"])
    config = read_config_file(config_path)

    directory = os.path.join(os.getcwd(), args["dir"])
    if not os.path.exists(directory):
        os.makedirs(directory)

    evaluator_dict = {
        "conda": {
            "path_affix": "-conda.csv",
            "function": reporec.conda.build_table
        },
        "github": {
            "path_affix": "-github.csv",
            "function": reporec.github.build_table
        },
    }

    for proj, records in config.items():
        write_path = os.path.join(directory, proj)

        # Build path and initial data blob for each entry
        data = {}
        for name, blob in evaluator_dict.items():
            t = {}
            t["path"] = write_path + blob["path_affix"]
            t["data"] = None
            if os.path.exists(t["path"]):
                t["data"] = pd.read_csv(t["path"])

            data[name] = t

        # Loop over records
        for num, r in enumerate(records):

            missing = {"type", "username"} - r.keys()
            if len(missing):
                raise KeyError("Did not find keys '{}' for record {}:{}".format(missing, proj, num))

            username = r["username"]
            repository = r.get("repository", proj)

            ftype = r["type"].lower()
            if ftype not in evaluator_dict:
                raise KeyError("Did not understand type key '{}'.".format(r["type"]))

            data[ftype]["data"] = evaluator_dict[ftype]["function"](username, repository, old_data=data[ftype]["data"])

        for k, v in data.items():
            if v["data"] is None:
                continue

            v["data"].sort_values(by=["timestamp"], inplace=True)
            v["data"].to_csv(v["path"], index=False)

        print("Finished project '{}'".format(proj))


if __name__ == '__main__':
    main()
