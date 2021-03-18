import sys
import logging
import subprocess
from permedcoe.core.constants import SEPARATOR

DECODING_FORMAT = 'utf-8'


def command_runner(cmd):
    """Run the command defined in the cmd list.

    Args:
        cmd (list[str]): Command to execute as list.

    Raises:
        Exception: Exit code != 0
    """
    logging.debug("Executing: %s" % str(cmd))
    p = subprocess.Popen(cmd,
                         stdout=subprocess.PIPE,
                         stderr=subprocess.PIPE)
    stdout, stderr = p.communicate()   # blocks until cmd is done
    stdout = stdout.decode(DECODING_FORMAT)
    stderr = stderr.decode(DECODING_FORMAT)
    return_code = p.returncode
    logging.debug("Exit code: %s" % str(return_code))

    print(SEPARATOR, flush=True)
    print("------------ STDOUT ------------",
          flush=True)
    print(stdout, flush=True)
    if stderr:
        print("------------ STDERR ------------",
              file=sys.stderr, flush=True)
        print(stderr, file=sys.stderr, flush=True)

    print(SEPARATOR, flush=True)
    if return_code != 0:
        print("Exit code: %s != 0" % str(return_code),
              file=sys.stderr, flush=True)
        exit(return_code)
