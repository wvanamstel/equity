from cassandra.cqlengine.models import Model
from cassandra.cqlengine import columns


class BaseModel(Model):
    __keyspace__ = "tickdata"
    __options__ = {"compaction": "LeveledCompactionStrategy",
                   "sstable_size_in_mb": "64"}
    __abstract__ = True


class Forex(BaseModel):
    forex_pair = columns.Text(primary_key=True)
    tick_time = columns.Time(primary_key=True)
    bid = columns.Text()
    ask = columns.Text()
