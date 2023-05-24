import datetime
import re
import sys


class Library:
    """
    A library is used to store items (books, articles, and digital media) to be accessed by people (members).
    It contains a unique ID and the name of the library.
    """

    def __init__(self, library_id, name):
        self.library_id = library_id
        self.name = name

    def __str__(self):
        return f"Library ID: {self.library_id} Name: {self.name}"

    def edit(self, name):
        self.name = name


class Item:
    """
    An item refers to something stored in a particular library.
    It contains four mandatory fields: a unique ID, a reference to a particular library, type of item and name.
    It contains three optional fields depending on the item type:
        - Author of a book - If the item type is a 'book'.
        - Journal of the article - If the item type is an 'article'.
        - Format of the Media - If the item type is 'Digital Media'.
    """

    def __init__(
        self, item_id, library_id, item_type, name, book_author=None, article_journal=None, media_format=None
    ):
        self.item_id = item_id
        self.library_id = library_id
        self.item_type = item_type
        self.name = name
        self.book_author = book_author
        self.article_journal = article_journal
        self.media_format = media_format

    def __str__(self):
        return f"Item ID: {self.item_id} Library ID: {self.library_id} Type: {self.item_type} Name: {self.name}"

    def edit(self, library_id, item_type, name, book_author=None, article_journal=None, media_format=None):
        self.library_id = library_id
        self.item_type = item_type
        self.name = name
        self.book_author = book_author
        self.article_journal = article_journal
        self.media_format = media_format


class Book(Item):
    """
    A book is an Item of type 'Book'.
    Aside from the mandatory fields of an Item, it also contains an author field.
    """

    def __init__(self, item_id, library_id, name, author):
        super().__init__(item_id, library_id, "Book", name, book_author=author)

    def __str__(self):
        return f"Book ID: {self.item_id} Library ID: {self.library_id} Name: {self.name} Author: {self.book_author}"


class Article(Item):
    """
    An article is an Item of type 'Article'.
    Aside from the mandatory fields of an Item, it also contains a journal field.
    """

    def __init__(self, item_id, library_id, name, journal):
        super().__init__(item_id, library_id, "Article", name, article_journal=journal)

    def __str__(self):
        return (
            f"Article ID: {self.item_id} Library ID: {self.library_id} Name: {self.name}"
            f" Journal: {self.article_journal}"
        )


class DigitalMedia(Item):
    """
    DigitalMedia is an Item of type 'Digital Media'.
    Aside from the mandatory fields of an Item, it also contains a media format field.
    """

    def __init__(self, item_id, library_id, name, media_format):
        super().__init__(item_id, library_id, "Digital Media", name, media_format=media_format)

    def __str__(self):
        return (
            f"Digital Media ID: {self.item_id} Library ID: {self.library_id} Name: {self.name}"
            f" Format: {self.media_format}"
        )


class Member:
    """
    A Member refers to the people who can access items from a library.
    It contains a unique ID, first name, last name and email.
    """

    def __init__(self, member_id, first_name, last_name, email):
        self.member_id = member_id
        self.first_name = first_name
        self.last_name = last_name
        self.email = email

    def __str__(self):
        return f"Member ID: {self.member_id} Name: {self.first_name} {self.last_name} Email: {self.email}"

    def edit(self, first_name, last_name, email):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email


