# Dependencies for OS
apt-get install --assume-yes python2.7
apt-get install --assume-yes python-pip fping arp-scan nmap
sudo apt-get install vim
sudo apt-get install git
mkdir /home/el/.vim
git clone https://github.com/sentientmachine/Pretty-Vim-Python.git
mv Pretty-Vim-Python/* .

# Dependencies for Python(2.7+)
pip install yattag python-nmap