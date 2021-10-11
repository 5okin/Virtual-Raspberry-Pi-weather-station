import random
import json
import time
from datetime import datetime
from requests import put
from selection_menus import select_operating_mode, server_ip_address


def percentage(new, old):
    '''Check if numbers are within 10% of eachother (old value ±10%)'''
    return bool(not (old - old * 10 / 100.0) <= new <= (old + old * 10 / 100.0))
    #return False


def weather_station():
    '''Create random weather data'''

    temp_min = 30       #Temperature range in Celsius
    temp_max = 45

    airhum_min = 40     #Air humidity range in percentage
    airhum_max = 90

    grdhum_min = 60     #Ground humidity range in percentage
    grdhum_max = 70

    wind_min = 0        #Wind speed in Km/h
    wind_max = 10

    measurment = {
        "temperature": random.randrange(temp_min * 10, temp_max * 10)/10,
        "air-humidity": random.randrange(airhum_min, airhum_max),
        "ground-humidity": random.randrange(grdhum_min, grdhum_max),
        "windspeed": random.randrange(wind_min, wind_max),
        "time": datetime.now().strftime("%H:%M:%S"),    #Log current time
    }
    return measurment


def more_than_10_percent(last_send_data, current_measurment):
    '''Check if data current measurment is 10% different than last send data'''

    if not last_send_data:
        return True
    else:
        for data in current_measurment:
            if data != 'time' and data != 'sensor-id':
                if percentage(current_measurment[data], last_send_data[data]):
                    print(data)
                    print("compaired " + str(current_measurment) + " with " + str(last_send_data))
                    return True


def five_minute_passed(time_last_send):
    '''Checks if 5min have passed'''

    time_last_send = time_last_send['time']
    time_now = datetime.now().strftime("%H:%M:%S")
    tdelta = datetime.strptime(time_now, '%H:%M:%S') - datetime.strptime(time_last_send, '%H:%M:%S')

    if tdelta.seconds >= 300:
        print("SEND CAUSE TIME PASSED")
        return True


def fake_data_from_json(i):
    '''Imports measurments from .json file named fake_weather for testing'''
    with open('./fake_weather.json') as json_file:
        data = json.load(json_file)

    data[i]['time'] = datetime.now().strftime("%H:%M:%S")
    return data[i], len(data)


def main(url, mode):
    '''Main function runs selected mode'''

    last_send = {}
    curr_measurement = {}

    i = 0
    while True:
        if mode is "json":
            if i < fake_data_from_json(i)[1]-1:
                curr_measurement = fake_data_from_json(i)[0]
            else:
                print("\nTesting over\n")
                break
            i += 1
        else:
            curr_measurement = weather_station()
        print("Current sensor value is: " + str(curr_measurement))

        if more_than_10_percent(last_send, curr_measurement) or five_minute_passed(last_send):
            last_send = curr_measurement.copy()
            print("Send: " + str(last_send) + "\n")
            try:
                put(url=url, json=json.dumps(last_send))
            except:
                print("ERROR: Lost connection with server\nmake sure server is still running.")
                break
        time.sleep(30)


if __name__ == "__main__":
    URL = server_ip_address()

    if select_operating_mode():
        print("IMPORT FROM JSON")
        main(URL, "json")
    else:
        print("GENERATE RANDOM DATA")
        main(URL, "random")
