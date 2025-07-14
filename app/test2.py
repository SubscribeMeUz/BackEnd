from pydantic import BaseModel


class MyModel(BaseModel):
    id: int
    name: str


dc = {
    'id': 12,
    'name': "Name"
}

"""
eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpYXQiOjE3NDkwOTg4MDMsInVzZXJuYW1lIjoiYWRtaW4ifQ.VMSLjdLk1wH2N8wqZOpAPxY_txlBHtB2Jl8iSr0JNC4

"""

from geopy.geocoders import Nominatim
import time

def get_location_name(lat: float, lon: float) -> str:
    geolocator = Nominatim(user_agent="u.shermetov11197@gmail.com")
    location = geolocator.reverse((lat, lon), language='en')
    if location:
        return location.address
    return "Unknown location"


arr = [
    (41.314684         , 69.298592),
    (41.317349         , 69.272615),
    (41.314684         , 69.298592),
    (41.30355464313827 , 69.24476925281206),
    (41.317349         , 69.272615),
    (41.317349         , 69.272615),
    (41.311783         , 69.276104),
    (41.311783         , 69.276104),
]

for latt, long in arr:
    time.sleep(3)
    print(get_location_name(latt, long))

"""
UPDATE providers SET location_name='Magic City, 174, Babur Street, Dustlik mahalla, Yakkasaray District, Tashkent, 100000, Uzbekistan' WHERE id=4;
UPDATE providers SET location_name='Magic City, 174, Babur Street, Dustlik mahalla, Yakkasaray District, Tashkent, 100000, Uzbekistan' WHERE id=2;
UPDATE providers SET location_name='Magic City, 174, Babur Street, Dustlik mahalla, Yakkasaray District, Tashkent, 100000, Uzbekistan' WHERE id=7;
UPDATE providers SET location_name='Бюро переводов "Respect", Buyuk Turan Street, Kashgar (C-4), Yunusabad district, Tashkent, 100084, Uzbekistan' WHERE id=5;
UPDATE providers SET location_name='Бюро переводов "Respect", Buyuk Turan Street, Kashgar (C-4), Yunusabad district, Tashkent, 100084, Uzbekistan' WHERE id=6;
UPDATE providers SET location_name='Yunusabad district, Tashkent, 100084, Uzbekistan' WHERE id=8;
UPDATE providers SET location_name='Yunusabad district, Tashkent, 100084, Uzbekistan' WHERE id=9;

"""
