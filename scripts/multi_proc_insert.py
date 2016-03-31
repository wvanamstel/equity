import multiprocessing as mp
import glob
from scripts.get_forex import GetForex


def fetch_file_names(mask):
    file_path = "/home/w/data/forex/"
    return glob.glob(file_path + mask)


def start_process():
    print("Starting process {}".format(mp.current_process().name))

if __name__ == "__main__":
    gf = GetForex()
    jobs = []
    files = fetch_file_names(mask="*-2016-02.csv")
    pool = mp.Pool(mp.cpu_count()*2, initializer=start_process)
    pool.map(gf.insert_cassandra, files)
    pool.close()
    pool.join()
    # for file in files:
    #     p = mp.Process(target=gf.insert_cassandra, args=(file,))
    #     jobs.append(p)
    #     p.start()
        # self.start_process()