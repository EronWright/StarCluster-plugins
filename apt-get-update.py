from starcluster import clustersetup
from starcluster.logger import log

class AptGetUpdate(clustersetup.DefaultClusterSetup):
    def __init__(self):
          super(AptGetUpdate, self).__init__()
          return

    def run(self, nodes, master, user, user_shell, volumes):
        log.info("Updating apt-get package list on all nodes...")
     	for node in nodes:
            self.pool.simple_job(self._configure_node, (node), jobid=node.alias)
        self.pool.wait(len(nodes))

    def _configure_node(self, node):
        node.ssh.execute('apt-get -y update')
        
