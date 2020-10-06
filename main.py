#Qt Imports
from PySide2.QtCore import Qt, Slot
from PySide2.QtWidgets import (QAction, QApplication, QMainWindow, QStackedWidget)

#General Imports
import sys

#Project Imports
import scraper_widget
import meal_plan_widget
import recipe_collection_widget


class KitchenManagerWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Meal Planner")

        # Menu bar
        self.menu = self.menuBar()
        self.file_menu = self.menu.addMenu("File")

        #Goto Meal Plan Action
        goto_meal_plan_action = QAction("Meal planner", self)
        goto_meal_plan_action.triggered.connect(self.goto_meal_planner_widget)

        # Goto Scraper Action
        goto_scraper_action = QAction("Scraper", self)
        goto_scraper_action.triggered.connect(self.goto_scraper_widget)

        # Goto Recipe Collection Action
        goto_recipe_collection_action = QAction("Recipe Collection", self)
        goto_recipe_collection_action.triggered.connect(self.goto_recipe_collection_widget)

        # Exit QAction
        exit_action = QAction("Exit", self)
        exit_action.setShortcut("Ctrl+Q")
        exit_action.triggered.connect(self.exit_app)

        self.file_menu.addAction(goto_meal_plan_action)
        self.file_menu.addAction(goto_recipe_collection_action)
        self.file_menu.addAction(goto_scraper_action)
        self.file_menu.addAction(exit_action)

        self.widget_scraper = scraper_widget.ScraperWidget()
        self.widget_meal_plan = meal_plan_widget.MealPlanWidget()
        self.widget_recipe_collection = recipe_collection_widget.RecipeCollectionWidget()

        #Start on the scraper
        self.stacked_widgets = QStackedWidget()
        self.stacked_widgets.addWidget(self.widget_scraper)
        self.stacked_widgets.addWidget(self.widget_meal_plan)
        self.stacked_widgets.addWidget(self.widget_recipe_collection)
        self.stacked_widgets.setCurrentWidget(self.widget_recipe_collection)
        self.setCentralWidget(self.stacked_widgets)

    @Slot()
    def goto_recipe_collection_widget(self, checked):
        self.stacked_widgets.setCurrentWidget(self.widget_recipe_collection)

    @Slot()
    def goto_meal_planner_widget(self, checked):
        self.stacked_widgets.setCurrentWidget(self.widget_meal_plan)

    @Slot()
    def goto_scraper_widget(self, checked):
        self.stacked_widgets.setCurrentWidget(self.widget_scraper)

    @Slot()
    def exit_app(self, checked):
        QApplication.quit()


if __name__ == "__main__":
    app = QApplication([])

    window = KitchenManagerWindow()
    window.resize(600, 800)
    window.show()

    sys.exit(app.exec_())


#scraper = CityGrossScraper()

#offers = scraper.run("eoelindholm@gmail.com", "Regel123", 7)

#print(offers)
