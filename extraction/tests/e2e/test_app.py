def test_dummy_function(client, make_cloudwatch_scheduled_event):
    assert client.lambda_.invoke(
        "dummy", make_cloudwatch_scheduled_event(client)
    ).payload == {"ping": "pong"}
