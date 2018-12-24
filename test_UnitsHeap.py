import unittest
from ui.units.BasicUnit import BasicUnit
from ui.units.UnitsHeap import UnitsHeap
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
        self.unit_b.uid = 13
        self.unit_c = BasicUnit(gameconfig=None)
        self.unit_c.worldPos.x = 5
        self.unit_c.worldPos.y = 3
        self.unit_c.uid = 45
        self.unit_d = BasicUnit(gameconfig=None)
        self.unit_d.worldPos.x = 6
        self.unit_d.worldPos.y = 7
        self.unit_d.uid = 55

        self.set_a = {self.unit_a, self.unit_b, self.unit_c}
        self.set_b = {self.unit_a, self.unit_d}

        self.heap_1 = UnitsHeap()
        for u in self.set_a:
            self.heap_1.add(u)
        pass

    def test_add_to_heap(self):
        self.assertEqual(self.heap_1.len, len(self.set_a))

    def test_remove_from_heap(self):
        self.heap_1.remove(self.unit_b)
        self.assertEqual(self.heap_1.units, {self.unit_a, self.unit_c})

    def test_update_to_heap(self):
        self.heap_1.update_units(self.set_b)
        self.assertEqual(self.heap_1.units, self.set_b)

    def test_change_and_update_to_heap(self):
        self.unit_d.uid = 32
        self.heap_1.update_units(self.set_a)
        self.assertEqual(self.heap_1.units, self.set_a)
        # self.assertTrue(self.heap_1.units == self.set_a)




if __name__ == '__main__':
    unittest.main()

