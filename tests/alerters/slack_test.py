import json

import mock
import pytest
from requests import RequestException

from elastalert.alerters.slack import SlackAlerter
from elastalert.alerts import BasicMatchString
from elastalert.loaders import FileRulesLoader
from elastalert.util import EAException


def test_slack_uses_custom_title():
    rule = {
        'name': 'Test Rule',
        'type': 'any',
        'slack_webhook_url': 'http://please.dontgohere.slack',
        'alert_subject': 'Cool subject',
        'alert': []
    }
    rules_loader = FileRulesLoader({})
    rules_loader.load_modules(rule)
    alert = SlackAlerter(rule)
    match = {
        '@timestamp': '2016-01-01T00:00:00',
        'somefield': 'foobarbaz'
    }
    with mock.patch('requests.post') as mock_post_request:
        alert.alert([match])

    expected_data = {
        'username': 'elastalert',
        'channel': '',
        'icon_emoji': ':ghost:',
        'attachments': [
            {
                'color': 'danger',
                'title': rule['alert_subject'],
                'text': BasicMatchString(rule, match).__str__(),
                'mrkdwn_in': ['text', 'pretext'],
                'fields': []
            }
        ],
        'text': '',
        'parse': 'none'
    }
    mock_post_request.assert_called_once_with(
        rule['slack_webhook_url'],
        data=mock.ANY,
        headers={'content-type': 'application/json'},
        proxies=None,
        verify=True,
        timeout=10
    )
    assert expected_data == json.loads(mock_post_request.call_args_list[0][1]['data'])


def test_slack_uses_custom_timeout():
    rule = {
        'name': 'Test Rule',
        'type': 'any',
        'slack_webhook_url': 'http://please.dontgohere.slack',
        'alert_subject': 'Cool subject',
        'alert': [],
        'slack_timeout': 20
    }
    rules_loader = FileRulesLoader({})
    rules_loader.load_modules(rule)
    alert = SlackAlerter(rule)
    match = {
        '@timestamp': '2016-01-01T00:00:00',
        'somefield': 'foobarbaz'
    }
    with mock.patch('requests.post') as mock_post_request:
        alert.alert([match])

    expected_data = {
        'username': 'elastalert',
        'channel': '',
        'icon_emoji': ':ghost:',
        'attachments': [
            {
                'color': 'danger',
                'title': rule['alert_subject'],
                'text': BasicMatchString(rule, match).__str__(),
                'mrkdwn_in': ['text', 'pretext'],
                'fields': []
            }
        ],
        'text': '',
        'parse': 'none'
    }
    mock_post_request.assert_called_once_with(
        rule['slack_webhook_url'],
        data=mock.ANY,
        headers={'content-type': 'application/json'},
        proxies=None,
        verify=True,
        timeout=20
    )
    assert expected_data == json.loads(mock_post_request.call_args_list[0][1]['data'])


def test_slack_uses_rule_name_when_custom_title_is_not_provided():
    rule = {
        'name': 'Test Rule',
        'type': 'any',
        'slack_webhook_url': ['http://please.dontgohere.slack'],
        'alert': []
    }
    rules_loader = FileRulesLoader({})
    rules_loader.load_modules(rule)
    alert = SlackAlerter(rule)
    match = {
        '@timestamp': '2016-01-01T00:00:00',
        'somefield': 'foobarbaz'
    }
    with mock.patch('requests.post') as mock_post_request:
        alert.alert([match])

    expected_data = {
        'username': 'elastalert',
        'channel': '',
        'icon_emoji': ':ghost:',
        'attachments': [
            {
                'color': 'danger',
                'title': rule['name'],
                'text': BasicMatchString(rule, match).__str__(),
                'mrkdwn_in': ['text', 'pretext'],
                'fields': []
            }
        ],
        'text': '',
        'parse': 'none',
    }
    mock_post_request.assert_called_once_with(
        rule['slack_webhook_url'][0],
        data=mock.ANY,
        headers={'content-type': 'application/json'},
        proxies=None,
        verify=True,
        timeout=10
    )
    assert expected_data == json.loads(mock_post_request.call_args_list[0][1]['data'])


def test_slack_uses_custom_slack_channel():
    rule = {
        'name': 'Test Rule',
        'type': 'any',
        'slack_webhook_url': ['http://please.dontgohere.slack'],
        'slack_channel_override': '#test-alert',
        'alert': []
    }
    rules_loader = FileRulesLoader({})
    rules_loader.load_modules(rule)
    alert = SlackAlerter(rule)
    match = {
        '@timestamp': '2016-01-01T00:00:00',
        'somefield': 'foobarbaz'
    }
    with mock.patch('requests.post') as mock_post_request:
        alert.alert([match])

    expected_data = {
        'username': 'elastalert',
        'channel': '#test-alert',
        'icon_emoji': ':ghost:',
        'attachments': [
            {
                'color': 'danger',
                'title': rule['name'],
                'text': BasicMatchString(rule, match).__str__(),
                'mrkdwn_in': ['text', 'pretext'],
                'fields': []
            }
        ],
        'text': '',
        'parse': 'none',
    }
    mock_post_request.assert_called_once_with(
        rule['slack_webhook_url'][0],
        data=mock.ANY,
        headers={'content-type': 'application/json'},
        proxies=None,
        verify=True,
        timeout=10
    )
    assert expected_data == json.loads(mock_post_request.call_args_list[0][1]['data'])


