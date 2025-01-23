from GUImanager import *
from datetime import *
from Controller import *
import DBmanager

goal = 2000
currentCalories = 0

try: # przed uruchomieniem programu jest sprawdzane czy istnieją już zapisane dane z aktualnego dnia
    days = DBmanager.readDaysData()

    for day in days:
        if datetime.now().strftime("%d.%m.%Y") == day.date:
            currentCalories = day.calories
            goal = day.caloriesGoal
except:
    print("nie udało się wczytać danych")

main = Controller(currentCalories, goal, datetime.now()) #tworzy obiekt klasy Controller, w którym znajduje się logika programu
gui = GUImanager(main) #wyświetlenie części graficznej programu poprzez utworzenie obiektu klasy GUImanager i przypisanie jej głownego kontrolera