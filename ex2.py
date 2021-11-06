from bs4 import BeautifulSoup
import requests
import os

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
  print("The file has been modified or has been created.")
else:
  print('An error occured')

print("-----------------------------")
