#include <iostream>
#include <algorithm>
#include <vector>

using namespace std;
const int MAXN = 1e5+152;

vector <int> adj[MAXN];
int n;


int main()
{
    cin>>n;

    for(int i = 0;i<n;i++)
    {
        int a,b;
        cin>>a>>b;

        adj[a].push_back(b);
        
        


    }
    





    return 0;
}