def test_slack_uses_list_of_custom_slack_channel():
    rule = {
        'name': 'Test Rule',
        'type': 'any',
        'slack_webhook_url': ['http://please.dontgohere.slack'],
        'slack_channel_override': ['#test-alert', '#test-alert2'],
        'alert': []
    }
    rules_loader = FileRulesLoader({})
    rules_loader.load_modules(rule)
    alert = SlackAlerter(rule)
    match = {
        '@timestamp': '2016-01-01T00:00:00',
        'somefield': 'foobarbaz'
    }
    with mock.patch('requests.post') as mock_post_request:
        alert.alert([match])

    expected_data1 = {
        'username': 'elastalert',
        'channel': '#test-alert',
        'icon_emoji': ':ghost:',
        'attachments': [
            {
                'color': 'danger',
                'title': rule['name'],
                'text': BasicMatchString(rule, match).__str__(),
                'mrkdwn_in': ['text', 'pretext'],
                'fields': []
            }
        ],
        'text': '',
        'parse': 'none'
    }
    expected_data2 = {
        'username': 'elastalert',
        'channel': '#test-alert2',
        'icon_emoji': ':ghost:',
        'attachments': [
            {
                'color': 'danger',
                'title': rule['name'],
                'text': BasicMatchString(rule, match).__str__(),
                'mrkdwn_in': ['text', 'pretext'],
                'fields': []
            }
        ],
        'text': '',
        'parse': 'none'
    }
    mock_post_request.assert_called_with(
        rule['slack_webhook_url'][0],
        data=mock.ANY,
        headers={'content-type': 'application/json'},
        proxies=None,
        verify=True,
        timeout=10
    )
    assert expected_data1 == json.loads(mock_post_request.call_args_list[0][1]['data'])
    assert expected_data2 == json.loads(mock_post_request.call_args_list[1][1]['data'])


def test_slack_attach_kibana_discover_url_when_generated():
    rule = {
        'name': 'Test Rule',
        'type': 'any',
        'slack_attach_kibana_discover_url': True,
        'slack_webhook_url': 'http://please.dontgohere.slack',
        'alert': []
    }
    rules_loader = FileRulesLoader({})
    rules_loader.load_modules(rule)
    alert = SlackAlerter(rule)
    match = {
        '@timestamp': '2016-01-01T00:00:00',
        'kibana_discover_url': 'http://kibana#discover'
    }
    with mock.patch('requests.post') as mock_post_request:
        alert.alert([match])

    expected_data = {
        'username': 'elastalert',
        'parse': 'none',
        'text': '',
        'attachments': [
            {
                'color': 'danger',
                'title': 'Test Rule',
                'text': BasicMatchString(rule, match).__str__(),
                'mrkdwn_in': ['text', 'pretext'],
                'fields': []
            },
            {
                'color': '#ec4b98',
                'title': 'Discover in Kibana',
                'title_link': 'http://kibana#discover'
            }
        ],
        'icon_emoji': ':ghost:',
        'channel': ''
    }
    mock_post_request.assert_called_once_with(
        rule['slack_webhook_url'],
        data=mock.ANY,
        headers={'content-type': 'application/json'},
        proxies=None,
        verify=True,
        timeout=10
    )
    actual_data = json.loads(mock_post_request.call_args_list[0][1]['data'])
    assert expected_data == actual_data


def test_slack_attach_kibana_discover_url_when_not_generated():
    rule = {
        'name': 'Test Rule',
        'type': 'any',
        'slack_attach_kibana_discover_url': True,
        'slack_webhook_url': 'http://please.dontgohere.slack',
        'alert': []
    }
    rules_loader = FileRulesLoader({})
    rules_loader.load_modules(rule)
    alert = SlackAlerter(rule)
    match = {
        '@timestamp': '2016-01-01T00:00:00'
    }
    with mock.patch('requests.post') as mock_post_request:
        alert.alert([match])

    expected_data = {
        'username': 'elastalert',
        'parse': 'none',
        'text': '',
        'attachments': [
            {
                'color': 'danger',
                'title': 'Test Rule',
                'text': BasicMatchString(rule, match).__str__(),
                'mrkdwn_in': ['text', 'pretext'],
                'fields': []
            }
        ],
        'icon_emoji': ':ghost:',
        'channel': ''
    }
    mock_post_request.assert_called_once_with(
        rule['slack_webhook_url'],
        data=mock.ANY,
        headers={'content-type': 'application/json'},
        proxies=None,
        verify=True,
        timeout=10
    )
    actual_data = json.loads(mock_post_request.call_args_list[0][1]['data'])
    assert expected_data == actual_data


