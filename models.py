import pandas as pd
from datetime import datetime


class EventRegistration:
    def __init__(self, date: str, on: str, organization_id: str, data: list = None) -> None:
        self.date = date
        self.on = on
        self.organization_id = organization_id
        self.data = data

    def to_json(self):
        return {
            "date": self.date,
            "on": self.on,
            "organization_id": self.organization_id,
            "data": [instance.to_json() for instance in self.data]
        }


class EventUpdate:
    def __init__(self, date: str, id: str, register_at: datetime, deregister_at: datetime, location: list = None) -> None:
        self.id = id
        self.register_at = register_at
        self.deregister_at = deregister_at
        self.location = location

    def to_json(self):
        return {
            "id": self.id,
            "register_at": self.register_at,
            "deregister_at": self.deregister_at,
            "location": [instance.to_json() for instance in self.location]
        }


class LocationUpdate:
    def __init__(self, id: str, lat: float, lng: float, at: str) -> None:
        self.id = id
        self.lat = lat
        self.lng = lng
        self.at = at

    def to_json(self):
        return {
            "lat": self.lat,
            "lng": self.lng,
            "at": self.at
        }
