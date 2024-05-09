import os
import pytest
import allure
from assertpy import assert_that, soft_assertions
from utils.parser import parse_file, validate_entity_id


file_path = os.environ.get("FILE_PATH") or "rt-feed-record/rt-feed-record"
parsed_data = parse_file(file_path)
unique_document_ids = set()


@allure.feature("Test Analytics records")
class TestAnalytics:
    @allure.story("Parse the records file")
    @allure.title("Verify the anallytics is loaded correctly")
    @allure.description(
        "Parse the analytics records data and verify we get the list of dicts"
    )
    @allure.severity("blocker")
    def test_get_analytics(self):
        with soft_assertions():
            assert_that(parsed_data).is_type_of(list)

    @allure.story("Parse the records file")
    @allure.title("Verify the anallytics entity ID format is correct")
    @allure.description(
        "Test each record in the analytics records data and verify the entity ID is in the expected format"
    )
    @allure.severity("blocker")
    def test_entities_ids_format(self):
        for data in parsed_data:
            with soft_assertions():
                assert_that(validate_entity_id(data["RP_ENTITY_ID"])).is_equal_to(True)

    @allure.story("Parse the records file")
    @allure.title("Verify the anallytics records number of distinct stories")
    @allure.description(
        "Test each record in the analytics records data and get the number of unique/distinct stories"
    )
    @allure.severity("blocker")
    def test_unique_document_ids_count(self):
        global unique_document_ids
        for data in parsed_data:
            unique_document_ids.add(data["RP_DOCUMENT_ID"])
        with soft_assertions():
            assert_that(len(unique_document_ids)).is_greater_than(0)
        print(len(unique_document_ids))

    @allure.story("Parse the records file")
    @allure.title("Verify the anallytics records has no dropped analytics")
    @allure.description(
        "Test the number of analytics records for each document and get the number of dropped analytics"
    )
    @allure.severity("blocker")
    def test_dropped_analytics_comparing_count_to_last_index(self):
        global unique_document_ids
        count = 0
        for data in parsed_data:
            if data["DOCUMENT_RECORD_COUNT"] == data["DOCUMENT_RECORD_INDEX"]:
                count += 1
        print(count)
        with soft_assertions():
            assert_that(
                count,
                "The number of analytics records from DOCUMENT_RECORD_INDEX equals unique document ids",
            ).is_equal_to(len(unique_document_ids))

    def test_missing_records_by_index_in_between(self):
        grouped_data = {}
        for item in parsed_data:
            rp_document_id = item["RP_DOCUMENT_ID"]
            if rp_document_id not in grouped_data:
                grouped_data[rp_document_id] = []
            grouped_data[rp_document_id].append(item["DOCUMENT_RECORD_INDEX"])
        for key in grouped_data:
            min_value = min(grouped_data[key])
            max_value = max(grouped_data[key])
            reference_list = list(range(min_value, max_value + 1))
            missing_numbers = [
                number for number in reference_list if number not in grouped_data[key]
            ]
            with soft_assertions():
                assert_that(
                    len(missing_numbers),
                    f"Missing records for document with RP_DOCUMENT_ID: {key}, missing DOCUMENT_RECORD_INDEX: {missing_numbers}",
                ).is_equal_to(0)


if __name__ == "__main__":
    pytest.main([__file__])
