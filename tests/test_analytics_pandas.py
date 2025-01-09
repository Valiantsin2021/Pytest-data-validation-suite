import os

import allure
import pandas as pd
import pytest
from assertpy import assert_that, soft_assertions

from utils.parser_pandas import parse_file, validate_dropped_analytics, validate_entity_id

file_path = os.environ.get("FILE_PATH") or "rt-feed-record/rt-feed-record"
parsed_data = parse_file(file_path)


@allure.feature("Test Analytics records")
class TestAnalytics:
    @pytest.fixture(scope="class")
    def analytics_df(self):
        """Fixture to provide the parsed DataFrame for all tests"""
        return parsed_data

    @allure.story("Parse the records file")
    @allure.title("Verify the analytics is loaded correctly")
    @allure.description(
        "Parse the analytics records data and verify we get a valid DataFrame"
    )
    @allure.severity("blocker")
    def test_get_analytics(self, analytics_df):
        assert_that(analytics_df).is_type_of(pd.DataFrame)
        assert_that(len(analytics_df)).is_greater_than(0)

    @allure.story("Parse the records file")
    @allure.title("Verify the analytics entity ID format is correct")
    @allure.description(
        "Test each record in the analytics records data and verify the entity ID is in the expected format"
    )
    @allure.severity("blocker")
    def test_entities_ids_format(self, analytics_df):
        invalid_ids = validate_entity_id(analytics_df)
        print(invalid_ids)
        with soft_assertions():
            assert_that(
                invalid_ids, f"Wrong format RP_ENTITY_IDs: {invalid_ids}"
            ).is_length(0)

    @allure.story("Parse the records file")
    @allure.title("Verify the analytics records number of distinct stories")
    @allure.description(
        "Test each record in the analytics records data and get the number of unique/distinct stories"
    )
    @allure.severity("blocker")
    def test_unique_document_ids_count(self, analytics_df):
        unique_document_ids = analytics_df["RP_DOCUMENT_ID"].nunique()
        with soft_assertions():
            assert_that(unique_document_ids).is_greater_than(0)
        print(
            "Number of unique distinct stories that appear in the record file: ",
            unique_document_ids,
        )

    @allure.story("Parse the records file")
    @allure.title("Verify no records are missing by index")
    @allure.description(
        "Test that there are no missing record indexes within each document"
    )
    @allure.severity("blocker")
    def test_missing_records_by_index_in_between(self, analytics_df):
        dropped_records = validate_dropped_analytics(analytics_df)
        with soft_assertions():
            assert_that(
                len(dropped_records),
                f"Missing/dropped records {dropped_records}",
            ).is_equal_to(0)


if __name__ == "__main__":
    pytest.main([__file__])
