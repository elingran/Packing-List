import json


class PackingList:
    """
    Attributes:
    name: the name of the list
    date: the date when the list is created
    elements: a list of all elements that will be brought on the trip
    marked_elements: a list with all marked elements
    """

    def __init__(self, name, date):
        """Creates a new packing list
        :param name: the name of the list
        :param date: the date when the list is created"""
        self.name = name
        self.date = date
        self.elements = []
        self.marked_elements = []

    def object_to_list(self):
        """Writes all attributes of an object into a list
        Used to be able to write (and then read) a dict with class objects as values to the json file.
        """
        class_object = [self.name, self.date, self.elements, self.marked_elements]
        return class_object

    def display_not_packed_elements(self):
        """Used to display the elements that has not been marked as packed yet.
        :return: prints out a string including name, date and elements (only not packed) of the
        packing list sorted in alphabetic order.
        """

        elements_list = ""
        for element in self.elements:
            elements_list += "\n   ☐ " + element
        if len(elements_list) == 0:
            elements_list = "(None)"                            # If the list is empty the program say that instead of
        else:                                                   # printing nothing.
            self.elements.sort()

        return ("\nPACKING LIST:\n" + "Name: " + self.name + "\nDate: " + str(self.date) +
                "\n\nDon't forget:\n" + elements_list + "\n")

    def __str__(self):
        """Packing list information will be printed out.
        :return: A string including name, date and elements (both packed and not packed) of the
        packing list sorted in alphabetic order."""

        elements_list = ""
        for element in self.elements:
            elements_list += "\n   ☐ " + element
        if len(elements_list) == 0:
            elements_list = "(None)"
        else:
            self.elements.sort()

        marked_list = ""
        for element in self.marked_elements:
            marked_list += "\n   ☑ " + element
        if len(marked_list) == 0:
            marked_list = "(None)\n"

        return ("\nPACKING LIST:\n" + "Name: " + self.name + "\nDate: " + str(self.date) +
                "\n\nDon't forget:\n" + elements_list +
                "\n\nAlready packed:\n" + marked_list + "\n")

    def add_element(self):
        """Used to add an element to the list. Asks for
        input (the new element) then adds it to the list.
        :return: a string confirming the successful act """
        while True:
            element = input("What object do you want to add?\n")
            if element == "":                                           # Identifies if the user leave the field empty.
                print("This field can't be left empty. Enter again: ")
            else:
                break
        self.elements.append(element)
        return print("Added!")

    def remove_element(self):
        """Used to remove an element from a list. Prints out the elements existing in the list and asks
        user which one to remove. The elements will be numbered so the program expects an int
        (runs get_int_input) and will only accept a number between 1 and (number of elements).
        return: a string confirming the successful act """
        print("Items in this list:")
        count = 1
        connects_element_with_number = {}
        for element in self.elements:
            print(count, "-", element)
            connects_element_with_number[count] = element
            count += 1
        if len(connects_element_with_number) == 0:
            print("--- This is empty ---")
        else:
            chosen_element = get_int_input("Enter the number representing the item you want to delete:\n")
            while True:
                if 1 <= chosen_element <= len(connects_element_with_number.keys()):
                    self.elements.pop(chosen_element - 1)
                    print("Deleted!")
                    break
                else:
                    chosen_element = int(get_int_input("That isn't an item. Try again:\n"))

    def mark_element_as_packed(self):
        """ Used to mark an element as packed. Takes an element from the list elements and moves it
        to the list marked elements.
        return: a string confirming the successful act
        """
        choice = get_int_input("Would you like to mark anything as packed?\n 1 - Yes\n 2 - No\n")
        while True:
            if 1 <= choice <= 2:
                if choice == 1:
                    print("Items in this list:")
                    count = 1
                    connects_element_with_number = {}
                    for element in self.elements:
                        print(count, "-", element)
                        connects_element_with_number[count] = element
                        count += 1
                    if len(connects_element_with_number) == 0:
                        print("--------- This is empty ---------\n"
                              "Weeehooo, you are ready to go! :D\n")
                        print(self.__str__())
                        break
                    else:
                        chosen_element = get_int_input("Enter the number representing the item you want to "
                                                       "mark:\n")
                        while True:
                            if 1 <= chosen_element <= len(connects_element_with_number.keys()):
                                self.marked_elements.append(self.elements.pop(chosen_element - 1))
                                print("Done!")
                                choice = get_int_input("Would you like to mark another item?\n 1 - Yes\n 2 - No\n")
                                if choice == 2:
                                    print(self.__str__())
                                break
                            else:
                                chosen_element = get_int_input("That isn't an item. Try again:\n")
                else:
                    break
            else:
                choice = get_int_input("That isn't a choice. Try again:\n")


