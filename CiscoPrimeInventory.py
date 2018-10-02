#Reference Script to create a inventory of access points from Cisco Prime. This script has been cleaned up for other people's reference who may run into a similar problem.

import requests
import json
import sys
import os
import csv
import pandas as pd
import numpy as np
import urllib3

f = open("resp.json", "a")
outFile = open("CiscoPrime.csv", "w", newline='')
csv_writer = csv.writer(outFile)
csv_writer.writerow(['hostName','DeviceType','model','primaryIPAddress','Source'])

page_count = 0
#API looks at 1000 devices at a time (e.g. first 1000, then 1000-2000, 2000-3000, etc. If the page count exceeds the number of devices, the API will error out, so set as appropriate
while page_count < 6000:
	urllib3.disable_warnings()
	resp = requests.get('https://user_name:password@cisco_prime_url/webacs/api/v3/data/AccessPointDetails.json?.full=true&.maxResults=1000&.firstResult=' + str(page_count), verify=False)
	data = resp.json()
	f.write(json.dumps(data, indent=2, sort_keys=True))
	page_count += 1000;
	#print(data)
	for r in data['queryResponse']['entity']:
		try: 
			DeviceType = 'A'
			model = r['accessPointDetailsDTO']['model']
			Source = 'Cisco Prime'
			
			output = str(r['accessPointDetailsDTO']['name'])+','
			output = output + str(DeviceType) + ','
			output = output + str(model)+','
			output = output + str(r['accessPointDetailsDTO']['ipAddress'])+','
			output = output + str(Source)

			outFile.write(output + '\n')

		except KeyError:
			break

