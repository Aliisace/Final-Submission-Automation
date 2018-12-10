import os
import json
hosts = {}

def getIPs(fileName):
	with open(fileName) as f:
		for line in f:
			(key, val) = line.split()
			hosts[key] = val

def getPing():
	for ip in hosts:
		val = []
		os.system("ping -c 1 " + ip + " > output.txt")
		with open("output.txt") as f:
			for line in f:
				val.append(line)
		hosts[ip] = val[1]

def searchMap(searchKey, searchVal):
	for ip in hosts:
		if (searchKey in hosts):
			if (searchVal not in hosts[searchKey]):
				return "Host OK"
			hosts[searchKey] = "Host not available"
			return hosts[searchKey]

getIPs("hostList.txt")
getPing()
for ip in hosts:
	searchMap(ip, "Unreachable")
print(json.dumps(hosts, sort_keys = True))
for ip in hosts:
	if (hosts[ip] != "Host not available"):
                os.mkdir("Results/" + ip)
		os.system("/usr/bin/nmap --script vuln -oN Results/" + ip + "nmap " + ip + " > Results/" + ip + "/nmapVuln" + ip + ".txt")
