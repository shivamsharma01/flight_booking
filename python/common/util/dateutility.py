import dateutil.parser
from datetime import datetime

class DateUtility:

    # utility function for date. Returns only date part
    @staticmethod
    def date_converter(date):
        return dateutil.parser.parse(date).date()
    
    # validation function for date
    @staticmethod
    def is_past_date(date):
        return date < datetime.now().date()