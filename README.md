# Server Status (For Microsoft Band)
An app to expose your Linux server status in JSON + a Microsoft Band webapp to display it.

## Installation

### API Installation
1. The API is written in Flask. It needs to be running on the server that will be monitored. [http://flask.pocoo.org/docs/0.10/deploying/](How to deploy a Flask app)
2. Publicly expose status via port-forwarding/reverse proxy

### Band App Installation
#### Pre-built webtile
1. Edit msband/manifest.json
  - Change server URL
  - Hard disk mountpoint binding
2. Zip msband folder into msband.zip
3. Rename msband.zip to msband.webtile
4. Move msband.webtile to phone
5. Open msband.webtile on phone

#### Custom webtile
Custom MS Band webtiles can be easily built via online GUI at https://developer.microsoftband.com/WebTile/ChooseLayout

## Sample API Output
```JSON
{
	"processes": [{
		"process": "Plex Media Serv",
		"cpu": "1.6"
	}, {
		"process": "python",
		"cpu": "1.1"
	}, {
		"process": "python",
		"cpu": "0.6"
	}, {
		"process": "Plex DLNA Serve",
		"cpu": "0.5"
	}, {
		"process": "pvestatd",
		"cpu": "0.2"
	}, {
		"process": "transmission-da",
		"cpu": "0.1"
	}, {
		"process": "python",
		"cpu": "0.1"
	}, {
		"process": "openvpn",
		"cpu": "0.1"
	}, {
		"process": "zvol/9",
		"cpu": "0.0"
	}, {
		"process": "zvol/8",
		"cpu": "0.0"
	}],
	"disks": {
		"/media/1tb": {
			"available": "252G",
			"used": "619G",
			"percent": "72%",
			"device": "/dev/sda1",
			"mountpoint": "/media/1tb",
			"size": "917G"
		},
		"/media/terry": {
			"available": "385G",
			"used": "548G",
			"percent": "59%",
			"device": "/dev/sdd1",
			"mountpoint": "/media/terry",
			"size": "932G"
		},
		"/media/320gb": {
			"available": "219G",
			"used": "60G",
			"percent": "22%",
			"device": "/dev/sdc1",
			"mountpoint": "/media/320gb",
			"size": "294G"
		}
	},
	"cpu": {
		"load": {
			"1": "0.00",
			"5": "0.04",
			"string": "0.00, 0.04, 0.07",
			"15": "0.07"
		},
		"uptime": "37 days",
		"servertime": "Thu 10:29 pm",
		"users": "2 users",
		"temperature": {
			"current_temp": "30C",
			"critical_temp": "105C"
		}
	},
	"power": {
		"Load": "0 Watt(0 %)",
		"Firmware Number": "BFC7101_CS1",
		"Last Power Event": "Blackout at 2015/12/08 19:18:26",
		"Utility Voltage": "120 V",
		"Battery Capacity": "100 %",
		"Remaining Runtime": "92 min",
		"Rating Voltage": "120 V",
		"Line Interaction": "None",
		"Power Supply by": "Utility Power",
		"State": "Normal",
		"Output Voltage": "120 V",
		"Model Name": "CP1000AVRLCD",
		"Rating Power": "600 Watt(1000 VA)",
		"Test Result": "Failed at 2015/12/01 20:08:07"
	},
	"memory": {
		"ram": {
			"used": "1.8g",
			"buffers": "189.2m",
			"percent": "15%",
			"cached": "9.9g",
			"shared": "0k",
			"total": "11.7g",
			"type": "Mem",
			"free": "98.4m"
		},
		"swap": {
			"percent": "0%",
			"total": "4.0g",
			"type": "Swap",
			"free": "4.0g",
			"used": "14.4m"
		}
	}
}
```
