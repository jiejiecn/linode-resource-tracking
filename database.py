from sqlalchemy import create_engine, text
from sqlalchemy import Column, Integer, String, Numeric, Boolean, DateTime, BigInteger
from sqlalchemy import func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
import config

Base = declarative_base()

class InstanceTraffic(Base):
    __tablename__ = "instancetraffic"

    id = Column(Integer, primary_key=True, autoincrement=True)
    linode_id = Column(Integer, nullable=False, index=True)
    linode_label = Column(String(50), index=True)
    dataCenter = Column(String(20), nullable=False, index=True)
    publicIp = Column(String(20), nullable=False)
    instanceType = Column(String(20), nullable=False)
    traffic_usage = Column(Numeric(20))
    traffic_usage_GB = Column(Numeric(20, 4))
    traffic_quota = Column(Numeric(20))
    traffic_billable = Column(Numeric(20))
    traffic_billable_GB = Column(Numeric(20, 4))

    createDt = Column(DateTime, server_default=func.now())
    updateDt = Column(DateTime, server_default=func.now(), onupdate=func.now())



engine = create_engine(config.db_string, echo=True, pool_size=8)

Base.metadata.create_all(engine)

session = sessionmaker(bind=engine)
db = session()