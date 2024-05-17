import json
import re


def parse_file(filename):
    data = []
    with open(filename, "r") as file:
        for line in file:
            json_data = json.loads(line)
            data.append(json_data)
    return data


def validate_entity_id(data):
    failed_entity_ids = []
    pattern = r"^[0-9A-Z]{6}$"
    for row in data:
        if not re.match(pattern, row["RP_ENTITY_ID"]):
            failed_entity_ids.append(f"RP_DOCUMENT_ID: {row['RP_DOCUMENT_ID']} with wrong format RP_ENTITY_ID: {row["RP_ENTITY_ID"]}")
    return failed_entity_ids

def validate_dropped_analytics(data):
    grouped_data = {}
    dropped_records = {}
    for item in data:
        rp_document_id = item["RP_DOCUMENT_ID"]
        if rp_document_id not in grouped_data:
            grouped_data[rp_document_id] = {}
            grouped_data[rp_document_id]['INDEXES'] = []
            grouped_data[rp_document_id]['DOCUMENT_RECORD_COUNT'] = item['DOCUMENT_RECORD_COUNT']
        grouped_data[rp_document_id]['INDEXES'].append(item["DOCUMENT_RECORD_INDEX"])
    for key in grouped_data:
        min_value = 1
        max_value = grouped_data[key]['DOCUMENT_RECORD_COUNT']
        reference_list = list(range(min_value, max_value + 1))
        missing_indexes = [
            number for number in reference_list if number not in grouped_data[key]['INDEXES']
        ]
        if len(missing_indexes) > 0:
            dropped_records[key] = missing_indexes
    return dropped_records
