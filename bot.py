from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
import time,bs4
from source import open_and_click,find

class MediumBot:
    def __init__(self,username):
        self.username=username
        
        self.driver = webdriver.Chrome("chromedriver")
        self.driver.maximize_window()
        self.actions = ActionChains(self.driver)
        self.following_number_xpath="/html/body/div/div/div[3]/div[1]/div[3/div/div/h2"
        self.followers_ul_xpath="/html/body/div/div/div[3]/div[1]/div[3]/divdiv/div/h2"
        self.followers_ul_xpath="/html/body/div/div/div[3]/div[1]/div[3]/div/div/div/h2"
        self.followers_ul_xpath="/html/body/div/div/div[3]/div[1]/div[3]/div/div/div/ul/li"
        self.following_ul_xpath="/html/body/div/div/div[3]/div[1]/div[3]/div/div/div[2]/ul/li"
        self.articles_xpath="/html/body/div[1]/div/div[3]/div/div/main/div/div[2]/div/div/article"
        self.articles_clap_xpath="/html/body/div/div/div[3]/div/div/main/div/div[2]/footer/div/div/div/div/div[1]/div[1]/span[2]/div/div[2]/div/div/p/button"
        self.alternate_clap_xpath="/html/body/div/div/div[3]/div/div/main/div/div[3]/footer/div/div/div/div/div[1]/div[1]/span[1]/div/div[2]/div/div/p/button"
        self.article_read_time_xpath="/html/body/div/div/div[3]/div/div/main/div/div[2]/div[1]/div/article/div/div[2]/header/div[1]/div[1]/div[2]/div[2]/div[2]"
        self.alternate_read_time_xpath="/html/body/div/div/div[3]/div/div/main/div/div[3]/div[1]/div/article/div/div[2]/header/div[1]/div[1]/div[2]/div[2]/div[2]"
        self.article_title_selector="h1"
        self.delay=30
    def GetArticleTitle(self):
        article_text=find(self.actions,self.driver,self.delay,selector=self.article_title_selector)
        article_text=article_text[0].get_attribute("innerHTML")
        return article_text
    def GetArticleClaps(self):
        article_clap=find(self.actions,self.driver,self.delay,xpath=self.articles_clap_xpath)
        try:
            article_clap=article_clap[0].get_attribute("innerHTML")
        except:
            article_clap=find(self.actions,self.driver,self.delay,xpath=self.alternate_clap_xpath)
            article_clap=article_clap[0].get_attribute("innerHTML")
        return article_clap    
    def GetArticleReadTime(self):
        article_read_time=find(self.actions,self.driver,self.delay,xpath=self.article_read_time_xpath)
        try:
            article_read_time=article_read_time[0].get_attribute("innerHTML")
        except:
            article_read_time=find(self.actions,self.driver,self.delay,xpath=self.alternate_read_time_xpath)
            article_read_time=article_read_time[0].get_attribute("innerHTML")
        return article_read_time
    def GetArticlesData(self,article_links):
        article_data=[]
        for article_link in article_links:
            self.driver.get(article_link)
            article_text=self.GetArticleTitle()
            article_clap=self.GetArticleClaps()
            article_read_time=self.GetArticleReadTime()
            article_obj=[article_text,article_clap,article_read_time]
            article_data.append(article_obj)
            print(article_obj)
        return article_data
    def GetArticles(self):
        self.driver.get(f"https://medium.com/@{self.username}")
        
        last_height = self.driver.execute_script("return document.body.scrollHeight")
        while True:
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight-1500);")
            time.sleep(5)
            new_height = self.driver.execute_script("return document.body.scrollHeight")
        
            if new_height == last_height:
                break
            last_height = new_height
            
        articles=find(self.actions,self.driver,self.delay,xpath=self.articles_xpath)
        article_links=[]
        for article in articles:
            innerhtml=article.get_attribute("innerHTML")
            soup=bs4.BeautifulSoup(innerhtml,"html.parser")
            elements=soup.find_all("a")
            
            if len(elements) >1:
                target=elements[1]
            else:
                target=elements[0]
            current_url= self.driver.current_url[:-1] if self.driver.current_url[-1] =="/" else self.driver.current_url 
            article_links.append(f"{current_url}{target['href']}")
        self.GetArticlesData(article_links)
        
    def GetFollowers(self):
        self.driver.get(f"https://medium.com/@{self.username}/followers")
        
        number_of_followers=int(find(self.actions,self.driver,self.delay,xpath=self.following_number_xpath)[0].get_attribute("textContent").replace("Followers",""))
        print(number_of_followers)
        scrolls=number_of_followers //8
        for i in range(scrolls):
            self.driver.execute_script("window.scrollBy(0,925)", "")
            time.sleep(1)
        following_list=find(self.actions,self.driver,self.delay,xpath=self.followers_ul_xpath)
        l=len(following_list)
        following_name=[]
        for i in range(0,l):
            innerhtml=following_list[i].get_attribute("innerHTML")
            soup = bs4.BeautifulSoup(innerhtml,"html.parser")
            elements=soup.find_all("h2")
            following_name.append(elements[0].get_text())
        print(following_name)
        return following_name
    def GetFollowing(self):
        ### Get Following's name
        self.driver.get(f"https://medium.com/@{self.username}/following")
        number_of_followers=int(find(self.actions,self.driver,self.delay,xpath=self.following_number_xpath)[0].get_attribute("textContent").replace("Following",""))
        print(number_of_followers)
        scrolls=number_of_followers //8
        for i in range(scrolls):
            self.driver.execute_script("window.scrollBy(0,925)", "")
            time.sleep(1)
        following_list=find(self.actions,self.driver,self.delay,xpath=self.following_ul_xpath)
        l=len(following_list)
        following_name=[]
        for i in range(0,l):
            innerhtml=following_list[i].get_attribute("innerHTML")
            soup = bs4.BeautifulSoup(innerhtml,"html.parser")
            elements=soup.find_all("h2")
            following_name.append(elements[0].get_text())
        print(following_name)
        return following_name
    def GetUnfollowers(self):
        followers=set(self.GetFollowers())
        following=set(self.GetFollowing())
        unfollowers=list(following.difference(followers))
        print(f"Unfollowers: {unfollowers}")

if "__main__" == __name__:
    bot=MediumBot("paulfrazee")
    bot.GetUnfollowers()
    bot.GetArticles()
    