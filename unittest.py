from datemanager import DateManager
from roommanager import RoomManager
from hotelregister import HotelRegister
from db import MGClient

#Receipt parameters
hotel_receipt = {
"start_date":"01-01-2017",
"end_date":"02-02-2017",
"hotel_type":0, 
"room_size":0,
"price":0,
"stay_date":0
}

if __name__ == "__main__":
    dateManager = DateManager()
    roomManager = RoomManager()
    hotelRegister = HotelRegister()
    print(dateManager.handle_date(hotel_receipt))
    mgclient = MGClient()
    output = mgclient.get_output()
