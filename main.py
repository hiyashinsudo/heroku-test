from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)
import os

from scrape import get_yahoonews_ranking, get_toyoukeizai_ranking

app = Flask(__name__)

line_bot_api = LineBotApi(os.environ["LINE_CHANNEL_ACCESS_TOKEN"])
handler = WebhookHandler(os.environ["LINE_CHANNEL_SECRET"])


@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        print("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    # スクレイピング
    print("user id: ", event.source.user_id)
    if event.message.text == "ヤフーニュース":
        print("ヤフーニュースモード")
        item3_list = get_yahoonews_ranking()
        for rank, headline, link in zip(item3_list["rank_list"], item3_list["headline_list"], item3_list["link_list"]):
            messages = TextSendMessage(text=f'{rank}:{headline} \n {link}')
            line_bot_api.push_message(to=event.source.user_id, messages=messages)
    elif event.message.text == "東洋経済オンライン":
        print("東洋経済オンライン")
        item3_list = get_toyoukeizai_ranking()
        for rank, headline, link in zip(item3_list["rank_list"], item3_list["headline_list"], item3_list["link_list"]):
            messages = TextSendMessage(text=f'{rank}:{headline} \n {link}')
            line_bot_api.push_message(to=event.source.user_id, messages=messages)
    else:
        print("テストモード")
        messages = TextSendMessage(text='Test')
        line_bot_api.push_message(to=event.source.user_id, messages=messages)
        # line_bot_api.reply_message(event.reply_token, TextSendMessage(text=event.message.text))
    # line_bot_api.reply_message(event.reply_token, TextSendMessage(text=event.message.text))


if __name__ == "__main__":
    port = int(os.getenv("PORT"))
    app.run(host="0.0.0.0", port=port)
