from tkinter import *
from tkinter import messagebox
from datetime import *
import DBmanager

#        
#       W klasie Controller znajduje się logika całego programu i część GUI (wyświetlanie okien innych niż główne odbywa się w tej klasie tj. lista dni i lista dań do usunięcia)
#

class Controller:
    def __init__(self, currentCalories, caloriesGoal, currentDate:datetime):
        self.currentCalories = currentCalories
        self.caloriesGoal = caloriesGoal
        self.currentDate = currentDate

    def __saveMessage(self, dayInfo:DBmanager.Day):
        if dayInfo.calories <= dayInfo.caloriesGoal:
            messagebox.showinfo("Zapisano", f"Zapisano dane z dnia: {dayInfo.date}, Ilość kalorii: {dayInfo.calories}, Cel nie został przekroczony")
        else:
            messagebox.showinfo("Zapisano", f"Zapisano dane z dnia: {dayInfo.date}, Ilość kalorii: {dayInfo.calories}, Cel został przekroczony!!!")

    def __returnDayListElement(self, root ,day:DBmanager.Day):
        frame = Frame(root, borderwidth=2, relief=SOLID, background='#fff')
        Label(frame, text=f"{day.date}: Liczba kalorii: {day.calories} Cel: {day.caloriesGoal}", padx=5, font=("Arial", 11, "normal"), background='#fff').pack(side="left")
        if day.calories <= day.caloriesGoal:
            Label(frame, text="Cel nie został przekroczony",fg="#0f0", font=("Arial", 11, "bold"), background='#fff').pack(side="left")
        else:
            Label(frame, text="Cel został przekroczony!",fg="#f00", font=("Arial", 11, "bold"), background='#fff').pack(side="left")

        return frame

    def addCaloriesButton(self, entry:Entry):
        try:
            value = int(entry.get())
        except:
            messagebox.showerror("Błąd", "Podana wartość kalorii nie jest liczbą!")
            return
        self.currentCalories += value
        entry.delete(0, 'end')

    def addDishAndCaloriesButton(self, name:Entry, calories:Entry, desc:Entry):


        dishes = DBmanager.readDishesData()
        try:
            caloriesNum = int(calories.get())
        except:
            messagebox.showerror("Błąd", "Podana wartość kalorii nie jest liczbą!")
            return
        try:
            dish = DBmanager.Dish(name.get(), caloriesNum, desc.get()) 
        except:
            messagebox.showerror("Błąd", "Błąd podczas dodawania dania")
            return
        
        dishes.append(dish)

        self.currentCalories += caloriesNum

        name.delete(0, 'end')
        calories.delete(0, 'end')
        desc.delete(0, 'end')

        DBmanager.writeDishesData(dishes)
        messagebox.showinfo("Pomyślnie dodano", f"Dodano danie {name.get()}") 

    def addCaloriesFromDishDbButton(self, dish:DBmanager.Dish):
        if messagebox.askyesno('Uwaga!', f'Nazwa produktu: {dish.name} \nOpis: {dish.description} \n \nCzy dodać {dish.calories} kalorii?'):
            self.currentCalories += dish.calories

    def changeCaloriesGoalButton(self, entry:Entry):
        try:
            value = int(entry.get())
        except:
            messagebox.showerror("Błąd", "Podana wartość kalorii nie jest liczbą!")
            return
        self.caloriesGoal = value
        entry.delete(0, 'end')
        messagebox.showinfo("Zmieniono cel", "Pomyślnie zmieniono cel") 

    def resetCaloriesButton(self):
        if messagebox.askyesno('Uwaga!', 'Czy na pewno chcesz zresetować licznik kalorii?'):
            self.currentCalories = 0

    def saveCaloriesButton(self):
        days = DBmanager.readDaysData()

        try:
            addNewDay = True
            for day in days:
                if self.currentDate.strftime("%d.%m.%Y") == day.date:
                    day.calories = self.currentCalories
                    day.caloriesGoal = self.caloriesGoal
                    addNewDay = False
                    self.__saveMessage(day)
                    break
            
            if addNewDay:
                day = DBmanager.Day(self.currentDate, self.currentCalories, self.caloriesGoal)
                days.append(day)
                self.__saveMessage(day)

            DBmanager.writeDaysData(days)
        except:
            messagebox.showerror("Błąd!", "Błąd podczas zapisywania danych")

    def showDaysInfoButton(self):
        daysWindow = Tk()

        width = 530
        height = 400

        daysWindow.title("Informacje z dni")
        screen_width = daysWindow.winfo_screenwidth()
        screen_height = daysWindow.winfo_screenheight()
        center_x = int(screen_width/2 - width / 2)
        center_y = int(screen_height/2 - height / 2)
        daysWindow.geometry(f'{width}x{height}+{center_x}+{center_y}')

        mainFrame = Frame(daysWindow)
        mainFrame.pack(fill=BOTH, expand=1)

        canvas = Canvas(mainFrame)
        canvas.pack(side=LEFT, fill=BOTH, expand=1)

        scrollbar = Scrollbar(mainFrame, orient=VERTICAL, command=canvas.yview)
        scrollbar.pack(side=RIGHT, fill=Y)

        canvas.configure(yscrollcommand=scrollbar.set)
        canvas.bind('<Configure>', lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

        scrollableFrame = Frame(canvas)

        canvas.create_window((0, 0), window=scrollableFrame, anchor="nw")

        days = DBmanager.readDaysData()
        for day in days:
            self.__returnDayListElement(scrollableFrame, day).pack(fill='x',pady=3, anchor="c" , expand=True)

        daysWindow.mainloop()
            
    def deleteDishesListButton(self):
        def deleteDishButton(index:int):
            dishes = DBmanager.readDishesData()
            if messagebox.askyesno("Uwaga!", f"Czy na pewno chcesz usunąć {dishes[index].name} z bazy dań?"):
                dishes.pop(index)
                DBmanager.writeDishesData(dishes)
        def generateButtons(container):
            dishes = DBmanager.readDishesData()

            dishesButtons = []
            for dish in dishes:
                button = Button(container, text=f'{dish.name}, kalorie: {dish.calories}')
                dishesButtons.append(button)

            for i in range(len(dishesButtons)):
                dishesButtons[i].config(command=lambda p=i: [deleteDishButton(p), generateButtons(container)])
                dishesButtons[i].grid(row=i, column=0, sticky='ew')
    
        deleteDishesWindow = Tk()

        width = 300
        height = 600

        deleteDishesWindow.title("Usuń danie z listy")
        screen_width = deleteDishesWindow.winfo_screenwidth()
        screen_height = deleteDishesWindow.winfo_screenheight()
        center_x = int(screen_width/2 - width / 2)
        center_y = int(screen_height/2 - height / 2)
        deleteDishesWindow.geometry(f'{width}x{height}+{center_x}+{center_y}')
        deleteDishesWindow.attributes("-topmost", True)

        mainFrame = LabelFrame(deleteDishesWindow, text="Kliknij na danie, aby je usunąć", width=width, height=height, pady=10, padx=5)
        mainFrame.grid_propagate(False)
        mainFrame.pack()
        mainFrame.columnconfigure(0, weight=1)

        generateButtons(mainFrame)

        deleteDishesWindow.mainloop()