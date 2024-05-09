import json
import re


def parse_file(filename):
    data = []
    with open(filename, "r") as file:
        for line in file:
            json_data = json.loads(line)
            data.append(json_data)
    return data


def validate_entity_id(entity_id):
    pattern = r"[A-Z0-9]{6}"
    return bool(re.match(pattern, entity_id))
