from urllib.request import Request, urlopen
from bs4 import BeautifulSoup as soup
import csv

csvfile = open('food.csv', 'a+', newline = '', encoding = "utf8")   #Opens CSV file
out_write = csv.writer(csvfile)

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.3'}     #Website Authenticates browser version

req = Request("https://www.simplyrecipes.com/index/", headers = headers)    #Requests to open website
webpage = urlopen(req).read()               #Opens webpage
page_soup = soup(webpage, "html.parser")    #Saves local copy of html in website
mylist = page_soup.findAll("a")             #finds all tags of "a"

Recipe_Name = []

for i in range(161, 1024): #Iterate through all categories in index
    req = Request(mylist[i]["href"], headers = headers)     #stores link of category located in href in req
    webpage = urlopen(req).read()                           #opens website
    page_soup = soup(webpage, "html.parser")                #saves local copy of category's html in website
    mySubList = page_soup.findAll("li", {"class" : "grd-tile grd-tile-normal"})     #

    for element in mySubList:
        try:
            req = Request(element.a["href"], headers = headers)
            webpage = urlopen(req).read()
            page_soup = soup(webpage, "html.parser")


            temp = page_soup.findAll("meta", {"name" : "description"})
            description = temp[0]["content"]

            temp = page_soup.findAll("h1", {"class" : "entry-title"})
            name = temp[0].text

            temp = page_soup.findAll("a", {"name" : "chiclet-terms"})
            categories = []
            for item in temp:
                categories.append(item.span.text)

            temp = page_soup.findAll("span", {"class" : "preptime"})
            prep_time = temp[0].text

            temp = page_soup.findAll("span", {"class" : "cooktime"})
            cook_time = temp[0].text

            temp = page_soup.findAll("span", {"class" : "yield"})
            yeild = temp[0].text

            temp = page_soup.findAll("li", {"class" : "ingredient"})
            ingredients = []
            for item in temp:
                ingredients.append(item.text)

            temp = page_soup.findAll("div", {"class" : "entry-details recipe-method instructions"})
            temp2 = temp[0].find_all("p")
            prep_steps = []
            
            for item in temp2:
                if (item.text != "" and item.text != " "):
                    prep_steps.append(item.text)

            temp = page_soup.findAll("div", {"class" : "featured-image"})
            picture = temp[0].img["src"]

            temp = page_soup.findAll("meta", {"name" : "shareaholic:article_author_name"})
            author = temp[0]["content"]

            if (name not in Recipe_Name):
                final_list = [name, description, categories, prep_time, cook_time, yeild, ingredients, prep_steps, picture, author]
                out_write.writerow(final_list)
                Recipe_Name.append(name)
        except:
            continue
        
csvfile.close()

