def test_dataset(df):
    column_list = ["tweet", "label", "cleaned_tweet"]
    df.expect_table_columns_to_match_ordered_list(column_list=column_list)
    labels = [1, 0]
    df.expect_column_values_to_be_in_set(column="label", value_set=labels)
    df.expect_column_values_to_not_be_null(column="label")
    df.expect_column_values_to_be_of_type(column="cleaned_tweet", type_="str")

    expectation_suite = df.get_expectation_suite(discard_failed_expectations=False)
    results = df.validate(
        expectation_suite=expectation_suite, only_return_failures=True
    ).to_json_dict()
    assert results["success"]
