
import os
import shutil
import sys


from openai import OpenAI

from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Indicate your target folders here
FoldersArray = ["General", "Database"]
existingFoldersArray = ', '.join(FoldersArray)

# Replace 'C:\\Users\\YourUsername\\Downloads' with the actual path to your Downloads folder, or whatever folder you want to organise
# downloads_path = 'C:\\Users\\65820\\Downloads\\TestingCool'
downloads_path = 'C:\\Users\\65820\\Downloads\\OrganiserDemo\\TestingCoolPart4'

client = OpenAI(
   
)

def list_files_in_directory(directory):
    file_list = []
    for filename in os.listdir(directory):
        path = os.path.join(directory, filename)
        if os.path.isfile(path):
            file_list.append(filename)
    if file_list == []:
        print("There are no files found in specified directory.")
        sys.exit()
    else: return file_list


files = list_files_in_directory(downloads_path)
files_paragraph = '#' + '#'.join(files) + '#'


foldersArray = 0
priority = ""
promptAddFolders = ""
stringoutput = ""


def list_folders_in_directory(directory):
    folder_list = []
    for filename in os.listdir(directory):
        path = os.path.join(directory, filename)
        if os.path.isdir(path):
            folder_list.append(filename)
    return folder_list

def readline_sync(prompt=""):
    while True:
        user_input = input(prompt).strip().upper()  # Convert input to uppercase and remove leading/trailing spaces
        if user_input in ('Y', 'N'):
            return user_input
        else:
            print("Invalid input. Please enter 'Y' or 'N'.")
            
def GPT_Organise(files_paragraph, insert):
    
    inputPrompt = "You are foldersGPT. You are excellent at organizing files. Using your immense deduction based on file naming structures and conventions, you are able to accurately group the files together. I will be giving you a list of file names. " + insert + " Using the EXACT file name e.g. 67-SQL64*9AE.docx, you will strictly present your output in the following format: {FolderA}#File1#File2#File3#{FolderB}#File4#File5#File6#{FolderC}#File7#File8#File9#{FolderD}#File10#File11#File12#.....and so on. Remember, you MUST output the EXACT file name even if it begins with a number, DO NOT autocorrect or make assumptions"

    # print(inputPrompt)
    print("Connecting to GPT... Loading...\n")

    # Make the API call
    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": inputPrompt},
            {"role": "user", "content": files_paragraph}
        ]
    )

    # Extract and return the string output
    return completion.choices[0].message.content
            
            
def create_folders_and_move_files(output_structure, base_folder):
    components = output_structure.split('#')
    current_folder = None

    for item in components:
        item = item.strip()
        
        # Skip further processing for empty items
        if not item:
            continue
        
        if item.startswith('{') and item.endswith('}'):
            # It's a folder
            current_folder = item.strip('{}')
            folder_path = os.path.join(base_folder, current_folder)
            os.makedirs(folder_path, exist_ok=True)
        elif current_folder:
            # It's a file and we have a current folder
            if os.path.isdir(os.path.join(base_folder, item)):
                # It's a directory
                print(f"Skipped moving: {item} to {current_folder}. Directories cannot be moved into themselves.")
            else:
                # It's a file
                source_path = os.path.join(base_folder, item)
                destination_path = os.path.join(base_folder, current_folder, item)

                try:
                    # Check if the source and destination paths are different
                    if source_path != destination_path:
                        shutil.move(source_path, destination_path)
                        print(f"Moved: {item} to {current_folder}")
                    else:
                        print(f"Skipped moving: {item} to {current_folder}. Source and destination are the same.")
                except FileNotFoundError:
                    print(f"File not found: {item}")


folders_paragraph = ""

print("Welcome to folder organiser")

# Example usage
ConfirmFirstStatus = readline_sync("Please state if you have existing folders (Y), or you would like AI to auto create new folders (N):\n")
# print(f"1: Confirmation status: {ConfirmFirstStatus}")  

