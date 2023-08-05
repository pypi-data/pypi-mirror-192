.. image:: http://img.shields.io/badge/benchmarked%20by-asv-blue.svg?style=flat
   :target: https://gitlab.com/modulispaces/admcycles/builds/artifacts/master/browse/.asv/html?job=benchmark

admcycles
=========

admcycles is a `SageMath <https://www.sagemath.org>`_ module to compute with
the tautological ring of the moduli spaces of complex curves. You can install
it on top of a SageMath installation on your computer (see the instructions
below). You can alternatively use one of the online services below that have
admcycles already installed:

- `SageMathCell <https://sagecell.sagemath.org/>`_: An online service for
  SageMath computations that does not require authentification.

- `CoCalc <https://cocalc.com/>`_: A complete computation environment that
  offers a free plan subscription (with limited resources).

admcycles includes the `SageMath <https://www.sagemath.org>`_ module diffstrata
to compute with the tautological ring of the moduli space of multi-scale 
differentials, a compactification of strata of flat surfaces. It is particularly
tailored towards computing Euler characteristics of these spaces.

Detailed information on the package is contained in the documents

- `admcycles -- a Sage package for calculations in the tautological ring of the 
  moduli space of stable curves [arXiv:2002.01709] <https://arxiv.org/abs/2002.01709>`_
- `diffstrata -- a Sage package for calculations in the tautological ring of the
  moduli space of Abelian differentials [arXiv:2006.12815] <https://arxiv.org/abs/2006.12815>`_
- `online documentation <https://modulispaces.gitlab.io/admcycles/>`_

**NEW: Online database with tautological relations (Feb 2023)**

The latest version of admcycles includes an automated `online lookup <https://gitlab.com/modulispaces/relations-database>`_ of pre-calculated tautological relations (see `the list of available cases <https://modulispaces.gitlab.io/relations-database/index.html>`_).
By default, if you attempt a calculation that needs tautological relations, the program will first try to look them up in your local storage (in the folder ``.sage/admcycles``). If not found there, the program will check the above database and download the relations to your computer in case they are available. If this fails as well, the program will then calculate the relations itself.

If you would like to deactivate this online lookup, execute the following lines in a Sage session::

    sage: from admcycles.admcycles import set_online_lookup_default
    sage: set_online_lookup_default(False)

If you have calculated and stored relations that are not yet in our database, we would be happy if you reach out so we can integrate them!

Installation
------------

Prerequisites
^^^^^^^^^^^^^

Make sure that `SageMath <https://www.sagemath.org>`_ version 9.0 or later
is installed on your computer. Detailed installation instructions for
different operating systems are available `here
<http://doc.sagemath.org/html/en/installation/binary.html>`_ and on the
SageMath website. If you need to use admcycles with an older version of SageMath,
use `admcycles version 1.3.2 <https://pypi.org/project/admcycles/1.3.2/>`_.

All the command below must be run inside a console (the last character of the
prompt is usally a ``$``). On Windows this is called ``SageMath Shell`` while
on linux and MacOS this is often referred to as a ``terminal``.

Inside the console, we assume that the command ``sage`` launches a Sage
session (whose prompt is usually ``sage:``). To quit the Sage session
type ``quit`` and press ``Enter``.

Installation with pip (the Python package manager)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The most convenient way to use admcycles is to add the package to your
Sage installation. The exact procedure for this depends on your operating
system and how you installed Sage. If the pip installation fails, see
the sections `Manual installation with pip` or `Use without installation`
below.

- If you manually installed Sage by downloading it from the website, then run
  in a shell console::

      $ sage -pip install admcycles --user

  Here, the ``--user`` is an optional argument to ``pip`` which, when
  provided, will install admcycles not inside the Sage folder but in your home
  directory.

- If you have a linux distribution and installed the sagemath package via your
  package manager then run in a shell console::

     $ pip install admcycles --user

  The ``pip`` command above might have to be changed to ``pip2`` or ``pip3``
  depending on your system. Also, on Debian/Ubuntu systems, the following step
  might be necessary before running the above command::

     $ source /usr/share/sagemath/bin/sage-env

Manual installation with pip
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The automatic installation with pip from Section `Installation with pip` might
fail. One common reason is the lack of SSL support of the SageMath binaries. In
such situation you can follow the procedure below that bypass the connection of
``pip`` to the web.

- Download the admcycles package as a ``tar.gz``-file or ``.zip`` file either from `PyPI
  <https://pypi.org/project/admcycles/>`_ or from `gitlab
  <https://gitlab.com/modulispaces/admcycles/-/archive/master/admcycles-master.tar.gz>`__.

- Inside a shell console run::

      $ sage -pip install /where/is/the/package.tar.gz --user

  Here, the ``--user`` is an optional argument to ``pip`` which, when
  provided, will install admcycles not inside the Sage folder but in your home
  directory.

Installation of the development version
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

