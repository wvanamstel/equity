import requests
import zipfile
import datetime as dt

from cql.models import Forex
from cql.cluster import CqlClient
from decimal import *


getcontext().prec = 5


class GetForex(object):
    def __init__(self):
        try:
            self.cl = CqlClient(Forex)
        except Exception as e:
            print("Error on C* init: {}".format(str(e)))

    def download_files(self):
        print("Enter currency pair, <enter> for all:")
        cur_pairs = input().split(",")
        if cur_pairs[0] == "":
            cur_pairs = ["AUDJPY", "AUDNZD", "AUDUSD", "CADJPY", "CHFJPY", "EURCHF", "EURGBP", "EURJPY", "EURUSD",
                         "GBPJPY", "GBPUSD", "NZDUSD", "USDCAD", "USDCHF", "USDJPY"]
        print("Enter year, <enter> for all:")
        years = input().split(",")
        if years[0] == "":
            years = [str(i) for i in range(2010, 2017)]
        print("Enter month, <enter> for all:")
        months = input().split(",")
        if months[0] == "":
            months = ["01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11", "12"]

        months_verbose = {"01": "JANUARY", "02": "FEBRUARY", "03": "MARCH", "04": "APRIL", "05": "MAY", "06": "JUNE",
                          "07": "JULY", "08": "AUGUST", "09": "SEPTEMBER", "10": "OCTOBER", "11": "NOVEMBER",
                          "12": "DECEMBER"}
        file_path = "/home/w/data/forex/"
        for year in years:
            for month in months:
                for pair in cur_pairs:
                    file_name = pair + "-" + year + "-" + month + ".zip"
                    base_url = "http://www.truefx.com/dev/data/" + year + "/" + months_verbose[month] + "-" + year + "/"
                    print("Downloading {0}".format(file_name))
                    r = requests.get(base_url + file_name)
                    if r.status_code == 200:
                        with open(file_path + file_name, "wb") as f:
                            for piece in r:
                                f.write(piece)
                        print("Unzipping {0}".format(file_name))
                        zip_file = zipfile.ZipFile(file_path + file_name)
                        zipfile.ZipFile.extractall(zip_file, path=file_path)
                    else:
                        print("Error retrieving file:{0}".format(file_name))

    def insert_cassandra(self, file_name):
        # files = self.fetch_file_names("*-2016-02.csv")
        # for file_name in files:
        with open(file_name, "r") as f_in:
            print(file_name)
            for i, line in enumerate(f_in):
                print(line, "num:{}".format(i))
                d = dict()
                line = line.rstrip().split(",")
                date_time = dt.datetime.strptime(line[1], "%Y%m%d %H:%M:%S.%f")
                date = dt.datetime.date(date_time)
                d = {"forex_pair": line[0],
                     "tick_time": date_time,
                     "date": date,
                     "bid": float(line[2]),
                     "ask": float(line[3]),
                     }
                Forex.create(**d)
                # if i % 1000 == 0:
                print("Inserting row {} from file {} into C* model {}".format(i, file_name, Forex))

