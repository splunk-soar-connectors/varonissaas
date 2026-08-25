# File: varonissaas_test.py
#
# Copyright (c) Varonis, 2024-2026
#
# This unpublished material is proprietary to Varonis SaaS. All
# rights reserved. The methods and techniques described herein are
# considered trade secrets and/or confidential. Reproduction or
# distribution, in whole or in part, is forbidden except by express
# written permission of Varonis SaaS.
#
# Licensed under the Apache License, Version 2.0 (the 'License');
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software distributed under
# the License is distributed on an 'AS IS' BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND,
# either express or implied. See the License for the specific language governing permissions
# and limitations under the License.

import json
import time
import unittest
from datetime import datetime, timedelta, timezone
from unittest.mock import MagicMock, patch

from phantom.action_result import ActionResult

from varonissaas_connector import REQUEST_BACKOFF_FACTOR, REQUEST_RETRIES, VaronisSaasConnector
from varonissaas_consts import *
from varonissaas_search import ALERT_STATUSES, CLOSE_REASONS
from varonissaas_tools import multi_value_to_string_list


class VaronisSaaSTest(unittest.TestCase):
    def setUp(self) -> None:
        self.connector = VaronisSaasConnector()
        self.connector._base_url = "https://test.com"

    def test_initialize_enables_tls_verification_by_default(self):
        self.connector.load_state = MagicMock(
            return_value={
                VDSP_ACCESS_TOKEN_KEY: "cached-token",
                VDSP_TOKEN_TYPE_KEY: "Bearer",
                VDSP_EXPIRES_IN_KEY: int(time.time()) + 3600,
            }
        )
        self.connector.get_config = MagicMock(return_value={VDSP_JSON_BASE_URL_KEY: "https://test.com", VDSP_SCRT: "api-key"})

        self.assertTrue(self.connector.initialize())

        self.assertTrue(self.connector._verify)

    def test_initialize_keeps_explicit_tls_opt_out(self):
        self.connector.load_state = MagicMock(
            return_value={
                VDSP_ACCESS_TOKEN_KEY: "cached-token",
                VDSP_TOKEN_TYPE_KEY: "Bearer",
                VDSP_EXPIRES_IN_KEY: int(time.time()) + 3600,
            }
        )
        self.connector.get_config = MagicMock(
            return_value={VDSP_JSON_BASE_URL_KEY: "https://test.com", VDSP_SCRT: "api-key", "verify_server_cert": False}
        )

        self.assertTrue(self.connector.initialize())

        self.assertFalse(self.connector._verify)

    @patch("varonissaas_connector.encryption_helper")
    def test_finalize_encrypts_legacy_access_token_state(self, encryption_helper):
        state = {
            VDSP_ACCESS_TOKEN_KEY: "legacy-token",
            VDSP_TOKEN_TYPE_KEY: "Bearer",
            VDSP_EXPIRES_IN_KEY: int(time.time()) + 3600,
        }
        self.connector.load_state = MagicMock(return_value=state)
        self.connector.get_config = MagicMock(return_value={VDSP_JSON_BASE_URL_KEY: "https://test.com", VDSP_SCRT: "api-key"})
        self.connector.get_asset_id = MagicMock(return_value=42)
        self.connector.save_state = MagicMock()
        encryption_helper.encrypt.return_value = "encrypted-token"

        self.assertTrue(self.connector.initialize())
        self.assertTrue(self.connector.finalize())

        encryption_helper.encrypt.assert_called_once_with("legacy-token", 42)
        self.assertTrue(state[VDSP_ACCESS_TOKEN_IS_ENCRYPTED])
        self.assertEqual(state[VDSP_ACCESS_TOKEN_KEY], "encrypted-token")
        self.connector.save_state.assert_called_once_with(state)

    @patch("varonissaas_connector.encryption_helper")
    def test_initialize_decrypts_persisted_access_token(self, encryption_helper):
        state = {
            VDSP_ACCESS_TOKEN_KEY: "encrypted-token",
            VDSP_ACCESS_TOKEN_IS_ENCRYPTED: True,
            VDSP_TOKEN_TYPE_KEY: "Bearer",
            VDSP_EXPIRES_IN_KEY: int(time.time()) + 3600,
        }
        self.connector.load_state = MagicMock(return_value=state)
        self.connector.get_config = MagicMock(return_value={VDSP_JSON_BASE_URL_KEY: "https://test.com", VDSP_SCRT: "api-key"})
        self.connector.get_asset_id = MagicMock(return_value=42)
        encryption_helper.decrypt.return_value = "decrypted-token"

        self.assertTrue(self.connector.initialize())

        encryption_helper.decrypt.assert_called_once_with("encrypted-token", 42)
        self.assertEqual(self.connector._headers["Authorization"], "Bearer decrypted-token")

    @patch("varonissaas_connector.encryption_helper")
    def test_initialize_refreshes_token_after_decryption_failure(self, encryption_helper):
        state = {
            VDSP_ACCESS_TOKEN_KEY: "encrypted-token",
            VDSP_ACCESS_TOKEN_IS_ENCRYPTED: True,
            VDSP_TOKEN_TYPE_KEY: "Bearer",
            VDSP_EXPIRES_IN_KEY: int(time.time()) + 3600,
        }
        self.connector.load_state = MagicMock(return_value=state)
        self.connector.get_config = MagicMock(return_value={VDSP_JSON_BASE_URL_KEY: "https://test.com", VDSP_SCRT: "api-key"})
        self.connector.get_asset_id = MagicMock(return_value=42)
        encryption_helper.decrypt.side_effect = ValueError("bad ciphertext")

        def authorize(_):
            self.connector._access_token = "fresh-token"
            state[VDSP_TOKEN_TYPE_KEY] = "Bearer"
            state[VDSP_EXPIRES_IN_KEY] = int(time.time()) + 3600

        self.connector._authorize = MagicMock(side_effect=authorize)

        self.assertTrue(self.connector.initialize())

        self.connector._authorize.assert_called_once_with("api-key")
        self.assertNotIn(VDSP_ACCESS_TOKEN_KEY, state)
        self.assertNotIn(VDSP_ACCESS_TOKEN_IS_ENCRYPTED, state)
        self.assertEqual(self.connector._headers["Authorization"], "Bearer fresh-token")

    def test_handle_get_alerts_empty_param(self):
        # Arrange
        with open("test_data/get_varonissaas_alerts_empty_param_query.json") as file:
            expected_search_query = json.load(file)
        with open("test_data/get_varonissaas_alerts_empty_param_response.json") as file:
            search_response = json.load(file)
        with open("test_data/get_varonissaas_alerts_empty_param_result.json") as file:
            expected_result = json.load(file)

        self.connector._make_search_call = MagicMock(return_value=(True, search_response))
        param = {}
        action_result = ActionResult(param)
        self.connector.add_action_result = MagicMock(return_value=action_result)

        # Act
        status = self.connector._handle_get_alerts(param)
        actual_result = action_result.get_data()

        # Assert
        self.connector._make_search_call.assert_called_once_with(action_result, query=expected_search_query, page=1, count=VDSP_MAX_ALERTS)
        self.assertTrue(status)
        self.assertEqual(
            actual_result,
            expected_result,
            "handle_get_alerts returns unexpected result.",
        )

    def test_handle_get_alerts(self):
        # Arrange
        with open("test_data/get_varonissaas_alerts_query.json") as file:
            expected_search_query = json.load(file)
        with open("test_data/get_varonissaas_alerts_response.json") as file:
            search_response = json.load(file)
        with open("test_data/get_varonissaas_alerts_result.json") as file:
            expected_result = json.load(file)

        self.connector._make_search_call = MagicMock(return_value=(True, search_response))
        param = {
            "page": 2,
            "max_results": VDSP_MAX_ALERTS,
            "descending_order": False,
            "threat_model_name": "Capture Access request for varadm|Capture Account authentication for varadm|Capture SYSTEM",
            "alert_status": "New|Closed",
            "end_time": "2023-12-30T13:59:00+02:00",
            "start_time": "2023-12-01T13:00:00+02:00",
            "alert_severity": "High| Low| Medium",
            "device_name": "dev3cf41col01|dev3cf41dh",
            "user_name": "varadm|SYSTEM",
            "last_days": "2",
        }
        action_result = ActionResult(param)
        self.connector.add_action_result = MagicMock(return_value=action_result)

        # Act
        status = self.connector._handle_get_alerts(param)
        actual_result = action_result.get_data()

        # Assert
        self.connector._make_search_call.assert_called_once_with(action_result, query=expected_search_query, page=2, count=VDSP_MAX_ALERTS)
        self.assertTrue(status)
        self.assertEqual(
            actual_result,
            expected_result,
            "handle_get_alerts returns unexpected result.",
        )
        action_result = ActionResult(param)
        self.connector.add_action_result = MagicMock(return_value=action_result)

    def test_handle_get_alerted_events(self):
        with open("test_data/get_varonissaas_alerted_events_query.json") as file:
            expected_search_query = json.load(file)
        with open("test_data/get_varonissaas_alerted_events_response.json") as file:
            search_response = json.load(file)
        with open("test_data/get_varonissaas_alerted_events_result.json") as file:
            expected_result = json.load(file)

        self.connector._make_search_call = MagicMock(return_value=(True, search_response))
        param = {"alert_id": "EE53B604-087A-499C-88F5-7E97ABA5BD9E|A08C35C2-731A-4EA1-B350-11204EACA972"}
        action_result = ActionResult(param)
        self.connector.add_action_result = MagicMock(return_value=action_result)

        # Act
        status = self.connector._handle_get_alerted_events(param)
        actual_result = action_result.get_data()

        # Assert
        self.connector._make_search_call.assert_called_once_with(
            action_result,
            query=expected_search_query,
            page=1,
            count=VDSP_MAX_ALERTED_EVENTS,
        )
        self.assertTrue(status)
        self.assertEqual(
            actual_result,
            expected_result,
            "handle_get_alerted_events returns unexpected result.",
        )

    def test_handle_update_alert_status(self):
        self.connector._make_rest_call = MagicMock()
        param = {
            "alert_id": "232c60e4-0f74-4f86-998b-8752a41f7910|176ee376-252c-44e0-a2d6-f8c4443ddec1",
            "status": "new",
        }
        action_result = ActionResult(param)
        self.connector.add_action_result = MagicMock(return_value=action_result)
        json_data = {
            "AlertGuids": [
                "232c60e4-0f74-4f86-998b-8752a41f7910",
                "176ee376-252c-44e0-a2d6-f8c4443ddec1",
            ],
            "closeReasonId": CLOSE_REASONS["none"],
            "statusId": ALERT_STATUSES["new"],
        }

        status = self.connector._handle_update_alert_status(param)

        self.connector._make_rest_call.assert_called_once_with(
            action_result,
            VDSP_UPDATE_ALET_STATUS_ENDPOINT,
            method="POST",
            json=json_data,
        )
        self.assertTrue(status)

    def test_handle_close_alert(self):
        self.connector._make_rest_call = MagicMock()
        param = {
            "alert_id": "232c60e4-0f74-4f86-998b-8752a41f7910|176ee376-252c-44e0-a2d6-f8c4443ddec1",
            "close_reason": "other",
        }
        action_result = ActionResult(param)
        self.connector.add_action_result = MagicMock(return_value=action_result)
        json_data = {
            "AlertGuids": [
                "232c60e4-0f74-4f86-998b-8752a41f7910",
                "176ee376-252c-44e0-a2d6-f8c4443ddec1",
            ],
            "closeReasonId": CLOSE_REASONS["other"],
            "statusId": ALERT_STATUSES["closed"],
        }

        status = self.connector._handle_close_alert(param)

        self.connector._make_rest_call.assert_called_once_with(
            action_result,
            VDSP_UPDATE_ALET_STATUS_ENDPOINT,
            method="POST",
            json=json_data,
        )
        self.assertTrue(status)

    def test_initialize_configures_retry_backoff(self):
        self.connector.load_state = MagicMock(
            return_value={
                VDSP_ACCESS_TOKEN_KEY: "cached-token",
                VDSP_TOKEN_TYPE_KEY: "Bearer",
                VDSP_EXPIRES_IN_KEY: int(time.time()) + 3600,
            }
        )
        self.connector.get_config = MagicMock(return_value={VDSP_JSON_BASE_URL_KEY: "https://test.com", VDSP_SCRT: "api-key"})

        self.assertTrue(self.connector.initialize())

        retry = self.connector._session.get_adapter("https://test.com").max_retries
        self.assertEqual(retry.total, REQUEST_RETRIES)
        self.assertEqual(retry.backoff_factor, REQUEST_BACKOFF_FACTOR)
        self.assertIn(304, retry.status_forcelist)
        self.assertIn(206, retry.status_forcelist)

    def test_on_poll_caps_activity_window_to_max_interval(self):
        # A large ingest_period must be clamped so the activity window never
        # spans more than VDSP_MAX_INGEST_INTERVAL_DAYS.
        recent_cursor = (datetime.now(timezone.utc) - timedelta(days=2)).strftime("%Y-%m-%dT%H:%M:%S.%f%z")
        self.connector._state = {VDSP_LAST_FETCH_TIME: recent_cursor}
        self.connector.get_config = MagicMock(return_value={VDSP_INGEST_PERIOD_KEY: "30 day", VDSP_INGEST_ARTIFACTS_FLAG: False})
        action_result = ActionResult({})
        self.connector.add_action_result = MagicMock(return_value=action_result)

        captured = {}
        self.connector._get_alerts_payload = MagicMock(side_effect=lambda **kwargs: captured.update(kwargs) or MagicMock())
        self.connector._make_search_call = MagicMock(return_value=(True, {"hasResults": False}))

        status = self.connector._on_poll({})

        self.assertTrue(status)
        earliest = datetime.now(timezone.utc).replace(tzinfo=None) - timedelta(days=VDSP_MAX_INGEST_INTERVAL_DAYS)
        self.assertAlmostEqual(captured["start_time"], earliest, delta=timedelta(seconds=60))

    def test_on_poll_caps_ingest_cursor_to_max_interval(self):
        # A cursor that has fallen far behind must be clamped so the ingest-time
        # window never spans more than VDSP_MAX_INGEST_INTERVAL_DAYS.
        old_cursor = (datetime.now(timezone.utc) - timedelta(days=30)).strftime("%Y-%m-%dT%H:%M:%S.%f%z")
        self.connector._state = {VDSP_LAST_FETCH_TIME: old_cursor}
        self.connector.get_config = MagicMock(return_value={VDSP_INGEST_PERIOD_KEY: "1 day", VDSP_INGEST_ARTIFACTS_FLAG: False})
        action_result = ActionResult({})
        self.connector.add_action_result = MagicMock(return_value=action_result)

        captured = {}
        self.connector._get_alerts_payload = MagicMock(side_effect=lambda **kwargs: captured.update(kwargs) or MagicMock())
        self.connector._make_search_call = MagicMock(return_value=(True, {"hasResults": False}))

        status = self.connector._on_poll({})

        self.assertTrue(status)
        earliest = datetime.now(timezone.utc) - timedelta(days=VDSP_MAX_INGEST_INTERVAL_DAYS)
        self.assertAlmostEqual(captured["from_ingest_time"], earliest, delta=timedelta(seconds=60))

    def test_handle_update_alert_status_reports_failure_on_exception(self):
        # A failure raised inside the handler must not be reported as success.
        self.connector._make_rest_call = MagicMock()
        param = {"alert_id": "232c60e4-0f74-4f86-998b-8752a41f7910", "status": "not-a-status"}
        action_result = ActionResult(param)
        self.connector.add_action_result = MagicMock(return_value=action_result)

        status = self.connector._handle_update_alert_status(param)

        self.assertFalse(status)
        self.connector._make_rest_call.assert_not_called()

    def test_handle_close_alert_reports_failure_on_exception(self):
        self.connector._make_rest_call = MagicMock()
        param = {"alert_id": "232c60e4-0f74-4f86-998b-8752a41f7910", "close_reason": "not-a-reason"}
        action_result = ActionResult(param)
        self.connector.add_action_result = MagicMock(return_value=action_result)

        status = self.connector._handle_close_alert(param)

        self.assertFalse(status)
        self.connector._make_rest_call.assert_not_called()

    def test_handle_get_alerted_events_reports_failure_on_exception(self):
        self.connector._make_search_call = MagicMock()
        param = {"alert_id": "EE53B604-087A-499C-88F5-7E97ABA5BD9E", "max_results": "not-a-number"}
        action_result = ActionResult(param)
        self.connector.add_action_result = MagicMock(return_value=action_result)

        status = self.connector._handle_get_alerted_events(param)

        self.assertFalse(status)
        self.connector._make_search_call.assert_not_called()

    @patch("varonissaas_connector.create_alert_request")
    def test_get_alerts_payload_matches_ingest_window_awareness(self, create_alert_request):
        # Both ends of the ingest-time window must share the same tzinfo awareness,
        # otherwise the range is interpreted in different timezones.
        aware_start = datetime.now(timezone.utc) - timedelta(days=1)
        self.connector._get_alerts_payload(from_ingest_time=aware_start)
        aware_end = create_alert_request.call_args.kwargs["ingest_time_end"]
        self.assertIsNotNone(aware_end.tzinfo)
        self.assertGreater(aware_end, aware_start)

        naive_start = datetime.now(timezone.utc).replace(tzinfo=None) - timedelta(days=1)
        self.connector._get_alerts_payload(from_ingest_time=naive_start)
        naive_end = create_alert_request.call_args.kwargs["ingest_time_end"]
        self.assertIsNone(naive_end.tzinfo)
        self.assertGreater(naive_end, naive_start)


