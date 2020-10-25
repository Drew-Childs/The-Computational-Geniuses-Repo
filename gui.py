import tkinter as tk
import tkinter.font as tkFont
from menu import Menu
import random

from PIL import Image, ImageTk
from io import BytesIO
from urllib import request

root = tk.Tk()
global m
m = Menu()
m.readRecipes()

class Application(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        self.pack()

        # Creates and shows the canvas
        canvas = tk.Canvas(root, height=900, width=900)
        canvas.pack()

        sideBar = tk.Canvas(root, bg="#660000")
        sideBar.place(relh=1, relw=.2)

        menuButton = tk.Button(sideBar, text="Menu", command=lambda: self.switchScene(menuScene))
        menuButton.place(relx=.1, rely=.0125, relw=.8, relh=.1)

        b1 = tk.Button(sideBar, text="Favorites", command=lambda: self.switchScene(favoriteScene))
        b1.place(relx=.1, rely=.125, relw=.8, relh=.1)

        b2 = tk.Button(sideBar, text="Browse", command=lambda: self.switchScene(browseScene))
        b2.place(relx=.1, rely=.2375, relw=.8, relh=.1)

        b3 = tk.Button(sideBar, text="Search", command=lambda: self.switchScene(searchScene))
        b3.place(relx=.1, rely=.35, relw=.8, relh=.1)

        b4 = tk.Button(sideBar, text="Shopping Cart", command=lambda: self.switchScene(shoppingCartScene))
        b4.place(relx=.1, rely=.4625, relw=.8, relh=.1)

        b5 = tk.Button(sideBar, text="History", command=lambda: self.switchScene(historyScene))
        b5.place(relx=.1, rely=.575, relw=.8, relh=.1)

        exitButton = tk.Button(sideBar, text="Exit", command=lambda: self.master.destroy())
        exitButton.place(relx=.1, rely=.885, relw=.8, relh=.1)

        self.currFrame = None
        self.switchScene(menuScene)

    def switchScene(self, newFrame):
        frame = newFrame(self)
        if self.currFrame is not None:
            self.currFrame.forget()
            self.currFrame.destroy()

        self.currFrame = frame
        self.currFrame.pack()

    def displayDetails(self, food):

        m.history.append(food)

        newWindow = tk.Toplevel(bg="#990000")
        tk.Label(newWindow, text=food.name, font=tkFont.Font(size=20), bg="#990000", fg="white").pack(side="top")
        tk.Label(newWindow, text=food.description, font=tkFont.Font(size=10), wraplength=200, bg="#990000", fg="white").pack(side="top")
        tk.Label(newWindow, text=("{:10} {}".format("Prep Time: ", food.prepTime)), bg="#990000", fg="white").pack(side="top")
        tk.Label(newWindow, text=("{:10} {}".format("Cook Time: ", food.cookTime)), bg="#990000", fg="white").pack(side="top")
        tk.Label(newWindow, text=("{:10} {}".format("Servings: ", food.servings)), bg="#990000", fg="white").pack(side="top")

        tk.Label(newWindow, text="Ingredients:").pack(side="top")
        ingredients = tk.Listbox(newWindow, selectmode=tk.MULTIPLE, width=200, justify=tk.CENTER)
        for x in food.recipe:
            ingredients.insert(tk.END, x)
        ingredients.pack(side="top")

        addToCart = tk.Button(newWindow, text="Add to Cart", command=lambda: m.addToShoppingList(food))
        addToCart.pack(side="bottom")

        favorite = tk.Button(newWindow)

        if food.isFavorite:
            favorite.config(text="Unfavorite", command=lambda: m.removeFavorite(food))
        else:
            favorite.config(text="Favorite", command=lambda: m.addToFavorites(food))
        favorite.pack(side="bottom")

        tk.Label(newWindow, text=food.instructions, bg="#990000", fg="white").pack(side="top")
        tk.Label(newWindow, text=("{:10} {}".format("Author: ", food.author)), bg="#990000", fg="white").pack(side="bottom")

class menuScene(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)

        frame = tk.Frame(root, bg="#990000")
        frame.place(relx=.2, relwidth=.8, relheight=1)

        header = tk.Message(frame, text="Menu ", bg="#990000", fg="white", font=tkFont.Font(size=30), width=400)
        header.pack(side="top")

class favoriteScene(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        try:

            frame = tk.Frame(root, bg="#990000")
            frame.place(relx=.2, relwidth=.8, relheight=1)

            header = tk.Message(frame, text="Favorites ", bg="#990000", fg="white", font=tkFont.Font(size=30), width=400)
            header.pack(side="top")

            results = tk.Listbox(frame)
            scrollBar = tk.Scrollbar(results)

            m.printFavorites(results, tk)

            results.place(relx=.1, rely=.1, relw=.7, relh=.8)  # sizing and placement of results box
            results.config(yscrollcommand=scrollBar.set)  # Connects scrollbar to results box size
            scrollBar.pack(side="right", fill="y")  # Sets the scrollbar to the right of the box, and fills vertically
            scrollBar.config(command=results.yview)  # Allows scroll bar to take control of box

            viewMore = tk.Button(frame, text="View More", command=lambda: self.master.displayDetails(m.allFavorites[results.curselection()[0]]))
            viewMore.place(relx=.825, rely=.45, relh=.1, relw=.15)

            tk.Tk.report_callback_exception = IndexError
        except:
            errorWindow = tk.Toplevel()
            tk.Label(errorWindow, text="Please click on an item/recipe").pack()
            tk.Button(errorWindow, text="Click to close", command=self.errorWindow.destroy()).pack()

class browseScene(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)

        frame = tk.Frame(root, bg="#990000")
        frame.place(relx=.2, relwidth=.8, relheight=1)

        header = tk.Message(frame, text="Browse ", bg="#990000", fg="white", font=tkFont.Font(size=30), width=300)
        header.pack(side="top")

        results = tk.Listbox(frame)
        scrollBar = tk.Scrollbar(results)

        recomList = m.recommendations()
        if len(recomList) != 0:
            for x in recomList:
                results.insert(tk.END, x.name)
        else:
            for x in range(20):
                rando = random.randint(0, len(m.foodList))
                m.recommendedHistory.append(m.foodList[rando])
                results.insert(tk.END, m.foodList[rando].name)
                x += 1

        results.place(relx=.1, rely=.1, relw=.7, relh=.8)  # sizing and placement of results box
        results.config(yscrollcommand=scrollBar.set)  # Connects scrollbar to results box size
        scrollBar.pack(side="right", fill="y")  # Sets the scrollbar to the right of the box, and fills vertically
        scrollBar.config(command=results.yview)  # Allows scroll bar to take control of box

        viewMore = tk.Button(frame, text="View More")
        viewMore.config(command=lambda: self.master.displayDetails(m.recommendedHistory[results.curselection()[0]]))  # Need to grab food object
        viewMore.place(relx=.825, rely=.45, relh=.1, relw=.15)

class searchScene(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)

        self.frame = tk.Frame(root, bg="#990000")
        self.frame.place(relx=.2, relwidth=.8, relheight=1)

        header = tk.Message(self.frame, text="Search ", bg="#990000", fg="white", font=tkFont.Font(size=30), width=300)
        header.pack(side="top")

        searchBar = tk.Entry(self.frame, bd=4)
        searchBar.place(relx=.1, rely=.15, relw=.7)

        searchButton = tk.Button(self.frame, text="Search!", command=lambda: self.searchDatabase(searchBar.get()))
        searchButton.place(relx=.825, rely=.15, relw=.15)


    def searchDatabase(self, searchBar):

        sortedDict = m.search(searchBar) # fills a dictionary for searched items

        results = tk.Listbox(self.frame) # creates listbox for the results, placed in the frame of [searchDatabase]
        scrollBar = tk.Scrollbar(results) # creates a scrollbar that is placed in [results]'s box

        hold = []

        for key, value in sortedDict.items():
            results.insert(tk.END, ("{:15} ({})".format(key.name, key.typeOfDish))) # iterates and inserts into results
            hold.append(key)

        results.place(relx=.1, rely=.22, relw=.7, relh=.6) # sizing and placement of results box
        results.config(yscrollcommand=scrollBar.set) # Connects scrollbar to results box size
        scrollBar.pack(side="right", fill="y") # Sets the scrollbar to the right of the box, and fills vertically
        scrollBar.config(command=results.yview) # Allows scroll bar to take control of box

        viewMore = tk.Button(self.frame, text="View More")
        viewMore.config(command=lambda: self.master.displayDetails(hold[results.curselection()[0]])) # Need to grab food object
        viewMore.place(relx=.825, rely=.45, relh=.1, relw=.15)

class shoppingCartScene(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)

        frame = tk.Frame(root, bg="#990000")
        frame.place(relx=.2, relwidth=.8, relheight=1)

        results = tk.Listbox(frame)
        scrollBar = tk.Scrollbar(results)

        m.printShoppingCart(results, tk)

        results.place(relx=.1, rely=.22, relw=.7, relh=.6)
        results.config(yscrollcommand=scrollBar.set)
        scrollBar.pack(side="right", fill="y")
        scrollBar.config(command=results.yview)

        header = tk.Message(frame, text="Shopping Cart ", bg="#990000", fg="white", font=tkFont.Font(size=30), width=400)
        header.pack(side="top")

class historyScene(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)

        frame = tk.Frame(root, bg="#990000")
        frame.place(relx=.2, relwidth=.8, relheight=1)

        results = tk.Listbox(frame)
        scrollBar = tk.Scrollbar(results)

        m.printHistory(results, tk)

        results.place(relx=.1, rely=.1, relw=.7, relh=.8)  # sizing and placement of results box
        results.config(yscrollcommand=scrollBar.set)  # Connects scrollbar to results box size
        scrollBar.pack(side="right", fill="y")  # Sets the scrollbar to the right of the box, and fills vertically
        scrollBar.config(command=results.yview)  # Allows scroll bar to take control of box

        viewMore = tk.Button(frame, text="View More", command=lambda: self.master.displayDetails(m.history[results.curselection()[0]]))
        viewMore.place(relx=.825, rely=.45, relh=.1, relw=.15)

        header = tk.Message(frame, text="History ", bg="#990000", fg="white", font=tkFont.Font(size=30), width=400)
        header.pack(side="top")

class customScene(tk.Frame)

app = Application(master=root)

app.master.title("The Computational Geniuses")

app.mainloop()
