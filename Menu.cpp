#include "Menu.h"

Menu::Menu() {
	foodList.resize(0);
	history.resize(0);
	shoppingCart.resize(0);
}


void Menu::search(vector<string> keyWord) {
	vector<Food> searchResults;

	for (unsigned int i = 0; i < foodList.size(); ++i) { // Iterates through all food

		int value = 0;

		for (unsigned int j = 0; j < foodList.at(i).getKeyWords().size(); ++j) { // Iterates through all key words in each food object

			for (unsigned int k = 0; k < keyWord.size(); ++k) {
				if (keyWord.at(k) == foodList.at(i).getKeyWords().at(j))
					++value;
			}
		}
	}

}

void Menu::Recommended() {

}

void Menu::addHistory(Food food) {
	history.push_back(food);
}

void Menu::removeHistory() {
	history.pop_front();
}

list<Food> Menu::getHistory() {
	return history;
}

void Menu::createFood(string name, vector<ingred> recipe) {
	foodList.push_back(Food(name, recipe));
}

void Menu::favorite(Food food) {
	food.setFavorite(!food.getFavorite());
}

void Menu::shoppingList() {

}