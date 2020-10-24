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

	void search();

	void Recommended();

	void getHistory();

	void createFood(string name, vector<ingred> recipe);

	void favorites();

	void shoppingList();

	void createFromOwn(vector<ingred> ingredients);

private:
	vector<Food> foodList;
};

