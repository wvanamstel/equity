import multiprocessing as mp
import glob
import os
from scripts.get_forex import GetForex
from cql.cluster import CqlClient
from cql.models import Forex


class MultiProc(object):
    def __init__(self, num_workers=None):
        self.gf = GetForex(cass_conn=False)
        self.months = ["01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11", "12"]
        self.file_names = self.fetch_file_names(mask="*-2015-12.csv")
        if num_workers is None:
            num_workers = len(self.file_names)
        self.pool = mp.Pool(processes=num_workers, initializer=self.start_process)

    @staticmethod
    def fetch_file_names(mask):
        file_path = os.path.expanduser("~") + "/data/forex/"
        return glob.glob(file_path + mask)

    @classmethod
    def start_process(cls):
        print("Starting process {}".format(mp.current_process().name))
        CqlClient(Forex, check_active=False)

    def do_insert(self):
        self.pool.map(self.gf.insert_cassandra, self.file_names)

    def close_pool(self):
        print("Closing pool")
        self.pool.close()
        self.pool.join()

multi=MultiProc()
multi.do_insert()
multi.close_pool()

