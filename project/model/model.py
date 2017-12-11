# Configuration
import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String, Boolean
from sqlalchemy import DateTime, Boolean, Enum, Float, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from connect import connect

Base = declarative_base()


def dump_datetime(value):
    """Deserialize datetime object into string for JSON processing"""
    if value is None:
        return None
    return [value.strftime("%Y-%m-%d"), value.strftime("%H:%M:%S")]


class Blog(Base):
    __tablename__ = 'blog'
    pid = Column(Integer, primary_key=True)
    bid = Column(Integer)
    title = Column(String(80), nullable=False)
    author = Column(String(80), nullable=False)
    date_time = Column(DateTime)
    category = Column('blog_cat',
                       Enum('general',
                            'travel',
                            'crafting',
                            'baking',
                            name = 'blog_cat'))
    content = Column(String)
    hidden = Column(Boolean)

con = connect()
Base.metadata.create_all(con)
