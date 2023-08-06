from unencryptedsocket import SC
import time


def rpc(sc_port):
    def sc():
        return SC(host="127.0.0.1", port=sc_port)

    def add_job(t, v):
        return sc().request(command="add_job", data=((t, v), {}))

    def get_job_result(t):
        r = sc().request(command="get_job_result", data=((t,), {}))
        if isinstance(r, Exception):
            raise KeyError
        return r

    def _rpc(name, *args):
        t = time.time()
        if not args:
            args = [tuple(), dict()]
        add_job(t, [name, *args])
        while time.time() - t < 30:
            try:
                return get_job_result(t)
            except KeyError:
                time.sleep(1 / 1000)
        return "timeout"

    return sc, add_job, get_job_result, _rpc


