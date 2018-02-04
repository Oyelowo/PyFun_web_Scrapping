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
#I am curious to know how many times a name has appeared in the news.
#What was the content pictures used e.tc? Perharps. 

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

len(items)
 
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

#The below is done to put the various attributes into a dataframe.
news_items= pd.DataFrame()
for i, item in enumerate(items):
    print(i)
    news_items.loc[i, 'title']=item.title.text
    news_items.loc[i, 'link']=item.link.text
    news_items.loc[i, 'description']=item.description.text
    news_items.loc[i, 'image']=item.enclosure['url'] if item.enclosure is not None else ''
#    publication date
    news_items.loc[i, 'pubDate']=item.pubDate.text
    if item.find('content:encoded') is not None:
        #get the content of each article
        content_xml=item.find('content:encoded').text
        content=''.join(bs(content_xml, "lxml").findAll(text=True))
    #    this  gets the body, removes the extra characters to leave plain text
        news_items.loc[i, 'content']= content
    #length of article
        news_items.loc[i, 'character']=len(content)
        news_items.loc[i, 'word_count']=len(content.split())
        news_items.loc[i, 'sentence']=len(content.split('.'))

#export the data frame
#news_items.to_csv(r'C:\Users\oyeda\Desktop\PYFUN\news_scrape.txt', sep=';')

#name to be explored in the rss feeds of the url.
name_of_interest='Helsinki'

# e.g: we can see how many times name_of_interest appeared in the news
name_of_interest_occur=len([rows for idx,rows in news_items.iterrows() if name_of_interest in rows.title])
print("{0}'s name appeared {1} times in the news publications".format(name_of_interest, name_of_interest_occur))
#here, it shows that name_of_interest name appeared a number of times. we can further check the content of the news and more.

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
name_of_interest_pics[0]
    

#second picture
#name_of_interest_pics[1]
