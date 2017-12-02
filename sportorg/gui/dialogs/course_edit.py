import logging
import sys

from PyQt5.QtCore import QModelIndex
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QFormLayout, QLabel, \
    QLineEdit, QApplication, QDialog, \
    QPushButton, QSpinBox, QTextEdit

from sportorg import config
from sportorg.gui.global_access import GlobalAccess
from sportorg.gui.utils.custom_controls import AdvComboBox
from sportorg.language import _
from sportorg.models.memory import race, Course, CourseControl


def get_course_types():
    return [_('order'), _('free'), _('marked route')]


class CourseEditDialog(QDialog):
    def __init__(self, table=None, index=None):
        super().__init__()
        if table is not None:
            self.table = table
            self.current_index = index

            assert (isinstance(index, QModelIndex))
            current_object = race().courses[index.row()]
            assert (isinstance(current_object, Course))
            self.current_object = current_object

    def exec(self):
        self.init_ui()
        self.set_values_from_table()
        return super().exec()

    def close_dialog(self):
        self.close()

    def init_ui(self):
        self.setWindowTitle(_('Course properties'))
        self.setWindowIcon(QIcon(config.ICON))
        self.setSizeGripEnabled(False)
        self.setModal(True)

        self.layout = QFormLayout(self)

        self.label_name = QLabel(_('Name'))
        self.item_name = QLineEdit()
        self.layout.addRow(self.label_name, self.item_name)

        self.label_type = QLabel(_('Type'))
        self.item_type = AdvComboBox()
        self.item_type.addItems(get_course_types())
        self.layout.addRow(self.label_type, self.item_type)

        self.label_length = QLabel(_('Length'))
        self.item_length = QSpinBox()
        self.item_length.setMaximum(100000)
        self.item_length.setSingleStep(100)
        self.item_length.setValue(0)
        self.layout.addRow(self.label_length, self.item_length)

        self.label_climb = QLabel(_('Climb'))
        self.item_climb = QSpinBox()
        self.item_climb.setValue(0)
        self.item_climb.setMaximum(10000)
        self.item_climb.setSingleStep(10)
        self.layout.addRow(self.label_climb, self.item_climb)

        self.label_control_qty = QLabel(_('Point count'))
        self.item_control_qty = QSpinBox()
        self.layout.addRow(self.label_control_qty, self.item_control_qty)

        self.label_controls = QLabel('{}\n\n31 150\n32 200\n33\n34 500\n...\n90 150'.format(_('Controls')))
        self.item_controls = QTextEdit()
        self.layout.addRow(self.label_controls, self.item_controls)

        def cancel_changes():
            self.close()

        def apply_changes():
            try:
                self.apply_changes_impl()
            except Exception as e:
                logging.exception(str(e))
            self.close()

        self.button_ok = QPushButton(_('OK'))
        self.button_ok.clicked.connect(apply_changes)
        self.button_cancel = QPushButton(_('Cancel'))
        self.button_cancel.clicked.connect(cancel_changes)
        self.layout.addRow(self.button_ok, self.button_cancel)

        self.show()

    def set_values_from_table(self):

        self.item_name.setText(self.current_object.name)

        if self.current_object.type:
            self.item_type.setCurrentText(str(self.current_object.type))
        if self.current_object.length:
            self.item_length.setValue(self.current_object.length)
        if self.current_object.climb:
            self.item_climb.setValue(self.current_object.climb)
        if self.current_object.controls:
            self.item_control_qty.setValue(len(self.current_object.controls))
        for i in self.current_object.controls:
            assert isinstance(i, CourseControl)
            self.item_controls.append('{} {}'.format(i.code, i.length if i.length else ''))

    def apply_changes_impl(self):
        changed = False
        course = self.current_object

        if course.name != self.item_name.text():
            course.name = self.item_name.text()
            changed = True

        if str(course.type) != self.item_type.currentText():
            course.type = self.item_type.currentText()
            changed = True

        if course.length != self.item_length.value():
            course.length = self.item_length.value()
            changed = True

        if course.climb != self.item_climb.value():
            course.climb = self.item_climb.value()
            changed = True

        text = self.item_controls.toPlainText()

        if len(course.controls) == 0 and len(text):
            changed = True

        course.controls.clear()
        for i in text.split('\n'):
            control = CourseControl()
            if i is None or len(i) == 0:
                continue
            control.code = i.split()[0]
            if len(i.split()) > 1:
                try:
                    control.length = int(i.split()[1])
                except Exception as e:
                    logging.exception(str(e))
                    control.length = 0
            course.controls.append(control)

        if changed:
            GlobalAccess().get_main_window().refresh()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = CourseEditDialog()
    sys.exit(app.exec_())