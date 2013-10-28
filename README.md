StarCluster-plugins
===================
Description
-----------
This project contains some useful plugins for StarCluster.

Usage
-----
Checkout the repository to ~/.starcluster/plugins directory.  Add plugin configuration sections to your config file.

Plugins
-------
###ZooKeeper
Configures Apache ZooKeeper on your cluster nodes.  All nodes are connected to the cluster.  
TODO:
- install ZooKeeper as a service
- start ZooKeeper ("/usr/share/zookeeper/bin/zkServer.sh start")

###apt-get-update
Updates the apt-get package list on your nodes.  This is helpful before using package manager commands.
