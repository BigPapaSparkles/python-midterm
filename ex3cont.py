from bs4 import BeautifulSoup
import requests
import re

search = input("What product do you want to search for? ")

url2 = f"https://www.newegg.com/p/pl?d={search}&N=4131"
result2 = requests.get(url2)
#add results of the get request into doc2
doc2 = BeautifulSoup(result2.text, "html.parser")

#run this to find out what tags you need. #MAKE SURE YOU DON'T FORGET THE TAGS.
page_num = doc2.find(class_="list-tool-pagination-text").strong
#<strong>1<!-- -->/<!-- -->15</strong> is the output. convert to string.
print(page_num)
#to convrrt it you need to split the text
pages = str(page_num).split("/")[-2]
print(pages)
#the output now should be <!-- -->15<, But that's not good enough we need to split it further.
pages2 = int(str(page_num).split("/")[-2].split(">")[-1][:-1])
print(pages2)
