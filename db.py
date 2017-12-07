from pymongo import MongoClient

class MGClient:
   def  __init__(self):
       self.client = MongoClient('mongodb://testbot:test123@ds129946.mlab.com:29946')
       self.db = self.client['hotel_booking']
       self.collection = self.db['records']
       self.recCol = self.collection.find({})
       print('\n All data from BookingData Database \n')

   def get_output(self):
       output = ""
       for rec in self.recCol:
           output+=rec
       return output
