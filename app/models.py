from sqlalchemy import Column, String, Integer
from database import Base



class AlgorithmModel(Base):
    __tablename__ = "task_algorithmmodel"
    id = Column(Integer, primary_key=True)
    text = Column(String)
    label = Column(String)