import pytest

from bluesky_kafka import BlueskyConsumer


def test_consumer_config():
    """
    This test targets combining bootstrap servers specified
    with the `bootstrap_servers` parameter and in the `consumer_config`.
    """
    test_topic = "test.consumer.config"
    bluesky_consumer = BlueskyConsumer(
        topics=[test_topic],
        bootstrap_servers="1.2.3.4:9092",
        group_id="abc",
        consumer_config={
            "bootstrap.servers": "5.6.7.8:9092",
            "auto.offset.reset": "latest",
        },
    )

    assert (
        bluesky_consumer._consumer_config["bootstrap.servers"]
        == "1.2.3.4:9092,5.6.7.8:9092"
    )


def test_redact_password_from_str_output():
    bluesky_consumer = BlueskyConsumer(
        topics=["test.redact.password"],
        bootstrap_servers="1.2.3.4:9092",
        group_id="test-redact-password-group",
        consumer_config={
            "sasl.password": "PASSWORD",
        },
    )

    bluesky_consumer_str_output = str(bluesky_consumer)
    assert "PASSWORD" not in bluesky_consumer_str_output
    assert "sasl.password" in bluesky_consumer_str_output
    assert "****" in bluesky_consumer_str_output


def test_bad_consumer_config():
    test_topic = "test.bad.consumer.config"
    with pytest.raises(ValueError) as excinfo:
        BlueskyConsumer(
            topics=[test_topic],
            bootstrap_servers="1.2.3.4:9092",
            group_id="test-bad-consumer_config",
            consumer_config={
                "bootstrap.servers": "5.6.7.8:9092",
                "auto.offset.reset": "latest",
                "group.id": "raise an exception!",
            },
        )
        assert (
            "do not specify 'group.id' in consumer_config, use only the 'group_id' argument"
            in excinfo.value
        )
