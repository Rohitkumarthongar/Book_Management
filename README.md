    User APIs:
        Get All Users: GET /api/users/
        User Registration: POST /api/user/register/
        User Login: POST /api/user/login/

    Book APIs:
        Create Book: POST /api/book/
        Get Book Detail: GET /api/book/{book_id}/
        Update Book: PUT /api/book/{book_id}/
        Delete Book: DELETE /api/book/{book_id}/

    Reading List Management APIs:
        Add Book to Reading List: POST /api/book/{reading_list_id}/add_book/{book_id}/
        Remove Book from Reading List: DELETE /api/book/{reading_list_id}/remove_book/{book_id}/
