__author__ = 'umidqssh'



from bundler import *

class Application:
    def __init__(self, ports, root, options={}):
        self.instances = []
        for port in ports:
            self.instances.append(instance.Instance(port,root))

    def run(self):
        for instance in self.instances:
            instance.setupFolders()
            instance.configfiles()
            instance.copymanual()
            instance.writeddixml()
            instance.copyindexfiles()
            instance.writeindexhtm()
            instance.writelistfiles()
            instance.copyfiles()

