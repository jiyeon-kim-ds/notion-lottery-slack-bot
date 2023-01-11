import requests
import json
import random

from config import NOTION_TOKEN, DB_ID, SLACK_TOKEN, CLOVA_CLIENT_ID, CLOVA_CLIENT_SECRET


def get_notion_pages():
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

    return results


def pick_page(results):
    """
    a function to return message containing randomly picked Notion page's property/
    :return: string
    """
    picked = random.choice(results)

    review = picked["properties"]["가본사람 의견"]["rich_text"]

    if review:
        sentiment = analyze_sentiment(review[0]['text']['content'])
    else:
        sentiment = "리뷰가 없습니다."

    # put your properties' keys
    picked_url = picked.get("properties").get("지도링크").get("url")

    return f"결과 확인을 위해 링크로 이동해주세요 > {picked_url}, 리뷰 감정 분석 결과 : {sentiment}"


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


def analyze_sentiment(review: str):
    headers = {
        "X-NCP-APIGW-API-KEY-ID": CLOVA_CLIENT_ID,
        "X-NCP-APIGW-API-KEY": CLOVA_CLIENT_SECRET,
        "Content-Type": "application/json"
    }

    data = {
        "content": review
    }

    url = "https://naveropenapi.apigw.ntruss.com/sentiment-analysis/v1/analyze"

    response = requests.post(url, headers=headers, data=json.dumps(data))

    return response.json().get('document', {}).get('sentiment')


def filter_by_tag(tag: str):
    results = get_notion_pages()

    filtered_pages = []
    for page in results:
        tag_dict_list = page['properties']['종목']['multi_select']

        for tag_dict in tag_dict_list:
            if tag_dict['name'] == tag:
                filtered_pages.append(page)

    return filtered_pages


def get_element_from_message(payload, element):
    string = payload.decode('utf-8')

    params = string.split("&")

    for param in params:
        if param.startswith(element):
            element = param.split("=")[-1]
            return element
    return None