class LibraryManagementSystem:
    """
    This class acts as an interface for the library.
    It performs the following operations:
        - Load data into memory from the files.
        - Save data from memory into the files.
        - Add/Edit/Delete Libraries
        - Add/Edit/Delete Items
        - Add/Edit/Delete Members
        - Borrow an item
        - Return an item
    """

    def __init__(self):
        self.libraries = []
        self.items = []
        self.members = []
        self.borrowings = []

    def load_data(self):
        # Load data into memory from the files.
        self.load_libraries()
        self.load_items()
        self.load_members()
        self.load_borrowings()

    def load_libraries(self):
        with open("data/library.txt", "r") as file:
            for line in file:
                library_id, name = line.strip().split(",")
                library = Library(library_id, name)
                self.libraries.append(library)

    def load_items(self):
        with open("data/items.txt", "r") as file:
            for line in file:
                item_id, library_id, item_type, name, book_author, article_journal, media_format = line.strip().split(
                    ","
                )
                if item_type == "Book":
                    item = Book(item_id, library_id, name, book_author)
                elif item_type == "Article":
                    item = Article(item_id, library_id, name, article_journal)
                elif item_type == "Digital Media":
                    item = DigitalMedia(item_id, library_id, name, media_format)
                self.items.append(item)

    def load_members(self):
        with open("data/members.txt", "r") as file:
            for line in file:
                member_id, first_name, last_name, email = line.strip().split(",")
                member = Member(member_id, first_name, last_name, email)
                self.members.append(member)

    def load_borrowings(self):
        with open("data/borrowing.txt", "r") as file:
            for line in file:
                borrowing_id, item_id, member_id, borrow_date, return_date = line.strip().split(",")
                borrowing = {
                    "borrowing_id": borrowing_id,
                    "item_id": item_id,
                    "member_id": member_id,
                    "borrow_date": datetime.datetime.strptime(borrow_date, "%Y-%m-%d").date(),
                }

                # If the book is not returned, the return date will be a Null value.
                try:
                    return_date = datetime.datetime.strptime(return_date, "%Y-%m-%d").date()
                except ValueError:
                    return_date = None
                borrowing["return_date"] = return_date

                self.borrowings.append(borrowing)

    def save_data(self):
        # Save data from memory into the files.

        self.save_libraries()
        self.save_items()
        self.save_members()
        self.save_borrowings()

    def save_libraries(self):
        with open("data/library.txt", "w") as file:
            for library in self.libraries:
                file.write(f"{library.library_id},{library.name}\n")

    def save_items(self):
        with open("data/items.txt", "w") as file:
            for item in self.items:
                file.write(
                    (
                        f"{item.item_id},{item.library_id},{item.item_type},{item.name},{item.book_author},"
                        f"{item.article_journal},{item.media_format}\n"
                    )
                )

    def save_members(self):
        with open("data/members.txt", "w") as file:
            for member in self.members:
                file.write(f"{member.member_id},{member.first_name},{member.last_name},{member.email}\n")

    def save_borrowings(self):
        with open("data/borrowing.txt", "w") as file:
            for borrowing in self.borrowings:
                borrow_date = borrowing["borrow_date"].strftime("%Y-%m-%d")
                # If the book is not returned, the return date will be a Null value.
                try:
                    return_date = borrowing["return_date"].strftime("%Y-%m-%d")
                except AttributeError:
                    return_date = None
                file.write(
                    (
                        f"{borrowing['borrowing_id']},{borrowing['item_id']},{borrowing['member_id']},{borrow_date},"
                        f"{return_date}\n"
                    )
                )

    def find_library(self, library_id):
        has_matches = [library for library in self.libraries if library.library_id == library_id]
        if len(has_matches) == 0:
            return False
        else:
            return True

    def add_library(self, library_id, name):
        # Library ID should remain unique.
        if self.find_library(library_id):
            return False

        library = Library(library_id, name)
        self.libraries.append(library)
        self.save_libraries()

        return True

    def edit_library(self, library_id, name):
        # Library ID should exists
        if not self.find_library(library_id):
            return False

        for library in self.libraries:
            if library.library_id == library_id:
                library.edit(name)
                self.save_libraries()
                break

        return True

    def delete_library(self, library_id):
        # Library ID should exist
        if not self.find_library(library_id):
            return False

        self.libraries = [library for library in self.libraries if library.library_id != library_id]
        self.save_libraries()

        self.items = [item for item in self.items if item.library_id != library_id]
        self.save_items()

        return True

    def find_item(self, item_id):
        has_matches = [item for item in self.items if item.item_id == item_id]
        if len(has_matches) == 0:
            return False
        else:
            return True

    def add_item(
        self, item_id, library_id, item_type, name, book_author=None, article_journal=None, media_format=None
    ):
        # Item ID should remain unique.
        if self.find_item(item_id):
            return False

        if item_type == "Book":
            item = Book(item_id, library_id, name, book_author)
        elif item_type == "Article":
            item = Article(item_id, library_id, name, article_journal)
        elif item_type == "Digital Media":
            item = DigitalMedia(item_id, library_id, name, media_format)

        self.items.append(item)
        self.save_items()

        return True

    def edit_item(
        self, item_id, library_id, item_type, name, book_author=None, article_journal=None, media_format=None
    ):
        # Item ID should remain exist.
        if not self.find_item(item_id):
            return False

        for item in self.items:
            if item.item_id == item_id:
                item.edit(library_id, item_type, name, book_author, article_journal, media_format)
                self.save_items()
                break

        return True

    def delete_item(self, item_id):
        # Item ID should remain exist.
        if not self.find_item(item_id):
            return False

        self.items = [item for item in self.items if item.item_id != item_id]
        self.save_items()

        return True

    def find_member(self, member_id):
        has_matches = [member for member in self.members if member.member_id == member_id]
        if len(has_matches) == 0:
            return False
        else:
            return True

    def add_member(self, member_id, first_name, last_name, email):
        # Member ID should remain unique.
        if self.find_member(member_id):
            return False

        member = Member(member_id, first_name, last_name, email)
        self.members.append(member)
        self.save_members()

        return True

    def edit_member(self, member_id, first_name, last_name, email):
        # Member ID should remain exist.
        if not self.find_member(member_id):
            return False

        for member in self.members:
            if member.member_id == member_id:
                member.edit(first_name, last_name, email)
                self.save_members()
                break

        return True

    def delete_member(self, member_id):
        # Member ID should remain exist.
        if not self.find_member(member_id):
            return False

        self.members = [member for member in self.members if member.member_id != member_id]
        self.save_members()

        return True

    def find_borrowing_transaction(self, borrowing_id):
        has_matches = [transaction for transaction in self.borrowings if transaction["borrowing_id"] == borrowing_id]
        if len(has_matches) == 0:
            return False
        else:
            return True

    def find_maximum_borrowing_id(self):
        # Least possible number of items expected (No borrowings yet)
        maximum = 0
        for transaction in self.borrowings:
            if int(transaction["borrowing_id"]) > maximum:
                maximum = int(transaction["borrowing_id"])
        return maximum

    def borrow_item(self, item_id, member_id):
        # Check if a member already has borrowed the item and hasn't returned it. (Shouldn't be able to borrow)
        match = False
        for transaction in self.borrowings:
            if (
                transaction["item_id"] == item_id
                and transaction["member_id"] == member_id
                and transaction["return_date"] is None
            ):
                match = True
                break
        if match:
            return False

        # Borrowing ID should remain unique.
        borrowing_id = str(self.find_maximum_borrowing_id() + 1)

        while self.find_borrowing_transaction(borrowing_id):
            borrowing_id += 1

        borrow_date = datetime.date.today()
        return_date = None
        borrowing = {
            "borrowing_id": borrowing_id,
            "item_id": item_id,
            "member_id": member_id,
            "borrow_date": borrow_date,
            "return_date": return_date,
        }
        self.borrowings.append(borrowing)
        self.save_borrowings()

        return True

    def return_item(self, borrowing_id):
        for borrowing in self.borrowings:
            if borrowing["borrowing_id"] == borrowing_id:
                borrowing["return_date"] = datetime.date.today()
                self.save_borrowings()
                break


