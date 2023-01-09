import requests
import json
import random

from config import NOTION_TOKEN, DB_ID, SLACK_TOKEN


def get_notion_page():
    """
    a function to return randomly picked Notion page.
    :return: dictionary
    """
    token = NOTION_TOKEN
    db_id = DB_ID

    url = f"https://api.notion.com/v1/databases/{db_id}/query"
    headers = {
        "Authorization": f"Bearer {token}",
        "Notion-Version": "2022-06-28",
        "Content-Type": "application/json"
    }

    response = requests.post(url, headers=headers)

    results = response.json().get("results")

    picked = random.choice(results)

    return picked


def pick_page():
    """
    a function to return message containing randomly picked Notion page's property/
    :return: string
    """
    picked = get_notion_page()

    # put your properties' keys
    picked_url = picked.get("properties").get("지도링크").get("url")

    return f"결과 확인을 위해 링크로 이동해주세요 > {picked_url}"


def get_channel_id(payload):
    """
    a function to return channel_id of channel from which user calls slack bot.
    :param payload: slack message containing channel_id
    :return: channel_id
    """
    string = payload.decode('utf-8')
    params = string.split("&")
    for param in params:
        if param.startswith("channel_id"):
            channel_id = param.split("=")[-1]
            return channel_id
    return None


def send_slack_msg(msg, channel_id):
    """
    a function to send Slack message to a specific channel.
    :param msg: a string to send via Slack API
    :param channel_id: a string to designate Slack channel to which a message above sent.
    :return: Response
    """
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {SLACK_TOKEN}"
    }
    data = json.dumps({
        "channel": channel_id,
        "text": msg
    })
    response = requests.post("https://slack.com/api/chat.postMessage", headers=headers, data=data)

    return response
