import datetime
import re

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

options = Options()
options.add_argument('--headless')
options.add_argument('--disable-gpu')  # 「暫定的なフラグ」らしい。。
options.add_argument('--no-sandbox')  # セキュリティ対策などのchromeに搭載してある保護機能をオフにする。
options.add_argument('--disable-dev-shm-usage')  # ディスクのメモリスペースを使う。
options.add_argument('--remote-debugging-port=9222')  # リモートデバッグフラグを立てる。


# Y!トピックからランキングtop5を取ってくる
def get_yahoonews_ranking():
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
        return None
    except Exception as e:
        print("エラー発生", e)
        return None
    driver.quit()
    print(f'ジョブ終了日時：{datetime.datetime.now().strftime("%Y年%m月%d日%H:%M:%S")}')
    return {
        "rank_list": rank_list,
        "headline_list": headline_list,
        "link_list": link_list
    }


# 東洋経済オンラインからランキングtop5を取ってくる（1時間）
def get_toyoukeizai_ranking():
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
        return None
    except Exception as e:
        print("エラー発生", e)
        return None
    driver.quit()
    print(f'ジョブ終了日時：{datetime.datetime.now().strftime("%Y年%m月%d日%H:%M:%S")}')
    return {
        "rank_list": rank_list,
        "headline_list": headline_list,
        "link_list": link_list
    }


# NHKニュースからランキングtop5を取ってくる（1時間）
def get_nhk_ranking():
    pass

# グルメカテゴリを取ってくる
def get_gurume_ranking():
    driver = webdriver.Chrome(options=options)
    print(f'ジョブ開始日時：{datetime.datetime.now().strftime("%Y年%m月%d日%H:%M:%S")}')
    driver.get('https://entabe.jp/news/sweets')
    driver.implicitly_wait(0.5)
    headline_list = []
    rank_list = []
    link_list = []
    # TODO: Selenium test
    try:
        for i in range(5):
            top_a_tag = driver.find_element(by=By.XPATH, value=f"//*[@id=\"contents\"]/div/div[2]/div/ul/li[{i + 2}]/a")
            link = top_a_tag.get_attribute("href")
            headline = re.sub('\n.*', '', top_a_tag.text[2:])
            print(f'{i + 1}：{headline} \n {link}')
            # リストに追加
            rank_list.append(i + 1)
            headline_list.append(headline)
            link_list.append(link)

    except NoSuchElementException as e:
        print("そんな要素ないぞ: ", e)
        return None
    except Exception as e:
        print("エラー発生", e)
        return None
    driver.quit()
    print(f'ジョブ終了日時：{datetime.datetime.now().strftime("%Y年%m月%d日%H:%M:%S")}')
    return {
        "rank_list": rank_list,
        "headline_list": headline_list,
        "link_list": link_list
    }


if __name__ == '__main__':
    item_list = get_yahoonews_ranking()
