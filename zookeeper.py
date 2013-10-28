from starcluster import clustersetup
from starcluster.logger import log

ZK_CONFIG = """
tickTime=2000
dataDir=/var/lib/zookeeper/
clientPort=2181
initLimit=5
syncLimit=2
"""

ZK_CONFIG_SERVER = "server.%(id)s=%(host)s:2888:3888\n"

class ZooKeeper(clustersetup.DefaultClusterSetup):
    """ 
    This plugin installs Apache ZooKeeper on all the nodes in the cluster.

    [plugin zookeeper]
    setup_class = zookeeper.ZooKeeper
    """

    def __init__(self, opts=None):
        super(ZooKeeper, self).__init__()
        self.opts = opts
        log.debug('opts = %s' % opts)
        self.packages = ["zookeeper"]
  
    def run(self, nodes, master, user, user_shell, volumes):

        # install the packages
        log.info('Installing the following packages on all nodes:')
        log.info(', '.join(self.packages), extra=dict(__raw__=True))
        pkgs = ' '.join(self.packages)
        for node in nodes:
            self.pool.simple_job(node.apt_install, (pkgs), jobid=node.alias)
        self.pool.wait(len(nodes))

        # write the ZooKeeper config
        log.info("Configuring ZooKeeper on all nodes...")
        for node in nodes:
            self.pool.simple_job(self._configure_node, (nodes, node),
                                 jobid=node.alias)
        self.pool.wait(len(nodes))

    def on_add_node(self, new_node, nodes, master, user, user_shell, volumes):
        log.info('Installing the following packages on %s:' % new_node.alias)
        pkgs = ' '.join(self.packages)
        new_node.apt_install(pkgs)

    def on_remove_node(self, node, nodes, master, user, user_shell, volumes):
        raise NotImplementedError("on_remove_node method not implemented")

    def _configure_node(self, nodes, node):
        configf = '/etc/zookeeper/conf/zoo.cfg'
        config = node.ssh.remote_file(configf, 'w')
        config.write(self._generate_config(nodes, node))
        config.close()

        myidf = "/etc/zookeeper/conf/myid"
        myid = node.ssh.remote_file(myidf, 'w')
        for i,n in enumerate(nodes):
            if node.alias == n.alias:
                myid.write("%(id)d\n" % dict(id=i))
        myid.close()

    def _generate_config(self, nodes, node):
        s = ZK_CONFIG % dict(host=node.alias)
        s += '\n'
	for i,n in enumerate(nodes):
            s += ZK_CONFIG_SERVER % dict(id=i,host=n.alias)
        return s