def read_lists_from_file(file_name):
    """Used to get data from file. Checks for errors and if something is found it will print out on
    which row and what error occurred. Then it moves on to the next packing list.
    :param file_name: The file with the information
    :return: A dictionary with all lists (as class objects) in it """
    global json_file
    while True:
        try:
            json_file = open(file_name, "r")
            list_dict = json.load(json_file)  # string
            for key in list_dict:
                list_of_object_attributes = list_dict[key]  # Takes the value from the dict (a list) and
                list_dict[key] = PackingList(list_of_object_attributes[0], list_of_object_attributes[1])
                list_dict[key].elements = list_of_object_attributes[2]  # Sets elements back into object
                list_dict[key].marked_elements = list_of_object_attributes[3]  # Sets packed elements back into object
            json_file.close()
            tuple = (list_dict, file_name)
            return tuple
        except IOError:
            file_name = input("Create a file to store your data.\n"
                              "What would you like it's name to be?\n") + ".json"
            open(file_name, "w")
        except json.decoder.JSONDecodeError:
            list_dict = {}
            while True:
                name = input("Now you have to create your first list!\nWhat would you like to name it to?\n")
                if name == "":
                    print("This field can't be left empty. Enter a name again: ")
                else:
                    break
            date = get_date_input("For which date is this list?")
            list_dict[name] = PackingList(name, date)
            answer = get_int_input("Would you like to add items to the list as well?\n1 - Yes\n2 - No\n")
            while True:
                if 1 <= answer <= 2:
                    if answer == 1:
                        list_dict[name].add_element()
                        answer = get_int_input("Would you like to add another one?\n1 - Yes\n2 - No\n")
                    else:
                        print(list_dict[name])
                        json_file.close()
                        tuple = (list_dict, file_name)
                        return tuple
                else:
                    answer = get_int_input("Enter either 1 or 2.\n")


def write_lists_to_file(list_dict, file_name):
    """Used to write the data to a file
    :param list_dict: The dictionary with the lists saved as Packing_list objects
    :param file_name: The file where all information will be saved.
    :return: (nothing)
    """
    json_file = open(file_name, "w")
    for key in list_dict:
        list_dict[key] = list_dict[key].object_to_list()
    json.dump(list_dict, json_file, indent=4)
    json_file.close()


def create_list():
    """Used to create a new packing list. Takes input from user (name and elements) and send it
    into the __init__-method together with todays_date. (self, name, date)
    :return: a string confirming that the list where successfully created
    """
    list_of_all_names = []
    for key in list_dict:
        list_of_all_names.append(list_dict[key].name)
    while True:
        name = input("The name of the list: ")
        if name == "":
            print("This field can't be left empty. Enter a name again: ")
        elif name in list_of_all_names:
            print("This list already exists.")
        else:
            break
    date = get_date_input("For which date is this list?")
    list_dict[name] = PackingList(name, date)
    answer = get_int_input("Would you like to add items to the list as well?\n1 - Yes\n2 - No\n")
    while True:
        if 1 <= answer <= 2:
            if answer == 1:
                list_dict[name].add_element()
                answer = get_int_input("Would you like to add another one?\n1 - Yes\n2 - No\n")
            else:
                print(list_dict[name])
                break
        else:
            answer = get_int_input("Enter either 1 or 2.\n")


def get_int_input(prompt_string):  # prompt_string = question
    """Used to get an int from the user, asks again if input is not convertible to int
    :param prompt_string: the string explaining what to input
    :return: the int that was asked for"""
    while True:
        try:
            number = int(input(prompt_string))
            return number
        except ValueError:
            prompt_string = "You didn't enter an integer, try again: "


