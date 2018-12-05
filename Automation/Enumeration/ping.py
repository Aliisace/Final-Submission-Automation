import os
import subprocess
import sys
import writeToFile

hosts = {}

results = {}
#Array of users with [name][info]
#Array of groups

# rpcclient credentials
username = "test"
password = "test123"

def splitIntoDict(txt):
    d = {}

    for index, i in enumerate(txt):
        # Split name and rid into an array
        txt[index] = [txt[index][:txt[index].find("rid:")-1], txt[index][txt[index].find("rid:"):]]
        # Splice out values and store in a dictionary
        d[txt[index][0][txt[index][0].find(":[")+2:-1]] = {"name": txt[index][0][txt[index][0].find(":[")+2:-1], "rid": txt[index][1][5:-1]}
    return d
# end splictIntoDict

def enumAliases(host):
    command = ["rpcclient", host, "-U", username + "%" + password, "-c"]
    dicts = {"builtin": {}, "domain": {}}

    for i in dicts:
        # Enumerate aliases and rids
        dicts[i] = splitIntoDict(subprocess.run(command+["enumalsgroups " + i], encoding="ascii", stdout=subprocess.PIPE).stdout.splitlines())

    return dicts
# end enumAliases

def enumAliasMembers(host, users):
    command = ["rpcclient", host, "-U", username + "%" + password, "-c"]
    aliases = enumAliases(host)
    usrAliases = {}

    for group in aliases:
        for name in users:
            users[name]["aliases"] = {group:{}}
            # Get a list of domain aliases for that user 
            usrAliases[group] = subprocess.run(command+["queryuseraliases " + group + " " + users[name]["sid"]], encoding="ascii", stdout=subprocess.PIPE).stdout
            for alias in aliases[group]:
                if aliases[group][alias]["rid"] in usrAliases[group]:
                    # Append alias to users[name]["aliases"]
                    users[name]["aliases"][group][alias] = aliases[group][alias]

    return users
# end enumAliasMembers

def enumGroups(host):
    command = ["rpcclient", host, "-U", username + "%" + password, "-c"]
    
    # Enumerate groups and rids
    groupsDict = splitIntoDict(subprocess.run(command+["enumdomgroups"], encoding="ascii", stdout=subprocess.PIPE).stdout.splitlines())

    return groupsDict
# end enumGroups

def enumGroupMembers(host, users):
    command = ["rpcclient", host, "-U", username + "%" + password, "-c"]
    groups = enumGroups(host)

    for name in users:
        users[name]["groups"] = {}
        # Get a list of groups for that user
        usrGroups = subprocess.run(command+["queryusergroups " + users[name]["rid"]], encoding="ascii", stdout=subprocess.PIPE).stdout

        for group in groups:
            if groups[group]["rid"] in usrGroups:
                # Append group to users[name]["aliases"]
                users[name]["groups"][group] = groups[group]

    return users
# end enumGroupMembers

def enumUsers(host):
    command = ["rpcclient", host, "-U", username + "%" + password, "-c"]

    # Enumerate usernames and rids
    usersTxt = subprocess.run(command+["enumdomusers"], encoding="ascii", stdout=subprocess.PIPE).stdout.splitlines()
    usersDict = splitIntoDict(usersTxt)

    for name in usersDict:
        # Enumerate SID and info of each user
        usersDict[name]["rawinfo"] = subprocess.run(command+["queryuser " + usersDict[name]["rid"]], encoding="ascii", stdout=subprocess.PIPE).stdout
        usersDict[name]["sid"] = subprocess.run(command+["lookupnames " + name], encoding="ascii", stdout=subprocess.PIPE).stdout
        usersDict[name]["sid"] = usersDict[name]["sid"][usersDict[name]["sid"].find("S-"):usersDict[name]["sid"].find(" (User")]

    usersDict = enumGroupMembers(host, usersDict)
    usersDict = enumAliasMembers(host, usersDict)

    return usersDict
# end enumUsers

if __name__ == "__main__":
    for host in hosts:
        print("host: " + host + "\nusers:")
        with open("/root/Desktop/Automation/Enumeration/Results/%s.txt" % host, "w") as file:
            file.write(str(host) + ":\n\n")
            results[host] = {"users": enumUsers(host)}
            for index,user in enumerate(results[host]["users"]):
                print("\t" + user)
                file.write("User: " + str(user)  + "\n")
                file.write("\t| SID: " + str(results[host]["users"][user]["sid"]) + "\n")
                file.write("\t| RID: " + str(results[host]["users"][user]["rid"]) + "\n") 
                file.write("\t| Groups: \n")
                for index,group in enumerate(results[host]["users"][user]["groups"]):
                    file.write("\t\t| Name: " + str(group) + "\n\t\t\t| RID: " + str(results[host]["users"][user]["groups"][group]["rid"]) + "\n")
                file.write("\n\t| Aliases: ") 
                for index,alias in enumerate(results[host]["users"][user]["aliases"]):
                    file.write("\n\t\t" + str(alias) + "\n")
                file.write("\n")
        print("\n")
        writeToFile.writeFile(results, host)
        with open("/root/Desktop/Automation/Enumeration/Results/Raw Info %s.txt" % host, "w") as file:
            file.write("Host: " + host + "\n") 
            for index,user in enumerate(results[host]["users"]):
                file.write("User: "+user +"\n | Raw info: \n")
                file.write(str(results[host]["users"][user]["rawinfo"]) + "\n")
