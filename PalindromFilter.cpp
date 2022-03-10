//============================================================================
// Name        : PalindromFilter.cpp
// Author      : Guguch
// Version     :
// Copyright   : Your copyright notice
// Description : Hello World in C++, Ansi-style
//============================================================================

#include <iostream>
#include <vector>
#include <string>
using namespace std;

void show_vector( vector<string>& a_vec)
{
        for (vector<string>::iterator it = a_vec.begin() ; it!=a_vec.end() ; ++it)
                cout<<*it << " ";
        cout << endl;
}

vector<string> PalindromFilter (vector<string> v, int minLength)
{
	string str;
	bool b;
	size_t min = minLength;
	vector<string> r;

	for(size_t i = 0; i < v.size(); i++)
	{
		str = v[i];
		//cout << "1)" << str << endl;
		b = 1;
		if (str.size() >= min)
		{
			//cout << "Working" << endl;
			for(size_t j = 0; j < str.size()/2; j++)
			{
				if (str[j] != str[str.size()-1-j])
					b = 0;
			}
		}
		else b = 0;

		if (b ==  1)
				r.push_back(str);
	}
	return r;
}

int main() {
	vector<string> v;
	int num_words =  0;
	int minLength = 0;
	string s;

	cin >> num_words;
	cin >> minLength;
	for (int i = 0; i < num_words; i++)
	{
		cin >> s;
		v.push_back(s);
	}

	//show_vector(v);

	//cout << "starting PalindromFilter" << endl;

	v = PalindromFilter (v, minLength);
	show_vector(v);

	//cout << "ending" << endl;

	return 0;
}
