import requests
import Quandl
import pandas as pd

url = "https://www.google.com/finance/getprices?i=60&p=30d&f=d,o,h,l,c,v&df=cpct&q=VXX"
# url = "http://www.netfonds.no/quotes/posdump.php?date=20160303&paper=AA.N&csv_format=csv"

data = requests.get(url)

vxz=Quandl.get("GOOG/NYSEARCA_VXZ")
vxx=Quandl.get("GOOG/NYSEARCA_VXX")

pair= pd.DataFrame(index=vxx.index)
pair["vxx_close"] = vxx["Close"]
pair["vxz_close"] = vxz["Close"]
pair=pair.dropna()
pair["spread"] = pair["vxx_close"]-pair["vxz_close"]
pair["mean"]=pair["spread"].rolling_mean(window=60)
pair["std"]=pair["spread"].rolling_std(window=60)

b=df.append([dict(a) for a in s.all()])
