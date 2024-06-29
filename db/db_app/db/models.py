from sqlalchemy import Column, Integer, String, Float
from db_app.db.database import Base


class Currency(Base):
    __tablename__ = "currencies"

    id = Column(Integer, primary_key=True, index=True)
    num_code = Column(String)
    char_code = Column(String, index=True)
    nominal = Column(Integer)
    name = Column(String)
    value = Column(Float)
    unit_rate = Column(Float)
