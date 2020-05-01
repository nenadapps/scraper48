from bs4 import BeautifulSoup
import datetime
from random import randint
from random import shuffle
import requests
from time import sleep

base_url = 'http://michael-hamilton.com/'

def get_html(url):
    
    html_content = ''
    try:
        page = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
        html_content = BeautifulSoup(page.content, "lxml")
    except: 
        pass
    
    return html_content

def get_details(html, category):
    
    stamp = {}
    
    try:
        title = html.select('b')[0].get_text().strip()
        title = title.replace(':', '')
        stamp['title'] = title
    except:
        stamp['title'] = None     
    
    try:
        price = html.select('b')[1].get_text().strip()
        stamp['price'] = price
    except:
        stamp['price'] = None  
       
    try:
        sku = html.find_all('input', attrs={'name':'id'})[0].get('value')
        stamp['sku'] = sku
    except:
        stamp['sku'] = None         
    
    try:
        raw_text_parts1 = str(html).split('</b><br/>')
        raw_text_parts2 = raw_text_parts1[1].split('<br/><b>')
        raw_text = raw_text_parts2[0].strip()
        stamp['raw_text'] = raw_text
    except:
        stamp['raw_text'] = None 
    
    stamp['currency'] = 'GBP'
    
    stamp['category'] = category
    
    images = []                    
    try:
        image_items = html.select('a')
        for image_item in image_items:
            image_item_href = image_item.get('href')
            if ('javascript:chgimg("' in image_item_href) or ("javascript:popup('" in image_item_href):
                img_parts1 = image_item_href.split('(')
                img_parts2 = img_parts1[1].split(',')
                img_src = img_parts2[0].replace('"', '').replace("'", '').replace(');', '')
                img = base_url + img_src
                if img not in images:
                    images.append(img)
    except:
        pass
    
    stamp['image_urls'] = images 
        
    # scrape date in format YYYY-MM-DD
    scrape_date = datetime.date.today().strftime('%Y-%m-%d')
    stamp['scrape_date'] = scrape_date
    
    print(stamp)
    print('+++++++++++++')
           
    return stamp

def get_page_items(url):

    items = []

    next_url = ''

    try:
        html = get_html(url)
    except:
        return items, next_url

    try:
        item_conts = html.select('.stamppop')
        if not(len(item_conts)): 
            item_conts = html.select('.listing')
        
        for item_cont in item_conts:
            if (item_cont not in items) and len(item_cont.select('b')):
                items.append(item_cont)
    except:
        pass
    
    try:
        for next_item in html.find_all('td', attrs={'align':'right'}):
            next_text = next_item.get_text().strip()
            if next_text == 'Next page':
                next_href = next_item.select('a')[0].get('href')
                next_url = base_url + next_href
    except: 
        pass
     
    shuffle(list(set(items)))
    
    return items, next_url

item_dict = {
"STAMPS": "http://michael-hamilton.com/stamps.php",
"POSTAL HISTORY": "http://michael-hamilton.com/covers.php",
"POSTMARKS": "http://michael-hamilton.com/postmarks.php",
"BUY THE BEST": "http://michael-hamilton.com/best.php"
    }
    
for key in item_dict:
    print(key + ': ' + item_dict[key])   

selection = input('Choose category: ')

page_url = item_dict[selection]
while page_url:
    page_items, page_url = get_page_items(page_url)
    for page_item in page_items:
        stamp = get_details(page_item, selection) 
    sleep(randint(25, 65))    
       
