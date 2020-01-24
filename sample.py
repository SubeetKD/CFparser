import string 
import requests 
from bs4 import BeautifulSoup

url = "https://codeforces.com/contest/1294/problems"
soup = BeautifulSoup(requests.get(url).text,'lxml')

title = soup.find_all(class_='problemindexholder')
for _ in title:
	#print(_.prettify())
	name = _.find(class_='title').text
	name,shit = name.split('.')
	print(name)
	input_data = _.find(class_='input').pre.text
	print(input_data)