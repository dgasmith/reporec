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

    for proj, records in config.items():
        write_path = os.path.join(directory, proj)

        # Handle conda
        conda_path = write_path + "-conda.csv"
        conda_df = None
        if os.path.exists(conda_path):
            conda_df = pd.read_csv(conda_path)

        # Handle github
        github_path = write_path + "-github.csv"
        github_df = None
        if os.path.exists(github_path):
            github_df = pd.read_csv(github_path)

        # Loop over records
        for num, r in enumerate(records):

            missing = {"type", "username"} - r.keys()
            if len(missing):
                raise KeyError("Did not find keys '{}' for record {}:{}".format(missing, proj, num))

            username = r["username"]
            repository = r.get("repository", proj)

            if r["type"].lower() == "conda":
                conda_df = reporec.conda.build_table(username, repository, old_data=conda_df)

            elif r["type"].lower() == "github":
                github_df = reporec.github.build_table(username, repository, old_data=github_df)
            else:
                raise KeyError("Did not understand type key '{}'.".format(r["type"]))

        # Write it out
        if github_df is not None:
            github_df.sort_values(by=["timestamp"], inplace=True)
            github_df.to_csv(github_path, index=False)

        if conda_df is not None:
            conda_df.sort_values(by=["timestamp"], inplace=True)
            conda_df.to_csv(conda_path, index=False)

        print("Finished project '{}'".format(proj))


if __name__ == '__main__':
    main()
