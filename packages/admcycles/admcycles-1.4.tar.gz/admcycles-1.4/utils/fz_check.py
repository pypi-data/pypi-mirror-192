r"""
Python script to check consistency of FZ relations in the DR submodule of admcycles

To see all options, run

    $ sage fz_check.py --help

Basic usage::

    $ sage fz_check.py

Minimal resources check::

    $ sage fz_check.py --maxmem=2000 --maxtime=1

A single check in genus 2, no marked points, degree 3::

    $ sage fz_check.py --gmin=2 --gmax=2 --nmin=0 --nmax=0 --rmin=3 --rmax=3

If you want to save the output for futher analysis either use redirection

    $ sage fz_check.py > my_log_file.log

or the ``tee`` unix tool for duplicating the standard output

    $ sage fz_check.py | tee my_log_file.log
"""
import sys
import argparse
import subprocess
from admcycles.moduli import get_moduli, socle_degree


parser = argparse.ArgumentParser(prog = 'fz_check', description = 'checking FZ relations')
parser.add_argument('--gmin', type=int, default=0, help='genus g lower bound')
parser.add_argument('--gmax', type=int, default=100, help='genus g upper bound')
parser.add_argument('--nmin', type=int, default=0, help='number of marked points n lower bound')
parser.add_argument('--nmax', type=int, default=100, help='number of marked points n upper bound')
parser.add_argument('--rmin', type=int, default=1, help='cohomology degree r lower bound')
parser.add_argument('--rmax', type=int, default=100, help='cohomology degree r upper bound')
parser.add_argument('--moduli', type=str, default='st', help='a moduli (either "st", "ct", "rt" or "sm")')
parser.add_argument('--maxmem', type=int, default=4000, help='a bound on memory (in MB)')
parser.add_argument('--maxtime', type=int, default=60, help='a bound on each check (in sec)')
parser.add_argument('--verbosity', type=int, default=1, help='verbosity (0 is quiet, 2 is verbose)')

args = parser.parse_args()

if args.verbosity >= 1:
    print("FZ check with gmin={} gmax={} nmin={} nmax={} rmin={} rmax={} moduli={} maxmem={} maxtime={} verbosity={}".format(args.gmin, args.gmax, args.nmin, args.nmax, args.rmin, args.rmax, args.moduli, args.maxmem, args.maxtime, args.verbosity))


def product_le(gnr1, gnr2):
    g1, n1, r1 = gnr1
    g2, n2, r2 = gnr2
    return g1 <= g2 and n1 <= n2 and r1 <= r2


moduli = get_moduli(args.moduli, DRpy=True)
limits = []  # (g, n, r) that hit memory limits
failed = []
success = []
for g in range(args.gmin, args.gmax + 1):
    if any(product_le((gg, nn, rr), (g, args.nmin, args.rmin)) for gg, nn, rr in limits):
        break
    if g == 0:
        nmin = max(args.nmin, 3)
    elif g == 1:
        nmin = max(args.nmin, 1)
    else:
        nmin = args.nmin
    for n in range(nmin, args.nmax + 1):
        if any(product_le((gg, nn, rr), (g, n, args.rmin)) for gg, nn, rr in limits):
            break
        for r in range(args.rmin, min(args.rmax, socle_degree(g, n, moduli)) + 1):
            if any(product_le((gg, nn, rr), (g, n, r)) for gg, nn, rr in limits):
                # already failed with smaller parameters
                break
            
            if args.verbosity >= 1:
                print("g={} n={} r={}".format(g, n, r), end=' ')
                sys.stdout.flush()

            sp = subprocess.run([sys.executable, "fz_check_once.py", str(g), str(n), str(r), str(moduli), str(args.maxmem), str(args.maxtime), str(args.verbosity)], capture_output=True, text=True)

            if args.verbosity >= 2:
                print()
                print('stdout\n', sp.stdout)
                print('stderr\n', sp.stderr)
                sys.stdout.flush()

            if sp.returncode == 0:
                success.append((g, n, r))
                if args.verbosity >= 1:
                    print("Success")
                    sys.stdout.flush()
            elif sp.returncode == 1:
                failed.append((g, n, r))
                if args.verbosity >= 1:
                    print("Failed")
                    sys.stdout.flush()
                continue
            else:
                # something went wrong
                if args.verbosity >= 1:
                    print("Overflow or overtime (ret code = {})".format(sp.returncode))
                limits.append((g, n, r))
                break

if not failed:
    print("Success: {} FZ check ran successfully".format(len(success)))
else:
    print("Failed: {} failures among {} checks".format(len(failed), len(failed) + len(success)))
    print(', '.join(map(str, failed)))
if limits:
    print("Timeout or memory overflow on (g, n, r) = {}".format(', '.join(map(str, limits))))
