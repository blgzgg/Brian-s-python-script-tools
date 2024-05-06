import sys
import os

def read_strings_from_file(filename):
    try:
        with open(filename, 'r') as file:
            strings = file.read().splitlines()
        return strings
    except FileNotFoundError:
        return []

def write_strings_to_file(filename, strings):
    with open(filename, 'w') as file:
        for string in strings:
            file.write(string + '\n')

def search():
    
    return

def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    filename = os.path.join(script_dir, 'pmu_recruit_list.txt')
    strings = read_strings_from_file(filename)

    while True:
        new_string = input("Enter a Pokemon (or press Enter to exit): ")

        if new_string == "":
            break

        if new_string == "1":
            search()
        elif new_string in strings:
            print("The Pokemon has already been recruited.")
        else:
            print("The Pokemon has been added to the list of recruits.")
            strings.append(new_string)
            write_strings_to_file(filename, strings)

    print("Exiting the program.")

if __name__ == "__main__":
    main()
