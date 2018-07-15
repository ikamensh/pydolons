from game_objects.battlefield_objects.attributes import Attribute

def test_summation():
    attrib1 = Attribute(100, 100, 100)
    attrib2 = Attribute(10, 20, 30)

    attrib3 = attrib1 + attrib2

    assert attrib3.base == attrib1.base + attrib2.base
    assert attrib3.multiplier == attrib1.multiplier + attrib2.multiplier
    assert attrib3.bonus == attrib1.bonus + attrib2.bonus

def test_value():
    attrib1 = Attribute(100, 100, 100)
    attrib2 = Attribute(100, 150, 200)

    assert attrib1.value() == 200
    assert attrib2.value() == 350