If you want to install the development version, you need to have the
versioning software ``git`` installed. The only change in the procedure
is to replace ``admcycles`` in the any of the command above by
``git+https://gitlab.com/modulispaces/admcycles``.

Upgrade
^^^^^^^

If you have already installed admcycles and a new version appears on PyPI, you
can update your installation by appending the option ``--upgrade`` above.

Use without installation
^^^^^^^^^^^^^^^^^^^^^^^^

To use the package without installing, download the package as a ``.zip`` or
``.tar.gz``-file either from `PyPI <https://pypi.org/project/admcycles/>`_ or
from `gitlab
<https://gitlab.com/modulispaces/admcycles/-/archive/master/admcycles-master.zip>`__.
Unpack the ``.zip`` or ``.tar.gz`` file. This creates a folder which should
contain a file ``setup.py``. In order to use the
module, you need to run Sage from this folder. For example, if the full path of
this folder is ``/u/You/Downloads/admcycles``, you could do::

    $ cd /u/You/Downloads/admcycles
    $ sage

Or directly inside a Sage session::

    sage: cd /u/You/Downloads/admcycles

If you run Sage in Windows using cygwin, the path above should be a cygwin path
and will looks something like
``/cygdrive/c/Users/You/Downloads/admcycles-master``.

Example
-------

To start using admcycles, start a Sage session (either in the command line, or
a Jupyter notebook, or inside one of the online services). Then type::

    sage: from admcycles import *

To try a first computation, you can compute the degree of the class kappa_1 on
Mbar_{1,1} by::

    sage: kappaclass(1,1,1).evaluate()
    1/24

You can have a look at the above computation directly in `SageMathCell <https://sagecell.sagemath.org/?z=eJxLK8rPVUhMyU2uTM5JLVbIzC3ILypR0OLlyk4sKEhMzkksLtYw1FEAIU291LLEnNLEklQNTQAYbhIb&lang=sage&interacts=eJyLjgUAARUAuQ==>`__.

Here is a more advanced computation::

    sage: t1 = 3*sepbdiv(1,(1,2),3,4) - psiclass(4,3,4)^2
    sage: t1
    Graph :      [1, 2] [[1, 2, 5], [3, 4, 6]] [(5, 6)]
    Polynomial : 3*
    <BLANKLINE>
    Graph :      [3] [[1, 2, 3, 4]] []
    Polynomial : (-1)*psi_4^2
  
To use diffstrata, the package must be imported separately. Type::

    sage: from admcycles.diffstrata import *

To try a first computation, you can compute the Euler characteristic of the
minimal stratum H(2) in genus 2::

    sage: X = Stratum((2,))
    sage: X.euler_characteristic()
    -1/40

Here is a more advanced computation::

    sage: X = Stratum((1,1))
    sage: (X.xi^2 * X.psi(1) * X.psi(2)).evaluate()
    -1/720

Building documentation
----------------------

The documentation is available online at https://modulispaces.gitlab.io/admcycles/

You can alternatively build the documentation as follows. Go in the repository
docs/ and then run in a console::

    $ sage -sh
    (sage-sh)$ make html
    (sage-sh)$ exit

The documentation is then available in the folder docs/build/html/. Note that you
need the package `nbsphinx <https://nbsphinx.readthedocs.io/en/0.8.12/>`_ to compile
the full documentation including the example Jupyter notebooks. On most systems, you
should be able to install nbsphinx by typing::

    $ sage -pip install nbsphinx

Running doctests
----------------

To run doctests, use the following command::

    $ sage -t --force-lib admcycles/ docs/source

If it succeeds, you should see a message::

    All tests passed!

License
-------

admcycles is distributed under the terms of the GNU General Public License (GPL)
published by the Free Software Foundation; either version 2 of
the License, or (at your option) any later version. See http://www.gnu.org/licenses/.

Authors
-------

- `Aaron Pixton <http://www-personal.umich.edu/~pixton/>`_
- `Johannes Schmitt <http://www.math.uni-bonn.de/~schmitt/>`_
- `Vincent Delecroix <http://www.labri.fr/perso/vdelecro/>`_
- `Jason van Zelm <https://sites.google.com/view/jasonvanzelm>`_
- `Jonathan Zachhuber <https://www.uni-frankfurt.de/50278800>`_

Funding
-------
Johannes Schmitt was supported by the grant SNF-200020162928 and has received funding
from the European Research Council (ERC) under the European Union Horizon 2020 research
and innovation programme (grant agreement No 786580). He also profited from the SNF Early 
Postdoc.Mobility grant 184245 and also wants to thank the Max Planck Institute for Mathematics 
in Bonn for its hospitality.
Vincent Delecroix was a guest of the Max-Planck Institut and then of the Hausdorff Institut
for Mathematics during the development of the project.
Jason van Zelm was supported by the Einstein Foundation Berlin during the course of this
work.
