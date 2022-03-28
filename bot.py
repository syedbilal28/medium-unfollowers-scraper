from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
import time
from source import open_and_click,open_and_input

class MediumBot:
    def __init__(self,email,password):
        self.username=username
        self.password=password
        self.driver = webdriver.Chrome("chromedriver.exe")
        self.actions = ActionChains(self.driver)
        self.gmail_url=r'https://accounts.google.com/signin/v2/identifier?continue='+'https%3A%2F%2Fmail.google.com%2Fmail%2F&service=mail&sacu=1&rip=1'+'&flowName=GlifWebSignIn&flowEntry = ServiceLogin'
        self.gmail_email_input_selector="/html/body/div[1]/div[1]/div[2]/div/div[2]/div/div/div[2]/div/div[1]/div/form/span/section/div/div/div[1]/div/div[1]/div/div[1]/input"
        self.gmail_password_input_selector="/html/body/div[1]/div[1]/div[2]/div/div[2]/div/div/div[2]/div/div[1]/div/form/span/section/div/div/div[1]/div[1]/div/div/div/div/div[1]/div/div[1]/input"
        self.outlook_url="https://login.live.com/login.srf?wa=wsignin1.0&rpsnv=13&ct=1648377358&rver=7.0.6737.0&wp=MBI_SSL&wreply=https%3a%2f%2foutlook.live.com%2fowa%2f%3fnlp%3d1%26RpsCsrfState%3d88a20daf-139a-bacd-1069-7c7706897f4a&id=292841&aadredir=1&CBCXT=out&lw=1&fl=dob%2cflname%2cwld&cobrandid=90015"
        self.medium_signin_xpath="/html/body/div/div/div[3]/div[1]/div/div/div/div[3]/span[4]/div/p/span/a"
        self.medium_signin_email_xpath="/html/body/div[2]/div/div/div/div[1]/div/div[2]/div[4]/button"
        self.medium_email_input_xpath="/html/body/div[2]/div/div/div/div[1]/div/div[2]/div/div[1]/div/div/div[2]/div/p/input"
        self.delay=30
    def login(self):
        if "gmail" in self.email:
            target_service=self.gmail_url    
        elif "outlook" in self.email or "hotmail" in self.email or "live" in self.email:
            target_service=self.gmail_url
        self.driver.get("https://medium.com")
        open_and_click(self.actions,self.driver,self.delay,xpath=self.medium_signin_xpath)
        time.sleep(2)
        open_and_click(self.actions,self.driver,self.delay,xpath=self.medium_signin_email_xpath)
        open_and_input(self.actions,self.driver,self.delay,xpath=self.medium_email_input_xpath,input=self.email,choice=(0,True))
        self.driver.get(target_service)
        open_and_input(self.actions,self.driver,self.delay,xpath=self.gmail_email_input_selector,input=self.email,choice=(0,True))
        time.sleep(5)
        open_and_input(self.actions,self.driver,self.delay,xpath=self.gmail_password_input_selector,input=self.password,choice=(0,True))

if "__main__" == __name__:
    bot=MediumBot("syed.bilal.sba@gmail.com","inspirehot")
    bot.login()