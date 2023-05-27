"""Index development configuration."""

import pathlib

# Root of this application, useful if it doesn't occupy an entire domain
APPLICATION_ROOT = '/'


# Secret key for encrypting cookies
# SECRET_KEY = b'FIXME SET WITH: $ python3 -c \
#     "import os; print(os.urandom(24))" '
# SESSION_COOKIE_NAME = 'login'


# File Upload to var/uploads/
SEARCH_ROOT = pathlib.Path(__file__).resolve().parent.parent.parent
MAX_CONTENT_LENGTH = 16 * 1024 * 1024


# Database file is var/insta485.sqlite3
# return a Path object representing the 
# parent directory of the parent 
# directory of the file containing this code.
DATABASE_FILENAME = SEARCH_ROOT/'var'/'search.sqlite3'

SEARCH_INDEX_SEGMENT_API_URLS = [
    "http://localhost:9000/api/v1/hits/",
    "http://localhost:9001/api/v1/hits/",
    "http://localhost:9002/api/v1/hits/",
]