import pytest
import binstruct


class TestSubrange:
    def testGettingSingleValue(self):
        array = range(20)

        range1 = binstruct.Subrange(array, 5, 5)

        assert range1[0] == 5
        assert range1[1] == 6

    def testGettingSlice(self):
        array = list(range(20))

        range1 = binstruct.Subrange(array, 5, 5)

        assert range1[2:5] == [7, 8, 9]

    def testSettingSingleValue(self):
        array = list(range(20))

        range1 = binstruct.Subrange(array, 3, 7)
        range1[4] = 42

        assert array[7] == 42

    def testSettingSliceValue(self):
        array = list(range(20))

        range1 = binstruct.Subrange(array, 4, 10)
        range1[3:7] = [42, 42, 42, 42]

        assert array == [0, 1, 2, 3, 4, 5, 6, 42, 42, 42, 42, 11, 12, 13, 14,
                         15, 16, 17, 18, 19]


class TestStructClass:
    def testCompactLength(self):
        class StructureUnderTest(binstruct.StructTemplate):
            field1 = binstruct.Int8Field(0)
            field2 = binstruct.StringField(1, 5)
            field3 = binstruct.Int16Field(6)
            field4 = binstruct.Int8Field(8)

        assert len(StructureUnderTest) == 9

    def testSparseLength(self):
        class StructureUnderTest(binstruct.StructTemplate):
            field1 = binstruct.RawField(0, 4)
            field2 = binstruct.Int8Field(7)
            field3 = binstruct.Int16Field(8)
            field4 = binstruct.StringField(15, 5)

        assert len(StructureUnderTest) == 20


class TestIntFields:
    def testGettingInts(self):
        class StructureUnderTest(binstruct.StructTemplate):
            int8 = binstruct.Int8Field(1)
            uint8 = binstruct.UInt8Field(2)
            int16 = binstruct.Int16Field(3)
            uint16 = binstruct.UInt16Field(5)

        array = list(range(20))
        struct = StructureUnderTest(array, 1)

        assert struct.int8 == 2
        assert struct.uint8 == 3
        assert struct.int16 == 1284
        assert struct.uint16 == 1798

    def testSettingInts(self):
        class StructureUnderTest(binstruct.StructTemplate):
            int8 = binstruct.Int8Field(1)
            uint8 = binstruct.UInt8Field(2)
            int16 = binstruct.Int16Field(3)
            uint16 = binstruct.UInt16Field(5)

        array = list(range(20))
        struct = StructureUnderTest(array, 1)
        struct.int8 = 30
        struct.uint8 = 40
        struct.int16 = 0xab9a
        struct.uint16 = 0x8498

        assert array[2] == 30
        assert array[3] == 40
        assert array[4] == 0x9a
        assert array[5] == 0xab
        assert array[6] == 0x98
        assert array[7] == 0x84

    def testGettingNestedStructs(self):
        class NestedStructure(binstruct.StructTemplate):
            value1 = binstruct.UInt8Field(0)
            value2 = binstruct.UInt8Field(1)

        class TheStructure(binstruct.StructTemplate):
            s1 = binstruct.NestedStructField(0, NestedStructure)
            s2 = binstruct.NestedStructField(2, NestedStructure)

        array = list(range(20))
        struct = TheStructure(array, 0)

        assert struct.s1.value1 == 0
        assert struct.s1.value2 == 1
        assert struct.s2.value1 == 2
        assert struct.s2.value2 == 3

    def testSettingNestedStructs(self):
        class NestedStructure(binstruct.StructTemplate):
            value1 = binstruct.UInt8Field(0)
            value2 = binstruct.UInt8Field(1)

        class TheStructure(binstruct.StructTemplate):
            s1 = binstruct.NestedStructField(0, NestedStructure)
            s2 = binstruct.NestedStructField(2, NestedStructure)

        array = list(range(20))
        struct = TheStructure(array, 0)
        struct.s1.value1 = 40
        struct.s1.value2 = 50
        struct.s2.value1 = 60
        struct.s2.value2 = 70

        assert array[0] == 40
        assert array[1] == 50
        assert array[2] == 60
        assert array[3] == 70


