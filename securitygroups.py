from starcluster import clustersetup
from starcluster.logger import log

class SecurityGroups(clustersetup.DefaultClusterSetup):
    def __init__(self, groups):
          super(SecurityGroups, self).__init__()
          self.groups = groups.split(',')

    def run(self, nodes, master, user, user_shell, volumes):
        log.info("Updating security groups on all nodes...")
        
        group_ids = [master.ec2.get_security_group(g).id for g in self.groups]
        
     	for node in nodes:
            self.pool.simple_job(self._configure_node, (node, group_ids), jobid=node.alias)
        self.pool.wait(len(nodes))

    def _configure_node(self, node, group_ids):
        existing_groups = node.instance.get_attribute('groupSet')['groupSet']
        modified_groups = list(set(group_ids + [g.id for g in existing_groups]))
        node.instance.modify_attribute('groupset', modified_groups)
        

        
