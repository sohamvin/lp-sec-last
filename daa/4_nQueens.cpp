#include<bits/stdc++.h>
using namespace std;

int solutionCount = 0; 

bool isSafe(int **arr, int x, int y, int n){
    // Check column
    for(int row=0;row<n;row++){
        if(row != x && arr[row][y]==1){
            return false;
        }
    }

    int row = x;
    int col = y;
    while(row>=0 && col>=0){
        if(arr[row][col]==1 && row != x){
            return false;
        }
        row--;
        col--;
    }


    row = x;
    col = y;
    while(row>=0 && col<n){
        if(arr[row][col]==1 && row != x){
            return false;
        }
        row--;
        col++;
    }


    row = x;
    col = y;
    while(row<n && col>=0){
        if(arr[row][col]==1 && row != x){
            return false;
        }
        row++;
        col--;
    }


    row = x;
    col = y;
    while(row<n && col<n){
        if(arr[row][col]==1 && row != x){
            return false;
        }
        row++;
        col++;
    }

    return true;
}

void printBoard(int **arr, int n){
	for(int i=0;i<n;i++){
        for(int j=0;j<n;j++){
			if(arr[i][j] == 1) cout << "[Q]";
			else cout << "[ ]";
		}
        cout << endl;
	}
	cout << endl;
	cout << endl;
}


void nQueen(int** arr, int x, int n, int startRow){
    if(x == n){
        solutionCount++;
        cout << "Solution " << solutionCount << ":\n";
        printBoard(arr, n);
		return;
    }

    // Skip the row where we already placed the starting queen
    if(x == startRow){
        nQueen(arr, x+1, n, startRow);
        return;
    }

    for(int col=0;col<n;col++){
        if(isSafe(arr,x,col,n)){
            arr[x][col]=1;
            nQueen(arr,x+1,n,startRow);
            arr[x][col]=0;
        }
    }
}


int main(){
    int n;
    int startRow, startCol;
    
    
    cout << "Enter the board size (n for nxn board): ";
    cin >> n;
    

    if(n <= 0){
        cout << "Invalid board size!" << endl;
        return 0;
    }
    
  
    cout << "Enter starting row (0 to " << n-1 << "): ";
    cin >> startRow;
    cout << "Enter starting column (0 to " << n-1 << "): ";
    cin >> startCol;
    

    if(startRow < 0 || startRow >= n || startCol < 0 || startCol >= n){
        cout << "Invalid starting position!" << endl;
        return 0;
    }
    
    int **arr = new int*[n];    
    for(int i=0;i<n;i++){
        arr[i] = new int[n];
        for(int j=0;j<n;j++){
            arr[i][j]=0;
        }
    }
    

    arr[startRow][startCol] = 1;
    

    if(!isSafe(arr, startRow, startCol, n)){
        cout << "\nInvalid starting position - conflicts detected!" << endl;
        // Clean up memory
        for(int i=0;i<n;i++){
            delete[] arr[i];
        }
        delete[] arr;
        return 0;
    }
    
    cout << "\n--------All possible solutions with Queen at (" 
         << startRow << "," << startCol << ")--------\n\n";
    
    // Reset solution counter
    solutionCount = 0;
    
    // Start solving from row 0, will skip startRow automatically
    nQueen(arr, 0, n, startRow);
    
    // Check if any solutions were found
    if(solutionCount == 0){
        cout << "No solutions exist with a queen at position (" 
             << startRow << "," << startCol << ")." << endl;
    } else {
        cout << "--------Total solutions found: " << solutionCount << "--------" << endl;
    }
    
    // Clean up memory
    for(int i=0;i<n;i++){
        delete[] arr[i];
    }
    delete[] arr;
    
    return 0;
}

/*
Time Complexity: O(N!)
Auxiliary Space: O(N^2)
*/