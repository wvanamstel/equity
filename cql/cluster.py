from cassandra.cluster import Cluster

class CqlClient(object):
    def __init__(self):
        self.session = None

    def connect(self, nodes):
        clus = Cluster(nodes)
        self.session = clus.connect()

    def close(self):
        self.session.close()
