class InternalServerError(Exception):
    pass

class SchemaValidationError(Exception):
    pass

class UserAlreadyExistsError(Exception):
    pass

class UpdatingUserError(Exception):
    pass

class DeletingUserError(Exception):
    pass

class UserNotExistsError(Exception):
    pass

class ContentsAlreadyExistsError(Exception):
    pass

class UpdatingContentsError(Exception):
    pass

class DeletingContentsError(Exception):
    pass

class ContentsNotExistsError(Exception):
    pass

class CategoriesAlreadyExistsError(Exception):
    pass

class UpdatingCategoriesError(Exception):
    pass

class DeletingCategoriesError(Exception):
    pass

class CategoriesNotExistsError(Exception):
    pass

class EmailAlreadyExistsError(Exception):
    pass

class UnauthorizedError(Exception):
    pass

class EmailDoesnotExistsError(Exception):
    pass

class BadTokenError(Exception):
    pass

errors = {
    "InternalServerError": {
        "message": "Something went wrong",
        "status": 500
    },
     "SchemaValidationError": {
         "message": "Request is missing required fields",
         "status": 400
     },
     "UserAlreadyExistsError": {
         "message": "User with given name already exists",
         "status": 400
     },
     "UpdatingUserError": {
         "message": "Updating User added by other is forbidden",
         "status": 403
     },
     "DeletingUserError": {
         "message": "Deleting User added by other is forbidden",
         "status": 403
     },
     "UserNotExistsError": {
         "message": "User with given id doesn't exists",
         "status": 400
     },
     "ContentsAlreadyExistsError": {
         "message": "Contents with given name already exists",
         "status": 400
     },
     "UpdatingContentsError": {
         "message": "Updating Contents added by other is forbidden",
         "status": 403
     },
     "DeletingContentsError": {
         "message": "Deleting Contents added by other is forbidden",
         "status": 403
     },
     "ContentsNotExistsError": {
         "message": "Contents with given id doesn't exists",
         "status": 400
     },
     "CategoriesAlreadyExistsError": {
         "message": "Contents with given name already exists",
         "status": 400
     },
     "UpdatingCategoriesError": {
         "message": "Updating Contents added by other is forbidden",
         "status": 403
     },
     "DeletingCategoriesError": {
         "message": "Deleting Contents added by other is forbidden",
         "status": 403
     },
     "CategoriesNotExistsError": {
         "message": "Contents with given id doesn't exists",
         "status": 400
     },
     "EmailAlreadyExistsError": {
         "message": "User with given email address already exists",
         "status": 400
     },
     "UnauthorizedError": {
         "message": "Invalid username or password",
         "status": 401
     },
     "EmailDoesnotExistsError": {
         "message": "Couldn't find the user with given email address",
         "status": 400
     },
     "BadTokenError": {
         "message": "Invalid token",
         "status": 403
     }
}