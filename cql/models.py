from cassandra.cqlengine.models import Model
from cassandra.cqlengine import columns


class BaseModel(Model):
    __keyspace__ = "tickdata"
    __options__ = {"compaction": {"class": "LeveledCompactionStrategy"}}
    __abstract__ = True


class Forex(BaseModel):
    forex_pair = columns.Text(primary_key=True)
    tick_time = columns.DateTime(primary_key=True)
    date = columns.Date(partition_key=True)
    bid = columns.Float()
    ask = columns.Float()
