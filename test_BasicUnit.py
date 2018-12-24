import unittest
from ui.units.BasicUnit import BasicUnit
from TestHelper import UsesQApp


class TestBasicUnit(UsesQApp):
    def setUp(self):
        super(TestBasicUnit, self).setUp()
        self.unit_a = BasicUnit(gameconfig=None)
        self.unit_a.worldPos.x = 2
        self.unit_a.worldPos.y = 3
        self.unit_a.uid = 32
        self.unit_b = BasicUnit(gameconfig=None)
        self.unit_b.worldPos.x = 2
        self.unit_b.worldPos.y = 1
        self.unit_b.uid = 32
        self.unit_c = BasicUnit(gameconfig=None)
        self.unit_c.worldPos.x = 2
        self.unit_c.worldPos.y = 3
        self.unit_c.uid = 32

        self.unit_list = [self.unit_a, self.unit_b, self.unit_c]
        self.unit_set = {self.unit_a, self.unit_b, self.unit_c}
        self.unit_dict = {self.unit_a:self.unit_a.worldPos, self.unit_b:self.unit_b.worldPos, self.unit_c:self.unit_c.worldPos}
        pass

    def test_first(self):
        self.assertEqual(self.unit_a, self.unit_a)

    def test_unit_is_self(self):
        self.assertTrue(self.unit_a is self.unit_a)

    def test_unit_is_other(self):
        self.assertFalse(self.unit_a is self.unit_b)

    def test_unit_is_other_self(self):
        self.assertTrue(self.unit_a == self.unit_c)

    def test_add_to_set(self):
        self.assertTrue(len(self.unit_set) == 2)

    def test_add_to_list(self):
        self.assertTrue(len(self.unit_list) == 3)

    def test_add_to_dict(self):
        self.assertTrue(len(self.unit_dict.items()) == 2)

    def test_remove_from_set_1(self):
        self.unit_set.remove(self.unit_a)
        self.assertTrue(len(self.unit_set) == 1)

    def test_remove_from_set_2(self):
        self.unit_set.add(self.unit_a)
        self.unit_set.remove(self.unit_c)
        self.assertTrue(len(self.unit_set) == 1)


if __name__ == '__main__':
    unittest.main()

