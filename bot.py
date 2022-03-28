from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
import time,bs4
from source import open_and_click,find

class MediumBot:
    def __init__(self,username):
        self.username=username
        
        self.driver = webdriver.Chrome("chromedriver.exe")
        self.driver.maximize_window()
        self.actions = ActionChains(self.driver)
        self.followers_btn_xpath="/html/body/div/div/div[3]/div/div/div[2]/div/div/div/div[1]/div/div[2]/p/span/button"
        self.followers_div_xpath="/html/body/div[2]/div/div[1]/div"
        self.more_followers_btn_selector="//button[contains(text(),'Show more followers')]"
        
        self.followers_div_xpath="/html/body/div[2]/div/div[1]/div/div"
        "/html/body/div[2]/div/div[1]/div/div[22]"
        
        self.delay=30
    def open_profile(self):
        self.driver.get(f"https://medium.com/@{self.username}")
        number_of_followers=int(find(self.actions,self.driver,self.delay,xpath=self.followers_btn_xpath)[0].get_attribute("textContent").replace("Followers",""))
        open_and_click(self.actions,self.driver,self.delay,xpath=self.followers_btn_xpath)
        no_clicks=number_of_followers // 10
        for i in range(no_clicks):
            i=find(self.actions,self.driver,self.delay,xpath=self.more_followers_btn_selector)
            self.driver.execute_script("arguments[0].scrollIntoView();", i[0])
            self.driver.execute_script("arguments[0].click();", i[0])
            time.sleep(2)
        followers_div=find(self.actions,self.driver,self.delay,xpath=self.followers_div_xpath)
        
        l=len(followers_div)
        followers_name=[]
        for i in range(1,l):
            innerhtml=followers_div[i].get_attribute("innerHTML")
            soup = bs4.BeautifulSoup(innerhtml,"html.parser")
            elements=soup.find_all("a")
            followers_name.append(elements[0].get_text())
        print(followers_name)
            
if "__main__" == __name__:
    bot=MediumBot("humble_bee")
    bot.open_profile()