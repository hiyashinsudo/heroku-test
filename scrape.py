import datetime

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

# Y!トピックからランキングtop5を取ってくる
def get_yahoonews_ranking():
    options = Options()
    options.add_argument('--headless')
    driver = webdriver.Chrome(options=options)
    print("start get_ranking")
    driver.get('https://news.yahoo.co.jp/topics')
    driver.implicitly_wait(0.5)
    headline_list = []
    rank_list = []
    link_list = []
    try:
        yjnSub_section = driver.find_element(by=By.CLASS_NAME, value="yjnSub_section")
        for item in yjnSub_section.find_elements(by=By.CLASS_NAME, value='yjnSub_list_item'):
            rank = item.find_element(by=By.CLASS_NAME, value="yjnSub_list_rankNum").text
            headline = item.find_element(by=By.CLASS_NAME, value="yjnSub_list_headline").text
            link = item.find_element(by=By.TAG_NAME, value="a").get_attribute("href")
            rank_list.append(rank)
            headline_list.append(headline)
            link_list.append(link)
            # line_bot_api.reply_message(event.reply_token, TextSendMessage(text=f'{rank} ヘッドライン：{headline} {link}'))
            print(f'{rank} ：{headline} {link}')
    except NoSuchElementException as e:
        print("そんな要素ないぞ")
        print(e)
    driver.quit()
    return {
        "rank_list": rank_list,
        "headline_list": headline_list,
        "link_list": link_list
    }


# 東洋経済オンラインからランキングtop5を取ってくる（1時間）
def get_toyoukeizai_ranking():
    options = Options()
    options.add_argument('--headless')
    driver = webdriver.Chrome(options=options)
    print(f'ジョブ開始日時：{datetime.datetime.now().strftime("%Y年%m月%d日%H:%M:%S")}')
    driver.get('https://toyokeizai.net/')
    driver.implicitly_wait(0.5)
    headline_list = []
    rank_list = []
    link_list = []
    try:
        access_ranking = driver.find_element(by=By.XPATH, value="//*[@id='access-ranking']/div[2]")
        for i in range(5):
            gtm_hourly_rank_i = access_ranking.find_element(by=By.ID, value=f"gtm_hourly_rank{i + 1}")
            link = gtm_hourly_rank_i.get_attribute("href")
            headline = gtm_hourly_rank_i.find_element(by=By.CLASS_NAME, value="title").text
            print(f'{i + 1}：{headline} \n {link}')
            rank_list.append(i + 1)
            headline_list.append(headline)
            link_list.append(link)

    except NoSuchElementException as e:
        print("そんな要素ないぞ: ", e)
    print(f'ジョブ終了日時：{datetime.datetime.now().strftime("%Y年%m月%d日%H:%M:%S")}')
    driver.quit()
    return {
        "rank_list": rank_list,
        "headline_list": headline_list,
        "link_list": link_list
    }


if __name__ == '__main__':
    item_list = get_yahoonews_ranking()
