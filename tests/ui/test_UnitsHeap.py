import unittest
from os import path
from config import pydolons_rootdir
from PySide2 import QtGui
from ui.gameworld.units.BasicUnit import BasicUnit
from ui.gameworld.units.UnitsHeap import UnitsHeap
from tests.ui.TestHelper import UsesQApp


class TestBasicUnit(UsesQApp):

    def getUnit(self, x=0, y=0, uid=0, pixmap=None):
        unit = BasicUnit(gameRoot=None)
        unit.worldPos.x = x
        unit.worldPos.y = y
        unit.uid = uid
        if pixmap is not None:
            unit.setPixmap(pixmap)
        return unit

    def setUp(self):
        super(TestBasicUnit, self).setUp()
        pic_path = path.join(pydolons_rootdir, 'resources', 'icons','default_128.png')
        pixmap = QtGui.QPixmap(pic_path)
        self.unit_a = self.getUnit(2, 1, 32, pixmap)
        self.unit_b = self.getUnit(2, 1, 13, pixmap)
        self.unit_c = self.getUnit(2, 1, 45, pixmap)
        self.unit_d = BasicUnit(gameRoot=None)
        self.unit_d.worldPos.x = 6
        self.unit_d.worldPos.y = 7
        self.unit_d.uid = 55

        self.set_a = [self.unit_a, self.unit_b, self.unit_c]
        self.set_b = [self.unit_a, self.unit_d]
        self.heap_1 = UnitsHeap()
        for u in self.set_a:
            self.heap_1.add(u)

        self.heap_2 = UnitsHeap()
        self.heap_2.update_units(self.set_a)

    def test_add_to_heap(self):
        self.assertEqual(self.heap_1.units, self.set_a)

    def test_remove_from_heap(self):
        self.heap_1.remove(self.unit_b)
        self.assertEqual(self.heap_1.units, [self.unit_a, self.unit_c])

    def test_update_to_heap(self):
        self.heap_1.update_units(self.set_b)
        self.assertEqual(self.heap_1.units, self.set_b)

    def test_change_and_update_to_heap(self):
        self.unit_d.uid = 32
        self.heap_1.update_units(self.set_a)
        self.assertEqual(self.heap_1.units, self.set_a)

    def test_getInter(self):
        self.assertTrue(self.heap_1.getInter())

    def test_get_contains_unit_c(self):
        self.assertEqual(list(self.heap_2.getContains(10, 10))[0], self.unit_c)

    def test_get_contains_unit_b_c(self):
        self.assertEqual(list(self.heap_2.getContains(60, 60))[0], self.unit_a)

    def test_getTopLayer_c(self):
        self.assertEqual(self.heap_2.getTopLayer(60, 60), self.unit_c)

    def test_getTopLayer_b(self):
        self.assertEqual(self.heap_2.getTopLayer(68, 68), self.unit_b)

    def test_getTopLayer_a(self):
        self.assertEqual(self.heap_2.getTopLayer(90, 90), self.unit_a)

    def test_getTopLayer_empty(self):
        self.assertEqual(self.heap_2.getTopLayer(120, 120), None)


if __name__ == '__main__':
    unittest.main()

