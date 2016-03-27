import requests
import zipfile


def download_files():
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


def insert_cassandra():
    with open("~/data/forex/USDJPY-2016-02.csv", "r") as f:
        for line in f:
            print(line)
