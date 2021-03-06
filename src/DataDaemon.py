__author__ = 'zmiller'
import sys

from Daemon import Daemon
from Run import Runable


class DataDaemon(Daemon):
    def run(self):
        Run = Runable()
        Run.run()

if __name__ == "__main__":
    daemon = DataDaemon('/tmp/daemon-example.pid')
    if len(sys.argv) == 2:
        if 'start' == sys.argv[1]:
            print "Starting DataDaemon..."
            daemon.start()
            print "DataDaemon Started"
        elif 'stop' == sys.argv[1]:
            print "Stopping DataDaemon..."
            daemon.stop()
            print  "DataDaemon Stopped"
        elif 'restart' == sys.argv[1]:
            print  "Restarting DataDaemon..."
            daemon.restart()
            print "DataDaemon Restarted"
        else:
            print "Unknown command"
            sys.exit(2)
        sys.exit(0)
    else:
        print "usage: %s start|stop|restart" % sys.argv[0]
        sys.exit(2)
