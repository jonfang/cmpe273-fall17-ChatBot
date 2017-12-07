#hotel & room info
hotel_list = {
"hotela" : 200,
"hotelb" : 250,
"hotelc" : 300
}

room_list = {
"single" : 100,
"double" : 200,
"luxury" : 350
}

class HotelRegister:
    """
       Manage and calculate date/time
    """
    def __init__(self):
        pass

    def checkout(self, receipt, s):
        arr = s.split(" ")
        #calculate result here
        name = arr[1]
        receipt["name"] = name
        price = 0
        unit_price = hotel_list[receipt["hotel_type"]] + room_list[receipt["room_type"]]
        price = unit_price*receipt["stay_date"]
        receipt["price"] = price
        msg =  "Thank you for booking! " + name + ". Your total is $" + str(price) + ". Below is the receipt:"
        return msg
