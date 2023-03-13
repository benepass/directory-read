def test_extract_function(
    client,
    freeze,
    mocked_merge_roster_response,
    make_cloudwatch_scheduled_event,
):
    assert client.lambda_.invoke(
        "extract", make_cloudwatch_scheduled_event(client)
    ).payload == {"ok": True, "data": ""}
