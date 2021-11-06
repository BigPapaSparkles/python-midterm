#EXAMPLE 3 comparing prices for a specific product on new newegg
from bs4 import BeautifulSoup
import requests
import re
#EXAMPLE #3 Finding the price of various results on NewEgg
#Taking the html directly from a website url
search = input("What product do you want to search for? ")
url2 = f"https://www.newegg.com/p/pl?d={search}&N=4131"
result2 = requests.get(url2)

#add results of the get request into doc1
doc2 = BeautifulSoup(result2.text, "html.parser")

#we do a bit of splitting and the use of the strong tag to find the exact amount of pages of our search.
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
	for item in results: #item for this case will be the item we're looking for.
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
