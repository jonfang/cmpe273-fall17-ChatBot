import os
import time
from slackclient import SlackClient
from datemanager import DateManager
from roommanager import RoomManager
from hotelregister import HotelRegister
from hotel import Hotel
from nlprocessor import NLProcessor

#Set up environment parameters
SLACK_BOT_TOKEN='masked-for-security-reason'
BOT_ID = 'U7V9S77V2'

# constants
AT_BOT = "<@" + BOT_ID + ">"
EXAMPLE_COMMAND = ["hi", "list", "reserve", "set_start_date", "set_end_date", "calculate_date", "book_hotel", "book_room","checkout", "receipt"]

EXAMPLE_COMMAND_DETAILS = [
"-hi: Introduction",
"-list: List available options",
"-reserve: Prompts to book a hotel",
"-set_start_date xx-xx-xxxx: set start date with month, day, and year",
"-set_end_date xx-xx-xxxx: set end date with month, day, and year",
"-calculate_date: calculate total sum of day to stay",
"-book_hotel hotel_type: book a type of hotel",
"-book_room room_type: book a room size",
"-checkout name: calculate the total price and print receipt",
"-receipt: Show current receipt"
]

#Receipt parameters
hotel_receipt = {
"start_date":"12-05-2017",
"end_date":"12-15-2017", 
"hotel_type":"hotela",
"room_type":"luxury",
"stay_date":10,
"name":"Jon",
"price":0
}

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

# instantiate Slack & Twilio clients
slack_client = SlackClient(SLACK_BOT_TOKEN)

class HotelBot:
    """
        Hotel Bot class that handles commands at the high level
    """
    def __init__(self):
        self.dateManager = DateManager()
        self.roomManager = RoomManager()
        self.hotelRegister = HotelRegister()
        self.hotels = {}
        self.nlp = NLProcessor()
        self.skipOwn = False #skip self message to avoid loop
        for h in hotel_list.keys():
            self.hotels[h] = Hotel(h, 10, 5, 2)

    def handle_command(self, command, channel):
        """
        Receive user input, use natural language processor to process input and
        convert into hotelbot commands
        """
        if self.skipOwn == True:
            self.skipOwn = False
            return
        command = self.nlp.process(command)
        #print(command)
        if any(command.startswith(s) for s in EXAMPLE_COMMAND):
            response = "" 
            if command.startswith('hi'):
                response = "Hello! I am Hotel Bot. What can I do for you?"
            elif command.startswith('list'):
                response = "Hotel bot is ready. Below are the list of commands:\n" + "\n".join(EXAMPLE_COMMAND_DETAILS)
            elif command.startswith('reserve'):
                response = "Great! Please let me know what day you want to check in?"
            elif command.startswith('set_start_date'):
                msg = self.dateManager.set_start_date(hotel_receipt, command) + ". Please let me know what day you want to check out?"
                response = msg
            elif command.startswith('set_end_date'):
                msg = self.dateManager.set_end_date(hotel_receipt, command) + ".Please pick a hotel. We have " + ','.join(['%s:$%s' % (key, value) for (key, value) in hotel_list.items()])
                response = msg
            elif command.startswith('calculate_date'):
                msg = self.dateManager.calculate_date(hotel_receipt)
                response = msg
            elif command.startswith('book_hotel'):
                msg = self.roomManager.book_hotel(hotel_receipt, command)
                response = msg + ".Please pick a room type. We have " + ','.join(['%s:$%s' % (key, value) for (key, value) in room_list.items()])
            elif command.startswith('book_room'):
                msg = self.roomManager.book_room(hotel_receipt, command, self.hotels)
                response = msg
            elif command.startswith('checkout'):
                response = self.hotelRegister.checkout(hotel_receipt, command) + "\n" + self.format_receipt(hotel_receipt)
            elif command.startswith('receipt'):
                response = self.format_receipt(hotel_receipt)
            else:
                response = "Sure...write some more code then I can do that!"
            self.skipOwn = True
            slack_client.api_call("chat.postMessage", channel=channel,
                          text=response, as_user=True)

    def format_receipt(self, receipt):
        response = ""
        pair = "Name" + " : " + receipt["name"] + "\n"
        response+=pair
        pair = "From" + " : " + receipt["start_date"] + "\n"
        response+=pair
        pair = "To" + " : " + receipt["end_date"] + "\n"
        response+=pair
        pair = "Hotel" + " : " + receipt["hotel_type"] + "\n"
        response+=pair
        pair = "Room size" + " : " + receipt["room_type"] + "\n"
        response+=pair
        pair = "Price" + " : " + "$" + str(receipt["price"]) + "\n"
        response+=pair
        return response

def parse_slack_output(slack_rtm_output):
    """
        The Slack Real Time Messaging API is an events firehose.
        this parsing function returns None unless a message is
        directed at the Bot, based on its ID.
    """
    output_list = slack_rtm_output
    if output_list and len(output_list) > 0:
        for output in output_list:
            #if output and 'text' in output and AT_BOT in output['text']:
            if output and 'text' in output:
                # return text after the @ mention, whitespace removed
                #return output['text'].split(AT_BOT)[1].strip().lower(), \
                       #output['channel']
                return output['text'], output['channel']
    return None, None

if __name__ == "__main__":
    READ_WEBSOCKET_DELAY = 1 # 1 second delay between reading from firehose
    if slack_client.rtm_connect():
        hotelBot = HotelBot()
        print("HotelBot connected and running!")
        while True:
            command, channel = parse_slack_output(slack_client.rtm_read())
            if command and channel:
                hotelBot.handle_command(command, channel)
            time.sleep(READ_WEBSOCKET_DELAY)
    else:
        print("Connection failed. Invalid Slack token or bot ID?")
