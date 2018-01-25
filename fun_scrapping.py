# -*- coding: utf-8 -*-
"""
Created on Thu Jan 25 03:39:32 2018

@author: oyedayo Oyelowo
"""
######AUTOMATE THE BORING STUFFS FOR FUN#################
########SCRAPPING NEWS WEBSITE###################
#import the necessary libraries
from bs4 import BeautifulSoup as bs
import requests as rq
import pandas as pd

#get the url. 
#I have decided to try YLE which is a news website in Finland"
#I am curious to know how many times name_of_interest has appeared in the news.

#get the page for rss feeds.
url='https://feeds.yle.fi/uutiset/v1/majorHeadlines/YLE_UUTISET.rss'

#This is the name I will be exploring. With this script, you can get the 
#number of times it has appeared in the news headlines in the rss feeds.
#you can also get the pictures that were used and the title and descritpions of 
#the news articles. 
# e.g: name_of_interest='Trump'

#TODO: Transform this script into a package.


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

#get all items in the rss feed
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
    #the english translation of the title
#    news_items.loc[i, 'title_en']=(tr.translate(item.title.text)).text
    news_items.loc[i, 'link']=item.link.text
    news_items.loc[i, 'description']=item.description.text
#    news_items.loc[i, 'description_en']=(tr.translate(item.description.text)).text
    news_items.loc[i, 'image']=item.enclosure['url'] if item.enclosure is not None else ''
    content_xml=item.find('content:encoded').text
    content=''.join(bs(content_xml, "lxml").findAll(text=True))
    #    this  gets the body, removes the extra characters to leave plain text
    news_items.loc[i, 'content']= content
#    news_items.loc[i, 'body_en']= (tr.translate(content)).text


#name to be explored in the rss feeds of the url.
name_of_interest='president'

# e.g: we can see how many times name_of_interest appeared in the news
name_of_interest_occur=len([rows for idx,rows in news_items.iterrows() if name_of_interest in rows.title])
print("{0}'s name appeared {1} times in the news publications".format(name_of_interest, name_of_interest_occur))
#here, it shows that name_of_interest name appeared a number of times. we can further check the content of the news and more.

# =============================================================================
#alternative
# name_of_interest=[]
# for idx, rows in news_items.iterrows():
#     if 'name_of_interest' in rows.title:
#         name_of_interest.append(rows.title)
#print("{0}'s name appeared {1} times in the news publications".format(name_of_interest, len(name_of_interest)))
# =============================================================================



#####THE FULL TITLES AND DEESCRIPTIONS OF WHERE TOPIC ABOUT name_of_interest APPEARED###############
for idx, rows in news_items.iterrows():
    if name_of_interest in rows.title:
        print('Title: ', rows.title+'.\nDescription: ', rows.description, '\n'*2)

####IN ENGLISH
for idx, rows in news_items.iterrows():
    if name_of_interest in rows.title:
        print('Title: ', tr.translate(rows.title).text, '.\nDescription: ', tr.translate(rows.description).text, '\n'*2)


#####CONTENT ORIGINALLY IN FINNISH
for idx, rows in news_items.iterrows():
    if name_of_interest in rows.title:
        print('Title: ', rows.title, '.\nCONTENT: \n', rows.content)



#####THE CONTENT  TRANSLATED INTO ENLISH
for idx, rows in news_items.iterrows():
    if name_of_interest in rows.title:
        print('Title: ', tr.translate(rows.title).text, '.\nCONTENT: \n', tr.translate(rows.content).text)



###########THE IMAGES USED IN THOSE PUBLICATIONS##########################
#Load library for viewing image online.
from IPython.display import Image as Img_ip

#get all the images in a list
#this is done by iterating over all rows in the dataframe, get the image column and use the Image(Img_ip)
#function on the url of the image. conditional statement is further created to know if name_of_interest is i the title.
name_of_interest_pics=[Img_ip(rows.image) for idx,rows in news_items.iterrows() if name_of_interest in rows.title]

#so, how many of them do we have?
print("There are {number} pictures used in all {name}'s publications.".format(number=len(name_of_interest_pics), name=name_of_interest))

#now, let's see the pictures.
#first picture
name_of_interest_pics[3]
    

#second picture
#name_of_interest_pics[1]

# =============================================================================
# #Alternative 
#from PIL import Image as Img_pil
#from IPython.display import Image as Img_ip
# img=[]     
# for idx, rows in news_items.iterrows():
#     if name_of_interest in rows.title:
#         url_img=rows.image
#         img.append(url_img)
#         
#     
# #now, we can see the first and second images
# Img_pil.open(rq.get(img[0], stream=True).raw)
# Img_ip(img[1])
# =============================================================================









######################
#alternative to getting the items into a dataframe which was done earlier
# =============================================================================
# #alternative 1
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
# #alternative 2
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

