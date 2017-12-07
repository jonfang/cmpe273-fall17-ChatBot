
class Hotel:
    def __init__(self, name, s, d, l):
        self.name = name
        self.dates = {}
        self.types = {"single": s, "double": d, "luxury": l}

    def get_name(self):
        return self.name

    def book_room(self, start, end, room_type):
        booked = True
        while end >= start:
            booked = booked and self.single_book(end, room_type)
            if booked is False:
                msg = "Sorry, this " + room_type + " room has been booked in this time frame"
                return booked, msg
            end-=1
        msg = "Thank you! This " + room_type +  " room is booked"
        return booked, msg

    def single_book(self, date, room_type):
        if date not in self.dates:
            self.dates[date] = {}
        if room_type not in self.dates[date]:
            self.dates[date][room_type] = 0

        if self.dates[date][room_type] < self.types[room_type]:
            self.dates[date][room_type]+=1
            #print(date , ": " , "Booked")
            return True
        else:
            #print(date , ": " , "No room available")
            return False
