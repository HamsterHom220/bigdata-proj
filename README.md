# 1. Problem statement
## Analysis of bird specie geospatial distribution over time
Especially I wanted to test a hypothesis that the noise pollution caused by recently built huge datacenters negatively affects local bird populations, causing them to migrate or even decreasing the birth rate during the nesting period. So I studied different sources to find out that the most dense cluster of datacenters all over the world is located at North Virginia, US (you may take a look here https://www.datacentermap.com/).
# 2. Methodology
To approach the problem, I queried a sample of the `ebird.org` database, requesting the records from Virginia only.

While waiting for the response I had the following alternatives... Their complete DB is huge: 200 GB gzipped.
Other options that I had to proceed with:
<ol>
    <li>Try to find insights from metadata of the full DB, which is a separate csv file, 7 GB in gzip (34 GB unpacked).</li>
    <li>Fallback: just use the little piece of the main DB (4800 records, 3 MB), that is provided open-source just for example and available to download here: https://ebird.org/downloads/samples/ebd-datafile-SAMPLE.zip</li>
</ol>

I couldn't find anything useful in the metadata, so I started building cluster infrastructure to approach big samples of the main DB.

My setup is 3 VMs, each having:
<ul>
    <li>4 CPU cores</li>
    <li>16 GB RAM</li>
    <li>50 GB SSD</li> 
</ul>


# 3. Implementation

## 3.1. Setting up the cluster

1. Run `setup.sh` on every node.
2. >`ansible-playbook -i inventory.ini setup-cluster.yaml` 

    on a host machine to compose the cluster nodes (cloud VMs).

## 3.2. Setting up HDFS

1. Run `install_hadoop.sh` on every node.
2. Edit `core-site.xml` and `hdfs-site.xml` at `$HADOOP_HOME/etc/hadoop/` <b>on every node</b>, as shown in the corresponding files provided in this repo.
* Replace 'namenode' hostname with '0.0.0.0' for the master node.
3. Add these lines to `$HADOOP_HOME/etc/hadoop/hadoop-env.sh` <b>on every node</b>:
```
export JAVA_HOME=/usr/lib/jvm/java-8-openjdk-amd64
export HADOOP_HOME=/opt/hadoophado
export HADOOP_CONF_DIR=$HADOOP_HOME/etc/hadoop
export HADOOP_LOG_DIR=$HADOOP_HOME/logs
export HADOOP_PID_DIR=$HADOOP_HOME/pids
export HADOOP_OPTS="-Djava.net.preferIPv4Stack=true"
export HADOOP_CLASSPATH=$HADOOP_CLASSPATH:$HADOOP_HOME/share/hadoop/common/lib/*:$HADOOP_HOME/share/hadoop/common/*:$HADOOP_HOME/share/hadoop/hdfs/*:$HADOOP_HOME/share/hadoop/hdfs/lib/*:$HADOOP_HOME/share/hadoop/mapreduce/*:$HADOOP_HOME/share/hadoop/yarn/*:$HADOOP_HOME/share/hadoop/yarn/lib/*
```
*To reload the environment: `source hadoop-env.sh`

4. List all the DataNode hostnames at `$HADOOP_HOME/etc/hadoop/workers` <b>on every node</b>. Also list them on every node at `/etc/hosts` in format `IP HOSTNAME`.
5. Run `hdfs_dir_setup.sh` on all nodes.
6. Configure SSH connection between nodes...
7. Run this on the master: `hdfs namenode -format`. Then start the HDFS! `start-dfs.sh`.
Now the HDFS UI is available at:
* `http://NAMENODE_IP:9870`
* `http://DATANODE_IP:9864`


## 3.3. Launching Spark jobs
1. Configure Spark...
2. Launch YARN

## 3.4 Visualize results in Apache Superset

# 4. Results
## 4.1. Insights
## 4.2. Discussion
## 4.3. Future work