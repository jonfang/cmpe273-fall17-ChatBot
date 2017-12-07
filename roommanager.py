from hotel import Hotel

class RoomManager:
    """
       Manage and calculate date/time
    """
    def __init__(self):
        pass

    def book_hotel(self, receipt, s):
        arr = s.split(" ")
        receipt["hotel_type"] = arr[1]
        msg = "Thank you! You will be staying at " + arr[1]
        return msg

    def book_room(self, receipt, s, hotels):
        """
        Set the room type and check if the room has been booked
        """
        arr = s.split(" ")
        room_type = arr[1]
        if room_type not in ['single', 'double', 'luxury']:
            return "Wrong room type, please choose single, double or luxury"
        receipt["room_type"] = arr[1]
        hotel_type = hotels[receipt["hotel_type"]]
        start_date = receipt["start_date"].split("-")
        end_date = receipt["end_date"].split("-")
        start = ""
        end = "" 
        for s in start_date:
            start+=s
        for e in end_date:
            end+=e
        start = int(start)
        end = int(end)
        state, msg = hotel_type.book_room(start, end, room_type)
        msg = msg + " between "+ receipt["start_date"] +" and "+ receipt["end_date"] +" at " + hotel_type.get_name() + ". Please provide your name to checkout."
        return msg
