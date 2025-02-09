import os
import pytest
import allure
from assertpy import assert_that, soft_assertions
from utils.parser import parse_file, validate_entity_id, validate_dropped_analytics


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
        assert_that(parsed_data).is_type_of(list)
        assert_that(len(parsed_data)).is_greater_than(0)

    @allure.story("Parse the records file")
    @allure.title("Verify the anallytics entity ID format is correct")
    @allure.description(
        "Test each record in the analytics records data and verify the entity ID is in the expected format"
    )
    @allure.severity("blocker")
    def test_entities_ids_format(self):
        data = validate_entity_id(parsed_data)
        print(data)
        with soft_assertions():
            assert_that(data, f"Wrong format RP_ENTITY_IDs: {data}").is_length(0)

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
        print(
            "Number of unique distinct stories that appear in the record file: ",
            len(unique_document_ids),
        )

    def test_missing_records_by_index_in_between(self):
        dropped_records = validate_dropped_analytics(parsed_data)
        with soft_assertions():
            assert_that(
                len(dropped_records),
                f"Missing/dropped records {dropped_records}",
            ).is_equal_to(0)


if __name__ == "__main__":
    pytest.main([__file__])