def test_slack_kibana_discover_title():
    rule = {
        'name': 'Test Rule',
        'type': 'any',
        'slack_attach_kibana_discover_url': True,
        'slack_kibana_discover_title': 'Click to discover in Kibana',
        'slack_webhook_url': 'http://please.dontgohere.slack',
        'alert': []
    }
    rules_loader = FileRulesLoader({})
    rules_loader.load_modules(rule)
    alert = SlackAlerter(rule)
    match = {
        '@timestamp': '2016-01-01T00:00:00',
        'kibana_discover_url': 'http://kibana#discover'
    }
    with mock.patch('requests.post') as mock_post_request:
        alert.alert([match])

    expected_data = {
        'username': 'elastalert',
        'parse': 'none',
        'text': '',
        'attachments': [
            {
                'color': 'danger',
                'title': 'Test Rule',
                'text': BasicMatchString(rule, match).__str__(),
                'mrkdwn_in': ['text', 'pretext'],
                'fields': []
            },
            {
                'color': '#ec4b98',
                'title': 'Click to discover in Kibana',
                'title_link': 'http://kibana#discover'
            }
        ],
        'icon_emoji': ':ghost:',
        'channel': ''
    }
    mock_post_request.assert_called_once_with(
        rule['slack_webhook_url'],
        data=mock.ANY,
        headers={'content-type': 'application/json'},
        proxies=None,
        verify=True,
        timeout=10
    )
    actual_data = json.loads(mock_post_request.call_args_list[0][1]['data'])
    assert expected_data == actual_data


def test_slack_kibana_discover_color():
    rule = {
        'name': 'Test Rule',
        'type': 'any',
        'slack_attach_kibana_discover_url': True,
        'slack_kibana_discover_color': 'blue',
        'slack_webhook_url': 'http://please.dontgohere.slack',
        'alert': []
    }
    rules_loader = FileRulesLoader({})
    rules_loader.load_modules(rule)
    alert = SlackAlerter(rule)
    match = {
        '@timestamp': '2016-01-01T00:00:00',
        'kibana_discover_url': 'http://kibana#discover'
    }
    with mock.patch('requests.post') as mock_post_request:
        alert.alert([match])

    expected_data = {
        'username': 'elastalert',
        'parse': 'none',
        'text': '',
        'attachments': [
            {
                'color': 'danger',
                'title': 'Test Rule',
                'text': BasicMatchString(rule, match).__str__(),
                'mrkdwn_in': ['text', 'pretext'],
                'fields': []
            },
            {
                'color': 'blue',
                'title': 'Discover in Kibana',
                'title_link': 'http://kibana#discover'
            }
        ],
        'icon_emoji': ':ghost:',
        'channel': ''
    }
    mock_post_request.assert_called_once_with(
        rule['slack_webhook_url'],
        data=mock.ANY,
        headers={'content-type': 'application/json'},
        proxies=None,
        verify=True,
        timeout=10
    )
    actual_data = json.loads(mock_post_request.call_args_list[0][1]['data'])
    assert expected_data == actual_data


def test_slack_ignore_ssl_errors():
    rule = {
        'name': 'Test Rule',
        'type': 'any',
        'slack_webhook_url': 'http://please.dontgohere.slack',
        'slack_ignore_ssl_errors': True,
        'alert': []
    }
    rules_loader = FileRulesLoader({})
    rules_loader.load_modules(rule)
    alert = SlackAlerter(rule)
    match = {
        '@timestamp': '2016-01-01T00:00:00'
    }
    with mock.patch('requests.post') as mock_post_request:
        alert.alert([match])

    mock_post_request.assert_called_once_with(
        rule['slack_webhook_url'],
        data=mock.ANY,
        headers={'content-type': 'application/json'},
        proxies=None,
        verify=False,
        timeout=10
    )

    expected_data = {
        'username': 'elastalert',
        'channel': '',
        'icon_emoji': ':ghost:',
        'attachments': [
            {
                'color': 'danger',
                'title': 'Test Rule',
                'text': BasicMatchString(rule, match).__str__(),
                'mrkdwn_in': ['text', 'pretext'],
                'fields': []
            }
        ],
        'text': '',
        'parse': 'none'
    }
    assert expected_data == json.loads(mock_post_request.call_args_list[0][1]['data'])


