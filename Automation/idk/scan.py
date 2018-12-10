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
		os.system("/usr/bin/nmap -sT -p1-65535 -v -v -T4 -sV -O -oN Results/" + ip + "TCP " + ip + " > Results/" + ip + "/nmapTCP" + ip + ".txt")
		os.system("rm Results/" + ip + "TCP")
		print("TCP complete")
		os.system("/usr/bin/nmap -sU -p1-500 -v -v -T4 -sV -oN Results/" + ip + "UDP " + ip + " > Results/" + ip + "/nmapUDP" + ip +".txt")
		os.system("rm Results/" + ip + "UDP")
		print("UDP complete")
		os.system("/usr/bin/dig host -t axfr uadtargetnet.com " + ip + " > Results/" + ip + "/dig" + ip + ".txt")
		os.system("/usr/bin/nslookup -type=any " + ip + " > Results/" + ip + "/dns" + ip + ".txt")
		os.system("/usr/bin/nslookup -type=any uadtargetnet.com > Results/" + ip + "/dns" + ip + ".txt")     
		print("nslookup complete") 
		os.system("/usr/bin/rpcclient  " + ip + " -A creds.txt -c srvinfo > Results/" + ip + "/rpcclient" + ip + ".txt")
		os.system("/usr/bin/rpcclient  " + ip + " -A creds.txt -c querydominfo >> Results/" + ip + "/rpcclient" + ip + ".txt")
		os.system("/usr/bin/rpcclient  " + ip + " -A creds.txt -c enumdomusers >> Results/" + ip + "/rpcclient" + ip + ".txt")
		os.system("/usr/bin/rpcclient  " + ip + " -A creds.txt -c 'enumalsgroups builtin' >> Results/" + ip + "/rpcclient" + ip + ".txt")
		os.system("/usr/bin/rpcclient  " + ip + " -A creds.txt -c 'lookupnames administrators' >> Results/" + ip + "/rpcclient" + ip + ".txt")
		os.system("/usr/bin/rpcclient  " + ip + " -A creds.txt -c 'lookupnames administrator' >> Results/" + ip + "/rpcclient" + ip + ".txt")
		os.system("/usr/bin/rpcclient  " + ip + " -A creds.txt -c 'queryuser 500' >> Results/" + ip + "/rpcclient" + ip + ".txt")
		print("rpcclient complete")
		print(ip + " complete")

#os.system("arping 192.168.0.1 -f -c 15 -I eth1") #cannot use because number of lines depends on if a response is received or not
