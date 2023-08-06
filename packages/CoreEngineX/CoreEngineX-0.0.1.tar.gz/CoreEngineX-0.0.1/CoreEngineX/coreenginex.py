"""
CoreEngineX will fetch the python files from the directory/sub-directories.
Display those files in the command line interface menu. Execute the files sequentially.
The option to check the pylint score of the files is provided and
also the option to load the environment variables.

Note:
    You can Ignore the directories, files and extensions by adding them in the
    IGNORE_DIRS, IGNORE_FILES and IGNORE_EXTENSIONS list.
"""
import os
import sys
import time


class CoreEngineX:
    """
    CoreEngineX will fetch the python files from the directory/sub-directories.
    Display those files in the command line interface menu. Execute the files sequentially.
    The option to check the pylint score of the files is provided and
    also the option to load the environment variables.

    Note:
        You can Ignore the directories, files and extensions by adding them in the
        IGNORE_DIRS, IGNORE_FILES and IGNORE_EXTENSIONS list.
    """
    IGNORE_DIRS = []
    IGNORE_FILES = []
    IGNORE_EXTENSIONS = []

    __IGNORE_DIRS = ['env', 'venv', '__pycache__'] + IGNORE_DIRS
    __IGNORE_FILES = ['__init__.py', 'setup.py'] + IGNORE_FILES
    # __IGNORE_EXTENSIONS = ['.pyc', '.pyo', '.txt'] + IGNORE_EXTENSIONS

    def __init__(self) -> None:
        """
        Initialize the variables.
        """
        self.__list_of_files = None

    def __coreenginex_display(self) -> None:
        """
        Display the CoreEngineX logo.

        Returns:
            None
        """
        print(
            """
░▒█▀▀▄░▄▀▀▄░█▀▀▄░█▀▀░▒█▀▀▀░█▀▀▄░█▀▀▀░░▀░░█▀▀▄░█▀▀░▀▄░▄▀
░▒█░░░░█░░█░█▄▄▀░█▀▀░▒█▀▀▀░█░▒█░█░▀▄░░█▀░█░▒█░█▀▀░░▒█░░
░▒█▄▄▀░░▀▀░░▀░▀▀░▀▀▀░▒█▄▄▄░▀░░▀░▀▀▀▀░▀▀▀░▀░░▀░▀▀▀░▄▀▒▀▄
                           - By Sai Akhil Kumar Reddy N
            """
        )

    def invalid_choice(self) -> None:
        """
        Display the invalid choice message.

        Returns:
            None
        """
        print("=====================================")
        print("Invalid Choice")
        print("Exiting the program")
        print("=====================================")
        sys.exit()

    def only_numbers_allowed(self) -> None:
        """
        Display the only numbers are allowed message.

        Returns:
            None
        """
        print("=====================================")
        print("Only numbers are allowed!!")
        print("=====================================")

    def selected_file_options(self) -> None:
        """
        Display the options for selected file.

        Returns:
            None
        """
        print("=====================================")
        print("Do you want to execute this file?")
        print("=====================================")
        print("1. Execute the file")
        print("2. Check pylint score")
        print("=====================================")

    def load_environment_variables(self, key_value: dict) -> None:
        """
        Create the environment variables using key_value dictionary

        Args:
            key_value (dict): The dictionary with key and value

        Returns:
            None
        """
        for key, value in key_value.items():
            os.environ[key] = value

    def fetch_files_from_dir(self, directory: str) -> list:
        """
        Fetch the files from the directory.

        Args:
            directory (str): The directory path

        Returns:
            list: The list of files in the directory

        Note:
            This method will fetch the files with .py extension only.
        """
        __file_extension = ".py"
        if os.path.isdir(directory):
            self.__list_of_files = [os.path.join(root, name)
                            for root, dirs, files in os.walk(directory)
                            if root.split(os.sep)[-1] not in self.__IGNORE_DIRS
                            for name in files
                            if name not in self.__IGNORE_FILES
                            if name.endswith((f"{__file_extension}"))]
            return self.__list_of_files
        raise FileNotFoundError(f"Directory not found: {directory}")

    def pylint_score_of_python_files(self):
        """
        Check the pylint score of the python files.
        """
        for each_file in self.__list_of_files:
            os.system(f'python -m pylint {each_file}')

    def execute_python_files(self):
        """
        Execute the python files sequentially.
        """
        for each_file in self.__list_of_files:
            print(f'Executing file: {each_file}')
            os.system(f'python {each_file}')
            time.sleep(1)

    def list_of_files_menu(self, list_of_files: dict):
        """
        List of files menu.
        """
        self.__coreenginex_display()
        print("=====================================")
        print("List of files in the directory: ")
        print("=====================================")
        for key, value in list_of_files.items():
            print(f'{key}.', end = ' ')
            for each_value in value:
                print(f'{each_value}')
        print("=====================================")

    def command_line_menu(self):
        """
        Command Line Interface Menu.
        """
        # Empty dictionary to store the file name and file path
        files_and_paths = {}

        # Empty dictionary to store the keys of file_path
        inc_file_dict = {}

        # Increment number
        inc_number = 0

        for each_file_path in self.__list_of_files:
            # Get the incrementing number
            inc_number += 1

            # Extract the file name from the file path
            file_name = each_file_path[each_file_path.rfind("\\") + 1:]

            # Extract the file name without the extension
            filename_wo_ext = file_name[:file_name.rfind(".")]
            # Output: login_profile_details_4_2

            # create a dictionary with the each_file as value and filename_wo_ext as key
            files_and_paths[filename_wo_ext] = each_file_path

            # Assign the key of file_path to testcases_dict as value
            # using dict comprehension
            inc_file_dict[inc_number] = {key for key, value in files_and_paths.items() \
                                                                    if key == filename_wo_ext}

        inc_file_dict[len(files_and_paths) + 1] = {"Execute the listed files": True}
        inc_file_dict[len(files_and_paths) + 2] = {"Check pylint score of listed files": False}
        inc_file_dict[len(files_and_paths) + 3] = {"Exit": False}

        self.list_of_files_menu(inc_file_dict)

        try:
            file_inc_number = int(input("Enter the number: "))
        except ValueError:
            self.only_numbers_allowed()
            self.command_line_menu()

        if file_inc_number == len(files_and_paths) + 1:
            self.execute_python_files()
        elif file_inc_number == len(files_and_paths) + 2:
            self.pylint_score_of_python_files()
        elif file_inc_number == len(files_and_paths) + 3:
            self.invalid_choice()
        elif file_inc_number in inc_file_dict:
            print("=====================================")
            print(f"You have selected the file: {file_inc_number}.", end = ' ')
            for each_value in inc_file_dict[file_inc_number]:
                print(f'{each_value}')
            self.selected_file_options()

            try:
                user_input = int(input("Enter your choice: "))
            except ValueError:
                self.only_numbers_allowed()
                self.command_line_menu()

            if user_input == 1:
                print("=====================================")
                print("Executing the file...\n")
                for each_value in inc_file_dict[file_inc_number]:
                    os.system(f'python {files_and_paths[each_value]}')
            elif user_input == 2:
                print("=====================================")
                for each_value in inc_file_dict[file_inc_number]:
                    os.system(f'python -m pylint {files_and_paths[each_value]}')
                print("=====================================")
                sys.exit()
            else:
                self.invalid_choice()
        else:
            self.invalid_choice()

    def run_coreenginex(self, folder_path: str):
        """
        Run the Core Engine X.

        Args:
            folder_path (str): The folder path where the files are present.
        """
        self.fetch_files_from_dir(directory = folder_path)
        self.command_line_menu()
