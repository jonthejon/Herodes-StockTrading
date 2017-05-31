import csv
import datetime as dt

def get_BOV_days(dt_start,dt_end):
    filename = "pythonfiles/calend/calend_Bovespa.csv"
    reader = csv.reader(open(filename,'rU'),delimiter=',')
    dates = []

    for row in reader:
        date = dt.datetime(int(row[0]),int(row[1]),int(row[2]))
        if date >= dt_start and date <= dt_end:
            date = date + dt.timedelta(hours=16)
            dates.append(date)
        
    dates = sorted(dates)
    return dates
