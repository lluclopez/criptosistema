def substitution(text, old, new):
    return text.replace(old, new)

def main():
    original_text = "Hello, World!"
    modified_text = substitution(original_text, "World", "Python")
    print(modified_text)

if __name__ == "__main__":
    main()