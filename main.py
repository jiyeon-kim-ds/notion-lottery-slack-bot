from fastapi import FastAPI, Request

from dependencies import pick_page, get_channel_id, send_slack_msg

app = FastAPI()


@app.post("/random")
async def get_random_pick(
    request: Request
):
    data = await request.body()

    channel_id = get_channel_id(data)

    if channel_id is None:
        return {"message": "다른 채널에서 이용해주세요."}

    message = pick_page()

    res = send_slack_msg(message, channel_id)

    if res.status_code == 200:
        return {"message": "success"}  # when requests succeed
    return {"return": "Slack API 연동 실패"}  # when requests fail