class LibraryMenuIterface(LibraryManagementSystem):
    """
    This class is the Menu system for a user to interact with the data.
    """

    # Determines whether the active user session has admin priviledges
    is_admin = True
    # Optional if is_admin is True. Stores the member ID of the active user session.
    current_member_id = None
    # Store the choice of a user in menus
    user_choice = None
    # Stores the library ID of the active user session
    current_library_ID = None

    def __init__(self, level=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.load_data()
        self.user_login()

    def exit_option(self):
        """
        Allows a user to exit the system.
        """
        print("")
        sys.exit("You have exited successful out of the program.")

    def validate_number_input(self, start, stop):
        """
        Validates whether the input of a user is of type integer.
        Start and stop defines the range of acceptable integers.
        """
        while True:
            print("")
            self.user_choice = input("Enter the number of your choice: ")
            try:
                self.user_choice = int(self.user_choice)
            except ValueError:
                print("Please input an integer")
                continue

            if self.user_choice in range(start, stop):
                break
            else:
                print(f"Please, choose either {start} or {stop - 1}")

    def validate_string_input(self, prompt):
        """
        Validates if the user input is not empty
        """
        while True:
            user_input = input(prompt)
            if len(user_input) == 0:
                print("")
                print("This value can not be empty")
            else:
                break
        return user_input

    def validate_email(self):
        """
        Validates member email to be a valid one. Returns the valid email.
        """
        while True:
            email = self.validate_string_input("What is your email? ")
            # In case of a valid email
            if re.match(r"[^@]+@[^@]+\.[^@]+", email):
                break
            else:
                print("Please enter a valid email.")
        return email

    def user_login(self):
        """
        Allows a user to gain admin rights and edit library data.
        Allows a member to access the system with their member ID if they want to borrow/return books.
        """
        print("")
        print("What would you like to do?")
        print("An administartor can modify library data. A member can only borrow/return library items")
        print("1. Log in as an administrator")
        print("2. Log in as an member")
        print("3. Exit program")

        self.validate_number_input(1, 4)

        if self.user_choice == 1:
            self.is_admin = True
            self.library_menu()
        elif self.user_choice == 2:
            self.is_admin = False
            self.member_login()
        else:
            self.exit_option()

    def member_login(self):
        """
        Allows a member to access the system with their member ID if they want to borrow/return books.
        If such a  member ID does not exist, a user creates their member profile.
        """
        print("")
        print("What would you like to do?")
        print("1. Create your member profile")
        print("2. Use an existing member profile")
        print("3. Go back to the main menu")
        print("4. Exit program")

        self.validate_number_input(1, 5)

        print("")
        if self.user_choice == 1:
            memberid = self.validate_string_input("What is your member ID? ")
            fname = self.validate_string_input("What is your first name? ")
            lname = self.validate_string_input("What is your last name? ")
            email = self.validate_email()
            is_succeessful = self.add_member(memberid, fname, lname, email)
            if is_succeessful:
                print("Operation was successful")
                self.current_member_id = memberid
                self.library_menu()
            else:
                print("Operation was not successful. Please try again, the member id already exixts.")
                self.member_login()

        elif self.user_choice == 2:
            memberid = self.validate_string_input("What is your member ID? ")
            # Check for such a member ID
            if not self.find_member(memberid):
                print("No such member was found")
                self.member_login()
            else:
                self.current_member_id = memberid
                self.library_menu()
        elif self.user_choice == 3:
            self.user_login()
        else:
            self.exit_option()

    def library_menu(self):
        """
        Displays all libraries present allowing members to choose.
        If active user is an admin, they can create a library
        """
        libary_count = len(self.libraries)
        print("")
        if self.is_admin:
            print("00. Add a library")
        # Decide what to dislay in the menu to navigate back
        if self.is_admin:
            display = "main"
        else:
            display = "member"
        print(f"01. Go back to the {display} menu")
        print("02. Exit program")
        print("")
        if libary_count == 0:
            print("Sorry, there are no libraries available yet. An admin can add them")
        else:
            for library in self.libraries:
                print(library)

        user_option = self.validate_string_input(
            "Enter your option here. (In case of a library, enter the library ID) "
        )
        print("")
        if user_option == "00":
            libraryid = self.validate_string_input("What is your library ID? ")
            # There should be no library with an ID of 00, 01, or 02
            if libraryid in ["00", "01", "02"]:
                print("Sorry, there you can't use 00, 01, 02 as library IDs.")
                self.library_menu()
            name = self.validate_string_input("What is your library name? ")
            is_succeessful = self.add_library(libraryid, name)
            if is_succeessful:
                print("Operation was successful")
                self.current_library_ID = libraryid
                self.library_operations_menu()
            else:
                print("Operation was not successful. Please try again, the library id already exixts.")
                self.library_menu()
        elif user_option == "01":
            if self.is_admin:
                self.user_login()
            else:
                self.member_login()
        elif user_option == "02":
            self.exit_option()
        else:
            # Check for such a library ID
            if not self.find_library(user_option):
                print("No such library was found")
                self.library_menu()
            else:
                self.current_library_ID = user_option
                self.library_operations_menu()

    def library_operations_menu(self):
        """
        Display operations that could be perfromed on a libary depending on if the user is an admin or a member
        """
        print("")
        print("0. Go back")
        print("1. Exit program")
        print("2. Books")
        print("3. Articles")
        print("4. Digital Media")
        print("5. Current Borrowings and Returns")
        if self.is_admin:
            print("6. Edit library")
            print("7. Delete library. (WARNING: It deletes all items related to a library. Borrowing are retained.)")

        if self.is_admin:
            self.validate_number_input(0, 8)
        else:
            self.validate_number_input(0, 6)

        if self.user_choice == 0:
            self.library_menu()
        elif self.user_choice == 1:
            self.exit_option()
        elif self.user_choice == 2:
            self.books_menu()
        elif self.user_choice == 3:
            self.articles_menu()
        elif self.user_choice == 4:
            self.digital_media_menu()
        elif self.user_choice == 5:
            # Should be accessible by a member only
            if not self.is_admin:
                self.member_borrwowings_menu()
            else:
                print("Sorry, to access this view, you need to log in as a member.")
                self.library_operations_menu()
        elif self.user_choice == 6:
            newname = self.validate_string_input("Enter the new name of the library: ")
            is_succeessful = self.edit_library(self.current_library_ID, newname)
            if is_succeessful:
                print("Operation was successful")
            else:
                print("Operation was not successful. Please try again")
            self.library_operations_menu()
        else:
            is_succeessful = self.delete_library(self.current_library_ID)
            if is_succeessful:
                print("Operation was successful")
            else:
                print("Operation was not successful. Please try again")
            self.library_menu()

    def books_menu(self):
        """
        Display operation for members and admin
        Borrow operation for members
        Add/edit/delete operations for admin
        """
        print("")
        print("0. Go back")
        print("1. Exit the program")
        print("2. Display books")
        print("3. Borrow book")
        if self.is_admin:
            print("4. Add book")
            print("5. Edit book")
            print("6. Delete book")

        if self.is_admin:
            self.validate_number_input(0, 7)
        else:
            self.validate_number_input(0, 4)

        library_books = [
            book for book in self.items if (book.item_type == "Book" and book.library_id == self.current_library_ID)
        ]

        print("")
        if self.user_choice == 0:
            self.library_operations_menu()
        elif self.user_choice == 1:
            self.exit_option()
        elif self.user_choice == 2:
            if len(library_books) == 0:
                print("There are no items to display")
            for book in library_books:
                print(book)
            self.books_menu()
        elif self.user_choice == 3:
            if self.is_admin:
                print("Sorry, you have to log in as a member to borrow.")
            else:
                itemid = self.validate_string_input("Enter the Item ID of the book: ")
                match = False
                for book in library_books:
                    if book.item_id == itemid:
                        match = True
                        break
                if not match:
                    print("Sorry, such a book does not exist")
                else:
                    is_success = self.borrow_item(itemid, self.current_member_id)
                    if is_success:
                        print("Operation was successful")
                    else:
                        print("Operation was not successful. You have to return the item first.")
            self.books_menu()
        elif self.user_choice == 4:
            bookid = self.validate_string_input("What is the book ID? ")
            bookname = self.validate_string_input("What is the book name? ")
            bookauthor = self.validate_string_input("What is the book author? ")
            is_succeessful = self.add_item(bookid, self.current_library_ID, "Book", bookname, book_author=bookauthor)
            if is_succeessful:
                print("Operation was successful")
            else:
                print("Operation was not successful. Please try again, the book id already exixts.")
            self.books_menu()
        elif self.user_choice == 5:
            bookid = self.validate_string_input("What is the book ID? ")
            match = False
            for book in library_books:
                if book.item_id == bookid:
                    match = True
                    break
            if not match:
                print("Sorry, such a book does not exist")
                self.books_menu()
            bookname = self.validate_string_input("What is the book name? ")
            bookauthor = self.validate_string_input("What is the book author? ")
            is_succeessful = self.edit_item(bookid, self.current_library_ID, "Book", bookname, book_author=bookauthor)
            if is_succeessful:
                print("Operation was successful")
            else:
                print("Operation was not successful. Please try again")
            self.books_menu()
        else:
            bookid = self.validate_string_input("What is the book ID? ")
            match = False
            for book in library_books:
                if book.item_id == bookid:
                    match = True
                    break
            if not match:
                print("Sorry, such a book does not exist")
                self.books_menu()
            is_succeessful = self.delete_item(bookid)
            if is_succeessful:
                print("Operation was successful")
            else:
                print("Operation was not successful. Please try again.")
            self.books_menu()

    def articles_menu(self):
        """
        Display operation for members and admin
        Borrow operation for members
        Add/edit/delete operations for admin
        """
        print("")
        print("0. Go back")
        print("1. Exit program")
        print("2. Display article")
        print("3. Borrow article")
        if self.is_admin:
            print("4. Add article")
            print("5. Edit article")
            print("6. Delete article")

        if self.is_admin:
            self.validate_number_input(0, 7)
        else:
            self.validate_number_input(0, 4)

        library_article = [
            article
            for article in self.items
            if (article.item_type == "Article" and article.library_id == self.current_library_ID)
        ]

        print("")
        if self.user_choice == 0:
            self.library_operations_menu()
        elif self.user_choice == 1:
            self.exit_option()
        elif self.user_choice == 2:
            if len(library_article) == 0:
                print("There are no items to display")
            for article in library_article:
                print(article)
            self.articles_menu()
        elif self.user_choice == 3:
            if self.is_admin:
                print("Sorry, you have to log in as a member to borrow.")
            else:
                itemid = self.validate_string_input("Enter the Item ID of the article: ")
                match = False
                for article in library_article:
                    if article.item_id == itemid:
                        match = True
                        break
                if not match:
                    print("Sorry, such a article does not exist")
                else:
                    is_success = self.borrow_item(itemid, self.current_member_id)
                    if is_success:
                        print("Operation was successful")
                    else:
                        print("Operation was not successful. You have to return the item first.")
            self.articles_menu()
        elif self.user_choice == 4:
            articleid = self.validate_string_input("What is the article ID? ")
            articlename = self.validate_string_input("What is the article name? ")
            articlejournal = self.validate_string_input("What is the article journal? ")
            is_succeessful = self.add_item(
                articleid, self.current_library_ID, "Article", articlename, article_journal=articlejournal
            )
            if is_succeessful:
                print("Operation was successful")
            else:
                print("Operation was not successful. Please try again, the article id already exixts.")
            self.articles_menu()
        elif self.user_choice == 5:
            articleid = self.validate_string_input("What is the article ID? ")
            match = False
            for article in library_article:
                if article.item_id == articleid:
                    match = True
                    break
            if not match:
                print("Sorry, such an article does not exist")
                self.articles_menu()
            articlename = self.validate_string_input("What is the article name? ")
            articlejournal = self.validate_string_input("What is the article journal? ")
            is_succeessful = self.edit_item(
                articleid, self.current_library_ID, "Article", articlename, article_journal=articlejournal
            )
            if is_succeessful:
                print("Operation was successful")
            else:
                print("Operation was not successful. Please try again")
            self.articles_menu()
        else:
            articleid = self.validate_string_input("What is the article ID? ")
            match = False
            for article in library_article:
                if article.item_id == articleid:
                    match = True
                    break
            if not match:
                print("Sorry, such a article does not exist")
                self.articles_menu()
            is_succeessful = self.delete_item(articleid)
            if is_succeessful:
                print("Operation was successful")
            else:
                print("Operation was not successful. Please try again.")
            self.articles_menu()

    def digital_media_menu(self):
        """
        Display operation for members and admin
        Borrow operation for members
        Add/edit/delete operations for admin
        """
        print("")
        print("0. Go back")
        print("1. Exit program")
        print("2. Display digital media")
        print("3. Borrow digital media")
        if self.is_admin:
            print("4. Add digital media")
            print("5. Edit digital media")
            print("6. Delete digital media")

        if self.is_admin:
            self.validate_number_input(0, 6)
        else:
            self.validate_number_input(0, 3)

        library_media = [
            media
            for media in self.items
            if (media.item_type == "Digital Media" and media.library_id == self.current_library_ID)
        ]

        print("")
        if self.user_choice == 0:
            self.library_operations_menu()
        elif self.user_choice == 1:
            self.exit_option()
        elif self.user_choice == 2:
            if len(library_media) == 0:
                print("There are no items to display")
            for media in library_media:
                print(media)
            self.digital_media_menu()
        elif self.user_choice == 3:
            if self.is_admin:
                print("Sorry, you have to log in as a member to borrow.")
            else:
                itemid = self.validate_string_input("Enter the Item ID of the media: ")
                match = False
                for media in library_media:
                    if media.item_id == itemid:
                        match = True
                        break
                if not match:
                    print("Sorry, such a media does not exist")
                else:
                    is_success = self.borrow_item(itemid, self.current_member_id)
                    if is_success:
                        print("Operation was successful")
                    else:
                        print("Operation was not successful. You have to return the item first.")
            self.digital_media_menu()

        elif self.user_choice == 4:
            mediaid = self.validate_string_input("What is the media ID? ")
            medianame = self.validate_string_input("What is the media name? ")
            mediafmt = self.validate_string_input("What is the media format? ")
            is_succeessful = self.add_item(
                mediaid, self.current_library_ID, "Digital Media", medianame, media_format=mediafmt
            )
            if is_succeessful:
                print("Operation was successful")
            else:
                print("Operation was not successful. Please try again, the media id already exixts.")
            self.digital_media_menu()

        elif self.user_choice == 5:
            mediaid = self.validate_string_input("What is the media ID? ")
            match = False
            for media in library_media:
                if media.item_id == mediaid:
                    match = True
                    break
            if not match:
                print("Sorry, such an media does not exist")
                self.digital_media_menu()

            medianame = self.validate_string_input("What is the media name? ")
            mediafmt = self.validate_string_input("What is the media format? ")
            is_succeessful = self.edit_item(
                mediaid, self.current_library_ID, "Digital Media", medianame, media_format=mediafmt
            )

            if is_succeessful:
                print("Operation was successful")
            else:
                print("Operation was not successful. Please try again")
            self.digital_media_menu()
        else:
            mediaid = self.validate_string_input("What is the media ID? ")
            match = False
            for media in library_media:
                if media.item_id == mediaid:
                    match = True
                    break
            if not match:
                print("Sorry, such a media does not exist")
                self.digital_media_menu()

            is_succeessful = self.delete_item(mediaid)
            if is_succeessful:
                print("Operation was successful")
            else:
                print("Operation was not successful. Please try again.")
            self.digital_media_menu()

    def member_borrwowings_menu(self):
        """
        Display all the borrowings made by a particular member.
        Allows a member to return items to which they have borrowed.
        """
        member_borrowings = [
            transaction for transaction in self.borrowings if transaction["member_id"] == self.current_member_id
        ]
        complete_member_borrowings = [
            transaction for transaction in member_borrowings if transaction["return_date"] is not None
        ]
        uncomplete_member_borrowings = [
            transaction for transaction in member_borrowings if transaction["return_date"] is None
        ]
        print("")
        print("Pending Borrowings")
        if len(uncomplete_member_borrowings) == 0:
            print("You have no uncompleted borrowings")
        else:
            for uncompleted in uncomplete_member_borrowings:
                print(
                    f"Borrowing ID: {uncompleted['borrowing_id']} Item ID: {uncompleted['item_id']} Borrowing date: "
                    f"{uncompleted['borrow_date']}"
                )
        print("Completed Borrowings")
        if len(complete_member_borrowings) == 0:
            print("You have no completed borrowings")
        else:
            for completed in complete_member_borrowings:
                print(
                    f"Borrowing ID: {completed['borrowing_id']} Item ID: {completed['item_id']} Borrowing date: "
                    f"{completed['borrow_date']} Return Date: {completed['return_date']}"
                )

        print("")
        print("What would you like to do?")
        print("1. Go back")
        print("2. Exit program")
        # Ensure a member has unreturned books first
        if len(uncomplete_member_borrowings) != 0:
            print("3. Return an item")

            self.validate_number_input(1, 4)
        else:
            print("Currently, you have no items to return.")
            self.validate_number_input(1, 3)

        if self.user_choice == 1:
            self.library_operations_menu()
        elif self.user_choice == 2:
            self.exit_option()
        else:
            borrowing_id = self.validate_string_input("Enter the borrowing ID: ")
            # Ensure the borrowing ID is valid for the member and the item is unreturned
            match = False
            for uncompleted in uncomplete_member_borrowings:
                if uncompleted["borrowing_id"] == borrowing_id:
                    match = True
                    break
            if not match:
                print("Please enter a valid borrowing ID")
            else:
                self.return_item(borrowing_id)
            self.member_borrwowings_menu()
