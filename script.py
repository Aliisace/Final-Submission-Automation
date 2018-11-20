import os
import json
import subprocess
import sys
import nmap
import pickle
import nmapParse

# rpcclient credentials
username = "test"
password = "test123"

hosts = {}

def main():
	# mode = getMode()
	mode = "Lab"
	if mode == "Test":
		filename = "test.txt"
		getIPs(filename)
	elif mode == "Lab":
		filename = "hostList.txt"
		getIPs(filename)
	getPing()
	for ip in hosts:
		searchMap(ip, "Unreachable")
	print((json.dumps(hosts, sort_keys = True)))
	for ip in hosts:
		if ping(ip):
			if not os.path.exists(ip):
				print(("mkdir " + ip))
				os.system("mkdir " + ip)
				scan(ip)
				rpcEnumDomUsers(ip)
				rpcEnumGroups(ip)
				getUserGroupNames(ip)
			else:
				scan(ip)
				rpcEnumDomUsers(ip)
				rpcEnumGroups(ip)
				getUserGroupNames(ip)


def getIPs(fileName):
	with open(fileName) as f:
		for line in f:
			(key, val) = line.split()
	hosts[key] = val
# end getIPs

def getPing():
	for ip in hosts:
		val = []
		os.system("ping -c 1 " + ip + " > output.txt")
		with open("output.txt") as f:
			for line in f:
 				val.append(line)
		hosts[ip] = val[1]
# end getPing

def searchMap(searchKey, searchVal):
 	for ip in hosts:
 		if (searchKey in hosts):
 			if (searchVal not in hosts[searchKey]):
 				return "Host OK"
 			hosts[searchKey] = "Host not available"
 			return hosts[searchKey]
# end searchMap

def ping(host):
	os.system("fping %s > %s.txt" % (host, host))
	pingFile = open("%s.txt" % host, 'r')
	# os.system("rm %s.txt" % host)

	if 'alive' in pingFile.read():
		print("%s Alive on ICMP" % host)
		return True
	else:
		print("%s Unavailable via ICMP" % host)
		return False
# end ping

# Runs an nmap scan on the host and parses using nmapParse.py
def scan(host):
	print("Scanning " + host)
	scanner = nmap.PortScanner()
	scanner.scan(host, arguments="-sV -O --script vuln")
	nmapParse.scanParse(scanner[host], host + "/nmap.txt")
# end scan

# Uses rpcclient to enumerate for dom users
# Writes list of users to host/users.txt
# Runs rpcQueryUser for each user found
def rpcEnumDomUsers(host):
	os.system("rpcclient " + host + " -U " + username + "%" + password + " -c enumdomusers > " + host + "/users.txt")
	userFile = open(host + "/users.txt")
	users = []
	for line in userFile:
		users.append(line[6:-14])
		os.system("mkdir " + host + "/users")
	for user in users:
		rpcQueryUser(host, user)
# end rpcEnumDomUsers

# Uses rpcclient to enumerate info about individual users
# Writes the info to host/users/user.txt
def rpcQueryUser(host, user):
	os.system("rpcclient " + host + " -U " + username + "%" + password + " -c \'queryuser \"" + user + "\"\' > " + host + "/users/\'" + user + ".txt\'")
# end rcpQueryUser

# Uses rpcclient to enumerate for all group types
# Writes the groups to host/groups.txt
def rpcEnumGroups(host):
	commands = ['enumdomgroups', '\'enumalsgroups builtin\'', '\'enumalsgroups domain\'']
	for i in commands:
		os.system("rpcclient " + host + " -U " + username + "%" + password + " -c " + i + " >> " + host + "/groups.txt")
# end rpcEnumGroups

# Sorts user txt files into folders of their respective groups
def getUserGroupNames(host):
	occupiedGroups = []
	userGroupId = {}
	usersDir = os.listdir(host + "/users")
	groups = open(host + "/groups.txt", 'r')

	# Populates userGroupId dict with the users and their group ids
	for user in usersDir:
		tempUserFile = open(host + "/users/" + user)
		for i, line in enumerate(tempUserFile):
		    if i == 0:
		        # Slice name from line 0
		        nm = line[15:-1]
		    if i == 18:
		        # Slice group id from line 18
		        gid = line[12:-1]
		userGroupId[nm] = gid

	# Creates a directory to sort the users into
	os.system("mkdir " + host + "/sortedUsers")

	# For each group
	for group in groups:
		# Make a folder of that groups name
		os.system("mkdir " + host + "/sortedUsers/\'" + group[7:-14] + "\'")
		# For each user
		for user in userGroupId:
		# Check if user is in the current group
			if userGroupId[user] == group[-7:-2]:
				# If so, move their .txt file into that group folder
				os.system("mv " + host + "/users/\'" + user + ".txt\' " + host + "/sortedUsers/\'" + group[7:-14] + "\'/")
				# Add group to the list of occupied groups
				if group[7:-14] not in occupiedGroups:
					occupiedGroups.append(group[7:-14])

	# For all occupied groups
	for group in occupiedGroups:
		# Move the groups folder to host/users
		os.system("mv " + host + "/sortedUsers/\'" + group + "\'" + " " + host + "/users")
	# Remove unoccupied folders
	os.system("rm -r " + host + "/sortedUsers")
# end getUserGroupNames


def getMode():
	while True:
		print(("\t" + os.path.basename(__file__)))
		mode = input("mode > ").upper()
		if mode in "T L Q".split():
			if mode[0] == "T":
				mode = "Test"
				return mode
			elif mode[0] == "L":
				mode = "Lab"
				return mode
			elif mode[0] == "Q":
				sys.exit()
		else:
			print("If you are testing please press T\n If you are in the lab please press L")


if __name__ == "__main__":
	main()
