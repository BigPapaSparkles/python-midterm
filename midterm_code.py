#Christopher Lara 10/28/2021  Midterm project BeautifulSoup
#IMPORTANT. if it doesn't work as one file for whatever reason, please break it down from each example into seperate files
#or temporarily delete the other examples if you run into an error.
from bs4 import BeautifulSoup
import requests #to take requests from the web
import re #lets you check if a particular string matches a given regular expression
import os #to check if the files created exists on current directory.


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

#EXAMPLE 2. changing textboxes in html, and creating a new file.
def doesFileExists(filePathAndName): #Will be used later.
    return os.path.exists(filePathAndName)

url1 = "https://www.facebook.com/"
result1 = requests.get(url1)
doc1 = BeautifulSoup(result1.text, "html.parser")

parent1 = doc1.find_all("input", id="email") #Since Email and Password had different id="" definitions I had to make two for loops. Not every website is built the same.
passw = doc1.find_all("input", id="pass")

for tags in parent1:
    tags['placeholder'] = "Hello everyone my name is Bowser"

for tags in passw:
    tags['placeholder'] = "I'm the best."

with open("fixed.html", "w", encoding='utf-8') as file: #the encoding argument is so it doesn't try to write in errors into the file.
        file.write(str(doc1))

if doesFileExists('fixed.html'): #Checks to see if the html file exists. and if it does that means it has been modified
  print ("The file has been modified")
else:
  print ('An error occured')

print("-----------------------------")


#EXAMPLE #3 Finding the price of various results on NewEgg
#Taking the html directly from a website url
search = input("What product do you want to search for? ")
url2 = f"https://www.newegg.com/p/pl?d={search}&N=4131"
result2 = requests.get(url2)

#add results of the get request into doc1
doc2 = BeautifulSoup(result2.text, "html.parser")

page_num = doc2.find(class_="list-tool-pagination-text").strong
pages = int(str(page_num).split("/")[-2].split(">")[-1][:-1])  #[-1][:-1} removes the last element for us.

items_found = {} #dictionary for the items we find.

for page in range(1, pages + 1):
	url = f"https://www.newegg.com/p/pl?d={search}&N=4131&page={page}"
	page = requests.get(url).text
	doc2 = BeautifulSoup(page, "html.parser")

#within this class we are only looking through SEARCH RESULTS.
#will match any text that contains the search term within the pages acquired.
	div = doc2.find(class_="item-cells-wrap border-cells items-grid-view four-cells expulsion-one-cell")
	results = div.find_all(text=re.compile(search)) #with re.compile it will match items that have more character than the search term.

#if the item we're looking for is in results.
	for item in results: #item for this case will be the item we're looking for. AKA 3080
		parent = item.parent
		if parent.name != "a":  #check if parent is in "a" tag
			continue

		link = parent['href'] #this is the link to the product.
		next_parent = item.find_parent(class_="item-container") #parent of the parent. this is where item info is located so we need this parent.
		try:
			price = next_parent.find(class_="price-current").find("strong").string #class_="price current" is where the price in the html was located.
			items_found[item] = {"price": int(price.replace(",", "")), "link": link} #another dictionary for the price. .replace to remove ','
		except:
			pass

sorted_items = sorted(items_found.items())
#A basic sort so it looks neat. it sorts the results alphabetically
for item in sorted_items:
	print(item[0])
	print(f"${item[1]['price']}")
	print(item[1]['link'])
	print("---------------------------------------------------------------------------")

#find_parent command finds the parent of the class we're looking for.

#use .attrs when looking for a tag to find all attributes
