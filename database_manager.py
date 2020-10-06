import sqlite3


class MealPlannerDatabase:
    def __init__(self):
        self.db_name = "test_meal_planner.db"

        # Connect to database
        self.conn_db = sqlite3.connect(self.db_name)

        # Create cursor
        self.cursor = self.conn_db.cursor()

        ##################
        # TABLE CREATION #
        ##################

        # self.cursor.execute("DROP TABLE recipe_steps")

        # RECIPE INGREDIENTS #
        # A "go-between" table for recipes and ingredients to go around the many to many problem
        try:
            self.cursor.execute(
                """
                CREATE TABLE recipe_ingredients (
                recipe_id INT NOT NULL,
                measurement_qty_id INT NOT NULL,
                measurement_id INT NOT NULL,
                ingredient_id INT NOT NULL
                )
                """
            )
        except sqlite3.OperationalError:
            print("Table recipe_ingredients exists")

        # The recipe database
        try:
            self.cursor.execute(
                """
                CREATE TABLE recipes (
                recipe_id INT NOT NULL PRIMARY KEY,
                name TEXT NOT NULL,
                desc TEXT,
                source TEXT,
                difficulty INT,
                prep_time INT,
                rating INT,
                last_date_planned TEXT,
                times_planned_last_four_weeks INT
                )
                """
            )
        except sqlite3.OperationalError:
            print("Table recipes exists")

        # The ingredient database (is_discounted is an int with 0 being False, 1 being True)
        try:
            self.cursor.execute(
                """
                CREATE TABLE ingredients (
                ingredient_id INT NOT NULL PRIMARY KEY,
                name TEXT UNIQUE NOT NULL,
                k_cals INT,
                carbs INT,
                sugars INT,
                fats INT,
                protein INT,
                is_discounted INT
                )
                """
            )
        except sqlite3.OperationalError:
            print("Table ingredients exists")

        try:
            self.cursor.execute(
                """
                CREATE TABLE measurement_units (
                measurement_id INT NOT NULL PRIMARY KEY,
                short_name TEXT UNIQUE NOT NULL
                )
                """
            )
        except sqlite3.OperationalError:
            print("Table measurement_units exists")

        try:
            self.cursor.execute(
                """
                CREATE TABLE measurement_qty (
                measurement_qty_id INT NOT NULL PRIMARY KEY,
                qty_amount TEXT UNIQUE NOT NULL
                )
                """
            )
        except sqlite3.OperationalError:
            print("Table measurement_qty exists")

        # RECIPE STEPS #

        # The recipe_steps table
        try:
            self.cursor.execute(
                """
                CREATE TABLE recipe_steps (
                recipe_id INT NOT NULL,
                step_nr INT NOT NULL,
                step_instruction TEXT NOT NULL
                )
                """
            )
        except sqlite3.OperationalError:
            print("Table recipe_steps exists")

        # TAG SYSTEM TABLES #

        # The recipe_tags table
        try:
            self.cursor.execute(
                """
                CREATE TABLE recipe_tags (
                recipe_id INT NOT NULL,
                tag_id INT NOT NULL
                )
                """
            )
        except sqlite3.OperationalError:
            print("Table recipe_tags exists")

        # The tags table
        try:
            self.cursor.execute(
                """
                CREATE TABLE tags (
                tag_id INT NOT NULL PRIMARY KEY,
                tag_text TEXT UNIQUE NOT NULL
                )
                """
            )
        except sqlite3.OperationalError:
            print("Table tags exists")

        self.commit_and_close_db()

    def connect_to_db(self):
        # Connect to database
        self.conn_db = sqlite3.connect(self.db_name)
        # Create cursor
        self.cursor = self.conn_db.cursor()

    def commit_and_close_db(self):
        # Commit changes
        self.conn_db.commit()
        # Close the database
        self.conn_db.close()

    def ingredient_exists(self, ingredient_name):
        self.connect_to_db()
        self.cursor.execute("SELECT ingredient_id FROM ingredients WHERE name=?", (ingredient_name,))
        ingredient = self.cursor.fetchone()
        if ingredient is None:
            self.commit_and_close_db()
            return False
        else:
            self.commit_and_close_db()
            return True

    def get_ingredient_id(self, ingredient_name):
        self.connect_to_db()
        self.cursor.execute("SELECT ingredient_id FROM ingredients WHERE name=?", (ingredient_name,))
        ingredient = self.cursor.fetchone()
        if ingredient is None:
            self.commit_and_close_db()
            return -1
        else:
            self.commit_and_close_db()
            return ingredient[0]

    def get_recipe_items(self):
        self.connect_to_db()
        self.cursor.execute("SELECT * FROM recipes")
        results = self.cursor.fetchall()
        self.commit_and_close_db()
        return results

    def del_recipe(self, recipe_name):
        self.connect_to_db()
        self.cursor.execute("SELECT recipe_id FROM recipes WHERE name='" + recipe_name + "'")
        recipe_info = self.cursor.fetchone()

        try:
            self.cursor.execute("DELETE FROM recipe_ingredients WHERE recipe_id=" + str(recipe_info[0]))
            self.cursor.execute("DELETE FROM recipes WHERE recipe_id=" + str(recipe_info[0]))
            self.cursor.execute("DELETE FROM recipe_steps WHERE recipe_id=" + str(recipe_info[0]))
            self.cursor.execute("DELETE FROM recipe_tags WHERE recipe_id=" + str(recipe_info[0]))
            self.commit_and_close_db()
            self.print_tables()
        except IndexError:
            self.commit_and_close_db()
            pass

    def del_recipe_ingredient(self, recipe_name, ingredient_name):
        self.connect_to_db()
        self.cursor.execute("SELECT recipe_id FROM recipes WHERE name='" + recipe_name + "'")
        recipe_id = self.cursor.fetchone()
        print(recipe_id[0])
        self.cursor.execute("SELECT ingredient_id FROM ingredients WHERE name='" + ingredient_name + "'")
        ingredient_id = self.cursor.fetchone()
        print(ingredient_id[0])

        try:
            self.cursor.execute("DELETE FROM recipe_ingredients WHERE recipe_id='" + str(recipe_id[0]) +
                                "' AND ingredient_id='" + str(ingredient_id[0]) + "'")

            self.commit_and_close_db()
            self.print_tables()
        except IndexError:
            self.commit_and_close_db()
            pass

    def edit_item(self):
        pass

    def get_table_len(self, table_name):
        self.connect_to_db()
        self.cursor.execute("SELECT * FROM " + table_name)
        size = len(self.cursor.fetchall())
        self.commit_and_close_db()
        return size

    # USED DURING DEVELOPMENT, NOT IN RELEASE!
    def print_tables(self):
        self.connect_to_db()
        self.cursor.execute("SELECT * FROM recipes")
        print("recipes:", self.cursor.fetchall())
        self.cursor.execute("SELECT * FROM recipe_ingredients")
        print("recipe_ingredients:", self.cursor.fetchall())
        self.cursor.execute("SELECT * FROM ingredients")
        print("ingredients:", self.cursor.fetchall())
        self.cursor.execute("SELECT * FROM measurement_units")
        print("measurement_units:", self.cursor.fetchall())
        self.cursor.execute("SELECT * FROM measurement_qty")
        print("measurement_qty:", self.cursor.fetchall())
        self.cursor.execute("SELECT * FROM recipe_steps")
        print("recipe_steps:", self.cursor.fetchall())
        self.cursor.execute("SELECT * FROM recipe_tags")
        print("recipe_tags:", self.cursor.fetchall())
        self.cursor.execute("SELECT * FROM tags")
        print("tags:", self.cursor.fetchall())
        self.commit_and_close_db()

    def get_full_recipe(self, recipe_name):
        self.connect_to_db()
        self.cursor.execute("""
        SELECT recipe_id, desc, source, difficulty, prep_time, rating 
        FROM recipes 
        WHERE name='""" + recipe_name + "'")
        recipe_info = self.cursor.fetchall()

        try:
            # In order of adding: desc, source, difficulty, prep_time, rating
            recipe_info_list = [recipe_info[0][1], recipe_info[0][2], recipe_info[0][3],
                                recipe_info[0][4], recipe_info[0][5]]

            self.cursor.execute("SELECT * FROM recipe_ingredients WHERE recipe_id=" + str(recipe_info[0][0]))
            id_lists = self.cursor.fetchall()
            ingredient_list = []
            for id_list in id_lists:
                self.cursor.execute("SELECT name FROM ingredients WHERE ingredient_id=" + str(id_list[1]))
                ingredient = self.cursor.fetchall()
                self.cursor.execute("SELECT short_name FROM measurement_units WHERE measurement_id=" + str(id_list[2]))
                measurement = self.cursor.fetchall()
                self.cursor.execute("SELECT qty_amount FROM measurement_qty WHERE measurement_qty_id=" + str(id_list[3]))
                quantity = self.cursor.fetchall()
                recipe_ingredient = [quantity[0], measurement[0], ingredient[0]]
                ingredient_list.append(recipe_ingredient)

            recipe_info_list.append(ingredient_list)
            self.cursor.execute("SELECT step_nr, step_instruction FROM recipe_steps WHERE recipe_id=" + str(recipe_info[0][0]))
            steps = self.cursor.fetchall()
            recipe_info_list.append(steps)

            # TAGS ADDED WRONG WAY AROUND, SHOULD WORK NOW WHEN RE-ADDING RECIPES! NEEDS TESTING!
            self.cursor.execute("SELECT recipe_id FROM recipe_tags WHERE tag_id='" + str(recipe_info[0][0]) + "'")
            tag_id_lists = self.cursor.fetchall()
            for id_ in tag_id_lists:
                self.cursor.execute("SELECT tag FROM tags WHERE tag_id='" + str(id_[0]) + "'")
                tag = self.cursor.fetchall()
                recipe_info_list.append(tag[0])

            self.commit_and_close_db()

            return recipe_info_list
        except IndexError:
            self.commit_and_close_db()
            return []

    def add_recipe_ingredient(self, rec_id, ing_id, unit_id, qty_id):
        self.connect_to_db()
        self.cursor.execute("INSERT INTO recipe_ingredients VALUES (:recipe_id, :ingredient_id, :measurement_id, "
                            ":measurement_qty_id)",
                            {
                                "recipe_id": rec_id,
                                "ingredient_id": ing_id,
                                "measurement_id": unit_id,
                                "measurement_qty_id": qty_id
                            }
                            )
        self.commit_and_close_db()

    def add_recipe(self, rec_id, name, desc, source, difficulty, prep_time,
                   rating, last_date_planned, times_planned_last_four_weeks):
        self.connect_to_db()
        self.cursor.execute("""
        INSERT INTO recipes VALUES 
        (:recipe_id,
         :name,
         :desc,
         :source,
         :difficulty,
         :prep_time,
         :rating,
         :last_date_planned,
         :times_planned_last_four_weeks)
        """,
                            {
                                "recipe_id": rec_id,
                                "name": name,
                                "desc": desc,
                                "source": source,
                                "difficulty": difficulty,
                                "prep_time": prep_time,
                                "rating": rating,
                                "last_date_planned": last_date_planned,
                                "times_planned_last_four_weeks": times_planned_last_four_weeks
                            }
                            )
        self.commit_and_close_db()

    def add_ingredient(self, ing_id, name, k_cals, carbs, sugar, fats, protein, is_discounted):
        self.connect_to_db()
        self.cursor.execute("SELECT ingredient_id FROM ingredients WHERE name=?", (name,))
        ingredient = self.cursor.fetchone()
        if ingredient is None:
            print("Element does not exist")
            self.cursor.execute("""
            INSERT INTO ingredients VALUES
             (
             :ingredient_id, 
             :name,
             :k_cals,
             :carbs,
             :sugar,
             :fats,
             :protein,
             :is_discounted
             )""",
                                {
                                    "ingredient_id": ing_id,
                                    "name": name,
                                    "k_cals": k_cals,
                                    "carbs": carbs,
                                    "sugar": sugar,
                                    "fats": fats,
                                    "protein": protein,
                                    "is_discounted": is_discounted
                                }
                                )
            self.commit_and_close_db()
            return ing_id
        else:
            print("Component exists with id:", ingredient[0])
            self.commit_and_close_db()
            return ingredient[0]

    def add_measurement(self, unit_id, short_name):
        self.connect_to_db()
        self.cursor.execute("SELECT measurement_id FROM measurement_units WHERE short_name=?", (short_name,))
        unit = self.cursor.fetchone()
        if unit is None:
            print("Element does not exist")
            self.cursor.execute("INSERT INTO measurement_units VALUES (:measurement_id, :short_name)",
                                {
                                    "measurement_id": unit_id,
                                    "short_name": short_name
                                }
                                )
            self.commit_and_close_db()
            return unit_id
        else:
            print("Component exists with id:", unit[0])
            self.commit_and_close_db()
            return unit[0]

    def add_qty(self, qty_id, qty_amount):
        self.connect_to_db()
        self.cursor.execute("SELECT measurement_qty_id FROM measurement_qty WHERE qty_amount=?", (qty_amount,))
        qty = self.cursor.fetchone()
        if qty is None:
            print("Element does not exist")
            self.cursor.execute("INSERT INTO measurement_qty VALUES (:measurement_qty_id, :qty_amount)",
                                {
                                    "measurement_qty_id": qty_id,
                                    "qty_amount": qty_amount
                                }
                                )
            self.commit_and_close_db()
            return qty_id
        else:
            print("Component exists with id:", qty[0])
            self.commit_and_close_db()
            return qty[0]

    def add_tag(self, tag_id, tag_text):
        self.connect_to_db()
        self.cursor.execute("SELECT tag_id FROM tags WHERE tag=?", (tag_text,))
        tag = self.cursor.fetchone()
        if tag is None:
            print("Element does not exist")
            self.cursor.execute("INSERT INTO tags VALUES (:tag_id, :tag)",
                                {
                                    "tag_id": tag_id,
                                    "tag": tag_text
                                }
                                )
            self.commit_and_close_db()
            return tag_id
        else:
            print("Component exists with id:", tag[0])
            self.commit_and_close_db()
            return tag[0]

    def add_ingredient_tag(self, tag_id, ingredient_id):
        self.connect_to_db()
        self.cursor.execute("INSERT INTO ingredient_tags VALUES (:tag_id, :ingredient_id)",
                            {
                                "ingredient_id": ingredient_id,
                                "tag_id": tag_id
                            }
                            )
        self.commit_and_close_db()

    def add_recipe_tag(self, tag_id, recipe_id):
        self.connect_to_db()
        self.cursor.execute("INSERT INTO recipe_tags VALUES (:recipe_id, :tag_id)",
                            {
                                "recipe_id": recipe_id,
                                "tag_id": tag_id
                            }
                            )
        self.commit_and_close_db()

    def add_step(self, recipe_id, step_id, step_instruction):
        self.connect_to_db()
        self.cursor.execute("INSERT INTO recipe_steps VALUES (:recipe_id, :step_id, :step_instruction)",
                            {
                                "recipe_id": recipe_id,
                                "step_id": step_id,
                                "step_instruction": step_instruction
                            }
                            )
        self.commit_and_close_db()
