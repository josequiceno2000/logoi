
abs_file_path = "./bibles/new-testament/2-john/2-john-eng.txt"
try:
    with open(abs_file_path, 'r', encoding='utf-8') as file:
        content = file.read()
        print(content)
except FileNotFoundError:
    print(f"Error: file does not exist at {abs_file_path}")
except Exception as e:
    print(f"An error occurred: {e}")