__author__ = 'Nathan Waddington'
__email__ = 'nathan_waddington@alumni.sfu.ca'

# based on "Python subprocess example: running a background subprocess with non-blocking output processing"
# found here: http://www.zultron.com/2012/06/python-subprocess-example-running-a-background-subprocess-with-non-blocking-output-processing/

import subprocess
import threading
from logging import getLogger

LOG = getLogger('socat')


class socat(subprocess.Popen):
    """
    Run socat as a subprocess sending output to a logger.
    This class subclasses subprocess.Popen
    """

    def __init__(self):
        # construct the command line
        cmd = ['/opt/local/bin/socat', '-d', '-d', 'pty,raw,echo=0', 'pty,raw,echo=0']


        # spawn the socat process
        super(socat, self).__init__(
            cmd, shell=False,
            stdout=subprocess.PIPE, stderr=subprocess.PIPE,
            bufsize=1, close_fds='posix')

        LOG.debug("Started socat subprocess, pid %s" % self.pid)
        LOG.debug("Command:  '%s'" % "','".join(cmd))

        # start stdout and stderr logging threads
        self.log_thread(self.stdout, LOG.info)
        self.log_thread(self.stderr, LOG.warn)


    def log_thread(self, pipe, logger):
        """
        Start a thread logging output from pipe
        """

        # thread function to log subprocess output
        def log_output(out, logger):
            for line in iter(out.readline, b''):
                logger(line.rstrip(b'\n'))

        # start thread
        t = threading.Thread(target=log_output,
                             args=(pipe, logger))
        t.daemon = True  # thread dies with the program
        t.start()
