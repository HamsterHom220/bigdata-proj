sudo su hadoop

sudo mkdir -p /opt/hadoop/{tmp,namenode,datanode,logs,pids}
sudo chown -R hadoop:hadoop /opt/hadoop  # Replace 'hadoop' with your user

chmod 755 /opt/hadoop
chmod -R 755 /opt/hadoop/tmp

chmod 644 /opt/hadoop/etc/hadoop/*.xml