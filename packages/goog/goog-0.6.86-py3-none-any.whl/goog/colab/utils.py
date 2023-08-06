from subprocess import Popen, PIPE


def runShell(cmd, **kwargs):
    from omnitools import IS_WIN32
    if IS_WIN32:
        cmd = cmd.replace("python3.7", "python")
    return Popen(cmd, shell=True, stdin=PIPE, stdout=PIPE, stderr=PIPE, close_fds=True, **kwargs)

