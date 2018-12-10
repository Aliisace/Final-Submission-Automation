nmap -sT -v -v -T4 -sV -O -oN 192.168.0.1TCP 192.168.0.1 > nmap.txt
nmap -sT -v -v -T4 -sV -O -oN 192.168.0.2TCP 192.168.0.2 >> nmap.txt
nmap -sU -v -v -T4 -sV -oN 192.168.0.1UDP 192.168.0.1 >> nmap.txt
nmap -sU -v -v -T4 -sV -oN 192.168.0.2UDP 192.168.0.2 >> nmap.txt

