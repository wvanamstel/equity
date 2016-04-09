import requests
import zipfile
import datetime as dt
import csv

from cql.models import Forex
from cql.cluster import CqlClient
from decimal import *


getcontext().prec = 5


class GetForex(object):
    def __init__(self, cass_conn=True):
        # self.model = model
        if cass_conn:
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
        with open(file_name, "r") as f_in:
            for i, line in enumerate(f_in):
                # ipdb.set_trace()
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
                if i % 10000 == 0:
                    print("Inserting {} from file {} into C* model {}".format(i, file_name, Forex.column_family_name()))


class GetFutures(object):
    def __init__(self):
        self.session = requests.session()

    def download_files(self, asset, start_date):
        # download tick data and serialise to csv
        assets = {"natgas":{"code": "NYMEX.NG",
                            "em": "18949",
                            "market": "24"
                            },
                  "gold": {"code":"comex.GC",
                           "em": "18953",
                           "market": "24",
                           },
                  "wti": {"code": "NYMEX.CL",
                          "em": "18948",
                          "market": "24",
                          },
                  "brent": {"code": "ICE.BRN",
                            "em": "19473",
                            "market": "24",
                            },
                  "heating": {"code": "NYMEX.HO",
                              "em": "18951",
                              "market": "24",
                              },
                  }
        params = {"market": assets[asset]["market"],
                  "em": assets[asset]["em"],
                  "code": assets[asset]["code"],
                  "apply": "1",
                  "from": "02.03.2016",
                  "df": "2",
                  "mf": "2",
                  "yf": "2016",
                  "dt": "4",
                  "mt": "2",
                  "yt": "2016",
                  "to": "04.03.2016",
                  "p": "1",
                  "f": "NYMEX.NG_160302_160304",
                  "e": ".csv",
                  "cn": "NYMEX.NG",
                  "dtf": "1",
                  "tmf": "1",
                  "MSOR": "1",
                  "mstimever": "0",
                  "sep": "1",
                  "sep2": "1",
                  "datf": "6",
                  "at": "1",
                  "fsp": "0",  # s/b "1"?
                  }
        url = "http://195.128.78.52/export9.out"
        data = self.session.get(url, params=params, allow_redirects=True)

        # write to csv
        split_data = data.text.splitlines()
        with open(params["f"] + params["e"], "w", newline="") as f_out:
            csv_writer = csv.writer(f_out, delimiter=",", quoting=csv.QUOTE_NONE)
            for row in split_data[0:20]:
                csv_writer.writerow(row.split(","))