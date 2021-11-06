from bs4 import BeautifulSoup
import requests


#EXAMPLE #1 Finding the price of an item on a NewEgg webpage.
#Taking the html directly from a website url
url = input("copy paste an item link from NewEgg: ")
result = requests.get(url)

#add results of the get request into doc1
doc = BeautifulSoup(result.text, "html.parser")

#finds a specific word in the website.
price = doc.find_all(text="$")
name = doc.find(class_="product-title")
#since html works in family we are looking for text="$", and the name of the product is within class_="product-title"
parent = price[0].parent
#once you know the parent tag, you can write can search for the words between that parent. For this case, The price is between Strong and Sup tags.
strong = parent.find("strong")
sup = parent.find("sup")
print("the price of " + name.string + " is: $" + strong.string + sup.string) #combine them and you have the accurate price of that specific webpage.
print("-----------------------------")
