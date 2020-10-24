#pragma once
#include "Food.h"

using namespace std;

class Menu
{
public:
	Menu();
	/*
		Search
		Recommended
		Create own Recipe
		Favorites
		History
		Location/Map if time allows
		Shopping List
		Make from Ingredients
	*/

	void search(vector<string> keyWord);

	void Recommended();

	void addHistory(Food food);
	void removeHistory();
	list<Food> getHistory();

	void createFood(string name, vector<ingred> recipe);

	void favorite(Food food);

	void shoppingList();

private:
	vector<Food> foodList;
	list<Food> history;
	vector<Food> shoppingCart;
};

