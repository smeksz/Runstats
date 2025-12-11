# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'window.ui'
##
## Created by: Qt User Interface Compiler version 6.10.1
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QLabel, QLayout, QSizePolicy,
    QVBoxLayout, QWidget)

class Ui_Runstats(object):
    def setupUi(self, Runstats):
        if not Runstats.objectName():
            Runstats.setObjectName(u"Runstats")
        Runstats.resize(571, 654)
        self.widget = QWidget(Runstats)
        self.widget.setObjectName(u"widget")
        self.widget.setGeometry(QRect(0, 0, 571, 421))
        self.verticalLayout = QVBoxLayout(self.widget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setSizeConstraint(QLayout.SizeConstraint.SetDefaultConstraint)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.title_label = QLabel(self.widget)
        self.title_label.setObjectName(u"title_label")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.title_label.sizePolicy().hasHeightForWidth())
        self.title_label.setSizePolicy(sizePolicy)
        font = QFont()
        font.setPointSize(25)
        font.setBold(True)
        self.title_label.setFont(font)
        self.title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.verticalLayout.addWidget(self.title_label)

        self.picture_test = QLabel(self.widget)
        self.picture_test.setObjectName(u"picture_test")
        self.picture_test.setMinimumSize(QSize(300, 300))
        self.picture_test.setMaximumSize(QSize(16777215, 300))
        self.picture_test.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.verticalLayout.addWidget(self.picture_test)

        self.label_2 = QLabel(self.widget)
        self.label_2.setObjectName(u"label_2")
        sizePolicy.setHeightForWidth(self.label_2.sizePolicy().hasHeightForWidth())
        self.label_2.setSizePolicy(sizePolicy)
        self.label_2.setLayoutDirection(Qt.LayoutDirection.LeftToRight)
        self.label_2.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.verticalLayout.addWidget(self.label_2)


        self.retranslateUi(Runstats)

        QMetaObject.connectSlotsByName(Runstats)
    # setupUi

    def retranslateUi(self, Runstats):
        Runstats.setWindowTitle(QCoreApplication.translate("Runstats", u"Runstats", None))
        self.title_label.setText(QCoreApplication.translate("Runstats", u"Runstats - Developed by smeks", None))
        self.picture_test.setText("")
        self.label_2.setText(QCoreApplication.translate("Runstats", u"Another label", None))
    # retranslateUi

