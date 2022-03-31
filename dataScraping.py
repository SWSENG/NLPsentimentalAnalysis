# -*- coding: utf-8 -*-
"""
Created on Fri Mar  4 14:39:25 2022

@author: HP
"""

import requests
from bs4 import BeautifulSoup
import pandas as pd

#url = 'https://www.amazon.com/100Pcs-Disposable-Face-Masks-Black/product-reviews/B09DY1W4L3/ref=cm_cr_arp_d_paging_btm_next_2?ie=UTF8&reviewerType=all_reviews&pageNumber=1'
reviewList = []

def get_soup(url):
    #to make sure we are not robot then use the localhost to assesss the url
    r = requests.get('http://localhost:8050/render.html', params = {'url':url, 'wait':2})
    soup = BeautifulSoup(r.text, 'html.parser')
    
    return soup

def get_reviews(soup):
    #print(soup.title.text)
    reviews = soup.find_all('div', {'data-hook': 'review'})
    try:   
        for item in reviews:
            review = {
                'product' : soup.title.text.replace('Amazon.com: Customer reviews: ', '').strip(),
                'title' : item.find('a', {'data-hook': 'review-title'}).text.strip(),
                'rating' : float(item.find('i',{'data-hook': 'review-star-rating'}).text.replace('out of 5 stars', '').strip()),
                'content' : item.find('span', {'data-hook': 'review-body'}).text.strip()
                }
            reviewList.append(review)

    except:
        pass
    
#soup = get_soup('https://www.amazon.com/100Pcs-Disposable-Face-Masks-Black/product-reviews/B09DY1W4L3/ref=cm_cr_arp_d_paging_btm_next_2?ie=UTF8&reviewerType=all_reviews&pageNumber=1')
#get_reviews(soup)
#print(reviewList[0])

for x in range(1,500):
    soup = get_soup(f'https://www.amazon.com/Face-Mask-Black-Disposable-Masks/product-reviews/B08FYBS2XW/ref=cm_cr_arp_d_paging_btm_next_2?ie=UTF8&reviewerType=all_reviews&pageNumber={x}')
    print(f'Getting page:{x}')
    get_reviews(soup)
    print(len(reviewList))
    if not soup.find('li', {'class': 'a-disabled a-last'}):
        pass
    else:
        break

        
df = pd.DataFrame(reviewList)
df.to_csv(r'D:\pythonPractical\testDataset.csv', index = False)

print('finnish')