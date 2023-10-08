from pydantic import BaseModel
from abc import ABC, abstractmethod
from pprint import pprint


class LibraryModel(BaseModel):
    title: str
    author: str
    date: int


class AbstractPrint(ABC):

    @abstractmethod
    def show_print_info(self):
        raise NotImplementedError


class Book(AbstractPrint):

    def __init__(self, model: LibraryModel):
        self._model = model

    def __str__(self):
        return f'{self._model.title} by {self._model.author} published on {self._model.date}'

    def show_print_info(self):
        return self.__str__()


class Journal(Book):
    pass


def log_add_book(func):
    def wrapper(self, book):
        print(f'Added book: {book._model.title} by {book._model.author}.')
        return func(self, book)

    return wrapper


def check_book_existence(func):
    def wrapper(self, book):
        if book in self.books:
            return func(self, book)
        else:
            print(f'Book not found!!!')

    return wrapper


class Library:
    def __init__(self):
        self.books = []

    @log_add_book
    def add_book(self, book: Book):
        self.books.append(book)

    @check_book_existence
    def remove_book(self, book: Book):
        if book in self.books:
            self.books.remove(book)
            print(f'Removed book: {book._model.title} by {book._model.author}')
        else:
            print(f'Book not found!')

    def __iter__(self):
        self.count = 0
        return self

    def __next__(self):
        if self.count >= len(self.books):
            raise StopIteration
        book = self.books[self.count]
        self.count += 1
        return book

    def books_by_author(self, author):
        return [book._model.title for book in self.books if book._model.author == author]


if __name__ == '__main__':
    library = Library()

    print("Library log:")
    book_1 = Book(LibraryModel(title="The Passage", author="John Smith", date=1985))
    book_2 = Book(LibraryModel(title="Alaska is calling me", author="Will Johnson", date=1998))
    book_3 = Book(LibraryModel(title="This day yesterday", author="Amy Wells", date=2022))
    book_4 = Book(LibraryModel(title="The sun", author="Bruce Mills", date=2022))
    library.add_book(book_1)
    library.add_book(book_2)
    library.add_book(book_3)
    library.add_book(book_4)

    print("-------")
    print("Books in our library:")
    for book in library:
        print(str(book))

    print("-------")
    library.remove_book(book_4)

    print("-------")
    books_left = [str(book) for book in library]
    print("Books still available:")
    print(books_left)

    print("-------")

    author1_books = library.books_by_author("John Smith")
    author2_books = library.books_by_author("Will Johnson")
    author3_books = library.books_by_author("Amy Wells")
    print("Books available by John Smith:")
    print(author1_books)
    print("Books available by Will Johnson:")
    print(author2_books)
    print("Books available by Amy Wells:")
    print(author3_books)

    print("-------")

    with open("library_list.txt", "w") as file_w:
        count = 0
        for book in library.books:
            count += 1
            file_w.write(f'{count}. {book}\n')

    with open("library_list.txt", "r") as file_r:
        library_list = [line.strip() for line in file_r.readlines()]
        pprint(library_list)
