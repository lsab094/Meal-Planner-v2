import sqlite3, math, pandas as pd, numpy as np

con = sqlite3.connect("RecipeList.db")
curs = con.cursor()

def CSVtoDB(fileName, tabName):
    file = pd.read_csv(fileName)
    file.columns = file.columns.str.replace(' ', '_')
    file.to_sql(tabName, con, if_exists='append', index = False)

def resetTab():
    # Clear the table if it exists, and create a new one.
    curs.execute("""
        DROP TABLE IF EXISTS RecipeTable
    """)
    CSVtoDB('RecipeList.csv', 'RecipeTable')

def getMeals():
    # Add recipe names to nameList for querying.
    nameList = []
    for row in curs.fetchall():
        nameList.append(row[0])

    def printMeals():
        ingredientList = []
        recipeList = []
        creditList = []
        if len(nameList) > 2:
            for name in nameList[0:3]:
                #Generate 3 meals for each week.
                curs.execute(("""
                        SELECT Name, ShoppingList, Recipe, Credits
                        FROM RecipeTable
                        WHERE Name = ?
                        """), (name,))
                for row in curs.fetchall():
                    #for the 3 chosen meals, retrieve name, ingredients, recipe, and website and add to list.
                    for i in row[1].split(','):
                        i = i.strip()
                        if i not in ingredientList:
                            ingredientList.append(i)
                        else:
                            pass
                    recipeList.append(row[0])
                    recipeList.append('')
                    recipeList.append(row[2])
                    recipeList.append('')
                    creditList.append(row[3])
            #Print shopping list, recipes, and websites.
            print('Weekly Shopping')
            print('')
            for i in ingredientList:
                print(i)
            print('')
            for r in recipeList:
                print(r)
            print("Credits:")
            print('')
            for c in creditList:
                print(c)
            print('')

            #Removed generated recipe names from nameList so the next 3 can be retrieved.
            del nameList[0:3]
            printMeals()

        else:
            #If there are less than 3 meals left to generate, restart the program.
            restart()

    printMeals()

def restart():
    print("\nPlanner finished. What would you like to do next?"
          "\n1. Restart"
          "\n2. Quit")
    choice = input()
    if choice.isdigit() == False:
        print("\nPlease enter a number.")
        restart()
    elif int(choice) == 1:
        menu()
    elif int(choice) == 2:
        quit()
    else:
        print("\nPlease enter a number.")
        restart()

def selectAllMeals():
    #Select all meals.
    curs.execute("""
        SELECT *
        FROM RecipeTable
        ORDER BY RANDOM()
        """)
    getMeals()

def selectAirFryerMeals():
    #Select only meals that need an air fryer.
    curs.execute(("""
        SELECT *
        FROM RecipeTable
        WHERE Tools IS NOT ?
        ORDER BY RANDOM()
        """), ('stove',))
    getMeals()

def selectStovetopMeals():
    # Select only meals that need a stovetop.
    curs.execute(("""
        SELECT *
        FROM RecipeTable
        WHERE Tools IS NOT ?
        ORDER BY RANDOM()
        """), ('air fryer',))
    getMeals()

def menu():
    resetTab()
    print("\nMEAL PLANNER V2"
          "\nGenerate 3 meals to make each week."
          "\nWhich recipes would you like to see?"
          "\n1. All recipes"
          "\n2. Air fryer recipes only"
          "\n3. Stovetop recipes only"
          "\n4. Quit")
    choice = input()
    if choice.isdigit() == False:
        print("\nPlease enter a number.")
        menu()
    elif int(choice) == 1:
        selectAllMeals()
    elif int(choice) == 2:
        selectAirFryerMeals()
    elif int(choice) == 3:
        selectStovetopMeals()
    elif int(choice) == 4:
        quit()
    else:
        print("\nPlease enter a number.")
        menu()

menu()

con.commit()
con.close()