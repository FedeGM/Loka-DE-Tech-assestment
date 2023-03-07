from sqlalchemy import Column, Date, Integer, Float, String, DateTime, ForeignKey, func
from sqlalchemy.orm import relationship
from datetime import datetime

from database import Base, engine

model_schema = 'loka'

###### Defining the Classes for MySQL database ######

class EventRegistration(Base):
    __tablename__ = "event_registrations"
    __table_args__ = {'schema': model_schema}
    event = Column(String(100))
    on = Column(String(100))
    id = Column(String(255), primary_key = True)
    register_at = Column(DateTime())
    deregister_at = Column(DateTime())
    organization_id = Column(String(250))
    snapshot = Column(Date(), default = func.now() )
    eventUpdate = relationship("EventUpdate", back_populates= "eventRegistration" )

    def __init__(self, event: str, on: str, id: str, register_at: str, deregister_at: str, organization_id: str) -> None:
        self.event = event
        self.on = on
        self.id = id
        self.register_at = datetime.strptime(register_at, '%Y-%m-%dT%H:%M:%S.%f%z') if register_at else None
        self.deregister_at = datetime.strptime(deregister_at, '%Y-%m-%dT%H:%M:%S.%f%z') if deregister_at else None
        self.organization_id = organization_id

    def to_json(self):
        return {
            "event": self.event,
            "on": self.on,
            "id": self.id,
            "register_at": self.register_at,
            "deregister_at": self.deregister_at,
            "organization_id": self.organization_id
        }


class EventUpdate(Base):
    __tablename__ = "event_updates"
    __table_args__ = {'schema': model_schema}
    event_id = Column(Integer, primary_key = True)
    id = Column(String(255), ForeignKey(f"{model_schema}.event_registrations.id"))
    latitud = Column(Float)
    longitud = Column(Float)
    at = Column(DateTime())
    eventRegistration = relationship("EventRegistration", back_populates= "eventUpdate")

    def __init__(self, id: str, lat: float, lng: float, at: str) -> None:
        self.id = id
        self.latitud = lat
        self.longitud = lng
        self.at = datetime.strptime(at, '%Y-%m-%dT%H:%M:%S.%f%z') if at else None

    def to_json(self):
        return {
            "id": self.id,
            "lat": self.lat,
            "lng": self.lng,
            "at": self.at
        }

###### Defining the Classes to process the data ###### 

class Register:
    def __init__(self, id: str, register_at: str) -> None:
        self.id = id
        self.register_at = register_at

    def to_json(self):
        return {
            "id": self.id,
            "register_at": self.register_at
        }

class Deregister:
    def __init__(self, id: str, deregister_at: str) -> None:
        self.id = id
        self.deregister_at = deregister_at
    
    def to_json(self):
        return {
            "id": self.id,
            "deregister_at": self.deregister_at
        }