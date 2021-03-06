import logging

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QModelIndex
from PyQt5.QtWidgets import QAbstractItemView, QHeaderView, QTextEdit

from sportorg.core.broker import Broker
from sportorg.gui.dialogs.results_edit import ResultEditDialog
from sportorg.gui.tabs.memory_model import ResultMemoryModel
from sportorg.gui.tabs.table import TableView
from sportorg.language import _
from sportorg.models.memory import race, Result, Course, CourseControl
from sportorg.utils.time import time_to_hhmmss


class ResultTable(TableView):
    def __init__(self, parent, obj):
        super().__init__(obj)

        self.parent_widget = parent
        self.setObjectName("ResultTable")

        self.setModel(ResultMemoryModel())
        self.setSortingEnabled(True)
        self.setSelectionBehavior(QAbstractItemView.SelectRows)

        self.clicked.connect(self.entry_single_clicked)
        self.activated.connect(self.double_clicked)

        self.popup_items = []

        Broker().subscribe('refresh', self.update_splits, 1)

    def update_splits(self):
        if -1 < self.currentIndex().row() < len(race().results):
            self.parent_widget.show_splits(self.currentIndex())

    def keyPressEvent(self, event):
        super().keyPressEvent(event)
        try:
            if event.key() == QtCore.Qt.Key_Up or event.key() == QtCore.Qt.Key_Down:
                self.entry_single_clicked(self.currentIndex())
        except Exception as e:
            logging.error(str(e))

    def entry_single_clicked(self, index):
        try:
            #  show splits in the left area
            if -1 < index.row() < len(race().results):
                self.parent_widget.show_splits(index)
        except Exception as e:
            logging.error(str(e))

    def double_clicked(self, index):
        try:
            logging.debug('Clicked on ' + str(index.row()))
            if index.row() < len(race().results):
                dialog = ResultEditDialog(race().results[index.row()])
                dialog.exec()
                # self.selectRow(index.row()+1)
        except Exception as e:
            logging.error(str(e))


