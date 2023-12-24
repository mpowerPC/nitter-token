# -*- coding: utf-8 -*-
"""
nitter-token.main
~~~~~~~~~~~~~
@author: mpowerPC

A simple script to grab a guest token from the unofficial X/Twitter api and store it in guest_accounts.json to be used
by the guest account branch of nitter. A token can be generated from a single ip every 24 hours or so.

"""
import logging.config
import sys
import os
import requests
import json


def main():
    directory = os.path.dirname(os.path.realpath(__file__))

    logging_file = os.path.join(directory, "logging.ini")
    if os.path.exists(logging_file):
        logging.config.fileConfig(logging_file)

    logger = logging.getLogger(__name__)
    logger.debug("Initialized: nitter-token.py")

    auth = "Bearer AAAAAAAAAAAAAAAAAAAAAFXzAwAAAAAAMHCxpeSDG1gLNLghVe8d74hl6k4%3DRUMF4xAQLsbeBhTSRrCiQpJtxoGWeyHrDb5te2jpGskWDFW82F"
    guest_token_headers = {"Authorization": auth}
    guest_token_response = requests.post("https://api.twitter.com/1.1/guest/activate.json", headers=guest_token_headers)

    if guest_token_response.status_code != 200:
        logger.error(guest_token_response.json())
        sys.exit(9)

    guest_token = guest_token_response.json()["guest_token"]
    logger.debug("guest_token: " + guest_token)

    token_headers = {
        "Authorization": auth,
        "Content-Type": "application/json",
        "User-Agent": "TwitterAndroid/9.95.0-release.0 (29950000-r-0) ONEPLUS+A3010/9 (OnePlus;ONEPLUS+A3010;OnePlus;OnePlus3;0;;1;2016)",
        "X-Twitter-API-Version": "5",
        "X-Twitter-Client": "TwitterAndroid",
        "X-Twitter-Client-Version": "9.95.0-release.0",
        "OS-Version": "28",
        "System-User-Agent": "Dalvik/2.1.0 (Linux; U; Android 9; ONEPLUS A3010 Build/PKQ1.181203.001)",
        "X-Twitter-Active-User": "yes",
        "X-Guest-Token": guest_token
    }

    subtask_versions = {"generic_urt": 3, "standard": 1, "open_home_timeline": 1, "app_locale_update": 1,
                        "enter_date": 1, "email_verification": 3, "enter_password": 5, "enter_text": 5, "one_tap": 2,
                        "cta": 7, "single_sign_on": 1, "fetch_persisted_data": 1, "enter_username": 3, "web_modal": 2,
                        "fetch_temporary_password": 1, "menu_dialog": 1, "sign_up_review": 5, "interest_picker": 4,
                        "user_recommendations_urt": 3, "in_app_notification": 1, "sign_up": 2, "typeahead_search": 1,
                        "user_recommendations_list": 4, "cta_inline": 1, "contacts_live_sync_permission_prompt": 3,
                        "choice_selection": 5, "js_instrumentation": 1, "alert_dialog_suppress_client_events": 1,
                        "privacy_options": 1, "topics_selector": 1, "wait_spinner": 3, "tweet_selection_urt": 1,
                        "end_flow": 1, "settings_list": 7, "open_external_link": 1, "phone_verification": 5,
                        "security_key": 3, "select_banner": 2, "upload_media": 1, "web": 2, "alert_dialog": 1,
                        "open_account": 2, "action_list": 2, "enter_phone": 2, "open_link": 1, "show_code": 1,
                        "update_users": 1, "check_logged_in_account": 1, "enter_email": 2, "select_avatar": 4,
                        "location_permission_prompt": 2, "notifications_permission_prompt": 4
                        }

    flow_token_data = {"flow_token": None,
                       "input_flow_data": {"country_code": None,
                                           "flow_context": {"start_location": {"location": "splash_screen"}},
                                           "requested_variant": None,
                                           "target_user_id": 0
                                           },
                       "subtask_versions": subtask_versions
                       }

    flow_token_response = requests.post(
        "https://api.twitter.com/1.1/onboarding/task.json?flow_name=welcome&api_version=1&known_device_token=&sim_country_code=us",
        headers=token_headers, json=flow_token_data)

    if flow_token_response.status_code != 200:
        logger.error(flow_token_response.json())
        sys.exit(9)

    flow_token = flow_token_response.json()["flow_token"]
    logger.debug("flow_token: " + flow_token)

    nitter_data = {"flow_token": flow_token,
                   "subtask_inputs": [{"open_link": {"link": "next_link"}, "subtask_id": "NextTaskOpenLink"}],
                   "subtask_versions": subtask_versions
                   }
    nitter_token_response = requests.post("https://api.twitter.com/1.1/onboarding/task.json",
                                          headers=token_headers, json=nitter_data)

    if nitter_token_response.status_code != 200:
        logger.error(nitter_token_response.json())
        sys.exit(9)

    if "open_account" in nitter_token_response.json()["subtasks"][0]:
        nitter_token = [].append(nitter_token_response.json()["subtasks"][0]["open_account"])
        logger.debug("nitter_token: \n" + json.dumps(nitter_token, indent=4))

        with open('/src/output/guest_accounts.json', 'w') as f:
            f.write(json.dumps(nitter_token, indent=4))

        logger.debug("Success: nitter-token updated")

    else:
        logger.debug("nitter_token: null")
        logger.debug("Failed: nitter-token was not updated.")


if __name__ == "__main__":
    main()