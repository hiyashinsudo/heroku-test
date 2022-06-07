from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By


def get_ranking():
    options = Options()
    options.add_argument('--headless')
    driver = webdriver.Chrome(options=options)
    driver.get('https://news.yahoo.co.jp/topics')
    driver.implicitly_wait(0.5)
    yjnSub_list_item = []
    yjnSub_section_title = ""
    news = []
    try:
        yjnSub_section = driver.find_element(by=By.CLASS_NAME, value="yjnSub_section")
        yjnSub_section_title = yjnSub_section.find_element(by=By.CLASS_NAME, value='yjnSub_section_title').text
        yjnSub_list_item = yjnSub_section.find_elements(by=By.CLASS_NAME, value='yjnSub_list_item')
    except NoSuchElementException as e:
        print("そんな要素ないぞ")
        print(e)
    for item in yjnSub_list_item:
        rank = item.find_element(by=By.CLASS_NAME, value="yjnSub_list_rankNum").text
        headline = item.find_element(by=By.CLASS_NAME, value="yjnSub_list_headline").text
        link = item.find_element(by=By.TAG_NAME, value="a").get_attribute("href")
        news.append(headline)
        print(f'{rank} ヘッドライン：{headline}')
        print(link)

    driver.quit()
    print('news...')
    print(news)
    return ','.join(s for s in news)


if __name__ == '__main__':
    news = get_ranking()
