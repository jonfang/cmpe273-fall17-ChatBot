from datetime import date
"""
def g(y,m,d):
    y=int(y)
    m=int(m)
    d=int(d)
    m = (m + 9) % 12
    y = y - m/10
    return 365*y + y/4 - y/100 + y/400 + (m*306 + 5)/10 + ( d - 1 )

"""
class DateManager:
    """
       Manage and calculate date/time
    """
    def __init__(self):
        pass

    def set_start_date(self, receipt, s):
        arr = s.split(" ")
        receipt["start_date"] = arr[1]
        msg = "Thank you! Your check in date will be " + arr[1]
        return msg

    def set_end_date(self, receipt, s):
        arr = s.split(" ")
        receipt["end_date"] = arr[1]
        msg = "Thank you! Your check out date will be " + arr[1] + "."
        msg = msg + " " + self.calculate_date(receipt)
        return msg

    def calculate_date(self, receipt):
        """
        Calculate how many days will be stayed
        """
        stay_date = 0
        start_date = receipt["start_date"].split("-")
        end_date = receipt["end_date"].split("-")
        e_y = int(end_date[2])
        e_m = int(end_date[0])
        e_d = int(end_date[1])
        s_y = int(start_date[2])
        s_m = int(start_date[0])
        s_d = int(start_date[1])
        print(e_y, ":", e_m , ":" , e_d)
        print(s_y, ":", s_m , ":" , s_d)
        stay_date = int((date(e_y, e_m, e_d) - date(s_y, s_m, s_d)).days)
        receipt['stay_date'] = stay_date
        msg = "You will be staying for " + str(stay_date) + " days"
        return msg
