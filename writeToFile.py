import json

def writeFile(dict, host):
    with open ('/root/Desktop/Automation/Enumeration/Results/raw %s.txt' % host, 'w') as file:
        file.write(json.dumps(dict, indent=4))
