from ncTools.mods import dock;              reload(dock)
from PySide2 import QtGui, QtCore, QtWidgets

def ExampleDock():
    '''
    Entry point to call ui from maya.
    '''
    DockManager.show()

class DockManager(dock.DockManager):
    '''
    overridden
    '''
    def __init__(self):
        super(DockManager, self).__init__()
        self.window_name = 'example_window'
        self.mixin_cls = lambda: dock.MayaMixin(window_name=self.window_name,
                                                           main_widget_cls=ExampleMainWidget,
                                                           title='Example Window')

class ExampleMainWidget(QtWidgets.QWidget):
    def __init__(self):
        '''
        Main widget
        '''
        super(ExampleMainWidget, self).__init__()
        layout = QtWidgets.QVBoxLayout()
        self.setLayout(layout)
        btn = QtWidgets.QPushButton('test')
        layout.addWidget(btn)

        # signal
        btn.pressed.connect(self.print_test)

    def print_test(self):
        print 'test'
