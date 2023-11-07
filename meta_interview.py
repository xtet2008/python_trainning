
''' database design
books_list data structure:
key: title#author
value: book data json
'''

books_list = {
    "C语言开发教程#谭浩强": {"available_count": 0},
    "Python 高级教程#张三": {"available_count": 0}
}


class Books():
    def add_book(self, title, author):
        # - Add a book to the library.
        if not title or not author:
            raise Exception('Please make sure the book data not empty')

        book = self.search_books(title, author)
        if book:
            # append
            books_list[title + '#' + author]['available_count'] += 1
        else:
            # insert
            books_list.update(
                {
                    title + '#' + author: {"available_count": 1}
                 }
            )

    def borrow_book(self, title, author):
        # - borrow a book to the library.
        book = self.search_books(title, author)
        if not book:
            print('The book not exist, please add the book to the libraly first')
        elif books_list[title + '#' + author]['available_count'] <= 0:
            # borrow fail
            print('The book not avalable, please return it first.')
        else:
            # borrow success
            books_list[title + '#' + author]['available_count'] -= 1

    def return_book(self, title, author):
        # return a book
        book = self.search_books(title, author)
        if not book:
            print('The book not exist, please add the book to the libraly first')
        else:
            # return success
            books_list[title + '#' + author]['available_count'] += 1

    def list_available_books(self):
        # - View all available books for borrowing.
        result = {}

        for book in books_list:
            if books_list[book]['available_count']:
                result.update(
                    {book:books_list[book]}
                )

        return result

    def search_books(self, title, author):
        # books_list 代表 图书馆现有的所有书
        if not title or not author:
            raise Exception('Please make sure the title and author not empty.')

        search_key = title + "#" + author
        # print('searching book :', search_key)

        book = books_list.get(search_key)
        if not book:
            # print(' ---- 查询失败 ----')
            return {}
        else:
            # print(' ---- search successfull ----')
            return book


print('\t\n --------- show result ---------')
print(books_list)
books_instance = Books()

# test the search book function
print ('\t\n -------- search book -----------')
books_instance.search_books('C# 编程教学', '李四')  # available_count should be 1
books_instance.search_books('C语言开发教程', '谭浩强') # available_count should be 2
books_instance.search_books('abcd', 'sdsfsd')  # search failed cause not exist


# test the add book function
print ('\t\n -------- add book -----------')
books_instance.add_book('C# 编程教学', '李四')  # available_count should be 1
books_instance.add_book('C语言开发教程', '谭浩强') # available_count should be 1
books_instance.add_book('C语言开发教程', '谭浩强') # available_count should be 2
print(books_instance.list_available_books())  # check the available_count


# test the borrow book function
print ('\t\n -------- borrow book -----------')
books_instance.borrow_book('C# 编程教学', '李四')  # after the function the available_count should be 0
print(books_instance.list_available_books())  # check the available_count if 0 or not
books_instance.borrow_book('C# 编程教学', '李四')  # borrow failed cause not available
books_instance.borrow_book('abcd', 'sdsfsd')  # borrow failed cause not exist



# test the borrow book function
print ('\t\n -------- return book -----------')
books_instance.return_book('C# 编程教学', '李四')  # after the function the available_count should be 1
print(books_instance.list_available_books())  # check the available_count if 1 or not
books_instance.borrow_book('abcd', 'sdsfsd')  # return failed cause not exist



# test the list available book function
print ('\t\n -------- list available book -----------')
print(books_instance.list_available_books())  # check the available_count if 1 or not
