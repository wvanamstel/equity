import requests

url = "https://www.google.com/finance/getprices?i=60&p=30d&f=d,o,h,l,c,v&df=cpct&q=VXX"
url = "http://www.netfonds.no/quotes/posdump.php?date=20160303&paper=AA.N&csv_format=csv"

data = requests.get(url)
