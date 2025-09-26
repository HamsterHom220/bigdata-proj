wget https://archive.apache.org/dist/hadoop/common/hadoop-3.3.6/hadoop-3.3.6.tar.gz
tar xzf hadoop-3.3.6.tar.gz
sudo mv hadoop-3.3.6 /opt/hadoop

sudo adduser hadoop
sudo usermod -aG sudo hadoop
#sudo su - hadoop
sudo chown -R hadoop:hadoop /opt/hadoop

echo 'export HADOOP_HOME=/opt/hadoop' >> /opt/hadoop/etc/hadoop/hadoop-env.sh
echo 'export HADOOP_INSTALL=$HADOOP_HOME' >> /opt/hadoop/etc/hadoop/hadoop-env.sh
echo 'export HADOOP_MAPRED_HOME=$HADOOP_HOME' >> /opt/hadoop/etc/hadoop/hadoop-env.sh
echo 'export HADOOP_COMMON_HOME=$HADOOP_HOME' >> /opt/hadoop/etc/hadoop/hadoop-env.sh
echo 'export HADOOP_HDFS_HOME=$HADOOP_HOME' >> /opt/hadoop/etc/hadoop/hadoop-env.sh
echo 'export YARN_HOME=$HADOOP_HOME' >> /opt/hadoop/etc/hadoop/hadoop-env.sh
echo 'export HADOOP_COMMON_LIB_NATIVE_DIR=$HADOOP_HOME/lib/native' >> /opt/hadoop/etc/hadoop/hadoop-env.sh
echo 'export PATH=$PATH:$HADOOP_HOME/bin:$HADOOP_HOME/sbin' >> /opt/hadoop/etc/hadoop/hadoop-env.sh
echo 'export HADOOP_OPTS="-Djava.library.path=$HADOOP_HOME/lib/native' >> /opt/hadoop/etc/hadoop/hadoop-env.sh
echo 'export JAVA_HOME=$JAVA_HOME' >> /opt/hadoop/etc/hadoop/hadoop-env.sh