from sqlalchemy import create_engine, ForeignKey
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String
from sqlalchemy.types import Date, JSON, Time


engine = create_engine('sqlite:///db')

Session = sessionmaker(bind=engine)

Base = declarative_base()


def setup_db():
    try:
        Base.metadata.drop_all(engine)
    except:
        pass

    Base.metadata.create_all(engine)


class Track(Base):
    __tablename__ = 'track'

    id = Column(Integer, primary_key=True)

    name = Column(String)
    country = Column(String)
    abv = Column(Integer)

    races = relationship('Race', back_populates="track")

    def __repr__(self):
        return "%s(%s)/%s"%(self.name, self.abv, self.country)

class Horse(Base):
    __tablename__ = 'horse'

    id = Column(Integer, primary_key=True)

    name = Column(String, nullable=False)
    country = Column(String, default='US', nullable=False)

    __table_args__ = (UniqueConstraint('name', 'country', name='unique_horse'),)


class Jockey(Base):
    __tablename__ = 'jockey'

    id = Column(Integer, primary_key=True)

    name = Column(String)

    __table_args__ = (UniqueConstraint('name', name='unique_jockey'),)

class Race(Base):
    __tablename__ = 'race'

    id = Column(Integer, primary_key=True)

    track_id = Column(Integer, ForeignKey('track.id'))
    track = relationship('Track', back_populates="races")
    date = Column(Date)
    race_number = Column(Integer)
    race_type = Column(Integer)
    registered = Column(String)
    sex = Column(Integer)
    age = Column(Integer)

    surface = Column(Integer)
    distance = Column(Integer)
    desc = Column(String)
    code = Column(String)

    claiming_price = Column(Integer)
    purse = Column(Integer)
    plus = Column(JSON)
    available_money = Column(JSON)
    value_of_race = Column(JSON)
    weather = Column(Integer)
    track_speed = Column(Integer)
    off_at = Column(Time)
#    start = Column(Integer)

    entries = relationship('RaceEntry', back_populates="race")

    def __repr__(self):
        return "%s - %s - %s"%(self.track, self.date, self.race_number)

class RaceEntry(Base):
    __tablename__ = 'race_entry'

    id = Column(Integer, primary_key=True)

    race_id = Column(Integer, ForeignKey('race.id'))
    race = relationship('Race', back_populates="entries")

    last_raced = Column(String)
    track_raced = Column(JSON)

    pgmn = Column(String)

    horse = relationship('Horse', back_populates="entries")
    jockey = relationship('Jockey', back_populates="entries")
   
    weight = Column(Integer)
    m_e = Column(String)

    pp = Column(Integer)

    result = relationship('RaceEntryResult', back_populates="race_entry")

    def __repr__(self):
        return "%s (%s)"%(self.horse_name, self.jockey_name)

class RaceEntryResult(Base):
    __tablename__ = 'race_entry_result'

    id = Column(Integer, primary_key=True)

    race_entry_id = Column(Integer, ForeignKey('race_entry.id'))
    race_entry = relationship('RaceEntry', back_populates="result")

    start = Column(Integer)

    quick_pos = Column(Integer)
    quick_behind = Column(Integer)

    quart_pos = Column(Integer)
    quart_behind = Column(Integer)

    quack_pos = Column(Integer)
    quack_behind = Column(Integer)

    half_pos = Column(Integer)
    half_behind = Column(Integer)

    last_quart_pos = Column(Integer)
    last_quart_behind = Column(Integer)

    mile_pos = Column(Integer)
    mile_behind = Column(Integer)

    mile_frth_pos = Column(Integer)
    mile_frth_behind = Column(Integer)

    str_pos = Column(Integer)
    str_behind = Column(Integer)

    fin_pos = Column(Integer)
    fin_behind = Column(Integer)