class Widget(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setup_ui()

    def setup_ui(self):
        self.gridLayout = QtWidgets.QGridLayout(self)
        self.gridLayout.setObjectName("gridLayout")
        self.ResultSplitter = QtWidgets.QSplitter(self)
        self.ResultSplitter.setOrientation(QtCore.Qt.Horizontal)
        self.ResultSplitter.setObjectName("ResultSplitter")
        self.ResultLeftPart = QtWidgets.QFrame(self.ResultSplitter)
        self.ResultLeftPart.setMaximumSize(QtCore.QSize(350, 16777215))
        self.ResultLeftPart.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.ResultLeftPart.setFrameShadow(QtWidgets.QFrame.Raised)
        self.ResultLeftPart.setObjectName("ResultLeftPart")
        self.ResultCourseGroupBox = QtWidgets.QGroupBox(self.ResultLeftPart)
        self.ResultCourseGroupBox.setObjectName("ResultCourseGroupBox")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.ResultCourseGroupBox)
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_2.setSpacing(0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.ResultCourseForm = QtWidgets.QFormLayout()
        self.ResultCourseForm.setObjectName("ResultCourseForm")
        self.ResultCourseNameLabel = QtWidgets.QLabel(self.ResultCourseGroupBox)
        self.ResultCourseNameLabel.setObjectName("ResultCourseNameLabel")
        self.ResultCourseForm.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.ResultCourseNameLabel)
        self.ResultCourseNameEdit = QtWidgets.QLineEdit(self.ResultCourseGroupBox)
        self.ResultCourseNameEdit.setObjectName("ResultCourseNameEdit")
        self.ResultCourseForm.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.ResultCourseNameEdit)
        self.ResultCourseLengthLabel = QtWidgets.QLabel(self.ResultCourseGroupBox)
        self.ResultCourseLengthLabel.setObjectName("ResultCourseLengthLabel")
        self.ResultCourseForm.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.ResultCourseLengthLabel)
        self.ResultCourseLengthEdit = QtWidgets.QLineEdit(self.ResultCourseGroupBox)
        self.ResultCourseLengthEdit.setObjectName("ResultCourseLengthEdit")
        self.ResultCourseForm.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.ResultCourseLengthEdit)
        self.verticalLayout_2.addLayout(self.ResultCourseForm)
        self.ResultCourseDetails = QtWidgets.QTextBrowser(self.ResultCourseGroupBox)
        font = QtGui.QFont()
        font.setFamily("Courier New")
        self.ResultCourseDetails.setFont(font)
        self.ResultCourseDetails.setObjectName("ResultCourseDetails")
        self.verticalLayout_2.addWidget(self.ResultCourseDetails)
        self.ResultChipGroupBox = QtWidgets.QGroupBox(self.ResultLeftPart)
        self.ResultChipGroupBox.setObjectName("ResultChipGroupBox")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.ResultChipGroupBox)
        self.verticalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_3.setSpacing(0)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.ResultChipForm = QtWidgets.QFormLayout()
        self.ResultChipForm.setObjectName("ResultChipForm")
        self.ResultChipStartLabel = QtWidgets.QLabel(self.ResultChipGroupBox)
        self.ResultChipStartLabel.setObjectName("ResultChipStartLabel")
        self.ResultChipForm.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.ResultChipStartLabel)
        self.ResultChipStartEdit = QtWidgets.QLineEdit(self.ResultChipGroupBox)
        self.ResultChipStartEdit.setObjectName("ResultChipStartEdit")
        self.ResultChipForm.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.ResultChipStartEdit)
        self.ResultChipFinishLabel = QtWidgets.QLabel(self.ResultChipGroupBox)
        self.ResultChipFinishLabel.setObjectName("ResultChipFinishLabel")
        self.ResultChipForm.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.ResultChipFinishLabel)
        self.ResultChipFinishEdit = QtWidgets.QLineEdit(self.ResultChipGroupBox)
        self.ResultChipFinishEdit.setObjectName("ResultChipFinishEdit")
        self.ResultChipForm.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.ResultChipFinishEdit)
        self.verticalLayout_3.addLayout(self.ResultChipForm)
        self.ResultChipDetails = QtWidgets.QTextBrowser(self.ResultChipGroupBox)
        font = QtGui.QFont()
        font.setFamily("Courier New")
        self.ResultChipDetails.setFont(font)
        self.ResultChipDetails.setObjectName("ResultChipDetails")
        self.verticalLayout_3.addWidget(self.ResultChipDetails)
        self.ResultTable = ResultTable(self, self.ResultSplitter)

        hor_header = self.ResultTable.horizontalHeader()
        assert (isinstance(hor_header, QHeaderView))
        hor_header.setSectionsMovable(True)
        hor_header.setDropIndicatorShown(True)
        hor_header.setSectionResizeMode(QHeaderView.ResizeToContents)
        Broker().subscribe('refresh', lambda: hor_header.setSectionResizeMode(QHeaderView.ResizeToContents))

        ver_header = self.ResultTable.verticalHeader()
        ver_header.setSectionResizeMode(QHeaderView.ResizeToContents)

        self.gridLayout.addWidget(self.ResultSplitter)
        self.ResultCourseGroupBox.setTitle(_("Course"))
        self.ResultCourseNameLabel.setText(_("Name"))
        self.ResultCourseLengthLabel.setText(_("Length"))
        # self.ResultCourseDetails.setHtml()
        self.ResultChipGroupBox.setTitle(_("Chip"))
        self.ResultChipStartLabel.setText(_("Start"))
        self.ResultChipFinishLabel.setText(_("Finish"))
        # self.ResultChipDetails.setHtml()

        Broker().subscribe('resize', self.resize_event)

    def show_splits(self, index):
        assert (isinstance(index, QModelIndex))
        result = race().results[index.row()]
        assert isinstance(result, Result)
        self.ResultChipDetails.clear()
        self.ResultChipDetails.setLineWrapMode(QTextEdit.NoWrap)
        self.ResultChipFinishEdit.setText('')
        self.ResultChipStartEdit.setText('')

        self.ResultCourseDetails.clear()
        self.ResultCourseDetails.setLineWrapMode(QTextEdit.NoWrap)
        self.ResultCourseNameEdit.setText('')
        self.ResultCourseLengthEdit.setText('')

        if result.is_manual():
            return

        course = None
        if result.person:
            course = race().find_course(result)

        control_codes = []
        is_highlight = True
        if course:
            assert isinstance(course, Course)
            is_highlight = not course.is_unknown()
            for control in course.controls:
                control_codes.append(str(control.code))

        code = ''
        index = 1
        time_accuracy = race().get_setting('time_accuracy', 0)
        for split in result.splits:
            str_fmt = '{index:02d} {code} {time} {diff}'
            if not split.is_correct:
                str_fmt = '-- {code} {time}'

            s = str_fmt.format(
                index=index,
                code=('(' + str(split.code) + ')   ')[:5],
                time=split.time.to_str(time_accuracy),
                diff=split.leg_time.to_str(time_accuracy),
                leg_place=split.leg_place,
                speed=split.speed,
            )
            if split.is_correct:
                index += 1

            if split.code == code:
                s = '<span style="background: red">{}</span>'.format(s)
            if is_highlight and len(control_codes) and split.code not in control_codes:
                s = '<span style="background: yellow">{}</span>'.format(s)

            self.ResultChipDetails.append(s)
            code = split.code

        if result.finish_time is not None:
            self.ResultChipFinishEdit.setText(time_to_hhmmss(result.finish_time))
        if result.start_time is not None:
            self.ResultChipStartEdit.setText(time_to_hhmmss(result.start_time))

        split_codes = []
        for split in result.splits:
            split_codes.append(split.code)

        if course:
            index = 1
            for control in course.controls:
                assert control, CourseControl
                s = '{index:02d} ({code}) {length}'.format(
                    index=index,
                    code=control.code,
                    length=control.length if control.length else '')
                if is_highlight and str(control.code) not in split_codes:
                    s = '<span style="background: yellow">{}</span>'.format(s)
                self.ResultCourseDetails.append(s)
                index += 1

            self.ResultCourseNameEdit.setText(course.name)
            self.ResultCourseLengthEdit.setText(str(course.length))

    def resize_event(self, koor):
        self.ResultCourseGroupBox.setGeometry(QtCore.QRect(1, 1, 120, koor['height']-140))
        self.ResultChipGroupBox.setGeometry(QtCore.QRect(120, 1, 235, koor['height']-140))
