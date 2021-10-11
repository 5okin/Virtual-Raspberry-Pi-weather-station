# Virtual Raspberry Pi weather station

A virtual weather station that periodically generates temperature, air humidity, ground humidity and wind speed data. It checks the values (locally) and if they differ by more than 10% they are send to server. If data hasn't been send to the server for over five minutes, the current measurements are send.

The server processes the incoming data, if the temperature increased by 40% and the air humidity decreased by 50% within the last five minutes, it sends a email alert to the user. The incoming data is also logged to a database and visualized using grafana.

<br />

## Overview

![Untitled Diagram](https://user-images.githubusercontent.com/70406237/129235542-80138cb9-794f-454d-a99b-b41229bf225b.png)

<br />


## Server architecture

The server is a multi-container Docker app that uses the following:

* [InfluxDB](https://github.com/influxdata/influxdb) - time series database.
* [Python3](https://github.com/python) - Programming language.
* [Flask](https://github.com/pallets/flask/) - Web development framework.
* [Grafana](https://github.com/grafana/grafana) - visualization UI for InfluxDB.

The database, grafana and the webApp are automatically connected. Furthermore grafana is setup with a user account and a working dashboard, displaying all the information.

<br />

## Client architecture

The client is a Python3 program designed to run a RaspberryPi, it generates random measurements every 30sec or loads them from a JSON file (fake_weather.json).

```json
{
    "temperature": 17.4, 
    "air-humidity": 72, 
    "ground-humidity": 70, 
    "windspeed": 8, 
    "time": ""
} 
```

<br/>

## Installation guide

#### Server:

1. Install [Docker](https://docs.docker.com/get-docker/) and [docker-compose](https://docs.docker.com/compose/install/).
1. Download the server folder from the repository to the host.
1. Change the usernames/passwords for the database, grafana, and the email in the `.env` file, more on that later.

<br />
Run the following command to start the server:

```bash
docker-compose up -d
```

To stop run:

```bash
docker-compose down
```

<br />

#### Client:

1. You have to have Python3 installed (comes pre-installed on Raspberry pi).
3. Download the client folder to the Raspberry pi.
4. Navigate to the downloaded file directory.
5. Install the required libraries using pip: 
```
pip install -r requirements.txt 
```
5. Start the client using: 
```
python3 client.py
```
6. Type in the IP of the server (without a port number, that is automatically 5000) and choose the operation mode.

<p align="center">
<img width="350" alt="mode_select" src="https://user-images.githubusercontent.com/70406237/129238525-241d6434-de82-439a-a5ee-ec0684d73e9a.png">
</p>


## Ports

| Service | Host Port |
|:---:|:---:|
| Grafana | 3000 |
| InfluxDB | 8086 |
| Flask WebApp | 127.0.0.1:5000 |

<br/>

Note that if you want Influx to be accessible outside of Docker, you have to uncomment the option from the `server/Docker-Compose.yml` file.

<br/>

## Volumes

Two docker volumes are created so that the data isn't lost on reboot.

* influxdata
* grafanadata

<br />

## Users, passwords and accounts

Three users are created, one user account for flask to connect to the database 
* `InfluxUser`
* `InfluxUserPass`

Two admin users, one for InfluxDB and one for Grafana.

* `InfluxAdminUser`
* `InfluxAdminPass`
* `GRAFANA_USERNAME`
* `GRAFANA_PASSWORD`

<br />

### Mail
If conditions are met (+50% temperature and -40% humidity) than a email notification is send.

<p align="left">
<img width="230" alt="alert" src="https://user-images.githubusercontent.com/70406237/129346584-cc1fa5d7-dd16-4931-b1e5-5ce2292c50d8.png">
</p>

To send the alerts a google email account is needed with the [Less secure app access](https://myaccount.google.com/security) option enabled.

Add the username and password to the ```.env``` file.

* `MailUser`
* `MailPass`

Read more about Less secure app access [here.](https://support.google.com/accounts/answer/6010255?hl=en#zippy=%2Cif-less-secure-app-access-is-on-for-your-account)

<br />

## Database

Influx DB creates a database with the name `InfluxDatabaseName = 'env_data'`.

<br />

## Grafana

Grafana is used to visualize the data, by default you can log in by going to `localhost:3000` and using username and password admin.

<p align="center">
<img width="500" alt="alert" src="https://user-images.githubusercontent.com/70406237/129348682-36e3919b-6f93-47f7-bde8-c580e3c17d2d.png">
</p>

A dashboard with the name Pi is automatically created with the graphs and the queries that are needed.

<br/>

### Grafana data sources

A data source with the name `Rpi_EnvSensor_Data` is created and is linked to the created database (`env_data`).

```
./grafana-provisioning/datasources/
```

Learn more about data sources from the [Grafana Documentation](http://docs.grafana.org/administration/provisioning/#datasources).
