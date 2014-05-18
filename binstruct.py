# binstruct is a Python library for reading writing binary data sources via
# structures
# Copyright (C) 2014  Silvan Wegmann
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.


def big_endian(original_class):
    orig_init = original_class.__init__

    def __init__(self, *args, **kwargs):
        orig_init(self, *args, **kwargs)
        self.endian = "big"

    original_class.__init__ = __init__
    return original_class


class Field(object):
    def __init__(self, start, size):
        self.start = start
        self.size = size


class NumericField(Field):
    def __get__(self, instance, owner):
        start = instance.start_offset + self.start
        values = instance.array[start:start+self.size]
        powers = range(len(values))
        powers = map(lambda x: 256**x, powers)
        if instance.endian == "big":
            powers = reversed(list(powers))
        summands = map(int.__mul__, values, powers)
        return sum(summands)

    def validate_set_value(self, value):
        if value >= 2**(self.size*8):
            raise ValueError("%u does not fit in this field" % value)

    def __set__(self, instance, value):
        self.validate_set_value(value)
        powers = []
        for i in range(self.size):
            powers.append(int(value % 256))
            value //= 256
        if instance.endian == "big":
            powers = list(reversed(powers))
        powers.extend(self.size*[0])

        start = instance.start_offset + self.start

        instance.array[start:start+self.size] = powers[0:self.size]


class Int8Field(NumericField):
    def __init__(self, start):
        NumericField.__init__(self, start, 1)


class UInt8Field(NumericField):
    def __init__(self, start):
        NumericField.__init__(self, start, 1)


class Int16Field(NumericField):
    def __init__(self, start):
        NumericField.__init__(self, start, 2)


class UInt16Field(NumericField):
    def __init__(self, start):
        NumericField.__init__(self, start, 2)


class Int32Field(NumericField):
    def __init__(self, start):
        NumericField.__init__(self, start, 4)


class UInt32Field(NumericField):
    def __init__(self, start):
        NumericField.__init__(self, start, 4)


class StringField(Field):
    def __init__(self, start, length):
        Field.__init__(self, start, length)

    def __get__(self, instance, owner):
        start = instance.start_offset + self.start
        values = instance.array[start:start+self.size]
        return "".join(map(chr, values))

    def __set__(self, instance, value):
        assert len(value) <= self.size
        start = instance.start_offset + self.start
        instance.array[start:start+len(value)] = list(map(ord, value))


class Subrange(object):
    """A sub range behaves like a list. It returns and modifies the values of
    an other list by selecting a subrange of it."""
    def __init__(self, array, start_offset, length):
        self.array = array
        self.start_offset = start_offset
        self.length = length

    def __len__(self):
        return self.length

    def __getitem__(self, key):
        if type(key) == slice:
            return self.array[self.start_offset + key.start:
                              self.start_offset + key.stop]
        else:
            return self.array[self.start_offset + key]

    def __setitem__(self, key, value):
        if type(key) == slice:
            self.array[self.start_offset + key.start:
                       self.start_offset + key.stop] = value
        else:
            self.array[self.start_offset + key] = value


class RawField(Field):
    def __init__(self, start, size):
        self.start = start
        self.size = size

    def __get__(self, instance, owner):
        return Subrange(instance.array, instance.start_offset + self.start,
                        self.size)

    def __set__(self, instance, value):
        raise ValueError("Cannot set a raw type field directly")


class NestedStructField(Field):
    def __init__(self, start, nested_structure_type):
        self.start = start
        self.nested_structure_type = nested_structure_type

    def __get__(self, instance, owner):
        return self.nested_structure_type(instance.array, self.start)

    def __set__(self, instance, value):
        raise ValueError("Cannot set a nested structure")


class ClassWithLengthMetaType(type):
    def __len__(self):
        return self.clslength()

ClassWithLength = ClassWithLengthMetaType('ClassWithLength', (object, ), {})


class StructTemplate(ClassWithLength):
    def __init__(self, array, start_offset):
        self.array = array
        self.start_offset = start_offset
        self.endian = "little"

    @classmethod
    def clslength(cls):
        len = 0
        for attr in cls.__dict__.values():
            if isinstance(attr, Field):
                len = max(len, attr.start + attr.size)
        return len

    def __len__(self):
        return len(self.__class__)

    def set_endianess(self, endianess):
        self.endian = endianess
