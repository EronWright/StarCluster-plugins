from starcluster import clustersetup
from starcluster.logger import log

class Mount(clustersetup.DefaultClusterSetup):
    def __init__(self, host, remote_path):
          super(Mount, self).__init__()
          self.host = host
          self.remote_path = remote_path

    def run(self, nodes, master, user, user_shell, volumes):
        log.info("Mounting %s:%s on all nodes..." % (self.host, self.remote_path))
        
     	for node in nodes:
            self.pool.simple_job(self._configure_node, (node), jobid=node.alias)
        self.pool.wait(len(nodes))

    def _configure_node(self, node):
        class FakeServerNode(object):
            alias = None
        n = FakeServerNode()
        n.alias = self.host
        
        node.mount_nfs_shares(n, [self.remote_path])
        #nconn = node.ssh
        #nconn.execute('mkdir -p %s %%> /dev/null' % self.local_path)
        
        #node.ssh
        

        
