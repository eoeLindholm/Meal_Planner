#Qt Imports
from PySide2 import QtWidgets, QtCore
from PySide2.QtCore import Slot, Qt
from PySide2.QtGui import QFont
from PySide2.QtWidgets import (QLabel, QLineEdit,
                               QPushButton, QTableWidget, QTableWidgetItem,
                               QVBoxLayout, QWidget, QTextEdit, QHBoxLayout, QCheckBox, QFrame)


class MealPlanWidget(QWidget):
    def __init__(self):
        QWidget.__init__(self)

        self.title_font = QFont("Arial", 32, QFont.Bold)
        self.day_font = QFont("Arial", 16, QFont.DemiBold)
        self.general_font = QFont("Arial", 10, QFont.StyleNormal)

        #Meal planner
        self.title_label = QLabel("Meal Planner")
        self.title_label.setFixedHeight(60)
        self.title_label.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        self.title_label.setFont(self.title_font)

        self.monday_layout = self.get_day_layout("Monday")
        self.tuesday_layout = self.get_day_layout("Tuesday")
        self.wednesday_layout = self.get_day_layout("Wednesday")
        self.thursday_layout = self.get_day_layout("Thursday")
        self.friday_layout = self.get_day_layout("Friday")
        self.saturday_layout = self.get_day_layout("Saturday")
        self.sunday_layout = self.get_day_layout("Sunday")

        self.plan_week_button = QPushButton("Plan Week")
        self.plan_week_button.setFont(self.day_font)
        self.plan_week_button.setFixedHeight(50)

        self.meal_plan_layout = QVBoxLayout()
        self.meal_plan_layout.addWidget(self.title_label)
        self.meal_plan_layout.addLayout(self.monday_layout)
        self.meal_plan_layout.addLayout(self.tuesday_layout)
        self.meal_plan_layout.addLayout(self.wednesday_layout)
        self.meal_plan_layout.addLayout(self.thursday_layout)
        self.meal_plan_layout.addLayout(self.friday_layout)
        self.meal_plan_layout.addLayout(self.saturday_layout)
        self.meal_plan_layout.addLayout(self.sunday_layout)
        self.meal_plan_layout.addWidget(self.plan_week_button)
        self.setLayout(self.meal_plan_layout)

    def get_day_layout(self, day_text):
        day_label = QLabel(day_text)
        day_label.setFixedWidth(120)
        day_label.setFixedHeight(50)
        day_label.setFont(self.day_font)
        day_label.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)

        gen_day_button = QPushButton("Plan day")
        gen_day_button.setFont(self.general_font)
        gen_day_button.font().setBold(False)

        use_day_check = QCheckBox("Use: ")
        use_day_check.setLayoutDirection(QtCore.Qt.RightToLeft)
        use_day_check.setChecked(True)
        use_day_check.setFont(self.general_font)
        day_layout = QHBoxLayout()
        day_layout.addWidget(day_label)
        day_layout.addWidget(use_day_check)

        info_layout = QVBoxLayout()
        info_layout.addLayout(day_layout)
        info_layout.addWidget(gen_day_button)

        day_text_edit = QTextEdit()
        day_text_edit.setFont(self.general_font)

        #Create, fill and return the day layout
        day_layout = QHBoxLayout()
        day_layout.addLayout(info_layout)
        day_layout.addWidget(day_text_edit)

        return day_layout
