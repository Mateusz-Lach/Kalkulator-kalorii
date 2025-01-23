import DBmanager
from tkinter import *
from datetime import *
from Controller import *

class GUImanager:

    def __init__(self, main:Controller):
        root = Tk()

        self.main = main
        self.date = self.main.currentDate

        window_width = 900
        window_height = 600

        self.mainWindowConfig(root, window_width, window_height)

        title = Label(root, text = "Program do liczenia kalorii", background='#333', fg='#eee', font=("Arial", 20, "bold"), width=window_width, pady=10)    
        settingsContainer = LabelFrame(root,text="Ustawienia", width=window_width/3, height=window_height, background='#bbb')
        mainContainer = LabelFrame(root,text="Panel Główny", width=window_width/3, height=window_height, background='#ccc', pady=10, padx=5)
        dishesContainer = LabelFrame(root,text="Baza dań, kliknij danie żeby dodać kalorie", width=window_width/3, height=window_height, background='#bbb', pady=10, padx=5)

        self.dishesCon = dishesContainer

        settingsContainer.grid_propagate(False)
        mainContainer.grid_propagate(False)
        dishesContainer.grid_propagate(False)

        title.pack(side='top')
        settingsContainer.pack(side='left')
        mainContainer.pack(side='left')
        dishesContainer.pack(side='left')

        self.generateSettingsPanel(settingsContainer)
        self.generateDishButtonsList(dishesContainer)
        self.generateMainPanel(mainContainer, main.currentCalories, main.caloriesGoal)

        root.mainloop()

    def mainWindowConfig(self, root:Tk ,width:int, height:int): # funcja zawierająca konfiguracje głównego okna
        root.title("Program do liczenia kalorii")
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        center_x = int(screen_width/2 - width / 2)
        center_y = int(screen_height/2 - height / 2)
        root.geometry(f'{width}x{height}+{center_x}+{center_y}')

    def getDishButtons(self, container): #zwraca liste przycisków z daniami, funkcja używana w funkcji generateDishButtonsList
        dishes = DBmanager.readDishesData()

        dishesButtons = []
        for dish in dishes:
            button = Button(container, text=f'{dish.name}, kalorie: {dish.calories}')
            dishesButtons.append(button)

        return dishesButtons

    def generateDishButtonsList(self, container): #generuje trzecią część graficzną programu (liste dań z pliku json)
        for widget in container.winfo_children():
            widget.destroy()

        dishesButtons = self.getDishButtons(container)

        dishes = DBmanager.readDishesData()

        container.columnconfigure(0, weight=1)
        for i in range(len(dishesButtons)):   
            dishesButtons[i].config(command=lambda p=dishes[i]: [self.main.addCaloriesFromDishDbButton(p), self.RefreshCaloriesCounter()]) 
            dishesButtons[i].grid(row=i, column=0, sticky='ew')

    def generateMainPanel(self, container, currentCalories:int, caloriesGoal:int): #generuje środkową (Główną) część graficzną programu
        container.columnconfigure(0, weight=1)
##----------------------------------------------------------------------------------------------------------------------------------------------------
        self.caloriesCounter = Label(container, text=f"Ilość kalorii dzisiaj: {currentCalories}", font=("Arial", 14, "bold"), background='#ccc')
        self.caloriesCounter.grid(row=0, column=0, sticky='ew')

        self.caloriesGoalLabel = Label(container, text=f"Twój cel kalorii na dziś: {caloriesGoal}", font=("Arial", 10, "bold"), background='#ccc')
        self.caloriesGoalLabel.grid(row=1, column=0, sticky='ew')

        day = self.date.strftime("%d")
        month = self.date.strftime("%m")
        dateLabel = Label(container, text=f"Dzisiaj jest: {day}.{month}.{self.date.year}", font=("Arial", 8, "normal"), background='#ccc')
        dateLabel.grid(row=2, column=0, sticky='ew')
##----------------------------------------------------------------------------------------------------------------------------------------------------
        addCalories = LabelFrame(container, text="Dodaj kalorie", pady=10, background='#ccc')
        addCalories.grid(row=3, column=0, sticky='ew', pady=10, padx=5)

        addCaloriesInput = Entry(addCalories, width=30)
        addCaloriesButton = Button(addCalories, command= lambda: [self.main.addCaloriesButton(addCaloriesInput), self.RefreshCaloriesCounter()], text="Dodaj", width=10)

        addCaloriesInput.pack(side='left',padx=5)
        addCaloriesButton.pack(side='left',padx=5)
