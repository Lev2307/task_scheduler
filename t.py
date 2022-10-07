from datetime import datetime

date_time_str = '2022-10-07'

d = datetime.strptime(date_time_str, '%Y-%m-%d')
print(d.date())