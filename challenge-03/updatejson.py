import json
import csv
import os
import sys
import argparse



def get_args():

    def is_valid_file(parser, file, ext):
        if not os.path.exists(file):
            parser.error("Given file {} does not exists..".format(file))

        elif not file.endswith('.{}'.format(ext)):
            parser.error("Please provide a valid {} file".format(ext))

        return file


    parser = argparse.ArgumentParser(description="Update Config Json using Input CSV")
    parser.add_argument('--env', dest='env', action='store', required=True)
    parser.add_argument('--json', dest='json_file', type=lambda f: is_valid_file(parser, f, 'json'), required=True)
    parser.add_argument('--csv', dest='csv_file', type=lambda f: is_valid_file(parser, f, 'csv'), required=True)

    return parser.parse_args()


if __name__ == '__main__':
    args = get_args()
    env = args.env

    
    config_json = {}

    try:
        with open(args.json_file, 'r') as file:
            config_json = json.load(file)
    except ValueError as e:
        print("Invalid JSON File.. Exiting...")
        sys.exit(0)


    with open(args.csv_file, 'r') as file:
        reader = csv.reader(file)
        keys = []
        for row in reader:
            if not keys:
                keys = row[1:]
                continue

            if row[0] == env and env in config_json:
                values_to_be_updated = {key: row[ind+1] for ind, key in enumerate(keys) if key in config_json[env]}
                print("Updated values", values_to_be_updated)
                config_json[env].update(values_to_be_updated)


    with open(args.json_file, 'w') as file:
        json.dump(config_json, file, indent=2)



