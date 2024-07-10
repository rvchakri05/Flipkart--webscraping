import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import nltk
from nltk.sentiment import SentimentIntensityAnalyzer
import time

web_link = """https://www.flipkart.com/search?q=mobiles+20000+to+40000&otracker=
                search&otracker1=search&marketplace=FLIPKART&as-show=on&as=off"""
browser = webdriver.Chrome()
nltk.download('vader_lexicon')
sid=SentimentIntensityAnalyzer()
#Function for scraping product information

def get_product_info(url):
    browser.get(url)
    data = BeautifulSoup(browser.page_source,features='html.parser')
    serial = len((pd.read_csv('prod.csv')))
    
    for i in data.findAll('a',attrs={'class': 'CGtC98'}):
        scrap_data = {'p_id': [], 'product_name': [], 'price': [], 'img': [], 'link': [], 'hightlights': [], 'Star': [],'5_star' : [],
                      '4_star' : [],'3_star' : [],'2_star' : [],'1_star' : [],}
        
        link=i.get('href')
        browser.get("https://www.flipkart.com"+link)
        data = BeautifulSoup(browser.page_source,features="html.parser")
        name = ((data.find('span', attrs={'class':"VU-ZEz"})).text).replace("\xa0\xa0"," ")
        img=(data.find('img',attrs={'class':"DByuf4 IZexXJ jLEJ7H"}))['src']
        price=(((data.find('div',attrs={'class':"Nx9bqj CxhGGd"})).text).replace("₹","")).replace("'","")
        high=(data.findAll('li',attrs={'class':"_7eSDEz"}))
        pid='flipkart'+str(serial) 
        gh=[]
        star_count=[]
        for i in high:
            gh.append(i.text)
        star=data.find('div',attrs={'class':"XQDdHH"}).text
        five_star = data.findAll('div', attrs={'class': "BArk-j"})
        for i in range(len(five_star)):
            star_count.append(five_star[i].text)


#pid is create product id for our reference
        scrap_data['p_id'].append(str(pid))
        scrap_data['product_name'].append(name)
        scrap_data['link'].append("https://www.flipkart.com"+link)
        scrap_data['price'].append(price)
        scrap_data['hightlights'].append(gh)
        scrap_data['img'].append(img)
        scrap_data['Star'].append(star)
        scrap_data['5_star'].append(star_count[0])
        scrap_data['4_star'].append(star_count[1])
        scrap_data['3_star'].append(star_count[2])
        scrap_data['2_star'].append(star_count[3])
        scrap_data['1_star'].append(star_count[4])
        df=pd.DataFrame(scrap_data)
        
        #scrapping data append to prod.csv file
        df.to_csv('prod.csv',mode='a',header=False,index=False)
        serial+=1
        
    products=(pd.read_csv('prod.csv')).drop_duplicates(subset=["price","Star",'5_star','4_star','3_star','2_star','1_star'],keep='first')
    products.to_csv('products.csv')
    
#iterate product for call function for reviews
    for i in range(len('products.csv')):
        review_id=pd.read_csv('products.csv',index_col=False)
        review_url = review_id['link'][i]
        p_id = review_id['p_id'][i]
        browser.get(review_url)
        jk=browser.find_element(By.CSS_SELECTOR, "div[class='_23J90q RcXBOT'] span")
        if jk:
            jk.click()
            curretnt = browser.current_url
            browser.get(curretnt)
            rev_1=BeautifulSoup(browser.page_source,'html.parser')
            #find pages of review
            pages= rev_1.find('div', class_='_1G0WLw mpIySA')
            if pages:
                pg_rev=pages.find('span').text
                pg_rep = pg_rev.find('of')
                total_page_count = int(pg_rev[int(pg_rep) + 2:len(pg_rev)])
                for j in range(1,total_page_count+1):
                    get_reviews(curretnt+"&page=" + str(j), p_id,0)
            else:
                get_reviews(curretnt, p_id,0)
        else:
            pass
        
#Function for review page clarification and clear error to load
def get_reviews(review,pid,error):
    browser.get(review)
    data=BeautifulSoup(browser.page_source,'html.parser')
    k = data.findAll('div', attrs={'class': 'EKFha-'})
#error rectification for blank page
    if k:
        review_fun(k,pid)
    else:
#condition for try 15 times for blank page or else skip that page
        if error==15:
            pass
        else:
            er=error+1
            browser.delete_all_cookies()
            get_reviews(review,pid,er)
# function for after clear error load review to csv file

def review_fun(k,pid):
    for i in k:
        reviews = {'p_id': [], 'reviewer': [], 'review_head': [], 'review_text': [], 'star': [],
                   'Positive': [], 'Negative': [], 'neutral': [], 'compound': []}
        star = i.find('div', attrs={'class': 'col EPCmJX Ma1fCG'})
        reviewer = i.find('p', attrs={'class': '_2NsDsF AwS1CA'})
        rev_head = i.find('p', attrs={'class': 'z9E0IG'})
        rev_text = i.find('div', attrs={'class': 'ZmyHeo'})
        review_t = (rev_text.text).replace('READ MORE', '')
        
        sentiment = sid.polarity_scores((review_t))
        
        reviews['p_id'].append(pid)
        reviews['reviewer'].append(reviewer.text)
        reviews['review_head'].append(rev_head.text)
        reviews['review_text'].append(review_t)
        reviews['star'].append((star.text)[0])
        reviews['Positive'].append(sentiment['pos'])
        reviews['Negative'].append(sentiment['neg'])
        reviews['neutral'].append(sentiment['neu'])
        reviews['compound'].append((sentiment['compound']))
        df = pd.DataFrame(reviews)
        df.to_csv('revi.csv', mode='a', header=False, index=False)
        
#Start function to scrap product
if __name__=='__main__':
    get_product_info(web_link)
