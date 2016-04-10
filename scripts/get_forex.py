import requests
import zipfile
import datetime as dt
import csv
import calendar

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

    def download_files(self, asset, dates, resolution=None):
        """
        download tick data and serialise to csv
        :param asset: string of asset name
        :param dates: dict
        :param resolution: string mins
        :return: write csv files
        """
        if resolution == "mins":
            res = {"p": "2", "datf": "7", "path": "mins"}
        else:
            res = {"p": "1", "datf": "7", "path": "ticks"}
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
                  "petrol": {"code": "NYMEX.XRB",
                             "em": "18950",
                             "market": "24",
                             },
                  "silver": {"code": "comex.SI",
                             "em": "18952",
                             "market": "24",
                             },
                  "copper": {"code": "LME.cooper",  # sic
                             "em": "18931",
                             "market": "24",
                             },
                  "aluminium": {"code": "LME.Alum",
                                "em": "18930",
                                "market": "24",
                                },
                  "nickel": {"code": "LME.Nickel",
                             "em": "18932",
                             "market": "24",
                             },
                  "tin": {"code": "LME.Tin",
                          "em": "18934",
                          "market": "24",
                          },
                  "palladium": {"code": "NYMEX.PA",
                                "em": "18959",
                                "market": "24",
                                },
                  "platinum": {"code": "NYMEX.PL",
                               "em": "18947",
                               "market": "24",
                               },
                  "lead": {"code": "LME.Lead",
                           "em": "18933",
                           "market": "24",
                           },
                  "zinc": {"code": "LME.Zinc",
                           "em": "18935",
                           "market": "24",
                           },
                  "wheat": {"code": "US3.ZW",
                            "em": "74453",
                            "market": "24",
                            },
                  "sugar": {"code": "US2.ZB",
                            "em": "74454",
                            "market": "24",
                            },
                  "spmini": {"code": "MINISANDP500",
                             "em": "13944",
                             "market": "7",
                             },
                  "sp500": {"code": "SANDP-FUT",  # since 2002
                            "em": "108",
                            "market": "7",
                            },
                  "djmini": {"code": "DANDI.MINIFUT",
                             "em": "21718",
                             "market": "7",
                             },
                  "nq100": {"code": "NQ-100-FUT",
                            "em": "21719",
                            "market": "7",
                            },
                  "dj50": {"code": "DSX",
                           "em": "12997",
                           "market": "7",
                           },
                  "tsy2y": {"code": "CBOT.TU",
                            "em": "18961",
                            "market": "26",
                            },
                  "tsy5y": {"code": "CBOT.FV",
                            "em": "18962",
                            "market": "26",
                            },
                  "tsy10y": {"code": "CBOT.TY",
                             "em": "18960",
                             "market": "26",
                             },
                  "tsy30y": {"code": "CBOT.US",
                             "em": "19474",
                             "market": "26",
                             },
                  }
        params = {"market": assets[asset]["market"],
                  "em": assets[asset]["em"],
                  "code": assets[asset]["code"],
                  "apply": "1",
                  "from": dates["from"],
                  "df": dates["df"],
                  "mf": dates["mf"],
                  "yf": dates["yf"],
                  "dt": dates["dt"],
                  "mt": dates["mt"],
                  "yt": dates["yt"],
                  "to": dates["to"],
                  "p": res["p"],  # 1: tick; 2: 1 min
                  "f": asset + "_" + dates["from"] + "_" + dates["to"],
                  "e": ".csv",
                  "cn": assets[asset]["code"],
                  "dtf": "1",
                  "tmf": "1",
                  "MSOR": "1",
                  "mstimever": "0",
                  "sep": "1", # comma sep
                  "sep2": "1", # newline sep
                  "datf": res["datf"],  # 7: last, 5: OHLCV
                  "at": "1",
                  "fsp": "0",  # s/b "1"?
                  }
        url = "http://195.128.78.52/export9.out"
        data = self.session.get(url, params=params, allow_redirects=True)

        # write to csv
        file_path = "/home/w/data/futures/" + asset + "/" + res["path"] + "/"
        with open(file_path + params["f"] + params["e"], "w", newline="") as f_out:
            csv_writer = csv.writer(f_out, delimiter=",", quoting=csv.QUOTE_NONE)
            for row in data.text.splitlines():
                csv_writer.writerow(row.split(","))

    def get_files(self, assets, years, months=None, resolution=None):
        """
        call this method to start downloading csv files
        :param assets: [string], asset names
        :param years: list of ints, years to download
        :param months: list of ints, specify months, none==all months
        :param resolution: mins or ticks
        :return: calls downloader
        """
        if months is None:
            months = range(1, 13)
        for asset in assets:
            for year in years:
                for month in months:
                    first_day = "1"
                    last_day = str(calendar.monthrange(int(year), month)[1])
                    dates_dict = {"from": first_day + "." + str(month) + "." + str(year),
                                  "to": last_day + "." + str(month) + "." + str(year),
                                  "df": first_day,
                                  "mf": str(month - 1),  #months are 0==jan for some reason
                                  "yf": str(year),
                                  "dt": last_day,
                                  "mt": str(month - 1),
                                  "yt": str(year),
                                  }
                    self.download_files(asset, dates_dict, resolution)