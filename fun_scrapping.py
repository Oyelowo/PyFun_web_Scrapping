# -*- coding: utf-8 -*-
"""
Created on Thu Jan 25 03:39:32 2018

@author: oyedayo
"""
######AUTOMATE THE BORING STUFFS FOR FUN#################
########SCRAPPING NEWS WEBSITE###################
#import the necessary libraries
from bs4 import BeautifulSoup as bs
import requests as rq
import pandas as pd

#get the url. 
#I have decided to try YLE which is a news website in Finland"
#I am curious to know how many times Trump has appeared in the news.

#get the page for rss feeds.
url='https://feeds.yle.fi/uutiset/v1/majorHeadlines/YLE_UUTISET.rss'

#the response
respo = rq.get(url)

#the content of the response
soup= bs(markup= respo.content, features='xml')
#check the type
type(soup)

items = soup.findAll('item') 
#or
#items=soup.find_all('item')

len(items)
#items[0].title.text
#items[149].enclosure['url']

    
#create empty list
news_items=[]
#get all items in the news
##This willbe achieved by iterating over all the items and inserting the 
##dictionaries into the empty list
for item in items:
    news_item={}
    news_item['title']= item.title.text
    news_item['description']=item.description.text
    news_item['link']=item.link.text
    news_item['image']= item.enclosure['url'] if item.enclosure is not None else ''
    news_items.append(news_item)


#google translator will be used to translate the words in finnish to english.
from googletrans import Translator
tr=Translator()
# =============================================================================
# #Alternative
# from translate import Translator
# tr=Translator(to_lang='en', from_lang='fi')
#tr.translate(text='Robert Muellerin johtamassa tutkinnassa selvitetään, sekaantuiko')
# =============================================================================


#The below is done to put the various attributes into a dataframe.
news_items= pd.DataFrame()
for i, item in enumerate(items):
    print(i)
    news_items.loc[i, 'title']=item.title.text
    news_items.loc[i, 'title_en']=(tr.translate(item.title.text)).text
    news_items.loc[i, 'link']=item.link.text
    news_items.loc[i, 'description']=item.description.text
    news_items.loc[i, 'description_en']=(tr.translate(item.description.text)).text
    news_items.loc[i, 'image']=item.enclosure['url'] if item.enclosure is not None else ''

# e.g: we can see how many times Trump appeared in the news
trump_occur=len([r for i,r in news_items.iterrows() if 'Trump' in r.title])
print("Trump's name appeared {0} times in the news publications".format(trump_occur))
# =============================================================================
#alternative
# trump=[]
# for idx, rows in news_items.iterrows():
#     if 'Trump' in rows.title:
#         trump.append(rows.title)
#print("Trump's name appeared {0} times in the news publications".format(len(trump)))
# =============================================================================

#here, it shows that trump name appeared twice. we can further check the content of the news and more.

# =============================================================================
# #Online images can be gotten by using these two libraries
# url2='https://images.cdn.yle.fi/image/upload//w_205,h_115,q_70/13-3-10039531.jpg'
# #we can also see the kind of image
# from PIL import Image as Img_pil
# im = Img_pil.open(rq.get(url2, stream=True).raw)
# 
# from IPython.display import Image as Img_ip
# Img_ip(url2)
# =============================================================================



#####THE FULL TITLES AND DEESCRIPTIONS OF WHERE TOPIC ABOUT TRUMP APPEARED###############
for idx, rows in news_items.iterrows():
    if 'Trump' in rows.title:
        print('Title: ', rows.title+'.\nDescription: ', rows.description, '\n'*2)

####IN ENGLISH
for idx, rows in news_items.iterrows():
    if 'Trump' in rows.title:
        print('Title: ', rows.title_en, '.\nDescription: ', rows.description_en, '\n'*2)



###########THE IMAGES USED IN THOSE PUBLICATIONS##########################
#Either of these two libraries can be used but I chose to use both in the alternative
from PIL import Image as Img_pil
from IPython.display import Image as Img_ip

#get all the images in a list
#this is done by iterating over all rows in the dataframe, get the image column and use the Image(Img_ip)
#function on the url of the image. conditional statement is further created to know if 'Trump' is i the title.
trump_pics=[Img_ip(rows.image) for idx,rows in news_items.iterrows() if 'Trump' in rows.title]

#so, how many of them do we have?
print("There are {number} pictures used in all Trump's publications.".format(number=len(trump_pics)))

#now, let's see the pictures.
#first picture
trump_pics[0]

#second picture
trump_pics[1]

# =============================================================================
# #Alternative 1
# img=[]     
# for idx, rows in news_items.iterrows():
#     if 'Trump' in rows.title:
#         url_img=rows.image
#         img.append(url_img)
#         
#     
# #now, we can see the first and second images
# Img_pil.open(rq.get(img[0], stream=True).raw)
# Img_ip(img[1])
# =============================================================================

# =============================================================================
# #alternative 2
# news_items= pd.DataFrame()
# title=[];link=[];descr=[];image=[]
# for item in items:
#      title.append(item.title.text)
#      link.append(item.link.text)
#      descr.append(item.description.text)
#      if item.enclosure is not None:
#          image.append(item.enclosure['url'])
#      else:
#          image.append('')
# news_items['title']=title
# news_items['link']=link
# news_items['description']=descr
# news_items['image']=image
# =============================================================================
        
        

# =============================================================================
# #alternative 3
# title=[];link=[];descr=[];image=[]
#for i in range(len(items)):
#    title.append(items[i].title.text)
#    link.append(items[i].link.text)
#    descr.append(items[i].description.text)
#    if items[i].enclosure is not None:
#        image.append(items[i].enclosure['url'])
#    else:
#        image.append('')
# =============================================================================
        

    
#this is how to get title alone as a list
#titles= [item.title.text for item in items]