def test_slack_proxy():
    rule = {
        'name': 'Test Rule',
        'type': 'any',
        'slack_webhook_url': 'http://please.dontgohere.slack',
        'slack_proxy': 'http://proxy.url',
        'alert_subject': 'Cool subject',
        'alert': []
    }
    rules_loader = FileRulesLoader({})
    rules_loader.load_modules(rule)
    alert = SlackAlerter(rule)
    match = {
        '@timestamp': '2016-01-01T00:00:00',
        'somefield': 'foobarbaz'
    }
    with mock.patch('requests.post') as mock_post_request:
        alert.alert([match])

    expected_data = {
        'username': 'elastalert',
        'channel': '',
        'icon_emoji': ':ghost:',
        'attachments': [
            {
                'color': 'danger',
                'title': rule['alert_subject'],
                'text': BasicMatchString(rule, match).__str__(),
                'mrkdwn_in': ['text', 'pretext'],
                'fields': []
            }
        ],
        'text': '',
        'parse': 'none'
    }
    mock_post_request.assert_called_once_with(
        rule['slack_webhook_url'],
        data=mock.ANY,
        headers={'content-type': 'application/json'},
        proxies={'https': rule['slack_proxy']},
        verify=True,
        timeout=10
    )
    assert expected_data == json.loads(mock_post_request.call_args_list[0][1]['data'])


def test_slack_username_override():
    rule = {
        'name': 'Test Rule',
        'type': 'any',
        'slack_webhook_url': 'http://please.dontgohere.slack',
        'slack_username_override': 'test elastalert',
        'alert_subject': 'Cool subject',
        'alert': []
    }
    rules_loader = FileRulesLoader({})
    rules_loader.load_modules(rule)
    alert = SlackAlerter(rule)
    match = {
        '@timestamp': '2016-01-01T00:00:00',
        'somefield': 'foobarbaz'
    }
    with mock.patch('requests.post') as mock_post_request:
        alert.alert([match])

    expected_data = {
        'username': 'test elastalert',
        'channel': '',
        'icon_emoji': ':ghost:',
        'attachments': [
            {
                'color': 'danger',
                'title': rule['alert_subject'],
                'text': BasicMatchString(rule, match).__str__(),
                'mrkdwn_in': ['text', 'pretext'],
                'fields': []
            }
        ],
        'text': '',
        'parse': 'none'
    }
    mock_post_request.assert_called_once_with(
        rule['slack_webhook_url'],
        data=mock.ANY,
        headers={'content-type': 'application/json'},
        proxies=None,
        verify=True,
        timeout=10
    )
    assert expected_data == json.loads(mock_post_request.call_args_list[0][1]['data'])


def test_slack_title_link():
    rule = {
        'name': 'Test Rule',
        'type': 'any',
        'slack_webhook_url': 'http://please.dontgohere.slack',
        'slack_username_override': 'elastalert',
        'slack_title_link': 'http://slack.title.link',
        'alert_subject': 'Cool subject',
        'alert': []
    }
    rules_loader = FileRulesLoader({})
    rules_loader.load_modules(rule)
    alert = SlackAlerter(rule)
    match = {
        '@timestamp': '2016-01-01T00:00:00',
        'somefield': 'foobarbaz'
    }
    with mock.patch('requests.post') as mock_post_request:
        alert.alert([match])

    expected_data = {
        'username': 'elastalert',
        'channel': '',
        'icon_emoji': ':ghost:',
        'attachments': [
            {
                'color': 'danger',
                'title': rule['alert_subject'],
                'text': BasicMatchString(rule, match).__str__(),
                'mrkdwn_in': ['text', 'pretext'],
                'fields': [],
                'title_link': 'http://slack.title.link'
            }
        ],
        'text': '',
        'parse': 'none'
    }
    mock_post_request.assert_called_once_with(
        rule['slack_webhook_url'],
        data=mock.ANY,
        headers={'content-type': 'application/json'},
        proxies=None,
        verify=True,
        timeout=10
    )
    assert expected_data == json.loads(mock_post_request.call_args_list[0][1]['data'])


def test_slack_title():
    rule = {
        'name': 'Test Rule',
        'type': 'any',
        'slack_webhook_url': 'http://please.dontgohere.slack',
        'slack_username_override': 'elastalert',
        'slack_title': 'slack title',
        'alert_subject': 'Cool subject',
        'alert': []
    }
    rules_loader = FileRulesLoader({})
    rules_loader.load_modules(rule)
    alert = SlackAlerter(rule)
    match = {
        '@timestamp': '2016-01-01T00:00:00',
        'somefield': 'foobarbaz'
    }
    with mock.patch('requests.post') as mock_post_request:
        alert.alert([match])

    expected_data = {
        'username': 'elastalert',
        'channel': '',
        'icon_emoji': ':ghost:',
        'attachments': [
            {
                'color': 'danger',
                'title': 'slack title',
                'text': BasicMatchString(rule, match).__str__(),
                'mrkdwn_in': ['text', 'pretext'],
                'fields': []
            }
        ],
        'text': '',
        'parse': 'none'
    }
    mock_post_request.assert_called_once_with(
        rule['slack_webhook_url'],
        data=mock.ANY,
        headers={'content-type': 'application/json'},
        proxies=None,
        verify=True,
        timeout=10
    )
    assert expected_data == json.loads(mock_post_request.call_args_list[0][1]['data'])


