#Qt Imports
import PySide2
from PySide2 import QtWidgets, QtCore
from PySide2.QtCore import Slot, Qt
from PySide2.QtGui import QFont
from PySide2.QtWidgets import (QApplication, QLabel, QLineEdit,
                               QPushButton, QTableWidget, QTableWidgetItem,
                               QVBoxLayout, QWidget, QTextEdit, QHBoxLayout, QCheckBox, QFrame, QFormLayout,
                               QDoubleSpinBox, QComboBox, QAbstractItemView, QSpinBox, QHeaderView)

import database_manager


class AddIngredientWidget(QWidget):
    def __init__(self, database, parent, ingredient_name):
        QWidget.__init__(self)
        self.add_ingredient_win = QWidget()
        self.add_ingredient_win.setFixedWidth(250)
        self.add_ingredient_win.setWindowTitle("Add Ingredient")
        self.add_ingredient_main_layout = QHBoxLayout()
        self.meal_planner_db = database

        self.setParent(parent)
        self.ingredient_name_input = QLineEdit()
        self.ingredient_name_input.setText(ingredient_name)

        self.calories_spinbox = QDoubleSpinBox()
        self.calories_spinbox.setMaximum(9999)
        self.carbs_spinbox = QDoubleSpinBox()
        self.carbs_spinbox.setMaximum(9999)
        self.sugar_spinbox = QDoubleSpinBox()
        self.sugar_spinbox.setMaximum(9999)
        self.fats_spinbox = QDoubleSpinBox()
        self.fats_spinbox.setMaximum(9999)
        self.protein_spinbox = QDoubleSpinBox()
        self.protein_spinbox.setMaximum(9999)

        self.add_ingredient_btn = QPushButton("Create Ingredient")
        self.add_ingredient_btn.clicked.connect(self.add_ingredient_to_recipe)
        self.cancel_win_btn = QPushButton("Cancel")
        self.cancel_win_btn.clicked.connect(self.add_ingredient_win.close)

        self.left_layout = QVBoxLayout()
        self.left_layout.addWidget(QLabel("Ingredient name"))
        self.left_layout.addWidget(self.ingredient_name_input)
        self.left_layout.addWidget(QLabel("Ingredient nutrition values"))
        self.left_layout.addWidget(QLabel("kCal/100g"))
        self.left_layout.addWidget(self.calories_spinbox)
        self.left_layout.addWidget(QLabel("carb/100g"))
        self.left_layout.addWidget(self.carbs_spinbox)
        self.left_layout.addWidget(QLabel("sugar/100g"))
        self.left_layout.addWidget(self.sugar_spinbox)
        self.left_layout.addWidget(QLabel("fat/100g"))
        self.left_layout.addWidget(self.fats_spinbox)
        self.left_layout.addWidget(QLabel("protein/100g"))
        self.left_layout.addWidget(self.protein_spinbox)
        self.left_layout.addWidget(self.add_ingredient_btn)
        self.left_layout.addWidget(self.cancel_win_btn)

        self.add_ingredient_main_layout.addLayout(self.left_layout)

        self.add_ingredient_win.setLayout(self.add_ingredient_main_layout)
        self.add_ingredient_win.show()

    @Slot()
    def add_ingredient_to_recipe(self):
        self.parent().ingredient_name_input.setText(self.ingredient_name_input.text())
        ing_id = self.meal_planner_db.get_table_len("ingredients")
        self.meal_planner_db.add_ingredient(ing_id, self.ingredient_name_input.text(),
                                            self.calories_spinbox.value(), self.carbs_spinbox.value(),
                                            self.sugar_spinbox.value(), self.fats_spinbox.value(),
                                            self.protein_spinbox.value(), False)

        self.add_ingredient_win.close()


