import unittest
from PySide2.QtGui import QGuiApplication
_instance = None


class UsesQApp(unittest.TestCase):
    qapplication = True

    def setUp(self):
        super(UsesQApp, self).setUp()
        global _instance
        if _instance is None:
            _instance = QGuiApplication()
        self.app = _instance

    def tearDown(self):
        del self.app
        super(UsesQApp, self).tearDown()