class MultiValueToStringListTest(unittest.TestCase):
    def test_splits_on_pipe(self):
        self.assertEqual(
            multi_value_to_string_list("New|Closed|Open"),
            ["New", "Closed", "Open"],
        )

    def test_strips_surrounding_whitespace(self):
        self.assertEqual(
            multi_value_to_string_list("High| Low | Medium"),
            ["High", "Low", "Medium"],
        )

    def test_preserves_commas_inside_values(self):
        # Names may legitimately contain commas; when a pipe is present it wins.
        self.assertEqual(
            multi_value_to_string_list("Doe, John|Roe, Jane"),
            ["Doe, John", "Roe, Jane"],
        )

    def test_falls_back_to_comma_for_legacy_values(self):
        # Assets and playbooks created before the pipe separator must keep working.
        self.assertEqual(
            multi_value_to_string_list("id1,id2,id3"),
            ["id1", "id2", "id3"],
        )
        self.assertEqual(
            multi_value_to_string_list("New, Closed"),
            ["New", "Closed"],
        )

    def test_single_value_returns_single_item_list(self):
        self.assertEqual(multi_value_to_string_list("Capture SYSTEM"), ["Capture SYSTEM"])

    def test_list_input_is_returned_unchanged(self):
        self.assertEqual(multi_value_to_string_list(["New", "Closed"]), ["New", "Closed"])

    def test_empty_input_returns_empty_list(self):
        self.assertEqual(multi_value_to_string_list(""), [])
        self.assertEqual(multi_value_to_string_list(None), [])

    def test_custom_separator_is_respected(self):
        self.assertEqual(multi_value_to_string_list("a,b,c", separator=","), ["a", "b", "c"])


if __name__ == "__main__":
    unittest.main()
