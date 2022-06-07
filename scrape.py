from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By


def get_ranking():
    print("start get_ranking")
    options = Options()
    options.add_argument('--headless')
    driver = webdriver.Chrome(options=options)
    driver.get('https://news.yahoo.co.jp/topics')
    driver.implicitly_wait(0.5)
    yjnSub_list_item = []
    yjnSub_section_title = ""
    headline_list = []
    news = []
    print("ここまできた1")
    try:
        yjnSub_section = driver.find_element(by=By.CLASS_NAME, value="yjnSub_section")
        yjnSub_section_title = yjnSub_section.find_element(by=By.CLASS_NAME, value='yjnSub_section_title').text
        yjnSub_list_item = yjnSub_section.find_elements(by=By.CLASS_NAME, value='yjnSub_list_item')
        print("ここまできた2")
        for item in yjnSub_list_item:
            rank = item.find_element(by=By.CLASS_NAME, value="yjnSub_list_rankNum").text
            headline = item.find_element(by=By.CLASS_NAME, value="yjnSub_list_headline").text
            link = item.find_element(by=By.TAG_NAME, value="a").get_attribute("href")
            headline_list.append(headline)
            # line_bot_api.reply_message(event.reply_token, TextSendMessage(text=f'{rank} ヘッドライン：{headline} {link}'))
            print(f'{rank} ヘッドライン：{headline} {link}')
    except NoSuchElementException as e:
        print("そんな要素ないぞ")
        print(e)
    print("ここまできた3")
    driver.quit()
    return headline_list


if __name__ == '__main__':
    item_list = get_ranking()
