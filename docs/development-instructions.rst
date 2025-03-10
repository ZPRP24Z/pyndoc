Development instructions
========================

Installation
------------

This project uses poetry as its packaging and dependency manager.

To install it follow `poetry instalation
guide <https://python-poetry.org/docs/#installation>`__

Managing dependencies
---------------------

Do not manage them by manually changing the ``pyproject.toml`` file.
Better way to manage dependencies is through poetry commands.

Adding dependencies
~~~~~~~~~~~~~~~~~~~

Simply run: ``poetry add <package_name> -G <group>`` Group could be for
example: ``test``, ``dev`` or ``docs`` To specify package version you
should use syntax: ``<package_name>@<version>``. Version can be
something like ``^4.0.0``, ``^3.0``, ``^4`` or simply ``latest``.
Otherwise poetry will automatically find a suitable version constraint
and install the package and sub-dependencies. For more information read
`poetry version constraint
documentation <https://python-poetry.org/docs/dependency-specification/#version-constraints>`__.

Removing dependencies
~~~~~~~~~~~~~~~~~~~~~

To remove dependency just run ``poetry remove <package_name>`` This
command changes pyprojet.toml

Validating dependencies
~~~~~~~~~~~~~~~~~~~~~~~

Run: ``poetry check``. It validates the content of pyproject.toml and
its consistency with poetry.lock. If everything is alright you should
recieve: ``All set!``

Installing dependencies
~~~~~~~~~~~~~~~~~~~~~~~

Simply run ``poetry install`` Poetry configuration is specified in file
``poetry.toml``. Currently we have there only:

::

   [virtualenvs]
   in-project = true

So running ``poetry install`` will trigger virtual environment creation
in ``{project-dir}.venv``

Running commands in virtual environment
---------------------------------------

Single command
~~~~~~~~~~~~~~

To run a single command use:

::

   poetry run <command>

The command can be something like: ``pytest``, ``tox`` or any other
command.

Using venv shell
~~~~~~~~~~~~~~~~

To spawn a shell within a project's virtual environment run:

::

   poetry shell

It is useful when you need to run multiple commands inside virtual
environment. So for example instead of running ``poetry run <command>``,
you just type the command.

Exiting venv shell
^^^^^^^^^^^^^^^^^^

To properly exit the venv shell run: ``exit``
