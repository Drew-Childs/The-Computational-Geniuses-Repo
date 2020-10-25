import tkinter as tk
import tkinter.font as tkFont
from menu import Menu
import random
from PIL import Image, ImageFilter, ImageTk
from urllib.request import Request, urlopen
from io import BytesIO

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

        b6 = tk.Button(sideBar, text="Custom Recipe", command= lambda: self.switchScene(customScene))
        b6.place(relx=.1, rely=.6875, relw=.8, relh=.1)

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

        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.3'}
        req = Request("https://simplyrecipes.com/wp-content/uploads/2017/09/2017-10-04-ChickenScampi-6.jpg", headers=headers)  # Requests to open website
        picture = urlopen(req).read()
        im = Image.open(BytesIO(picture))
        im = im.resize((600, 600), resample=3)
        photo = ImageTk.PhotoImage(im)

        newWindow = tk.Toplevel(bg="#990000")
        tk.Label(newWindow, text=food.name, font=tkFont.Font(size=20), bg="#990000", fg="white").pack(side="top")

        canvas = tk.Canvas(newWindow, width=400, height=400)
        canvas.pack()
        img = ImageTk.PhotoImage(im)
        canvas.create_image(100, 100, anchor=tk.N, image=img)

        tk.Label(newWindow, text=food.description, font=tkFont.Font(size=10), wraplength=200, bg="#990000", fg="white").pack(side="top")
        tk.Label(newWindow, text=("{:10} {}".format("Prep Time: ", food.prepTime)), bg="#990000", fg="white").pack(side="top")
        tk.Label(newWindow, text=("{:10} {}".format("Cook Time: ", food.cookTime)), bg="#990000", fg="white").pack(side="top")
        tk.Label(newWindow, text=("{:10} {}".format("Servings: ", food.servings)), bg="#990000", fg="white").pack(side="top")

        tk.Label(newWindow, text="Ingredients:", bg="#990000").pack(side="top")
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

        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.3'}

        req = Request("https://simplyrecipes.com/wp-content/uploads/2017/09/2017-10-04-ChickenScampi-6.jpg",
                      headers=headers)  # Requests to open website
        picture = urlopen(req).read()

        im = Image.open(BytesIO(picture))

        im = im.resize((600, 600), Image.ANTIALIAS)

        photo = ImageTk.PhotoImage(im)

        canvas = tk.Canvas(frame, width=600, height=600)
        canvas.pack()
        img = ImageTk.PhotoImage(im)
        canvas.create_image(100, 100, anchor=tk.NW, image=img)

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
        if len(recomList) > 20:
            for x in recomList:
                results.insert(tk.END, x.name)
        else:
            if m.custom is not None:
                for x in m.custom:
                    m.recommendedHistory.append(x)
                    results.insert(tk.END, x.name)

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

class customScene(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)

        frame = tk.Frame(root, bg="#990000")
        frame.place(relx=.2, relwidth=.8, relheight=1)

        header = tk.Message(frame, text="Custom Recipe ", bg="#990000", fg="white", font=tkFont.Font(size=30), width=300)
        header.pack(side="top")

        nameBox = tk.LabelFrame(frame, bg="#990000", text="Name of New Recipe", fg="white")
        nameBox.place(relx=.1, rely=.15, relw=.8, relh=.075)
        nameEntry = tk.Entry(nameBox)
        nameEntry.place(relx=.025, rely=.1, relw=.95, relh=.7)

        descBox = tk.LabelFrame(frame, bg="#990000", text="Description of New Recipe", fg="white")
        descBox.place(relx=.1, rely=.25, relw=.8, relh=.075)
        descEntry = tk.Entry(descBox)
        descEntry.place(relx=.025, rely=.1, relw=.95, relh=.7)

        tagsBox = tk.LabelFrame(frame, bg="#990000", text="Tags.  Please separate each tag by a comma ( , )", fg="white")
        tagsBox.place(relx=.1, rely=.35, relw=.8, relh=.075)
        tagEntry = tk.Entry(tagsBox)
        tagEntry.place(relx=.025, rely=.1, relw=.95, relh=.7)

        recipeBox = tk.LabelFrame(frame, bg="#990000", text="List of Ingredients.  Please separate each ingredient by a comma ( , )", fg="white")
        recipeBox.place(relx=.1, rely=.45, relw=.8, relh=.075)
        recipeEntry = tk.Entry(recipeBox)
        recipeEntry.place(relx=.025, rely=.1, relw=.95, relh=.7)

        prepBox = tk.LabelFrame(frame, bg="#990000", text="Prep Time", fg="white")
        prepBox.place(relx=.1, rely=.55, relw=.375, relh=.075)
        prepEntry = tk.Entry(prepBox)
        prepEntry.place(relx=.025, rely=.1, relw=.95, relh=.7)

        cookBox = tk.LabelFrame(frame, bg="#990000", text="Cook Time", fg="white")
        cookBox.place(relx=.5, rely=.55, relw=.4, relh=.075)
        cookEntry = tk.Entry(cookBox)
        cookEntry.place(relx=.025, rely=.1, relw=.95, relh=.7)

        servingBox = tk.LabelFrame(frame, bg="#990000", text="Serving Size", fg="white")
        servingBox.place(relx=.1, rely=.65, relw=.375, relh=.075)
        servingEntry = tk.Entry(servingBox)
        servingEntry.place(relx=.025, rely=.1, relw=.95, relh=.7)

        authorBox = tk.LabelFrame(frame, bg="#990000", text="Author", fg="white")
        authorBox.place(relx=.5, rely=.65, relw=.4, relh=.075)
        authorEntry = tk.Entry(authorBox)
        authorEntry.place(relx=.025, rely=.1, relw=.95, relh=.7)

        instrucBox = tk.LabelFrame(frame, bg="#990000", text="Instructions", fg="white")
        instrucBox.place(relx=.1, rely=.75, relw=.8, relh=.075)
        instrucEntry = tk.Entry(instrucBox)
        instrucEntry.place(relx=.025, rely=.1, relw=.95, relh=.7)

        confirm = tk.Button(frame, text="Confirm", command=lambda: m.createFood(nameEntry.get(), descEntry.get(), tagEntry.get(), prepEntry.get(), cookEntry.get(), servingEntry.get(), recipeEntry.get(), instrucEntry.get(), authorEntry.get()))
        confirm.place(relx=.125, rely=.85, relw=.3, relh=.075)

        reset = tk.Button(frame, text="Reset Fields", command=lambda: self.master.switchScene(customScene))
        reset.place(relx=.55, rely=.85, relw=.3, relh=.075)

# 0Name, 1Description, 2Tags, 3Prep Time, 4Cook Time, 5Servings, 6Recipe, 7Instructions, 8Picture, 9Author

app = Application(master=root)

app.master.title("The Computational Cookbook")

app.mainloop()
