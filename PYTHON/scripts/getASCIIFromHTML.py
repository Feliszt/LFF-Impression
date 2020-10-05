from lxml import html
import requests

# link
url = "https://websitebuilders.com/tools/html-codes/ascii/"

# fetch page info
page = requests.get(url)
tree = html.fromstring(page.content)

# get link for picture
asciiChar  = tree.xpath("//td[@class='table_entity']")

#
str = ''
for el in asciiChar:
    str = str + el.text_content()

# write file
with open("../../DATA/others/asciichar.txt", "w", encoding="utf8") as f:
    f.write(str)
