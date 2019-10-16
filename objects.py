from sqlalchemy import create_engine, ForeignKey, UniqueConstraint
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
    result = relationship('RaceResult', back_populates="race")

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

    horse_id = Column(Integer, ForeignKey('horse.id'))
    horse = relationship('Horse', back_populates="entries")
    jockey_id = Column(Integer, ForeignKey('jockey.id'))
    jockey = relationship('Jockey', back_populates="entries")
   
    weight = Column(Integer)
    m_e = Column(String)

    pp = Column(Integer)

    result = relationship('RaceEntryResult', back_populates="race_entry")

    def __repr__(self):
        return "%s-%s (%s)"%(self.pgmn, self.horse.name, self.jockey.name)

class Horse(Base):
    __tablename__ = 'horse'

    id = Column(Integer, primary_key=True)

    name = Column(String, nullable=False)
    country = Column(String, default='US', nullable=False)

    entries = relationship('RaceEntry', back_populates="horse")

    __table_args__ = (UniqueConstraint('name', 'country', name='unique_horse'),)

    def __repr__(self):
        return "%s(%s)"%(self.name, self.country)


class Jockey(Base):
    __tablename__ = 'jockey'

    id = Column(Integer, primary_key=True)

    name = Column(String)

    entries = relationship('RaceEntry', back_populates="jockey")

    __table_args__ = (UniqueConstraint('name', name='unique_jockey'),)

    def __repr__(self):
        return "%s"%(self.name)



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

    def __repr__(self):
        _str = ""
        if self.quick_pos:
            _str += "3/16=%s,%s "%(self.quick_pos, self.quick_behind)
        if self.quart_pos:
            _str += "1/4=%s,%s "%(self.quart_pos, self.quart_behind)
        if self.quack_pos:
            _str += "3/8=%s,%s "%(self.quack_pos, self.quack_behind)
        if self.half_pos:
            _str += "1/2=%s,%s "%(self.half_pos, self.half_behind)
        if self.last_quart_pos:
            _str += "3/4=%s,%s "%(self.last_quart_pos, 
                    self.last_quart_behind)
        if self.mile_pos:
            _str += "1=%s,%s "%(self.mile_pos, self.mile_behind)
        if self.mile_frth_pos:
            _str += "1 1/4=%s,%s "%(self.mile_frth_pos, 
                    self.mile_frth_behind)
        if self.str_pos:
            _str += "Str=%s,%s "%(self.str_pos, self.str_behind)
        if self.fin_pos:
            _str += "Fin=%s,%s "%(self.fin_pos, self.fin_behind)

        return _str


class RaceResult(Base):
    __tablename__ = 'race_result'

    id = Column(Integer, primary_key=True)

    race_id = Column(Integer, ForeignKey('race.id'))
    race = relationship('Race', back_populates="result")

    first_call = Column(Integer)
    second_call = Column(Integer)
    third_call = Column(Integer)
    fourth_call = Column(Integer)
    fifth_call = Column(Integer)
    final_call = Column(Integer)

    def __repr__(self):
        _str = ""
        if self.first_call:
            _str += "1st=%s "%(self.first_call)
        if self.second_call:
            _str += "2nd=%s "%(self.second_call)
        if self.third_call:
            _str += "3rd=%s "%(self.third_call)
        if self.fourth_call:
            _str += "4th=%s "%(self.fourth_call)
        if self.fifth_call:
            _str += "5th=%s "%(self.fifth_call)
        if self.final_call:
            _str += "final=%s "%(self.final_call)

        return _str
