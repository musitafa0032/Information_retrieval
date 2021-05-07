import requests
from bs4 import BeautifulSoup
r = requests.get("https://www.yicai.com/")
r.encoding="utf-8"
soup = BeautifulSoup(r.text,"html.parser")
items=soup.select('.m-con>a')
outF = open("crawled.txt","w")
for item in items:
    outF.write(f"title:\t{item.select('h2')[0].text}")
    outF.write("\n")
    outF.write(f"content:\t{item.select('p')[0].text}")
    outF.write("\n")
    outF.write(f"time:\t{item.select('span')[0].text}")
    outF.write("\n")
    outF.write(f"ID:\t{item['href']}")
    outF.write("\n")
    outF.write("\n")

