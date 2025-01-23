import json
import datetime

dbDishesPath = "dishesDB.json" #ścieżka do pliku json z bazą dań
dbDaysPath = "daysDB.json"     #ścieżka do pliku json z bazą dni

class Dish:
    def __init__(self, name:str, calories:int, description:str):
        self.name = name
        self.calories = calories
        self.description = description

class Day:
    def __init__(self, date:datetime.datetime, calories:int, caloriesGoal:int):
        self.date = date.strftime("%d.%m.%Y")
        self.calories = calories
        self.caloriesGoal = caloriesGoal
        

def readDishesData(): #wczytuje liste słowników z pliku dbDishesPath, deserializuje ją do listy obiektów klasy Dish i zwraca ją
    file = open(dbDishesPath, "r")
    db = json.loads(file.read())
    file.close()

    dishes = []

    for dish in db:
        dishes.append(Dish(dish['Name'], dish['Calories'], dish['Description']))

    return dishes

def readDaysData(): #wczytuje liste słowników z pliku dbDaysPath, deserializuje ją do listy obiektów klasy Day i zwraca ją
    file = open(dbDaysPath, "r")
    db = json.loads(file.read())
    file.close()

    days = []

    for day in db:
        days.append(Day(datetime.datetime.strptime(day['Date'], "%d.%m.%Y"), day['Calories'], day['CaloriesGoal']))

    return days

def writeDishesData(dishList:list): #jako parametr przyjmuje LISTĘ OBIEKTÓW KLASY Dish, serializuje ją do formatu json i zapisuje do pliku dbDishesPath
    file = open(dbDishesPath, "w")

    Dishes = []
    try:
        for dish in dishList:
            if type(dish) != Dish:
                raise Exception()
            dishSerialized = {"Name": dish.name, "Calories": dish.calories, "Description": dish.description}
            Dishes.append(dishSerialized)
    except:
        file.close()
        return "Nie udało się zapisać danych"
    
    db = json.dumps(Dishes, indent=4)

    file.write(db)
    file.close()
    return "Zapisano dane" 

def writeDaysData(daysList:list):   #jako parametr przyjmuje LISTĘ OBIEKTÓW KLASY Day, serializuje ją do formatu json i zapisuje do pliku dbDaysPath

    file = open(dbDaysPath, "w")

    Days = []
    try:
        for day in daysList:
            if type(day) != Day:
                raise Exception()
            daySerialized = {"Date": day.date, "Calories": day.calories, "CaloriesGoal": day.caloriesGoal}
            Days.append(daySerialized)
    except:
        file.close()
        return 0
    
    db = json.dumps(Days, indent=4)

    file.write(db)
    file.close()
    return 1 
