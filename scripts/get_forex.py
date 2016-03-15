import requests
import zipfile


def download_files():
    cur_pairs = ["AUDJPY", "AUDNZD", "AUDUSD", "CADJPY", "CHFJPY", "EURCHF", "EURGBP", "EURJPY", "EURUSD",
                 "GBPJPY", "GBPUSD", "NZDUSD", "USDCAD", "USDCHF", "USDJPY"]
    years = [str(i) for i in range(2010, 2017)]
    months = ["01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11", "12"]
    months_verbose = ["JANUARY", "FEBRUARY", "MARCH", "APRIL", "MAY", "JUNE", "JULY", "AUGUST", "SEPTEMBER",
                      "OCTOBER", "NOVEMBER", "DECEMBER"]
    file_path = "/home/w/data/forex/"
    for year in years:
        for number, month in enumerate(months):
            for pair in cur_pairs:
                file_name = pair + "-" + year + "-" + month + ".zip"
                base_url = "http://www.truefx.com/dev/data/" + year + "/" + months_verbose[number] + "-" + year + "/"
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

download_files()