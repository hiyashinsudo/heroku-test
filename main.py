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

from selenium.webdriver.common.by import By

from scrape import get_ranking

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
    if event.message.text == "ヤフーニュース":
        print("ヤフーニュースモード")
        item_list = get_ranking()
        for item in item_list:
            rank = item.find_element(by=By.CLASS_NAME, value="yjnSub_list_rankNum").text
            headline = item.find_element(by=By.CLASS_NAME, value="yjnSub_list_headline").text
            link = item.find_element(by=By.TAG_NAME, value="a").get_attribute("href")
            # line_bot_api.reply_message(event.reply_token, TextSendMessage(text=f'{rank} ヘッドライン：{headline} {link}'))
            print(f'{rank} ヘッドライン：{headline} {link}')
            print("yasu id: ", event.source.user_id)
            messages = TextSendMessage(text=f'{rank} ヘッドライン：{headline} {link}')
            line_bot_api.push_message(to=event.source.user_id, messages=messages)
    else:
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=event.message.text))
    # line_bot_api.reply_message(event.reply_token, TextSendMessage(text=event.message.text))

if __name__ == "__main__":
    port = int(os.getenv("PORT"))
    app.run(host="0.0.0.0", port=port)
