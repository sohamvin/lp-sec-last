import heapq
from collections import Counter

class Node:
    def __init__(self, char, freq):
        self.char = char
        self.freq = freq
        self.left = None
        self.right = None
    
    # For heap comparison (lower frequency = higher priority)
    def __lt__(self, other):
        return self.freq < other.freq

def build_huffman_tree(text):
    """Build Huffman tree from input text"""
    # Count character frequencies
    frequency = Counter(text)
    
    # Create a min-heap with leaf nodes
    heap = [Node(char, freq) for char, freq in frequency.items()]
    heapq.heapify(heap)
    
    # Build the tree by combining nodes
    while len(heap) > 1:
        left = heapq.heappop(heap)
        right = heapq.heappop(heap)
        
        # Create parent node
        parent = Node(None, left.freq + right.freq)
        parent.left = left
        parent.right = right
        
        heapq.heappush(heap, parent)
    
    return heap[0]  # Root of the tree

def generate_codes(node, code="", codes={}):
    """Generate Huffman codes by traversing the tree"""
    if node is None:
        return codes
    
    # If leaf node, store the code
    if node.char is not None:
        codes[node.char] = code
        return codes
    
    # Traverse left (add '0') and right (add '1')
    generate_codes(node.left, code + "0", codes)
    generate_codes(node.right, code + "1", codes)
    
    return codes

def huffman_encoding(text):
    """Complete Huffman encoding process"""
    if not text:
        return "", {}
    
    # Build tree and generate codes
    root = build_huffman_tree(text)
    codes = generate_codes(root)
    
    # Encode the text
    encoded = "".join(codes[char] for char in text)
    
    return encoded, codes

# Example usage
if __name__ == "__main__":
    text = input("Enter text to encode: ")
    
    encoded_text, huffman_codes = huffman_encoding(text)
    
    print("\nHuffman Codes:")
    for char, code in sorted(huffman_codes.items()):
        print(f"'{char}': {code}")
    
    print(f"\nOriginal text: {text}")
    print(f"Encoded text: {encoded_text}")
    print(f"\nOriginal size: {len(text) * 8} bits")
    print(f"Compressed size: {len(encoded_text)} bits")
    print(f"Compression ratio: {len(encoded_text) / (len(text) * 8):.2%}")