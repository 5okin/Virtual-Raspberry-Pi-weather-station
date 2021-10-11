import time
from datetime import datetime
from .weather_mail import send_mail


def percentage(old, new, operator, percent):
    '''Check if numbers are within range'''

    if operator == '+':
        return bool(round((old + old * percent / 100.0), 1) == new)
    elif operator == '-':
        return bool(round((old - old * percent / 100.0)) == new)


def process(data):
    '''Check incoming data for +40% temp and -50% ground humidity'''

    if len(data) > 0:
        latest_measurement = data[len(data)-1]

        for measurement in data:
            if measurement != data[len(data)-1]:
                tdelta = datetime.strptime(latest_measurement['time'], '%H:%M:%S') - datetime.strptime(measurement['time'], '%H:%M:%S')
                if tdelta.seconds < 300:
                    if percentage(measurement['temperature'], latest_measurement['temperature'], '+', 40) and percentage(measurement['air-humidity'], latest_measurement['air-humidity'], '-', 50):
                        send_mail(measurement['temperature'], latest_measurement['temperature'], measurement['air-humidity'], latest_measurement['air-humidity'])
                else:
                    data.remove(measurement)