##----------------------------------------------------------------------------------------------------------------------------------------------------
        addDish = LabelFrame(container, text="Dodaj danie do kalorii i bazy", pady=10, background='#ccc')
        addDish.grid(row=4, column=0, sticky='ew', pady=10, padx=5)

        nameLabel = Label(addDish, text="Nazwa:", font=("Arial", 10, "normal"), background='#ccc')
        nameLabel.grid(row=0, column=0, sticky='ew', padx=7)
        nameInput = Entry(addDish, width=30)
        nameInput.grid(row=0, column=1, sticky='ew')

        caloriesLabel = Label(addDish, text="Kalorie:", font=("Arial", 10, "normal"), background='#ccc')
        caloriesLabel.grid(row=1, column=0, sticky='ew')
        caloriesInput = Entry(addDish, width=30)
        caloriesInput.grid(row=1, column=1, sticky='ew')

        descLabel = Label(addDish, text="Opis:", font=("Arial", 10, "normal"), background='#ccc')
        descLabel.grid(row=2, column=0, sticky='ew')
        descInput = Entry(addDish, width=30)
        descInput.grid(row=2, column=1, sticky='ew')

        addDishButton = Button(addDish, command= lambda: [self.main.addDishAndCaloriesButton( nameInput, caloriesInput, descInput), self.generateDishButtonsList(self.dishesCon), self.RefreshCaloriesCounter()], text="Dodaj", width=10)
        addDishButton.grid(row=3, column=1, sticky='e', pady=5)
##----------------------------------------------------------------------------------------------------------------------------------------------------
        deleteDish = LabelFrame(container, text="Usuń danie z bazy", pady=10, background='#ccc')
        deleteDish.grid(row=5, column=0, sticky='ew', pady=10, padx=5)

        deleteLabel = Label(deleteDish, text="Przycisk wyświetla listę dań do usunięcia", font=("Arial", 10, "normal"), background='#ccc')
        deleteLabel.grid(row = 0, column=0, sticky='ew', padx=5)

        deleteButton = Button(deleteDish,command=lambda: self.main.deleteDishesListButton() , text="Pokaż", width=10)
        deleteButton.grid(row=1, column=0, padx=10, pady=3)

    def generateSettingsPanel(self, container): #generuje pierwszą część graficzną programu (Menu ustawień)

        container.columnconfigure(0, weight=1)
##----------------------------------------------------------------------------------------------------------------------------------------------------
        changeCaloriesGoal = LabelFrame(container, text="Zmień cel kalorii", pady=10, background='#bbb')
        changeCaloriesGoal.grid(row=0, column=0, sticky='ew', pady=10, padx=5)

        goalInput = Entry(changeCaloriesGoal, width=30)
        goalButton = Button(changeCaloriesGoal, command=lambda: [self.main.changeCaloriesGoalButton(goalInput), self.RefreshCaloriesGoal()], text="Ustaw", width=10)

        goalInput.pack(side="left",padx=5)
        goalButton.pack(side="left",padx=5)
##----------------------------------------------------------------------------------------------------------------------------------------------------
        resetCalories = LabelFrame(container, text="Zresetuj dzisiejsze kalorie", pady=10, padx=5, background='#bbb')
        resetCalories.grid(row=1, column=0, sticky='ew', pady=10, padx=5)

        resetLabel = Label(resetCalories, text="Przycisk trwale resetuje licznik kalorii", font=("Arial", 7, "bold"), background='#bbb')
        resetButton = Button(resetCalories, command= lambda:[self.main.resetCaloriesButton(), self.RefreshCaloriesCounter()], text="Resetuj", width=10)

        resetButton.pack(side="left")
        resetLabel.pack(side="left")
##----------------------------------------------------------------------------------------------------------------------------------------------------
        saveCalories = LabelFrame(container, text="Zapisz dzisiejsze kalorie", pady=10, padx=5, background='#bbb')
        saveCalories.grid(row=2, column=0, sticky='ew', pady=10, padx=5)

        saveLabel = Label(saveCalories, text="Przycisk zapisuje dzisiejsze kalorie", font=("Arial", 7, "bold"), background='#bbb')
        saveButton = Button(saveCalories, command=self.main.saveCaloriesButton, text="Zapisz", width=10)

        saveButton.pack(side="left")
        saveLabel.pack(side="left")
##----------------------------------------------------------------------------------------------------------------------------------------------------
        openDays = LabelFrame(container, text="Lista dni", pady=10, padx=5, background='#bbb')
        openDays.grid(row=3, column=0, sticky='ew', pady=10, padx=5)

        daysLabel = Label(openDays, text="Przycisk wyświetla wyniki z innych dni", font=("Arial", 7, "bold"), background='#bbb')
        daysButton = Button(openDays, text="Otwórz", command=self.main.showDaysInfoButton, width=10)

        daysButton.pack(side="left")
        daysLabel.pack(side="left")
##----------------------------------------------------------------------------------------------------------------------------------------------------
        refreshDishes = LabelFrame(container, text="Odśwież liste dań", pady=10, padx=5, background='#bbb')
        refreshDishes.grid(row=4, column=0, sticky='ew', pady=10, padx=5)

        refreshLabel = Label(refreshDishes, text="Przycisk odświeża listę dań", font=("Arial", 7, "bold"), background='#bbb')
        refreshButton = Button(refreshDishes, text="Odśwież", command=lambda: self.generateDishButtonsList(self.dishesCon), width=10)

        refreshButton.pack(side="left")
        refreshLabel.pack(side="left")

    def RefreshCaloriesCounter(self): #odświeża licznik kalorii
        self.caloriesCounter.config(text=f"Ilość kalorii dzisiaj: {self.main.currentCalories}")
    def RefreshCaloriesGoal(self): #odświeża tekst z celem kalorii
        self.caloriesGoalLabel.config(text=f"Twój cel kalorii na dziś: {self.main.caloriesGoal}")