class TestRawField:
    def testGettingRawField(self):
        class StructureUnderTest(binstruct.StructTemplate):
            raw1 = binstruct.RawField(0, 5)
            raw2 = binstruct.RawField(7, 5)

        array = list(range(20))
        struct = StructureUnderTest(array, 3)

        assert struct.raw1[0] == 3
        assert struct.raw1[1] == 4
        assert struct.raw2[2:5] == [12, 13, 14]

    def testSettingRawField(self):
        class StructureUnderTest(binstruct.StructTemplate):
            raw1 = binstruct.RawField(0, 5)
            raw2 = binstruct.RawField(5, 5)

        array = list(range(20))
        struct = StructureUnderTest(array, 3)
        struct.raw1[0:2] = [42, 43]

        assert array[0] == 0
        assert array[1] == 1
        assert array[2] == 2
        assert array[3] == 42
        assert array[4] == 43
        assert array[5] == 5


class TestStringfield:
    def testGettingStringField(self):
        class StructureUnderTest(binstruct.StructTemplate):
            s1 = binstruct.StringField(0, 5)
            s2 = binstruct.StringField(5, 1)

        array = list(map(ord, "part1k"))
        struct = StructureUnderTest(array, 0)

        assert struct.s1 == "part1"
        assert struct.s2 == "k"

    def testGettingZeroCharacterStringField(self):
        class StructureUnderTest(binstruct.StructTemplate):
            s1 = binstruct.StringField(0, 5)
            s2 = binstruct.StringField(5, 1)

        array = 6*[0]
        struct = StructureUnderTest(array, 0)

        assert struct.s1 == 5*"\0"
        assert struct.s1[0] == "\0"
        assert struct.s2 == "\0"


class TestLittleEndian:
    def testGettingInts(self):
        class StructureUnderTest(binstruct.StructTemplate):
            int8 = binstruct.Int8Field(0)
            uint8 = binstruct.UInt8Field(1)
            int16 = binstruct.Int16Field(2)
            uint16 = binstruct.UInt16Field(4)
            int32 = binstruct.Int32Field(6)
            uint32 = binstruct.UInt32Field(10)

        array = list(range(20))
        struct = StructureUnderTest(array, 1)

        struct.set_endianess("big")

        assert struct.int8 == 1
        assert struct.uint8 == 2
        assert struct.int16 == 772
        assert struct.uint16 == 1286
        assert struct.int32 == 117967114
        assert struct.uint32 == 185339150

    def testGettingIntsWithDecorator(self):
        @binstruct.big_endian
        class StructureUnderTest(binstruct.StructTemplate):
            uint32 = binstruct.UInt32Field(0)

        array = list(range(4))
        struct = StructureUnderTest(array, 0)

        assert struct.uint32 == 66051

    def testSettingInts(self):
        @binstruct.big_endian
        class StructureUnderTest(binstruct.StructTemplate):
            int16 = binstruct.Int16Field(0)
            uint32 = binstruct.UInt32Field(2)

        array = 6 * [0]
        struct = StructureUnderTest(array, 0)
        struct.int16 = 0x3218
        struct.uint32 = 0x50a53710

        assert array[0:2] == [0x32, 0x18]
        assert array[2:6] == [0x50, 0xa5, 0x37, 0x10]

    def testSettingSmallIntsWithBigEndian(self):
        @binstruct.big_endian
        class StructureUnderTest(binstruct.StructTemplate):
            uint32 = binstruct.UInt32Field(0)

        array = 4 * [0]
        struct = StructureUnderTest(array, 0)
        struct.uint32 = 0x1234

        assert array[0:4] == [0, 0, 0x12, 0x34]
