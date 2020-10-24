#include "Menu.h"

Menu::Menu() {
	foodList.resize(0);
}


void Menu::search() {

}

void Menu::Recommended() {

}

void Menu::getHistory() {

}

void Menu::createFood(string name, vector<ingred> recipe) {
	foodList.push_back(Food(name, recipe));

}

void Menu::favorites() {

}

void Menu::shoppingList() {

}

void Menu::createFromOwn(vector<ingred> ingredients) {

}