def test_slack_icon_url_override():
    rule = {
        'name': 'Test Rule',
        'type': 'any',
        'slack_webhook_url': 'http://please.dontgohere.slack',
        'slack_username_override': 'elastalert',
        'slack_icon_url_override': 'http://slack.icon.url.override',
        'alert_subject': 'Cool subject',
        'alert': []
    }
    rules_loader = FileRulesLoader({})
    rules_loader.load_modules(rule)
    alert = SlackAlerter(rule)
    match = {
        '@timestamp': '2016-01-01T00:00:00',
        'somefield': 'foobarbaz'
    }
    with mock.patch('requests.post') as mock_post_request:
        alert.alert([match])

    expected_data = {
        'username': 'elastalert',
        'channel': '',
        'icon_url': 'http://slack.icon.url.override',
        'attachments': [
            {
                'color': 'danger',
                'title': rule['alert_subject'],
                'text': BasicMatchString(rule, match).__str__(),
                'mrkdwn_in': ['text', 'pretext'],
                'fields': []
            }
        ],
        'text': '',
        'parse': 'none'
    }
    mock_post_request.assert_called_once_with(
        rule['slack_webhook_url'],
        data=mock.ANY,
        headers={'content-type': 'application/json'},
        proxies=None,
        verify=True,
        timeout=10
    )
    assert expected_data == json.loads(mock_post_request.call_args_list[0][1]['data'])


def test_slack_msg_color():
    rule = {
        'name': 'Test Rule',
        'type': 'any',
        'slack_webhook_url': 'http://please.dontgohere.slack',
        'slack_username_override': 'elastalert',
        'slack_msg_color': 'good',
        'alert_subject': 'Cool subject',
        'alert': []
    }
    rules_loader = FileRulesLoader({})
    rules_loader.load_modules(rule)
    alert = SlackAlerter(rule)
    match = {
        '@timestamp': '2016-01-01T00:00:00',
        'somefield': 'foobarbaz'
    }
    with mock.patch('requests.post') as mock_post_request:
        alert.alert([match])

    expected_data = {
        'username': 'elastalert',
        'channel': '',
        'icon_emoji': ':ghost:',
        'attachments': [
            {
                'color': 'good',
                'title': rule['alert_subject'],
                'text': BasicMatchString(rule, match).__str__(),
                'mrkdwn_in': ['text', 'pretext'],
                'fields': []
            }
        ],
        'text': '',
        'parse': 'none'
    }
    mock_post_request.assert_called_once_with(
        rule['slack_webhook_url'],
        data=mock.ANY,
        headers={'content-type': 'application/json'},
        proxies=None,
        verify=True,
        timeout=10
    )
    assert expected_data == json.loads(mock_post_request.call_args_list[0][1]['data'])


def test_slack_parse_override():
    rule = {
        'name': 'Test Rule',
        'type': 'any',
        'slack_webhook_url': 'http://please.dontgohere.slack',
        'slack_username_override': 'elastalert',
        'slack_parse_override': 'full',
        'alert_subject': 'Cool subject',
        'alert': []
    }
    rules_loader = FileRulesLoader({})
    rules_loader.load_modules(rule)
    alert = SlackAlerter(rule)
    match = {
        '@timestamp': '2016-01-01T00:00:00',
        'somefield': 'foobarbaz'
    }
    with mock.patch('requests.post') as mock_post_request:
        alert.alert([match])

    expected_data = {
        'username': 'elastalert',
        'channel': '',
        'icon_emoji': ':ghost:',
        'attachments': [
            {
                'color': 'danger',
                'title': rule['alert_subject'],
                'text': BasicMatchString(rule, match).__str__(),
                'mrkdwn_in': ['text', 'pretext'],
                'fields': []
            }
        ],
        'text': '',
        'parse': 'full'
    }
    mock_post_request.assert_called_once_with(
        rule['slack_webhook_url'],
        data=mock.ANY,
        headers={'content-type': 'application/json'},
        proxies=None,
        verify=True,
        timeout=10
    )
    assert expected_data == json.loads(mock_post_request.call_args_list[0][1]['data'])


