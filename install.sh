# Dependencies for OS
sudo apt-get update
sudo apt-get python3
apt-get install --assume-yes python3.7
apt-get install --assume-yes --fix-missing python3-pip fping arp-scan nmap
sudo apt-get install vim
sudo apt-get install git
mkdir /home/el/.vim
git clone https://github.com/sentientmachine/Pretty-Vim-Python.git
rsync /root/Desktop/HScript/Pretty-Vim-Python/* /usr/share/vim/vim81


# Dependencies for Python(2.7+)
python3 -m pip install yattag python-nmap
python3.7 -m pip install yattag python-nmap
