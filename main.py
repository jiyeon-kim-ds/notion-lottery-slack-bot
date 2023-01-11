import urllib.parse

from fastapi import FastAPI, Request

from dependencies import pick_page, get_element_from_message, send_slack_msg, filter_by_tag, get_notion_pages

app = FastAPI()


@app.post("/random")
async def post_random_pick(
    request: Request
):
    data = await request.body()

    channel_id = get_element_from_message(data, 'channel_id')
    msg = get_element_from_message(data, 'text')
    decoded_msg = urllib.parse.unquote(msg)

    if channel_id is None:
        return {"message": "다른 채널에서 이용해주세요."}

    if decoded_msg:
        pages = filter_by_tag(decoded_msg)
        if not pages:
            return {"message": "해당 태그에 관한 결과가 없습니다."}
    else:
        pages = get_notion_pages()

    # TODO: pick page/write message 분리
    message = pick_page(pages)

    res = send_slack_msg(message, channel_id)

    if res.status_code == 200:
        return {"message": "success"}  # when requests succeed
    return {"return": "Slack API 연동 실패"}  # when requests fail
