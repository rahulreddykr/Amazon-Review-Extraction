# -*- coding: utf-8 -*-
"""
Created on Fri Mar 30 15:15:55 2018

@author: Rahul Reddy
"""

from lxml import html
import json
import requests

def ReadAsin():
    #Replace your own ASIN here 
    asin = 'B0756ZD5PM'
    #Set the number of pages of reviews you need
    maxpages = '10'
    
    review_data = ParseReviews(asin,maxpages)
 
    with open('review_filename.txt', 'w',encoding="utf8",newline='') as f:
        json.dump(review_data, f, sort_keys = True, indent = 4,ensure_ascii = False)
 
    print("File created successfully")
    
def ParseReviews(asin,maxpage):
    # Try to connect for 3 times 
    for i in range(3):
        try:
            # Add some user agent to prevent amazon from blocking the request 
            headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.90 Safari/537.36'}
            extracted_data=[]
            
            for p in range(int(maxpage)):           
                amazon_reviews_url  = 'http://www.amazon.in/product-reviews/'+asin+'/ref=cm_cr_getr_d_paging_btm_'+str(p+1)+'?pageNumber='+str(p+1)                
                print ("Downloading and processing page "+amazon_reviews_url)  
                page = requests.get(amazon_reviews_url, headers = headers)
                page_response = page.text
                parser = html.fromstring(page_response)
  
                reviews_list = []                
                for elem in parser.xpath('//div[@class="a-section celwidget"]'):  
                    #Create a dictionary/json of review elements
                    review_dict = {
                                'review_text':elem.xpath('.//span[@class="a-size-base review-text"]//text()'),
                                'review_posted_date':elem.xpath('.//span[@data-hook="review-date"]//text()'),
                                'review_header':elem.xpath('.//a[@data-hook="review-title"]//text()'),
                                'review_rating':elem.xpath('.//span[@class="a-icon-alt"]//text()'),
                                'review_author':elem.xpath('.//a[@data-hook="review-author"]//text()')
                                }
                    reviews_list.append(review_dict) 
         
                extracted_data.append(reviews_list)
 
            return extracted_data

        except ValueError:
            print ("Retrying to get the correct response")

    return {"error":"failed to process the page","asin":asin}

if __name__ == '__main__':
    ReadAsin()
