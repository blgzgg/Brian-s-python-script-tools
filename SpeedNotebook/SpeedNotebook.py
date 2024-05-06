import os
from datetime import datetime

def createOrOpenJournal():
    journalFile = "MySpeedNotebook.txt"
    if not os.path.exists(journalFile):
        with open(journalFile, 'w') as file:
            file.write("My Speed Notebook\n\n")
    return journalFile

def writeEntry(journalFile):
    entry = input("Enter your journal entry: ")
    timestamp = datetime.now().strftime("%Y-%m-%d %I:%M:%S %p")
    with open(journalFile, 'a') as file:
        file.write(f"\n{timestamp}\n{entry}\n")

def main():
    journalFile = createOrOpenJournal()
    writeEntry(journalFile)

if __name__ == "__main__":
    main()