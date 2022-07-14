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

from scrape import *

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


def send_articles(article_dict: dict, event: MessageEvent):
    for rank, headline, link in zip(article_dict["rank_list"], article_dict["headline_list"],
                                    article_dict["link_list"]):
        messages = TextSendMessage(text=f'{rank}:{headline} \n {link}')
        line_bot_api.push_message(to=event.source.user_id, messages=messages)


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    # スクレイピング
    print("user id: ", event.source.user_id)
    if event.message.text == "ヤフーニュース":
        print("ヤフーニュースモード")
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text="Yニュースからだな、待っとけ"))
        article_dict = get_yahoonews_ranking()
        if article_dict:
            send_articles(article_dict=article_dict, event=event)
        else:
            line_bot_api.push_message(to=event.source.user_id, messages=TextSendMessage(text='なんかエラー出たわ'))
    elif event.message.text == "東洋経済オンライン":
        print("東洋経済オンラインモード")
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text="東オンからだな、待っとけ"))
        article_dict = get_toyoukeizai_ranking()
        if article_dict:
            send_articles(article_dict=article_dict, event=event)
        else:
            line_bot_api.push_message(to=event.source.user_id, messages=TextSendMessage(text='ソーリー'))
    elif event.message.text == "NHK":
        print("NHKモード")
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text="NHKからだな、待っとけ"))
        article_dict = get_nhk_ranking()
        if article_dict:
            send_articles(article_dict=article_dict, event=event)
        else:
            line_bot_api.push_message(to=event.source.user_id, messages=TextSendMessage(text='すまんうまくいかなかった'))
    elif event.message.text == "グルメ":
        print("グルメモード")
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text="グルメだな、待っとけ"))
        article_dict = get_gurume_ranking()
        if article_dict:
            send_articles(article_dict=article_dict, event=event)
        else:
            line_bot_api.push_message(to=event.source.user_id, messages=TextSendMessage(text='ごめん失敗したわ'))
    else:
        print("テストモード")
        messages = TextSendMessage(text='Test')
        line_bot_api.push_message(to=event.source.user_id, messages=messages)
        # line_bot_api.reply_message(event.reply_token, TextSendMessage(text=event.message.text))


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT")))
