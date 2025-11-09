#include <iostream>
#include <queue>
#include <vector>
#include <unordered_map>
using namespace std;

struct HuffmanNode {
    char data;                  // Input character
    int frequency;              // Frequency of the character
    HuffmanNode *left, *right;  // Left and right children

    HuffmanNode(char data, int frequency) {
        left = right = nullptr;
        this->data = data;
        this->frequency = frequency;
    }
};

// Comparator to order the min-heap (priority queue)
struct Compare {
    bool operator()(HuffmanNode* left, HuffmanNode* right) {
        return left->frequency > right->frequency;
    }
};

// Function to print the Huffman codes
void printCodes(HuffmanNode* root, string code, unordered_map<char, string>& huffmanCodes) {
    if (!root) return;

    // If this node is a leaf node, it contains a character
    if (!root->left && !root->right) {
        huffmanCodes[root->data] = code;
        cout << root->data << ": " << code << endl;
    }

    // Traverse left and right subtrees
    printCodes(root->left, code + "0", huffmanCodes);
    printCodes(root->right, code + "1", huffmanCodes);
}

// Function to build the Huffman tree and print codes
void buildHuffmanTree(const string& text) {
    // Count the frequency of each character
    unordered_map<char, int> frequencyMap;
    for (char ch : text) {
        frequencyMap[ch]++;
    }

    // Create a priority queue (min-heap)
    priority_queue<HuffmanNode*, vector<HuffmanNode*>, Compare> pq;

    // Create a leaf node for each character and add it to the priority queue
    for (auto pair : frequencyMap) {
        pq.push(new HuffmanNode(pair.first, pair.second));
    }

    // Iterate until there is only one node left in the priority queue
    while (pq.size() > 1) {
        // Remove two nodes of the highest priority (lowest frequency)
        HuffmanNode* left = pq.top();
        pq.pop();
        HuffmanNode* right = pq.top();
        pq.pop();

        // Create a new internal node with frequency equal to the sum of the two nodes' frequencies
        HuffmanNode* newNode = new HuffmanNode('\0', left->frequency + right->frequency);

        newNode->left = left;
        newNode->right = right;

        // Add the new node to the priority queue
        pq.push(newNode);
    }

    // The remaining node is the root of the Huffman tree
    HuffmanNode* root = pq.top();

    // Traverse the Huffman tree and store the codes in a map
    unordered_map<char, string> huffmanCodes;
    printCodes(root, "", huffmanCodes);

    // Print the encoded string
    cout << "\nEncoded string: ";
    for (char ch : text) {
        cout << huffmanCodes[ch];
    }
    cout << endl;
}

int main() {
    string text;
    cout << "Enter text to encode using Huffman Encoding: ";
    getline(cin, text);

    buildHuffmanTree(text);

    return 0;
}