# Dependencies for OS
apt-get install --assume-yes python3.7
apt-get install --assume-yes --fix-missing python3-pip fping arp-scan nmap
sudo apt-get install vim
sudo apt-get install git
mkdir /home/el/.vim
git clone https://github.com/sentientmachine/Pretty-Vim-Python.git
mv Pretty-Vim-Python/* .

# Dependencies for Python(2.7+)
python3 -m pip install yattag python-nmap
python3.7 -m pip install yattag python-nmap
