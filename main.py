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
import datetime

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

driver = webdriver.Remote(
    command_executor=os.environ["SELENIUM_URL"],
    desired_capabilities=DesiredCapabilities.FIREFOX.copy()
)


# Y!トピックからランキングtop10を取ってくる
def job() -> str:
    print(f'ジョブ開始日時：{datetime.datetime.now().strftime("%Y年%m月%d日%H:%M:%S")}')
    driver.get('https://news.yahoo.co.jp/topics')
    driver.implicitly_wait(0.5)
    yjnSub_list_item = []
    yjnSub_section_title = ""
    try:
        yjnSub_section = driver.find_element(by=By.CLASS_NAME, value="yjnSub_section")
        yjnSub_section_title = yjnSub_section.find_element(by=By.CLASS_NAME, value='yjnSub_section_title').text
        yjnSub_list_item = yjnSub_section.find_elements(by=By.CLASS_NAME, value='yjnSub_list_item')
    except NoSuchElementException as e:
        print("そんな要素ないぞ")
        print(e)
    print(yjnSub_section_title)
    for item in yjnSub_list_item:
        rank = item.find_element(by=By.CLASS_NAME, value="yjnSub_list_rankNum").text
        headline = item.find_element(by=By.CLASS_NAME, value="yjnSub_list_headline").text
        link = item.find_element(by=By.TAG_NAME, value="a").get_attribute("href")
        print(f'{rank} ヘッドライン：{headline}')
        print(link)
    print(f'ジョブ終了日時：{datetime.datetime.now().strftime("%Y年%m月%d日%H:%M:%S")}')

    return yjnSub_list_item


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
    result = job()
    # line_bot_api.reply_message(event.reply_token, TextSendMessage(text=event.message.text))
    line_bot_api.reply_message(event.reply_token, TextSendMessage(text=result))


if __name__ == "__main__":
    port = int(os.getenv("PORT"))
    app.run(host="0.0.0.0", port=port)