#####################################################
class AddRecipeWidget(QWidget):
    def __init__(self, database, parent):
        QWidget.__init__(self)
        self.recipe_ingredients = 0
        self.add_recipe_win = QWidget()
        self.add_recipe_win.setFixedWidth(400)
        self.add_recipe_win.setWindowTitle("Add Recipe")
        add_rec_main_layout = QVBoxLayout()

        self.meal_planner_db = database
        self.setParent(parent)

        self.rec_name_input = QLineEdit()
        self.rec_desc_input = QLineEdit()
        self.rec_source_input = QLineEdit()
        rec_form_layout = QFormLayout()
        rec_form_layout.addRow(QLabel("Recipe Name"), self.rec_name_input)
        rec_form_layout.addRow(QLabel("Recipe Desc"), self.rec_desc_input)
        rec_form_layout.addRow(QLabel("Recipe Source"), self.rec_source_input)
        add_rec_main_layout.addLayout(rec_form_layout)

        rec_info_layout = QHBoxLayout()
        difficulty_layout = QVBoxLayout()
        self.difficulty_spinbox = QSpinBox()
        self.difficulty_spinbox.setRange(1, 5)
        self.difficulty_spinbox.setValue(3)
        difficulty_layout.addWidget(QLabel("Difficulty"))
        difficulty_layout.addWidget(self.difficulty_spinbox)

        prep_time_layout = QVBoxLayout()
        self.prep_time_spinbox = QSpinBox()
        self.prep_time_spinbox.setRange(0, 600)
        self.prep_time_spinbox.setValue(30)
        prep_time_layout.addWidget(QLabel("Prep. Time (min.)"))
        prep_time_layout.addWidget(self.prep_time_spinbox)

        rating_layout = QVBoxLayout()
        self.rating_spinbox = QSpinBox()
        self.rating_spinbox.setRange(1, 5)
        self.rating_spinbox.setValue(3)
        rating_layout.addWidget(QLabel("Rating"))
        rating_layout.addWidget(self.rating_spinbox)

        rec_info_layout.addLayout(difficulty_layout)
        rec_info_layout.addLayout(prep_time_layout)
        rec_info_layout.addLayout(rating_layout)

        add_rec_main_layout.addLayout(rec_info_layout)

        rec_tags_layout = QHBoxLayout()
        rec_cuisine_layout = QVBoxLayout()
        cuisines = ["Mexican", "Swedish", "Austrian", "Italian", "Spanish", "American", "British", "Thai", "Greek",
                    "Vietnamese", "Caribbean", "Japanese", "Chinese", "Indian", "French", "Swiss", "Portuguese",
                    "Korean", "Turkish", "Moroccan", "Russian", "Malaysian", "Philippines", "Ethiopian", "Lebanese",
                    "Arab", "Peruvian", "Brazilian", "Asian", "Middle Eastern", "South American", "African", "-"]
        cuisines.sort()
        self.tag_cuisine = QComboBox()
        self.tag_cuisine.addItems(cuisines)
        rec_cuisine_layout.addWidget(QLabel("Cuisine"))
        rec_cuisine_layout.addWidget(self.tag_cuisine)
        rec_tags_layout.addLayout(rec_cuisine_layout)

        rec_category_layout = QVBoxLayout()
        categories = ["Beef & Calf", "Chicken & Poultry", "Lamb", "Pork", "Preservation", "Salad", "Sandwich", "Soup",
                      "Stew", "Pasta", "Rice", "Grain & Beans", "Fish & Seafood", "Vegetables", "Eggs & Cheese", "BBQ",
                      "Fruits", "Cake & Pie (Sweet)", "Pie", "Bread", "Beverage", "Cookies & Sweets", "Sauce", "-"]
        categories.sort()
        self.tag_category = QComboBox()
        self.tag_category.addItems(categories)
        rec_category_layout.addWidget(QLabel("Category"))
        rec_category_layout.addWidget(self.tag_category)
        rec_tags_layout.addLayout(rec_category_layout)

        rec_meal_type_layout = QVBoxLayout()
        meal_types = ["Breakfast", "Brunch", "Lunch", "Dinner", "Dessert", "Starter", "Side", "Buffet", "Snack", "-"]
        meal_types.sort()
        self.tag_meal_types = QComboBox()
        self.tag_meal_types.addItems(meal_types)
        rec_meal_type_layout.addWidget(QLabel("Meal Type"))
        rec_meal_type_layout.addWidget(self.tag_meal_types)
        rec_tags_layout.addLayout(rec_meal_type_layout)

        add_rec_main_layout.addLayout(rec_tags_layout)

        self.ingredient_name_input = QLineEdit()
        self.ingredient_qty_input = QDoubleSpinBox()
        self.ingredient_qty_input.setValue(1.0)
        self.ingredient_qty_input.setMaximum(1000)
        self.ingredient_qty_input.setDecimals(2)
        self.ingredient_unit_input = QComboBox()
        self.ingredient_unit_input.addItems(["g", "ml", "dl", "l", "msk", "tsk", "st", "-"])
        add_ingredient_btn = QPushButton("Create ingredient")
        add_ingredient_btn.clicked.connect(self.create_ingredient)
        add_ingredient_layout = QHBoxLayout()
        add_rec_main_layout.addWidget(QLabel("Ingredient"))
        add_ingredient_layout.addWidget(self.ingredient_name_input)
        add_ingredient_layout.addWidget(self.ingredient_qty_input)
        add_ingredient_layout.addWidget(self.ingredient_unit_input)
        add_ingredient_layout.addWidget(add_ingredient_btn)
        add_rec_main_layout.addLayout(add_ingredient_layout)

        btn_layout = QHBoxLayout()
        add_ingredient_to_recipe_btn = QPushButton("Add ingredient")
        add_ingredient_to_recipe_btn.clicked.connect(self.add_ingredient_to_recipe)

        del_ingredient_from_recipe_btn = QPushButton("Remove ingredient")
        del_ingredient_from_recipe_btn.clicked.connect(self.del_ingredient_from_recipe)
        btn_layout.addWidget(add_ingredient_to_recipe_btn)
        btn_layout.addWidget(del_ingredient_from_recipe_btn)
        add_rec_main_layout.addLayout(btn_layout)

        self.rec_ingredient_table = QTableWidget()
        self.rec_ingredient_table.setColumnCount(3)
        self.rec_ingredient_table.setHorizontalHeaderLabels(["Amount", "Unit", "Ingredient"])
        header = self.rec_ingredient_table.horizontalHeader()
        header.setSectionResizeMode(0, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(1, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(2, QtWidgets.QHeaderView.Stretch)
        add_rec_main_layout.addWidget(self.rec_ingredient_table)

        self.step_count = 0
        self.add_recipe_step_btn = QPushButton("Add recipe instruction")
        add_rec_main_layout.addWidget(self.add_recipe_step_btn)
        self.add_recipe_step_btn.clicked.connect(self.add_recipe_step_win)
        self.rec_step_table = QTableWidget()
        self.rec_step_table.setColumnCount(1)
        self.rec_step_table.setHorizontalHeaderLabels(["Instructions"])
        self.rec_step_table.setWordWrap(True)
        header = self.rec_step_table.horizontalHeader()
        header.setSectionResizeMode(0, QtWidgets.QHeaderView.Stretch)
        add_rec_main_layout.addWidget(self.rec_step_table)

        bottom_btn_layout = QHBoxLayout()
        self.add_rec_btn = QPushButton("Add recipe")
        self.add_rec_btn.clicked.connect(self.add_recipe_to_db)

        self.back_btn = QPushButton("Cancel")
        self.back_btn.clicked.connect(self.add_recipe_win.close)

        bottom_btn_layout.addWidget(self.add_rec_btn)
        bottom_btn_layout.addWidget(self.back_btn)
        add_rec_main_layout.addLayout(bottom_btn_layout)

        self.add_recipe_win.setLayout(add_rec_main_layout)
        self.add_recipe_win.show()

    @Slot()
    def add_recipe_step_win(self):
        self.rec_step_table.insertRow(self.step_count)
        self.step_count += 1

    @Slot()
    def create_ingredient(self):
        self.add_ingredient_widget = AddIngredientWidget(self.meal_planner_db, self, self.ingredient_name_input.text())

    @Slot()
    def add_ingredient_to_recipe(self):
        if self.meal_planner_db.ingredient_exists(self.ingredient_name_input.text()):
            self.rec_ingredient_table.insertRow(self.recipe_ingredients)
            self.rec_ingredient_table.setItem(self.recipe_ingredients, 0, QTableWidgetItem(str(self.ingredient_qty_input.value())))
            self.rec_ingredient_table.setItem(self.recipe_ingredients, 1, QTableWidgetItem(self.ingredient_unit_input.currentText()))
            self.rec_ingredient_table.setItem(self.recipe_ingredients, 2, QTableWidgetItem(self.ingredient_name_input.text()))
            self.recipe_ingredients += 1

            self.ingredient_name_input.clear()
            self.ingredient_qty_input.setValue(1.0)
            self.ingredient_unit_input.setCurrentIndex(0)
        else:
            print("Ingredient does not exist in database, please add it first")

    @Slot()
    def del_ingredient_from_recipe(self):
        recipe = self.rec_name_input.text()
        ingredient = self.rec_ingredient_table.currentItem().text()
        self.rec_ingredient_table.removeRow(self.rec_ingredient_table.currentRow())
        self.meal_planner_db.del_recipe_ingredient(recipe, ingredient)

    @Slot()
    def add_recipe_to_db(self):
        rec_id = self.meal_planner_db.get_table_len("recipes")
        self.meal_planner_db.add_recipe(rec_id, self.rec_name_input.text(), self.rec_desc_input.text(),
                                        self.rec_source_input.text(), self.difficulty_spinbox.value(),
                                        self.prep_time_spinbox.value(), self.rating_spinbox.value(), "2000-01-01", 0)

        for row in range(self.rec_ingredient_table.rowCount()):
            qty_id = self.meal_planner_db.get_table_len("measurement_qty")
            qty_id = self.meal_planner_db.add_qty(qty_id, self.rec_ingredient_table.item(row, 0).text())
            unit_id = self.meal_planner_db.get_table_len("measurement_units")
            unit_id = self.meal_planner_db.add_measurement(unit_id, self.rec_ingredient_table.item(row, 1).text())
            ing_id = self.meal_planner_db.get_ingredient_id(self.rec_ingredient_table.item(row, 2).text())
            if ing_id == -1:
                print("INGREDIENT DOES NOT EXIST! WE FUCKED UP!")
                break
            self.meal_planner_db.add_recipe_ingredient(rec_id, ing_id, unit_id, qty_id)

        for row in range(self.step_count):
            print(row, self.rec_step_table.item(row, 0).text())
            self.meal_planner_db.add_step(rec_id, row, self.rec_step_table.item(row, 0).text())

        # Cuisine tag
        tag_id = self.meal_planner_db.get_table_len("tags")
        tag_id = self.meal_planner_db.add_tag(tag_id, self.tag_cuisine.currentText())
        self.meal_planner_db.add_recipe_tag(tag_id, rec_id)
        # Category tag
        tag_id = self.meal_planner_db.get_table_len("tags")
        tag_id = self.meal_planner_db.add_tag(tag_id, self.tag_category.currentText())
        self.meal_planner_db.add_recipe_tag(tag_id, rec_id)
        # Meal type tag
        tag_id = self.meal_planner_db.get_table_len("tags")
        tag_id = self.meal_planner_db.add_tag(tag_id, self.tag_meal_types.currentText())
        self.meal_planner_db.add_recipe_tag(tag_id, rec_id)

        self.rec_name_input.clear()
        self.rec_desc_input.clear()
        self.rec_ingredient_table.setRowCount(0)
        self.rec_step_table.setRowCount(0)
        self.step_count = 0

        self.parent().update_recipe_table()


#####################################################
class EditRecipeWidget(QWidget):
    def __init__(self, database, parent):
        QWidget.__init__(self)
        self.recipe_ingredients = 0
        self.edit_recipe_win = QWidget()
        self.edit_recipe_win.setFixedWidth(400)
        self.edit_recipe_win.setWindowTitle("Edit Recipe")
        edit_rec_main_layout = QVBoxLayout()

        self.meal_planner_db = database
        self.setParent(parent)

        recipe_name = self.parent().recipe_table.selectedItems()[0].text()
        recipe_info = self.meal_planner_db.get_full_recipe(recipe_name)

        self.rec_name_input = QLineEdit(recipe_name)
        self.rec_desc_input = QLineEdit(recipe_info[0])
        self.rec_source_input = QLineEdit(recipe_info[1])
        rec_form_layout = QFormLayout()
        rec_form_layout.addRow(QLabel("Recipe Name"), self.rec_name_input)
        rec_form_layout.addRow(QLabel("Recipe Desc"), self.rec_desc_input)
        rec_form_layout.addRow(QLabel("Recipe Source"), self.rec_source_input)
        edit_rec_main_layout.addLayout(rec_form_layout)

        rec_info_layout = QHBoxLayout()
        difficulty_layout = QVBoxLayout()
        self.difficulty_spinbox = QSpinBox()
        self.difficulty_spinbox.setRange(1, 5)
        self.difficulty_spinbox.setValue(recipe_info[2])
        difficulty_layout.addWidget(QLabel("Difficulty"))
        difficulty_layout.addWidget(self.difficulty_spinbox)

        prep_time_layout = QVBoxLayout()
        self.prep_time_spinbox = QSpinBox()
        self.prep_time_spinbox.setRange(0, 600)
        self.prep_time_spinbox.setValue(recipe_info[3])
        prep_time_layout.addWidget(QLabel("Prep. Time (min.)"))
        prep_time_layout.addWidget(self.prep_time_spinbox)

        rating_layout = QVBoxLayout()
        self.rating_spinbox = QSpinBox()
        self.rating_spinbox.setRange(1, 5)
        self.rating_spinbox.setValue(recipe_info[4])
        rating_layout.addWidget(QLabel("Rating"))
        rating_layout.addWidget(self.rating_spinbox)

        rec_info_layout.addLayout(difficulty_layout)
        rec_info_layout.addLayout(prep_time_layout)
        rec_info_layout.addLayout(rating_layout)

        edit_rec_main_layout.addLayout(rec_info_layout)

        rec_tags_layout = QHBoxLayout()
        rec_cuisine_layout = QVBoxLayout()
        cuisines = ["Mexican", "Swedish", "Austrian", "Italian", "Spanish", "American", "British", "Thai", "Greek",
                    "Vietnamese", "Caribbean", "Japanese", "Chinese", "Indian", "French", "Swiss", "Portuguese",
                    "Korean", "Turkish", "Moroccan", "Russian", "Malaysian", "Philippines", "Ethiopian", "Lebanese",
                    "Arab", "Peruvian", "Brazilian", "Asian", "Middle Eastern", "South American", "African", "-"]
        cuisines.sort()
        self.tag_cuisine = QComboBox()
        self.tag_cuisine.addItems(cuisines)
        self.tag_cuisine.setCurrentText(recipe_info[7][0])
        rec_cuisine_layout.addWidget(QLabel("Cuisine"))
        rec_cuisine_layout.addWidget(self.tag_cuisine)
        rec_tags_layout.addLayout(rec_cuisine_layout)

        rec_category_layout = QVBoxLayout()
        categories = ["Beef & Calf", "Chicken & Poultry", "Lamb", "Pork", "Preservation", "Salad", "Sandwich", "Soup",
                      "Stew", "Pasta", "Rice", "Grain & Beans", "Fish & Seafood", "Vegetables", "Eggs & Cheese", "BBQ",
                      "Fruits", "Cake & Pie (Sweet)", "Pie", "Bread", "Beverage", "Cookies & Sweets", "Sauce", "-"]
        categories.sort()
        self.tag_category = QComboBox()
        self.tag_category.addItems(categories)
        self.tag_category.setCurrentText(recipe_info[8][0])
        rec_category_layout.addWidget(QLabel("Category"))
        rec_category_layout.addWidget(self.tag_category)
        rec_tags_layout.addLayout(rec_category_layout)

        rec_meal_type_layout = QVBoxLayout()
        meal_types = ["Breakfast", "Brunch", "Lunch", "Dinner", "Dessert", "Starter", "Side", "Buffet", "Snack", "-"]
        meal_types.sort()
        self.tag_meal_types = QComboBox()
        self.tag_meal_types.addItems(meal_types)
        self.tag_meal_types.setCurrentText(recipe_info[9][0])
        rec_meal_type_layout.addWidget(QLabel("Meal Type"))
        rec_meal_type_layout.addWidget(self.tag_meal_types)
        rec_tags_layout.addLayout(rec_meal_type_layout)

        edit_rec_main_layout.addLayout(rec_tags_layout)

        self.ingredient_name_input = QLineEdit()
        self.ingredient_qty_input = QDoubleSpinBox()
        self.ingredient_qty_input.setValue(1.0)
        self.ingredient_qty_input.setMaximum(1000)
        self.ingredient_qty_input.setDecimals(2)
        self.ingredient_unit_input = QComboBox()
        self.ingredient_unit_input.addItems(["g", "ml", "dl", "l", "msk", "tsk", "st", "-"])
        add_ingredient_btn = QPushButton("Create ingredient")
        add_ingredient_btn.clicked.connect(self.create_ingredient)
        add_ingredient_layout = QHBoxLayout()
        edit_rec_main_layout.addWidget(QLabel("Ingredient"))
        add_ingredient_layout.addWidget(self.ingredient_name_input)
        add_ingredient_layout.addWidget(self.ingredient_qty_input)
        add_ingredient_layout.addWidget(self.ingredient_unit_input)
        add_ingredient_layout.addWidget(add_ingredient_btn)
        edit_rec_main_layout.addLayout(add_ingredient_layout)

        btn_layout = QHBoxLayout()
        add_ingredient_to_recipe_btn = QPushButton("Add ingredient")
        add_ingredient_to_recipe_btn.clicked.connect(self.add_ingredient_to_recipe)

        # Removes recipe_ingredient from database on press
        # Best would be to delete when 'Apply Changes' is pressed...
        del_ingredient_from_recipe_btn = QPushButton("Remove ingredient")
        del_ingredient_from_recipe_btn.clicked.connect(self.del_ingredient_from_recipe)

        btn_layout.addWidget(add_ingredient_to_recipe_btn)
        btn_layout.addWidget(del_ingredient_from_recipe_btn)
        edit_rec_main_layout.addLayout(btn_layout)

        self.rec_ingredient_table = QTableWidget()
        self.rec_ingredient_table.setColumnCount(3)
        self.rec_ingredient_table.setHorizontalHeaderLabels(["Amount", "Unit", "Ingredient"])
        header = self.rec_ingredient_table.horizontalHeader()
        header.setSectionResizeMode(0, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(1, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(2, QtWidgets.QHeaderView.Stretch)

        # Fill table with ingredients
        i = 0
        for ingredient in recipe_info[5]:
            self.rec_ingredient_table.insertRow(i)
            self.rec_ingredient_table.setItem(i, 0, QTableWidgetItem(ingredient[0][0]))
            self.rec_ingredient_table.setItem(i, 1, QTableWidgetItem(ingredient[1][0]))
            self.rec_ingredient_table.setItem(i, 2, QTableWidgetItem(ingredient[2][0]))
            i += 1

        edit_rec_main_layout.addWidget(self.rec_ingredient_table)

        self.step_count = 0
        self.add_recipe_step_btn = QPushButton("Add recipe instruction")
        edit_rec_main_layout.addWidget(self.add_recipe_step_btn)
        self.add_recipe_step_btn.clicked.connect(self.add_recipe_step_win)
        self.rec_step_table = QTableWidget()
        self.rec_step_table.setColumnCount(1)
        self.rec_step_table.setHorizontalHeaderLabels(["Instructions"])
        header = self.rec_step_table.horizontalHeader()
        header.setSectionResizeMode(0, QtWidgets.QHeaderView.Stretch)
        edit_rec_main_layout.addWidget(self.rec_step_table)

        i = 0
        for step in recipe_info[6]:
            self.rec_step_table.insertRow(i)
            self.rec_step_table.setItem(i, 0, QTableWidgetItem(step[1]))
            i += 1
        self.rec_step_table.resizeRowsToContents()

        bottom_btn_layout = QHBoxLayout()
        self.edit_recipe_btn = QPushButton("Apply Changes")
        self.back_btn = QPushButton("Cancel")
        self.back_btn.clicked.connect(self.edit_recipe_win.close)

        bottom_btn_layout.addWidget(self.edit_recipe_btn)
        bottom_btn_layout.addWidget(self.back_btn)
        edit_rec_main_layout.addLayout(bottom_btn_layout)

        self.edit_recipe_win.setLayout(edit_rec_main_layout)
        self.edit_recipe_win.show()

    @Slot()
    def add_recipe_step_win(self):
        self.rec_step_table.insertRow(self.step_count)
        self.step_count += 1

    @Slot()
    def create_ingredient(self):
        self.add_ingredient_widget = AddIngredientWidget(self.meal_planner_db, self, self.ingredient_name_input.text())

    @Slot()
    def add_ingredient_to_recipe(self):
        if self.meal_planner_db.ingredient_exists(self.ingredient_name_input.text()):
            self.rec_ingredient_table.insertRow(self.recipe_ingredients)
            self.rec_ingredient_table.setItem(self.recipe_ingredients, 0, QTableWidgetItem(str(self.ingredient_qty_input.value())))
            self.rec_ingredient_table.setItem(self.recipe_ingredients, 1, QTableWidgetItem(self.ingredient_unit_input.currentText()))
            self.rec_ingredient_table.setItem(self.recipe_ingredients, 2, QTableWidgetItem(self.ingredient_name_input.text()))
            self.recipe_ingredients += 1

            self.ingredient_name_input.clear()
            self.ingredient_qty_input.setValue(1.0)
            self.ingredient_unit_input.setCurrentIndex(0)
        else:
            print("Ingredient does not exist in database, please add it first")

    @Slot()
    def del_ingredient_from_recipe(self):
        recipe = self.rec_name_input.text()
        ingredient = self.rec_ingredient_table.currentItem().text()
        self.rec_ingredient_table.removeRow(self.rec_ingredient_table.currentRow())
        self.meal_planner_db.del_recipe_ingredient(recipe, ingredient)

    @Slot()
    def add_recipe_to_db(self):
        rec_id = self.meal_planner_db.get_table_len("recipes")
        self.meal_planner_db.add_recipe(rec_id, self.rec_name_input.text(), self.rec_desc_input.text(),
                                        self.rec_source_input.text(), self.difficulty_spinbox.value(),
                                        self.prep_time_spinbox.value(), self.rating_spinbox.value(), "2000-01-01", 0)

        for row in range(self.rec_ingredient_table.rowCount()):
            qty_id = self.meal_planner_db.get_table_len("measurement_qty")
            qty_id = self.meal_planner_db.add_qty(qty_id, self.rec_ingredient_table.item(row, 0).text())
            unit_id = self.meal_planner_db.get_table_len("measurement_units")
            unit_id = self.meal_planner_db.add_measurement(unit_id, self.rec_ingredient_table.item(row, 1).text())
            ing_id = self.meal_planner_db.get_ingredient_id(self.rec_ingredient_table.item(row, 2).text())
            if ing_id == -1:
                print("INGREDIENT DOES NOT EXIST! WE FUCKED UP!")
                break
            self.meal_planner_db.add_recipe_ingredient(rec_id, ing_id, unit_id, qty_id)

        for row in range(self.step_count):
            print(row, self.rec_step_table.item(row, 0).text())
            self.meal_planner_db.add_step(rec_id, row, self.rec_step_table.item(row, 0).text())

        # Cuisine tag
        tag_id = self.meal_planner_db.get_table_len("tags")
        tag_id = self.meal_planner_db.add_tag(tag_id, self.tag_cuisine.currentText())
        self.meal_planner_db.add_recipe_tag(tag_id, rec_id)
        # Category tag
        tag_id = self.meal_planner_db.get_table_len("tags")
        tag_id = self.meal_planner_db.add_tag(tag_id, self.tag_category.currentText())
        self.meal_planner_db.add_recipe_tag(tag_id, rec_id)
        # Meal type tag
        tag_id = self.meal_planner_db.get_table_len("tags")
        tag_id = self.meal_planner_db.add_tag(tag_id, self.tag_meal_types.currentText())
        self.meal_planner_db.add_recipe_tag(tag_id, rec_id)

        self.rec_name_input.clear()
        self.rec_desc_input.clear()
        self.rec_ingredient_table.setRowCount(0)
        self.rec_step_table.setRowCount(0)
        self.step_count = 0

        self.parent().update_recipe_table()


#####################################################
class ShowRecipeWidget(QWidget):
    def __init__(self, database, parent):
        QWidget.__init__(self)
        self.recipe_ingredients = 0
        self.step_count = 0
        self.meal_planner_db = database
        self.setParent(parent)
        self.show_recipe_win = QWidget()
        self.show_recipe_win.setFixedWidth(500)
        self.show_recipe_win.setFixedHeight(700)
        self.show_recipe_win.setWindowTitle("Recipe Name")
        show_rec_main_layout = QVBoxLayout()

        recipe_name = self.parent().recipe_table.selectedItems()[0].text()
        recipe_info = self.meal_planner_db.get_full_recipe(recipe_name)

        self.recipe_text = QTextEdit()
        show_rec_main_layout.addWidget(self.recipe_text)

        self.recipe_text.setFontFamily("Helvetica")
        self.recipe_text.setReadOnly(True)
        self.recipe_text.setFontPointSize(18)
        self.recipe_text.setFontUnderline(True)
        self.recipe_text.append(recipe_name)
        self.recipe_text.setFontPointSize(13)
        self.recipe_text.setFontUnderline(False)
        self.recipe_text.append("Source: " + recipe_info[1])  # Source
        self.recipe_text.setFontItalic(True)
        self.recipe_text.setFontPointSize(11)
        self.recipe_text.append(recipe_info[0])  # Description
        self.recipe_text.setFontItalic(False)
        self.recipe_text.append("-------------------------------------------------------------")
        self.recipe_text.setFontPointSize(9)
        self.recipe_text.append("Difficulty: " + str(recipe_info[2]) + "    " +
                                "Prep. Time: " + str(recipe_info[3]) + "    " +
                                "Rating: " + str(recipe_info[4]))
        self.recipe_text.append("Cuisine: " + str(recipe_info[7][0]) + "\n" +
                                "Category: " + str(recipe_info[8][0]) + "\n" +
                                "Meal type: " + str(recipe_info[9][0]))
        self.recipe_text.setFontPointSize(11)
        self.recipe_text.append("-------------------------------------------------------------")
        self.recipe_text.setFontPointSize(13)
        self.recipe_text.setFontUnderline(True)
        self.recipe_text.append("Ingredients:")
        self.recipe_text.setFontUnderline(False)
        self.recipe_text.setFontPointSize(11)
        for ingredient in recipe_info[5]:
            self.recipe_text.append(ingredient[0][0] + " " + ingredient[1][0] + "\t" + ingredient[2][0])
        self.recipe_text.append("-------------------------------------------------------------")
        self.recipe_text.setFontPointSize(13)
        self.recipe_text.setFontUnderline(True)
        self.recipe_text.append("How To:")
        self.recipe_text.setFontUnderline(False)
        self.recipe_text.setFontPointSize(11)
        for step in recipe_info[6]:
            print(step)
            self.recipe_text.append(str(step[0] + 1) + ": " + step[1] + "\n")

        bottom_btn_layout = QHBoxLayout()
        self.print_recipe_btn = QPushButton("Print Recipe")

        self.back_btn = QPushButton("Back")
        self.back_btn.clicked.connect(self.show_recipe_win.close)

        bottom_btn_layout.addWidget(self.print_recipe_btn)
        bottom_btn_layout.addWidget(self.back_btn)
        show_rec_main_layout.addLayout(bottom_btn_layout)

        self.show_recipe_win.setLayout(show_rec_main_layout)
        self.show_recipe_win.show()


#####################################################
class RecipeCollectionWidget(QWidget):
    def __init__(self):
        QWidget.__init__(self)
        self.recipe_items = 0
        self.meal_planner_db = database_manager.MealPlannerDatabase()

        self.title_font = QFont("Arial", 32, QFont.Bold)
        self.day_font = QFont("Arial", 16, QFont.DemiBold)
        self.general_font = QFont("Arial", 10, QFont.StyleNormal)

        #Meal planner
        self.title_label = QLabel("Recipe Collection")
        self.title_label.setFixedHeight(40)
        self.title_label.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        self.title_label.setFont(self.title_font)

        self.add_recipe_button = QPushButton("Add recipe")
        self.add_recipe_button.setFont(self.day_font)
        self.add_recipe_button.setFixedHeight(35)
        self.add_recipe_button.clicked.connect(self.add_recipe)
        self.del_recipe_button = QPushButton("Remove recipe")
        self.del_recipe_button.setFont(self.day_font)
        self.del_recipe_button.setFixedHeight(35)
        self.del_recipe_button.clicked.connect(self.del_recipe)
        self.edit_recipe_button = QPushButton("Edit recipe")
        self.edit_recipe_button.setFont(self.day_font)
        self.edit_recipe_button.setFixedHeight(35)
        self.edit_recipe_button.clicked.connect(self.edit_recipe)
        self.show_recipe_button = QPushButton("Show recipe")
        self.show_recipe_button.setFont(self.day_font)
        self.show_recipe_button.setFixedHeight(35)
        self.show_recipe_button.clicked.connect(self.show_recipe)

        self.btn_layout = QHBoxLayout()
        self.btn_layout.addWidget(self.add_recipe_button)
        self.btn_layout.addWidget(self.del_recipe_button)
        self.btn_layout.addWidget(self.edit_recipe_button)
        self.btn_layout.addWidget(self.show_recipe_button)

        self.recipe_table = QTableWidget()
        self.recipe_table.setColumnCount(3)
        self.recipe_table.setHorizontalHeaderLabels(["Name", "Desc", "ID"])
        self.recipe_table.setSelectionBehavior(QAbstractItemView.SelectItems)
        self.recipe_table.setSelectionMode(QAbstractItemView.SingleSelection)
        header = self.recipe_table.horizontalHeader()
        header.setSectionResizeMode(0, QtWidgets.QHeaderView.Stretch)
        header.setSectionResizeMode(1, QtWidgets.QHeaderView.Stretch)
        header.setSectionResizeMode(2, QtWidgets.QHeaderView.ResizeToContents)

        self.recipe_collection_layout = QVBoxLayout()
        self.recipe_collection_layout.addWidget(self.title_label)
        self.recipe_collection_layout.addLayout(self.btn_layout)
        self.recipe_collection_layout.addWidget(self.recipe_table)

        self.setLayout(self.recipe_collection_layout)

        self.update_recipe_table()
        #self.meal_planner_db.print_tables()

    @Slot()
    def add_recipe(self):
        add_recipe_widget = AddRecipeWidget(self.meal_planner_db, self)
        self.update_recipe_table()

    @Slot()
    def del_recipe(self):
        try:
            recipe_line = self.recipe_table.selectedItems()
            self.meal_planner_db.del_item(recipe_line[0].text())
            self.update_recipe_table()
        except IndexError:
            #Proper handling needed
            print("Click to select a recipe to show.")
        except TypeError:
            # Proper handling needed
            print("Make sure to select the recipe by name")

    @Slot()
    def edit_recipe(self):
        edit_recipe_widget = EditRecipeWidget(self.meal_planner_db, self)

    @Slot()
    def show_recipe(self):
        show_recipe_widget = ShowRecipeWidget(self.meal_planner_db, self)


    def update_recipe_table(self):
        recipes = self.meal_planner_db.get_recipe_items()
        self.recipe_table.setRowCount(0)
        self.recipe_items = 0
        for item in recipes:
            self.recipe_table.insertRow(self.recipe_items)
            self.recipe_table.setItem(self.recipe_items, 0, QTableWidgetItem(item[1]))
            self.recipe_table.setItem(self.recipe_items, 1, QTableWidgetItem(item[2]))
            self.recipe_table.setItem(self.recipe_items, 2, QTableWidgetItem(str(item[0])))
            self.recipe_items += 1

