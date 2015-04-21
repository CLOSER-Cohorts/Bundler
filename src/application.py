__author__ = 'umidqssh'



from bundler import *

class Application:
    def __init__(self, ports, options={}):
        self.instances = []
        for port in ports:
            self.instances.append(instance.Instance(port))

    def run(self):
        for instance in self.instances:
            instance.setupFolders()
