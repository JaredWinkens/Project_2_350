Steps for Installation:  
  
Set up WSL  
  
Install WSL on your Windows system with Ubuntu as the default distribution:  
bash  
  
wsl --install  
Update your package list:  
bash  
  
sudo apt update  
  
Install Java  
Apache Cassandra requires Java. Install OpenJDK 11:  
  
bash  
  
sudo apt install openjdk-11-jdk  
  
Add Cassandra’s Repository  
Add Cassandra's repository to the sources list:  
  
bash  
  
echo "deb https://downloads.apache.org/cassandra/debian 40x main" | sudo tee -a /etc/apt/sources.list.d/cassandra.sources.list  
curl https://downloads.apache.org/cassandra/KEYS | sudo apt-key add -  
  
Install Cassandra  
Install the latest stable version of Cassandra: 
  
bash  
  
sudo apt update  
sudo apt install cassandra  
  
Start the Cassandra Service  
Start and enable Cassandra:  
  
bash  
  
sudo systemctl start cassandra  
sudo systemctl enable cassandra  
  
Verify Installation  
Check Cassandra status:  
  
bash  
  
nodetool status  
Access the command-line interface (CLI) for Cassandra:  
  
bash  
  
cqlsh  
  