def test_slack_text_string():
    rule = {
        'name': 'Test Rule',
        'type': 'any',
        'slack_webhook_url': 'http://please.dontgohere.slack',
        'slack_username_override': 'elastalert',
        'slack_text_string': 'text str',
        'alert_subject': 'Cool subject',
        'alert': []
    }
    rules_loader = FileRulesLoader({})
    rules_loader.load_modules(rule)
    alert = SlackAlerter(rule)
    match = {
        '@timestamp': '2016-01-01T00:00:00',
        'somefield': 'foobarbaz'
    }
    with mock.patch('requests.post') as mock_post_request:
        alert.alert([match])

    expected_data = {
        'username': 'elastalert',
        'channel': '',
        'icon_emoji': ':ghost:',
        'attachments': [
            {
                'color': 'danger',
                'title': rule['alert_subject'],
                'text': BasicMatchString(rule, match).__str__(),
                'mrkdwn_in': ['text', 'pretext'],
                'fields': []
            }
        ],
        'text': 'text str',
        'parse': 'none'
    }
    mock_post_request.assert_called_once_with(
        rule['slack_webhook_url'],
        data=mock.ANY,
        headers={'content-type': 'application/json'},
        proxies=None,
        verify=True,
        timeout=10
    )
    assert expected_data == json.loads(mock_post_request.call_args_list[0][1]['data'])


def test_slack_alert_fields():
    rule = {
        'name': 'Test Rule',
        'type': 'any',
        'slack_webhook_url': 'http://please.dontgohere.slack',
        'slack_username_override': 'elastalert',
        'slack_alert_fields': [
            {
                'title': 'Host',
                'value': 'somefield',
                'short': 'true'
            },
            {
                'title': 'Sensors',
                'value': '@timestamp',
                'short': 'true'
            }
        ],
        'alert_subject': 'Cool subject',
        'alert': []
    }
    rules_loader = FileRulesLoader({})
    rules_loader.load_modules(rule)
    alert = SlackAlerter(rule)
    match = {
        '@timestamp': '2016-01-01T00:00:00',
        'somefield': 'foobarbaz'
    }
    with mock.patch('requests.post') as mock_post_request:
        alert.alert([match])

    expected_data = {
        'username': 'elastalert',
        'channel': '',
        'icon_emoji': ':ghost:',
        'attachments': [
            {
                'color': 'danger',
                'title': rule['alert_subject'],
                'text': BasicMatchString(rule, match).__str__(),
                'mrkdwn_in': ['text', 'pretext'],
                'fields':
                [
                    {
                        'short': 'true',
                        'title': 'Host',
                        'value': 'foobarbaz'
                    },
                    {
                        'short': 'true',
                        'title': 'Sensors',
                        'value': '2016-01-01T00:00:00'
                    }
                ],
            }
        ],
        'text': '',
        'parse': 'none'
    }
    mock_post_request.assert_called_once_with(
        rule['slack_webhook_url'],
        data=mock.ANY,
        headers={'content-type': 'application/json'},
        proxies=None,
        verify=True,
        timeout=10
    )
    assert expected_data == json.loads(mock_post_request.call_args_list[0][1]['data'])


def test_slack_ca_certs():
    rule = {
        'name': 'Test Rule',
        'type': 'any',
        'slack_webhook_url': 'http://please.dontgohere.slack',
        'slack_username_override': 'elastalert',
        'slack_ca_certs': True,
        'alert_subject': 'Cool subject',
        'alert': []
    }
    rules_loader = FileRulesLoader({})
    rules_loader.load_modules(rule)
    alert = SlackAlerter(rule)
    match = {
        '@timestamp': '2016-01-01T00:00:00',
        'somefield': 'foobarbaz'
    }
    with mock.patch('requests.post') as mock_post_request:
        alert.alert([match])

    expected_data = {
        'username': 'elastalert',
        'channel': '',
        'icon_emoji': ':ghost:',
        'attachments': [
            {
                'color': 'danger',
                'title': rule['alert_subject'],
                'text': BasicMatchString(rule, match).__str__(),
                'mrkdwn_in': ['text', 'pretext'],
                'fields': [],
            }
        ],
        'text': '',
        'parse': 'none'
    }
    mock_post_request.assert_called_once_with(
        rule['slack_webhook_url'],
        data=mock.ANY,
        headers={'content-type': 'application/json'},
        proxies=None,
        verify=True,
        timeout=10
    )
    assert expected_data == json.loads(mock_post_request.call_args_list[0][1]['data'])


def test_slack_footer():
    rule = {
        'name': 'Test Rule',
        'type': 'any',
        'slack_webhook_url': 'http://please.dontgohere.slack',
        'slack_username_override': 'elastalert',
        'slack_footer': 'Elastic Alerts',
        'slack_footer_icon': 'http://footer.icon.url',
        'alert_subject': 'Cool subject',
        'alert': []
    }
    rules_loader = FileRulesLoader({})
    rules_loader.load_modules(rule)
    alert = SlackAlerter(rule)
    match = {
        '@timestamp': '2016-01-01T00:00:00',
        'somefield': 'foobarbaz'
    }
    with mock.patch('requests.post') as mock_post_request:
        alert.alert([match])

    expected_data = {
        'username': 'elastalert',
        'channel': '',
        'icon_emoji': ':ghost:',
        'attachments': [
            {
                'color': 'danger',
                'title': rule['alert_subject'],
                'text': BasicMatchString(rule, match).__str__(),
                'mrkdwn_in': ['text', 'pretext'],
                'fields': [],
                'footer': 'Elastic Alerts',
                'footer_icon': 'http://footer.icon.url'
            }
        ],
        'text': '',
        'parse': 'none'
    }
    mock_post_request.assert_called_once_with(
        rule['slack_webhook_url'],
        data=mock.ANY,
        headers={'content-type': 'application/json'},
        proxies=None,
        verify=True,
        timeout=10
    )
    assert expected_data == json.loads(mock_post_request.call_args_list[0][1]['data'])


