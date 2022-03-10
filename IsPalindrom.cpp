//============================================================================
// Name        : IsPalindrom.cpp
// Author      : Guguch
// Version     :
// Copyright   : Your copyright notice
// Description : Hello World in C++, Ansi-style
//============================================================================

#include <iostream>
#include <string>
using namespace std;

bool IsPalindrom (string str)
{
	for(size_t i = 0; i < str.size()/2; i++)
		if (str[i] != str[str.size()-1-i])
			return false;
	return true;
}

int main() {
	string str;
	bool b;

	cin >> str;
	b = IsPalindrom (str);
	cout << b;

	return 0;
}
