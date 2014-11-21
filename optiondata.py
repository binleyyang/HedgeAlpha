from pandas.io.data import Options
import datetime

aapl = Options('AAPL', 'yahoo')
expiry = datetime.date(2014, 5, 1)
aapl.get_call_data(expiry=expiry)