def test_slack_image_url():
    rule = {
        'name': 'Test Rule',
        'type': 'any',
        'slack_webhook_url': 'http://please.dontgohere.slack',
        'slack_username_override': 'elastalert',
        'slack_image_url': 'http://image.url',
        'alert_subject': 'Cool subject',
        'alert': []
    }
    rules_loader = FileRulesLoader({})
    rules_loader.load_modules(rule)
    alert = SlackAlerter(rule)
    match = {
        '@timestamp': '2016-01-01T00:00:00',
        'somefield': 'foobarbaz'
    }
    with mock.patch('requests.post') as mock_post_request:
        alert.alert([match])

    expected_data = {
        'username': 'elastalert',
        'channel': '',
        'icon_emoji': ':ghost:',
        'attachments': [
            {
                'color': 'danger',
                'title': rule['alert_subject'],
                'text': BasicMatchString(rule, match).__str__(),
                'mrkdwn_in': ['text', 'pretext'],
                'fields': [],
                'image_url': 'http://image.url',
            }
        ],
        'text': '',
        'parse': 'none'
    }
    mock_post_request.assert_called_once_with(
        rule['slack_webhook_url'],
        data=mock.ANY,
        headers={'content-type': 'application/json'},
        proxies=None,
        verify=True,
        timeout=10
    )
    assert expected_data == json.loads(mock_post_request.call_args_list[0][1]['data'])


def test_slack_thumb_url():
    rule = {
        'name': 'Test Rule',
        'type': 'any',
        'slack_webhook_url': 'http://please.dontgohere.slack',
        'slack_username_override': 'elastalert',
        'slack_thumb_url': 'http://thumb.url',
        'alert_subject': 'Cool subject',
        'alert': []
    }
    rules_loader = FileRulesLoader({})
    rules_loader.load_modules(rule)
    alert = SlackAlerter(rule)
    match = {
        '@timestamp': '2016-01-01T00:00:00',
        'somefield': 'foobarbaz'
    }
    with mock.patch('requests.post') as mock_post_request:
        alert.alert([match])

    expected_data = {
        'username': 'elastalert',
        'channel': '',
        'icon_emoji': ':ghost:',
        'attachments': [
            {
                'color': 'danger',
                'title': rule['alert_subject'],
                'text': BasicMatchString(rule, match).__str__(),
                'mrkdwn_in': ['text', 'pretext'],
                'fields': [],
                'thumb_url': 'http://thumb.url',
            }
        ],
        'text': '',
        'parse': 'none'
    }
    mock_post_request.assert_called_once_with(
        rule['slack_webhook_url'],
        data=mock.ANY,
        headers={'content-type': 'application/json'},
        proxies=None,
        verify=True,
        timeout=10
    )
    assert expected_data == json.loads(mock_post_request.call_args_list[0][1]['data'])


def test_slack_author_name():
    rule = {
        'name': 'Test Rule',
        'type': 'any',
        'slack_webhook_url': 'http://please.dontgohere.slack',
        'slack_username_override': 'elastalert',
        'slack_author_name': 'author name',
        'alert_subject': 'Cool subject',
        'alert': []
    }
    rules_loader = FileRulesLoader({})
    rules_loader.load_modules(rule)
    alert = SlackAlerter(rule)
    match = {
        '@timestamp': '2016-01-01T00:00:00',
        'somefield': 'foobarbaz'
    }
    with mock.patch('requests.post') as mock_post_request:
        alert.alert([match])

    expected_data = {
        'username': 'elastalert',
        'channel': '',
        'icon_emoji': ':ghost:',
        'attachments': [
            {
                'color': 'danger',
                'title': rule['alert_subject'],
                'text': BasicMatchString(rule, match).__str__(),
                'mrkdwn_in': ['text', 'pretext'],
                'fields': [],
                'author_name': 'author name',
            }
        ],
        'text': '',
        'parse': 'none'
    }
    mock_post_request.assert_called_once_with(
        rule['slack_webhook_url'],
        data=mock.ANY,
        headers={'content-type': 'application/json'},
        proxies=None,
        verify=True,
        timeout=10
    )
    assert expected_data == json.loads(mock_post_request.call_args_list[0][1]['data'])


