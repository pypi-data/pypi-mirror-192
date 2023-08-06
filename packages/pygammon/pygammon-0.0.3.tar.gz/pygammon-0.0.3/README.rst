pygammon
========

Backgammon engine core
----------------------

.. image:: https://img.shields.io/pypi/v/pygammon.svg
   :target: https://pypi.org/project/pygammon/
   :alt: PyPI

.. image:: https://img.shields.io/pypi/l/pygammon.svg
   :target: https://pypi.org/project/pygammon/
   :alt: PyPI - License

.. image:: https://img.shields.io/pypi/pyversions/pygammon.svg
   :target: https://pypi.org/project/pygammon/
   :alt: PyPI - Python Version

.. image:: https://codecov.io/gh/amikrop/pygammon/branch/main/graph/badge.svg
   :target: https://codecov.io/gh/amikrop/pygammon
   :alt: Coverage

.. image:: https://img.shields.io/circleci/build/github/amikrop/pygammon
   :target: https://dl.circleci.com/status-badge/redirect/gh/amikrop/pygammon/tree/main
   :alt: CircleCI

.. image:: https://readthedocs.org/projects/pygammon/badge/?version=latest
    :target: https://pygammon.readthedocs.io/en/latest/?badge=latest
    :alt: Documentation Status

*pygammon* is the base of a `backgammon <https://en.wikipedia.org/wiki/Backgammon>`_ engine,
written in Python. It provides the core functionality for running a game, given a source of
input (player moves) and a destination for output (game state/events).

Installation
------------

The following Python versions are supported:

    - CPython: 3.8, 3.9, 3.10, 3.11, 3.12
    - PyPy: 3.8

- Install via `pip <https://packaging.python.org/tutorials/installing-packages/>`_:

.. code-block:: bash

   $ pip install pygammon

Usage
-----

To build a complete game, you have to provide a function for getting each side's moves (input),
and a function for informing each side about the game state and events (output):

.. code-block:: python

   from typing import Optional, Tuple, Union
   from pygammon import GameState, InputType, InvalidMoveCode, OutputType, Side, run

   def receive_input(side: Side) -> Tuple[InputType, Optional[Tuple[int, Optional[int]]]]:
       # Return move of given side
       ...

   def send_output(
       output_type: OutputType,
       data: Union[GameState, Tuple[int, int], InvalidMoveCode, Side],
       side: Optional[Side] = None,
   ) -> None:
       # Show output to given side
       ...

   run(receive_input, send_output)

The input function could send to the game, moves made in any way (calculated by AI, read from stdin,
selected from GUI, either locally or through network). Similarly, the output function could do anything
with the info it gets from the game (inform AI tactics, write to stdout, show to GUI, either locally or
through network).

For more details, see the `protocol <https://pygammon.readthedocs.io/en/latest/protocol.html>`_.

License
-------

Distributed under the `MIT License <https://github.com/amikrop/pygammon/blob/master/LICENSE>`_.
