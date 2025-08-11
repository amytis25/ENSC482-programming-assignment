#include <iostream>
#include <iomanip> 
#include <iomanip>
#include <cmath>
using std::cout;
using std::endl;
using std::cin;
using std::setw;
using std::fixed;
using std::setprecision;
using std::abs;
#include <string>
using std::string;

// sorting algorithm reference: https://www.softwaretestinghelp.com/sorting-techniques-in-cpp/
int main() {
    
    int i, j;
    string temp;
    string a[] = {"Apples","Olive Oil","Bananas","Grapes","Oranges"};
    string sorted [sizeof(a)];
    cout <<"Grocery list:" <<endl;
    for(i = 0; i<5; i++) {
        cout <<a[i]<<endl;
    }
    cout<<endl;
for(i = 0; i<5; i++) {
   for(j = i+1; j<5; j++)
   {
      if(a[j] < a[i]) {
         temp = a[i];
         a[i] = a[j];
         a[j] = temp;
      }
   }
}
cout <<"Sorted Grocery List ...\n";
for(i = 0; i<5; i++) {
   cout <<a[i]<<endl;
   }

    return 0;
}