def test_slack_author_link():
    rule = {
        'name': 'Test Rule',
        'type': 'any',
        'slack_webhook_url': 'http://please.dontgohere.slack',
        'slack_username_override': 'elastalert',
        'slack_author_link': 'http://author.url',
        'alert_subject': 'Cool subject',
        'alert': []
    }
    rules_loader = FileRulesLoader({})
    rules_loader.load_modules(rule)
    alert = SlackAlerter(rule)
    match = {
        '@timestamp': '2016-01-01T00:00:00',
        'somefield': 'foobarbaz'
    }
    with mock.patch('requests.post') as mock_post_request:
        alert.alert([match])

    expected_data = {
        'username': 'elastalert',
        'channel': '',
        'icon_emoji': ':ghost:',
        'attachments': [
            {
                'color': 'danger',
                'title': rule['alert_subject'],
                'text': BasicMatchString(rule, match).__str__(),
                'mrkdwn_in': ['text', 'pretext'],
                'fields': [],
                'author_link': 'http://author.url',
            }
        ],
        'text': '',
        'parse': 'none'
    }
    mock_post_request.assert_called_once_with(
        rule['slack_webhook_url'],
        data=mock.ANY,
        headers={'content-type': 'application/json'},
        proxies=None,
        verify=True,
        timeout=10
    )
    assert expected_data == json.loads(mock_post_request.call_args_list[0][1]['data'])


def test_slack_author_icon():
    rule = {
        'name': 'Test Rule',
        'type': 'any',
        'slack_webhook_url': 'http://please.dontgohere.slack',
        'slack_username_override': 'elastalert',
        'slack_author_icon': 'http://author.icon',
        'alert_subject': 'Cool subject',
        'alert': []
    }
    rules_loader = FileRulesLoader({})
    rules_loader.load_modules(rule)
    alert = SlackAlerter(rule)
    match = {
        '@timestamp': '2016-01-01T00:00:00',
        'somefield': 'foobarbaz'
    }
    with mock.patch('requests.post') as mock_post_request:
        alert.alert([match])

    expected_data = {
        'username': 'elastalert',
        'channel': '',
        'icon_emoji': ':ghost:',
        'attachments': [
            {
                'color': 'danger',
                'title': rule['alert_subject'],
                'text': BasicMatchString(rule, match).__str__(),
                'mrkdwn_in': ['text', 'pretext'],
                'fields': [],
                'author_icon': 'http://author.icon',
            }
        ],
        'text': '',
        'parse': 'none'
    }
    mock_post_request.assert_called_once_with(
        rule['slack_webhook_url'],
        data=mock.ANY,
        headers={'content-type': 'application/json'},
        proxies=None,
        verify=True,
        timeout=10
    )
    assert expected_data == json.loads(mock_post_request.call_args_list[0][1]['data'])


def test_slack_msg_pretext():
    rule = {
        'name': 'Test Rule',
        'type': 'any',
        'slack_webhook_url': 'http://please.dontgohere.slack',
        'slack_username_override': 'elastalert',
        'slack_msg_pretext': 'pretext value',
        'alert_subject': 'Cool subject',
        'alert': []
    }
    rules_loader = FileRulesLoader({})
    rules_loader.load_modules(rule)
    alert = SlackAlerter(rule)
    match = {
        '@timestamp': '2016-01-01T00:00:00',
        'somefield': 'foobarbaz'
    }
    with mock.patch('requests.post') as mock_post_request:
        alert.alert([match])

    expected_data = {
        'username': 'elastalert',
        'channel': '',
        'icon_emoji': ':ghost:',
        'attachments': [
            {
                'color': 'danger',
                'title': rule['alert_subject'],
                'text': BasicMatchString(rule, match).__str__(),
                'mrkdwn_in': ['text', 'pretext'],
                'fields': [],
                'pretext': 'pretext value'
            }
        ],
        'text': '',
        'parse': 'none'
    }
    mock_post_request.assert_called_once_with(
        rule['slack_webhook_url'],
        data=mock.ANY,
        headers={'content-type': 'application/json'},
        proxies=None,
        verify=True,
        timeout=10
    )
    assert expected_data == json.loads(mock_post_request.call_args_list[0][1]['data'])


def test_slack_ea_exception():
    try:
        rule = {
            'name': 'Test Rule',
            'type': 'any',
            'slack_webhook_url': 'http://please.dontgohere.slack',
            'slack_username_override': 'elastalert',
            'slack_msg_pretext': 'pretext value',
            'alert_subject': 'Cool subject',
            'alert': []
        }
        rules_loader = FileRulesLoader({})
        rules_loader.load_modules(rule)
        alert = SlackAlerter(rule)
        match = {
            '@timestamp': '2016-01-01T00:00:00',
            'somefield': 'foobarbaz'
        }
        mock_run = mock.MagicMock(side_effect=RequestException)
        with mock.patch('requests.post', mock_run), pytest.raises(RequestException):
            alert.alert([match])
    except EAException:
        assert True
