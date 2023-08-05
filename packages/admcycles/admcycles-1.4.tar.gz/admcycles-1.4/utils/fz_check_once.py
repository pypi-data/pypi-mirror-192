import signal
import sys
import resource

if len(sys.argv) != 8:
    print('invalid arguments')
    sys.exit(3)

g = int(sys.argv[1])
n = int(sys.argv[2])
r = int(sys.argv[3])
moduli = int(sys.argv[4])
maxmem = int(sys.argv[5])
maxtime = int(sys.argv[6])
verbosity = int(sys.argv[7])

if verbosity >= 2:
    print(sys.argv)
    sys.stdout.flush()

MAX_VIRTUAL_MEMORY = maxmem * 1024 * 1024  # maxmem MB
resource.setrlimit(resource.RLIMIT_AS, (MAX_VIRTUAL_MEMORY, resource.RLIM_INFINITY))

try:
    import sage.all
    from admcycles.DR import FZ_methods_sanity_check
except (MemoryError, ImportError) as e:
    if verbosity >= 2:
        print(e, file=sys.stderr)
    sys.exit(2)

class TimeoutException(Exception):
    pass

def handler(signum, frame):
    raise TimeoutException("timeout")

signal.signal(signal.SIGALRM, handler)
signal.alarm(maxtime)

try:
    result = FZ_methods_sanity_check(g, r, n, moduli)
except TimeoutException as e:
    # time limit
    if verbosity >= 2:
        print(e, file=sys.stderr)
    sys.exit(2)
except MemoryError:
    # (probably) memory limit
    if verbosity >= 2:
        print(e, file=sys.stderr)
    sys.exit(3)
except Exception:
    # something
    if verbosity >= 2:
        print(e, file=sys.stderr)
    sys.exit(4)

sys.exit(0 if result else 1)
