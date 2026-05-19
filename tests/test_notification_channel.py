"""Tests for notification channel models (config union, Channel,
ChannelCreate, ChannelUpdate)."""
from datetime import datetime, timezone

import pytest
from pydantic import TypeAdapter, ValidationError


def test_apprise_channel_config():
    from arm_contracts.notification_channel import AppriseChannelConfig
    c = AppriseChannelConfig(url="discord://id/token")
    assert c.type == "apprise"
    assert c.url == "discord://id/token"


def test_webhook_channel_config_with_secret():
    from arm_contracts.notification_channel import WebhookChannelConfig
    c = WebhookChannelConfig(
        url="https://example.com/hook",
        shared_secret="s3cret",
    )
    assert c.type == "webhook"
    # SecretStr masks on repr/str but exposes via get_secret_value().
    assert str(c.shared_secret) == "**********"
    assert c.shared_secret.get_secret_value() == "s3cret"


def test_webhook_channel_config_no_secret():
    from arm_contracts.notification_channel import WebhookChannelConfig
    c = WebhookChannelConfig(url="https://example.com/hook")
    assert c.shared_secret is None
    assert c.headers is None


def test_webhook_channel_config_rejects_non_http_url():
    from arm_contracts.notification_channel import WebhookChannelConfig
    with pytest.raises(ValidationError):
        WebhookChannelConfig(url="ftp://example.com/")


def test_bash_channel_config():
    from arm_contracts.notification_channel import BashChannelConfig
    c = BashChannelConfig(script_path="/opt/arm/scripts/notify.sh")
    assert c.type == "bash"
    assert c.script_path == "/opt/arm/scripts/notify.sh"


def test_channel_config_union_discriminates_apprise():
    from arm_contracts.notification_channel import (
        ChannelConfig,
        AppriseChannelConfig,
    )
    adapter = TypeAdapter(ChannelConfig)
    parsed = adapter.validate_python({"type": "apprise", "url": "discord://x/y"})
    assert isinstance(parsed, AppriseChannelConfig)


def test_channel_config_union_discriminates_webhook():
    from arm_contracts.notification_channel import (
        ChannelConfig,
        WebhookChannelConfig,
    )
    adapter = TypeAdapter(ChannelConfig)
    parsed = adapter.validate_python({
        "type": "webhook",
        "url": "https://example.com/hook",
    })
    assert isinstance(parsed, WebhookChannelConfig)


def test_channel_config_union_discriminates_bash():
    from arm_contracts.notification_channel import (
        ChannelConfig,
        BashChannelConfig,
    )
    adapter = TypeAdapter(ChannelConfig)
    parsed = adapter.validate_python({"type": "bash", "script_path": "/x"})
    assert isinstance(parsed, BashChannelConfig)


def test_channel_config_union_rejects_unknown_type():
    from arm_contracts.notification_channel import ChannelConfig
    adapter = TypeAdapter(ChannelConfig)
    with pytest.raises(ValidationError):
        adapter.validate_python({"type": "smoke-signal", "url": "x"})


def test_event_keys_literal_matches_event_union():
    """The four keys in EVENT_KEYS must be exactly the four event_key
    literals used by NotificationEvent. If anyone adds an event, both
    sides must update together."""
    from typing import get_args
    from arm_contracts.notification_channel import EVENT_KEYS
    from arm_contracts.notification_event import (
        JobStartedEvent,
        JobRipCompleteEvent,
        JobTranscodeCompleteEvent,
        JobFailedEvent,
    )
    event_keys_set = set(get_args(EVENT_KEYS))
    union_keys = {
        JobStartedEvent.model_fields["event_key"].default,
        JobRipCompleteEvent.model_fields["event_key"].default,
        JobTranscodeCompleteEvent.model_fields["event_key"].default,
        JobFailedEvent.model_fields["event_key"].default,
    }
    assert event_keys_set == union_keys


def test_channel_template_all_fields_optional():
    from arm_contracts.notification_channel import ChannelTemplate
    t = ChannelTemplate()
    assert t.title is None
    assert t.body is None
    t2 = ChannelTemplate(title="X", body="Y")
    assert t2.title == "X"
    assert t2.body == "Y"


def test_public_re_exports():
    """All new names must be importable from the package root."""
    from arm_contracts import (
        # event types
        NotificationEvent,
        JobStartedEvent,
        JobRipCompleteEvent,
        JobTranscodeCompleteEvent,
        JobFailedEvent,
        # channel types
        AppriseChannelConfig,
        WebhookChannelConfig,
        BashChannelConfig,
        ChannelConfig,
        ChannelTemplate,
        EVENT_KEYS,
    )
    # If any name is missing the import raises ImportError, failing the test.
    assert NotificationEvent is not None
    assert ChannelConfig is not None
