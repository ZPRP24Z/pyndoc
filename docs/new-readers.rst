Guide to adding new AST readers
===============================

Pyndoc's reader functions in a way that makes it independent of the
language being processed, the structure of syntax tree makes it simple
to add new blocks or modify existing ones.

AST Blocks
----------

AST blocks are divided into two subcategories:

-  *Atom blocks* - cannot hold other blocks inside of them
-  *Composite blocks* - can hold other blocks inside of them

The reader will treat these two types completely independently and has a
different way for reading them

Default AST Blocks
~~~~~~~~~~~~~~~~~~

The default representation of AST Blocks has been defined in
``pyndoc.ast.blocks`` and contains definitions for most blocks found in
any markup language. Any language parser or reader added to ``pyndoc``
should define these blocks

The blocks defined in the aforementioned file all derive from either the
``ASTAtomBlock`` or ``ASTCompositeBlock`` class, found in
``pyndoc.ast.basic_blocks``. These classes define the default behaviour
and contents of Atom and Composite blocks

Read Handler
~~~~~~~~~~~~

A read handler is a class containing default methods for parsing tokens
related to certain AST Blocks, every AST Block derives from a Read
Handler, allowing for custom reading functions and definitions

CompositeReadHandler
^^^^^^^^^^^^^^^^^^^^

A class defining the Read Handler for all composite blocks, it contains
attributes related to the **start** and **end** patterns of a Composite
Block, as well as information whether the block is an **inline** block
(if it can exist on its own, not wrapped in any other composite block)

``CompositeReadHandler`` contains the following methods important for
creating new readers:

-  ``process_read`` - invoked after a block is created, can process
   additional arguments after a block's definition, by default - does
   nothing
-  ``start`` - matches a token against a start pattern
-  ``end`` - matches a token against an end pattern
-  ``handle_premature_closure`` - special handling of any situation in
   which the file has ended and the block needs extra processing

AtomReadHandler
^^^^^^^^^^^^^^^

A class defining the Read Handler for atom blocks, contains attributes
related to the pattern that matches an atom block, and a boolean
indicating if the block has any content (for example: a Str block will
have a string as the content, and a Space block won't have anything)

``AtomReadHandler`` contains the following methods important for
creating new readers

-  ``match_pattern`` - matches the token against the block's pattern

Atom Wrapper
~~~~~~~~~~~~

An atom wrapper is a block that will catch, and wrap around any atom or
inline blocks that are defined without any context existing, most of the
time, ``ast.Para`` will be used for this, but any other function can be
used as well

Defining a reader
-----------------

New readers can be defined in the ``src/pyndoc/readers`` directory.

First create a directory with the language's name, inside of the
directory, create an empty ``__init__.py`` file.

.. _tokenspy:

tokens.py
~~~~~~~~~

``tokens.py`` is a required file for each language reader, it contains
details on all tokens and their start and end patterns, it will be used
to define attribute values for AST Blocks

A ``tokens.py`` file should contain the following definitions:

-  A ``declared_tokens`` dict, containing a specific **AST Block class**
   as a key, and a tuple containing a regex pattern defining the block's
   start, and a boolean as a value. The boolean will be used as the
   ``is_inline`` attribute
-  A ``declared_ends`` dict, containing information on declared end
   patterns, key values are same as above, values are **just** the
   **regex pattern**
-  an ``atom_wrapper`` variable - containing the class name for the atom
   wrapper
-  A ``declared_atomic_patterns`` dict - keys as above, values are a
   tuple containing a regex string for each atomic pattern, and a
   boolean indicating if the block has any contents

Default block processing
------------------------

The reader goes over a file character by character and forms *tokens*
that are then matched, by the parser, against the patterns defined in
``tokens.py``. With the default bahaviour of all read handles, the
reader will do the following for each read character:

1. Check if the currently processed block has ended:

   -  Run the ``end`` method of a read handler, it will return a match
      and a new token
   -  If there is a match, pop the current block from the context tree,
      and place it into the parsed tree if the context is empty, or into
      the block below it otherwise

2. Check if a new block has started:

   -  Run the ``start`` method of a read handler, it will return a match
      and a new token
   -  if the block is an inline block, it will be wrapped in an atom
      handler first
   -  Add the block to the context tree

3. Check if an atom block has **ended**

   -  Check if an atom block has been matched in a previous iteration,
      and does not match now, the ``match_pattern`` method is used for
      this
   -  this indicates that the atom block has ended
   -  insert the atom block into the current context, or wrap it around
      the atom wrapper if there is no context.

Defining custom blocks
----------------------

Custom blocks can be defined within a language module (directory under
``pyndoc/readers``) in its own ``blocks.py`` file, custom behaviour such
as overriden ``start()``, ``end()`` and ``process_read()`` methods can
be defined here

Examples
~~~~~~~~

*All of these can be found under ``pyndoc.ast.gfm.blocks``*

Getting a header level from a matched string

.. code:: python

   class Header(ast.Header):
       def __init__(self) -> None:
           super().__init__()

       def process_read(self, **kwargs: Unpack[ast_helpers.ProcessParams]) -> None:
           match = kwargs["match"]
           level = len(match.group("h"))
           self.contents.metadata = [level]

Handling premature closure of an Emph

.. code:: python

     @classmethod
       def handle_premature_closure(cls, token: str) -> str:
           return token[:-1] if token[-1] == "*" else token

Adding a `Plain` inside of a newly created bullet list

.. code:: python

       def process_read(self, **kwargs: Unpack[ast_helpers.ProcessParams]) -> None:
           match = kwargs["match"]
           indent = len(match.group("s"))
           self.contents.metadata = [indent]
           self.add_plain(kwargs["context"])

       @staticmethod
       def add_plain(context: list) -> None:
           plain = ast.Plain()
           context.append(plain)

