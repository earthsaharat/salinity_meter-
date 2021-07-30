import requests
import random
import threading
import datetime
import pytz

# SERVER_IP = 'http://localhost:8000'
SERVER_IP = 'http://salinity.saharatss.com'

def random_data():
	_data = {
		'lat':13.75,
		'lng':100.5,
		'salinity':round(random.uniform(0,100),2),
		'ppm':round(random.uniform(0,35000),2),
		'ppt':round(random.uniform(0,100),2),
	}
	return _data

def req():
	data = random_data()
	url = SERVER_IP+'/api/?device=1&key=F0KY1KPXjKBOy1Mq4hAOnzeRp6eETFgJ&salinity='+str(data['salinity'])+'&ppm='+str(data['ppm'])+'&ppt='+str(data['ppt'])+'&lat='+str(data['lat'])+'&lng='+str(data['lng'])
	r = requests.get(url)
	print('Mobile -> '+str(r.status_code)+' '+r.text)

def req_station():
	data = random_data()
	datetime_now = datetime.datetime.now(tz=pytz.timezone('Asia/Bangkok'))
	payload = {
		"siteID" : "BK001",
		"timestamp" : datetime_now.timestamp(),
		"waterSensorData" : {
			"Level" : 0,
			"Flow" : 0,
			"Temperature" : 0,
			"ElectricalConductivity" : 0,
			"Salinity" : data['salinity']
		},
		"powerMeterData" : {
			"Voltage" : 1,
			"Current" : 0,
			"Power" : 0,
			"Energy" : 0
		},
		"status" : {
			"ACPowerOK" : True,
			"BatteryLow" : False,
			"CabTamper" : False,
			"SurgeProtectionFailure" : False
		}
	}
	r = requests.post(SERVER_IP+'/api/station', json=payload)
	print(datetime_now.strftime("%d/%m/%Y %H:%M:%S")+' Station -> '+str(r.status_code)+' '+r.text)

def thread_function():
	threading.Timer(1, thread_function).start()
	req()
	# req_station()

if __name__ == "__main__":
	thread_function()
	# print(datetime.datetime.fromtimestamp(1611942541))

