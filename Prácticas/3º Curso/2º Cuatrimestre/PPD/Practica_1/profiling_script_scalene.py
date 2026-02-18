import re
from collections import defaultdict
from scalene import scalene_profiler

# Function to read a text file
def read_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        text = file.read()
    return text

# Function to clean the text
def clean_text(text):
    text = text.lower()
    text = re.sub(r'[^\w\s]', '', text)
    return text

# Non-optimized function: word counting
def count_words_slow(text):
    words = text.split()
    count = {}
    for word in words:
        if word in count:
            count[word] += 1
        else:
            count[word] = 1
    return count

# Optimized function: word counting
def count_words_fast(text):
    words = text.split()
    count = defaultdict(int)
    for word in words:
        count[word] += 1
    return count

# Function to find the N most common words
def most_common_words(count, n=10):
    return sorted(count.items(), key=lambda x: x[1], reverse=True)[:n]

# Main function
def main():
    file_path = 'book.txt'
    text = read_file(file_path)
    cleaned_text = clean_text(text)

    # Word count (slow algorithm)
    slow_count = count_words_slow(cleaned_text)

    # Word count (fast algorithm)
    fast_count = count_words_fast(cleaned_text)

    # Find the 10 most common words
    common_words = most_common_words(fast_count, n=10) 
    print("Most common words:", common_words)

if __name__ == "__main__":
    main()
