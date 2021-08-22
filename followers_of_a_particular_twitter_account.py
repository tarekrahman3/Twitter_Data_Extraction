from selenium import webdriver
from selenium.webdriver.firefox.options import Options
import pandas as pd
import time

options = Options()
options.add_argument("--start-maximized")
options.add_argument("--no-sandbox")

def auth(driver):
    driver.get('https://twitter.com/login')
    time.sleep(5)
    username = 'your username'
    password = 'your password'
    username_box = driver.find_element_by_xpath('//input[@name="session[username_or_email]"]').send_keys(username)
    password_box = driver.find_element_by_xpath('//input[@name="session[password]"]').send_keys(password)
    driver.find_element_by_xpath('//div[@dir="auto" and span/span[text()="Log in"]]').click()

def GetAllVisibleFollowers(driver):
    each_followers__username_xpath = '//div[@aria-label="Timeline: Followers"]/div/div//a[@aria-hidden]'
    All_Visible_Followers = driver.find_elements_by_xpath(each_followers__username_xpath)
    return All_Visible_Followers

def scrollvisibleheight(driver):
    driver.execute_script('window.scrollBy(0,window.top.innerHeight+window.top.innerHeight/2)')

def initiate_main_sequence(url:str, followers_amount:int, list_:list):
    driver = webdriver.Firefox(executable_path="./geckodriver")
    auth(driver)
    driver.get(url)
    while True:
        if len(set(list_))>=followers_amount:
            break
        try:
            users = GetAllVisibleFollowers(driver)
            [d.append(user.get_attribute('href')) for user in users]
            scrollvisibleheight(driver)
            time.sleep(2)
            print(len(set(list_)))
        except KeyboardInterrupt:
            break

if __name__ == '__main__':
    user_input = input('twitter account username: ')
    followers = int(input('how many followers does this account have? : '))
    target_account = "https://twitter.com/" + user_input + "/followers"
    d = []
    initiate_main_sequence(target_account, followers, d)
    final_data = {'user_id':list(set(d))}
    pd.DataFrame(final_data).to_csv(f'{user_input} followers.csv')
