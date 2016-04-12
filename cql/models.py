from cassandra.cqlengine.models import Model
from cassandra.cqlengine import columns


class BaseModel(Model):
    __keyspace__ = "tickdata"
    __options__ = {"compaction": {"class": "LeveledCompactionStrategy"}}
    __abstract__ = True


class MinuteModel(Model):
    __keyspace__ = "minutedata"
    __options__ = {"compaction": {"class": "LeveledCompactionStrategy"}}
    ticker = columns.Text(partition_key=True)
    date = columns.Date(primary_key=True)
    time = columns.DateTime(primary_key=True)
    open = columns.Double()
    high = columns.Double()
    low = columns.Double()
    close = columns.Double()
    volume = columns.SmallInt()


class Forex(BaseModel):
    forex_pair = columns.Text(partition_key=True)
    date = columns.Date(primary_key=True)
    tick_time = columns.DateTime(primary_key=True)
    bid = columns.Double()  # Considered using Decimal, for space considerations use double
    ask = columns.Double()


class FuturesTicks(BaseModel):
    ticker = columns.Text(partition_key=True)
    date = columns.Date(primary_key=True)
    tick_time = columns.DateTime(primary_key=True)
    last = columns.Double()
    volume = columns.SmallInt()


class FuturesMins(MinuteModel):
    pass


class EquitiesMins(MinuteModel):
    pass