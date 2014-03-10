=========
binstruct
=========

The binstruct library allows you to access binary data using a predefined
structure. The binary data can be provided in any form that allows an indexed
access to single bytes. This could for example be an mmaped file. The data
structure itself is defined in way similar to Django database table definitions
by declaring a new class with its fields.

Simple Example
--------------

First you have to define the structure which you want to use to access your
binary data. This is done by specifying all desired fields with their types and
their position inside a new class. As an example let's take the first of the
ELF header which in C would look like this

.. code-block:: c

    #define EI_NIDENT 16

    typedef struct {
        unsigned char e_ident[EI_NIDENT];
        uint16_t      e_type;
        uint16_t      e_machine;
        uint32_t      e_version;
        // rest of the fields omitted for simplicity
    } ElfN_Ehdr;

Using binstruct you now declare the following Python class

.. code-block:: python

    from binstruct import *

    class ElfN_Ehdr(StructTemplate):
        e_ident = RawField(0, 16)
        e_type = UInt16Field(16)
        e_machine = UInt16Field(18)
        e_version = UInt32Field(20)

Note that you have to specify the offset of the fields even though it would be
possible to derive that from the size of the previous fields. I opted for this
solution because it makes the implementation easier and because it allows for
easier skipping of irrelevant or reserved fields.

Now we can create an instance of this class by providing the constructor an
indexable data structure and an offset. The indexable data structure is any
Python object representing binary data to which you want to have "structured
access". The offset allows you to place the structure at any place inside the
indexable data structure.

For this example lets just use a simple list for the binary data

.. code-block:: python

    binary_data = 24 * [0]
    header = ElfN_Ehdr(binary_data, 0)

Now you can simply read and write any of the fields

.. code-block:: python

    header.e_type = 0x0
    header.e_ident[0] = 0x7f
    header.e_ident[1] = ord('E')
    header.e_ident[2] = ord('L')
    header.e_ident[3] = ord('F')

    print(header.e_type)
    print(header.e_ident[1])

The current implementation provides signed and unsigned fields for 8-bit,
16-bit and 32-bit integers, strings, raw data fields and even nested
structures. For some ideas of how to use them, also checkout the unit tests.

Contributing
------------

The library is fully standalone and only requires py.test to run the unit
tests. To contribute any changes simply clone the project on GitHub:
https://github.com/Jokymon/binstruct, push your changes to your own GitHub
project and send a pull request. For any changes please make sure you have good
unit tests.