if ConfirmFirstStatus == 'Y':
    FirstStatusChoice1 = readline_sync("Target all existing folders in directory (Y) or specific folders (N):\n")
    
    if FirstStatusChoice1 == 'Y':
    
        # Retireve All Folders
        folders = list_folders_in_directory(downloads_path)

        folders_paragraph = ',' + ','.join(folders) + ','
        
        promptAddFolders = "Your aim is to group the files into specific THESE folders NAMES: " + folders_paragraph + ". Prioritize file grouping based on the folder name, you MUST use all the folders"
        
        stringoutput = GPT_Organise(files_paragraph, promptAddFolders)

    elif FirstStatusChoice1 == 'N':
        
        FirstStatusChoice2 = readline_sync("Your targetted existing folders are " + existingFoldersArray + ", or you would like to continue (Y) or exit and amend it at FoldersArray (N):\n")
   
        if FirstStatusChoice2 == 'Y':
            
            folders_paragraph = existingFoldersArray
            
            promptAddFolders = "Your aim is to group the files into specific THESE folders NAMES: " + folders_paragraph + ". Prioritize file grouping based on the folder name, you MUST use all the folders"
            
            stringoutput = GPT_Organise(files_paragraph, promptAddFolders)
            
        elif FirstStatusChoice2 == 'N':
            
            exit()
            
        else:
            print("You should not be seeing this")
    else:
        print("You should not be seeing this")
       
    # Your code for the 'Y' case
    # existingFoldersConfirmation = readline_sync("Your targetted existing folders are in the array " + existingFoldersArray + ", or you would like to continue (Y) or go back and amend it (N):\n")
    #create_folders_and_move_files()
    
elif ConfirmFirstStatus == 'N':
    
    SecondStatusChoice1 = readline_sync("Sort by File Name (Y) or File Type (N):\n")
    
    
    if SecondStatusChoice1 == 'Y':
        
        priority = "Your aim is to create new folders for them, and then, group the files into those folders. The folder you name must be a CONCISE and SHORT SINGLE KEYWORD. Prioritize grouping by a SHORT key word in common file names. Do NOT organise by file type."
        
        # GPT_Organise(files_paragraph, priority, promptAddFolders)
        stringoutput = GPT_Organise(files_paragraph, priority)
        
    elif SecondStatusChoice1 == 'N':
        
        priority = "Your aim is to create new folders for them, and then, group the files into those folders. The folder you name must be concise and SHORT. Prioritize grouping by file type before name." 
        stringoutput = GPT_Organise(files_paragraph, priority)
    
    else:
        print("You should not be seeing this")

else:
    print("You should not be seeing this")


# print(stringoutput)

print("\nLoaded, ChatGPT output generated!")
print("Folder Structure Summary:") 

# Iterate through each entry and print the overview
current_folder = None


def print_folder_structure(stringoutput):
    entries = stringoutput.split('#')

    # Iterate through each entry and print the overview
    current_folder = None

    for entry in entries:
        entry = entry.strip()

        if entry.startswith('{') and entry.endswith('}'):
            # It's a folder
            current_folder = entry.strip('{}')
            print(f"\n{current_folder}:")
        elif current_folder:
            # It's a file and we have a current folder
            print(entry)

    print("\n")
    
print_folder_structure(stringoutput)

def confirm_and_proceed():
    ConfirmStatus = readline_sync("I confirm that I want to proceed (Y or N):\n")
    # print(f"Confirmation status: {ConfirmStatus}")

    if ConfirmStatus == 'Y':
        # Your code for the 'Y' case
        print("You confirmed to proceed. Proceeding...\n")
        return True
    elif ConfirmStatus == 'N':
        # Your code for the 'N' case
        print("You chose not to proceed, Bye! Maybe try again if the response wasnt satisfactory ;)")
        return False
    else:
        print("Invalid input. Please enter 'Y' or 'N'.")
        return False


# Example usage
if confirm_and_proceed():
    create_folders_and_move_files(stringoutput, downloads_path)