def get_date_input(prompt_string):
    """
    Used to get date input from the user, asks again if input is not integers or an existing date. Decided to set a
    span over which year the date will be in to make it more realistic. Saves all dates on the format YYYYMMYY so
    it will be easy to sort them later.
    :param prompt_string: the string explaining what to input
    :return: an int with the date that was asked for """
    global dd, mm, yyyy
    print(prompt_string)
    while True:
        try:
            while True:
                year = input("Year (YYYY): ")
                if len(year) == 4:
                    yyyy = int(year)  # If year != int, except ValueError
                    if 1900 <= yyyy <= 2100:
                        yyyy = str(yyyy)
                        break
                    elif yyyy < 1900:
                        print("This was too long time ago. Please enter year 1900 or later.")
                    elif yyyy > 2100:
                        print("This is too far into the future. Please enter year 2100 or earlier.")
                else:
                    print("Enter year with four digits, please.")
            while True:
                month = int(input("Month (MM): "))
                if 1 <= month <= 9:
                    mm = str(0) + str(month)
                    break
                elif 10 <= month <= 12:
                    mm = str(month)
                    break
                else:
                    print("That is not a month. Try again.")
            while True:
                day = int(input("Day (DD): "))
                if 1 <= day <= 9:
                    dd = str(0) + str(day)
                    break
                elif 10 <= day <= 31:
                    dd = str(day)
                    break
                else:
                    print("That is not an existing day. Try again.")
        except ValueError:
            get_date_input("You didn't enter integers. Try again! ")
        months_without_31_days = ("04", "06", "09", "11")
        leap_years = list(range(1904, 2101, 4))
        if dd == "31" and mm in months_without_31_days:                             # Here it's validatig if the date
            print(dd + "/" + mm + "-" + yyyy + " is not an existing date... Try again!") # is existing.
        elif dd in ("30", "31") and mm == "02" and yyyy in leap_years:
            print(dd + "/" + mm + "-" + yyyy + " is not an existing date... Try again!")
        elif dd in ("29", "30", "31") and mm == "02" and yyyy not in leap_years:
            print(dd + "/" + mm + "-" + yyyy + " is not an existing date... Try again!")
        else:
            return yyyy + mm + dd


def display_a_list(list):
    """Gets a list (from either search through name or date), the user chooses whether to print all
    it's content or not the marked items.
    :param list: the list the user wants to display
    :return: nothing
    """
    choice = get_int_input("Would you like to display all items or just the ones you haven't packed yet??"
                           "\n1 - All\n2 - Just not packed\n")
    while True:
        if 1 <= choice <= 2:
            if choice == 1:
                print(list)
                if len(list.elements) != 0:
                    list.mark_element_as_packed()
                    break
                break
            elif choice == 2:
                print(list.display_not_packed_elements())
                if len(list.elements) != 0:
                    list.mark_element_as_packed()
                    break
                break
        else:
            choice = get_int_input("Please enter either 1 or 2.")


def display_upcoming_lists():
    """Used to display the coming lists after a defined date
    :return: prints the list the user wanted to see
    """
    a_choice = get_int_input("Would you like to display all lists or just the ones current after a certain date?"
                             "\n1 - All\n2 - I would like to enter a date\n")
    while True:
        if 1 <= a_choice <= 2:
            if a_choice == 1:
                upcoming_lists = sort_upcoming_lists_by_date(19000101)  # The first date a list can be created on
                if len(upcoming_lists) == 0:                            # will therefor print all lists.
                    print("There are no lists saved.")
                else:
                    print("These lists were found:")
                    for list in upcoming_lists:
                        print(list)
                    break
            elif a_choice == 2:
                date = int(get_date_input("From which date would you like to display lists?")) # func returns yyyy+mm+dd
                upcoming_lists = sort_upcoming_lists_by_date(date)
                if len(upcoming_lists) == 0:
                    print("There are no upcoming lists on or after this date.")
                else:
                    print("These lists were found:")
                    for list in upcoming_lists:
                        print(list)
                    break
        else:
            a_choice = get_int_input("Please enter either 1 or 2.")


def search_for_list_by_name():
    """Used to search for an existing list and show their content. Takes a string input from the user
    that should contain characters existing in any of the names. If not, print a
    string saying that no such list was found. If more than one list, show all lists whose name
    contains the search word.
    :return: the chosen list (referred to as class object)
    """
    while True:
        search_word = input("Enter the name of the list you want to display: ")
        if search_word == "":
            print("This field can't be left empty. Enter a name again: ")
        else:
            break
    while True:
        list_of_packing_lists_matched = []
        for key in list_dict:
            if search_word in key:
                list_of_packing_lists_matched.append(key)
        if len(list_of_packing_lists_matched) == 0:
            print("No list were found.")
            while True:
                search_word = input("\nWrite a new search word:\n")
                if search_word == "":
                    print("This field can't be left empty. Enter a name again: ")
                else:
                    break
        else:
            print("Lists found:")
            count = 1
            connects_list_with_number = {}
            for name_of_list in list_of_packing_lists_matched:
                print(count, "-", name_of_list)
                connects_list_with_number[count] = name_of_list
                count += 1
            chosen_list = get_int_input("Enter the number representing the list you're looking for:\n")
            while True:
                if 1 <= chosen_list <= len(connects_list_with_number.keys()):
                    return list_dict[connects_list_with_number[chosen_list]]
                else:
                    chosen_list = get_int_input("That isn't an option. Try again:\n")


def search_for_list_by_date():
    """ Used to search for lists via its date. Prints out all found
    list and makes the user decide which one it is.
    :return: the chosen list reffered to as class object
    """
    search_word = get_date_input("Enter the date of when the list is supposed to be used: ")
    while True:
        list_of_packing_lists_matched = []
        for key in list_dict:
            if search_word == list_dict[key].date:
                list_of_packing_lists_matched.append(list_dict[key].name)
        if len(list_of_packing_lists_matched) == 0:
            print("No list were found.")
            search_word = get_date_input("\nEnter a new date:\n")
        else:
            print("Lists found:")
            count = 1
            connects_list_with_number = {}
            for name_of_list in list_of_packing_lists_matched:
                print(count, "-", name_of_list)
                connects_list_with_number[count] = name_of_list
                count += 1
            chosen_list = get_int_input("Enter the number representing the list you're looking for:\n")
            while True:
                if 1 <= chosen_list <= len(connects_list_with_number.keys()):
                    return list_dict[connects_list_with_number[chosen_list]]
                else:
                    chosen_list = get_int_input("That isn't an option. Try again:\n")


def sort_upcoming_lists_by_date(date):
    """Used to sort all packing list depending on date
    :param: date: the first date the user wants to display packing lists from
    :return: a list where the class objects now are sorted after date and the lists that are left are the ones
             that are current after the date the user entered.
    """
    date_dict = {}
    upcoming_lists = []
    for keys in list_dict:
        date_dict[int(list_dict[keys].date)] = list_dict[keys]  # Creates a new dict with date as key and class object as value
    for key in sorted(date_dict.keys()):  # Sorts the new dict
        if key >= date:
            upcoming_lists.append(date_dict[key])  # Saves a new dict with the lists that will be displayed
    return upcoming_lists


def menu():
    """
    Used to display the menu
    :return: (nothing) """

    return print("----------- MENU -----------\n"
                 "\nWhat would you like to do?\n"
                 "\n1 – Create a new packing list\n"
                 "2 – Display content of list\n"
                 "3 – Add an element to a list\n"
                 "4 – Remove an element from a list\n"
                 "5 - Display upcoming packing lists\n"
                 "6 - Exit")


def menu_choice():
    """Used to get input on what the user wants to do
    :return: choice = an int between 1 and 6 (the chosen menu option)
    """
    while True:
        try:
            menu_option = int(input("Enter option: "))
            if 6 >= menu_option > 0:
                return menu_option  # if input is between 1 and 6
            else:
                print("Write a number between 1 and 6.")
        except ValueError:
            print("You have to write an integer, try again.")


def execute():
    """Used to execute the option that the user chooses
    :return: (nothing)
    """
    while True:
        menu()
        choice = menu_choice()
        if choice == 1:  # Create a new packing list
            create_list()

        elif choice == 2:  # Display content of list
            answer = get_int_input("Would you like to search for a list by name or date?\n1 - Name\n2 - Date\n")
            while True:
                if 1 <= answer <= 2:
                    if answer == 1:
                        display_a_list(search_for_list_by_name())
                        break
                    else:
                        display_a_list(search_for_list_by_date())
                        break
                else:
                    answer = get_int_input("Enter either 1 or 2.\n")

        elif choice == 3:  # Add an element to a list
            search_for_list_by_name().add_element()

        elif choice == 4:  # Remove an element from a list
            search_for_list_by_name().remove_element()

        elif choice == 5:  # Display upcoming packing lists
            display_upcoming_lists()

        elif choice == 6:  # Exit
            break


def main():
    execute()


if __name__ == "__main__":
    print("\nWELCOME TO THIS PACKING LIST PROGRAM\n")
    tuple = read_lists_from_file("saved_list.json")
    list_dict = tuple[0]
    file_name = tuple[1]
    main()
    write_lists_to_file(list_dict, file_name)

