# Investment Account API 
## Project Description
This project is a Django Rest Framework (DRF) API for managing Investment Accounts with custom user permissions.
It allows multiple users to belong to an investment account and allows users to be part of more than one account with different levels of access control.

## Features
* Multiple Investment Accounts for Users: Users can belong to multiple investment accounts, each with different permissions.
* Permission Levels:
  * View Only:  Users can view details of an account but cannot make transactions.
  * Full CRUD: Users can create, read, update, and delete transactions in the account.
  * Post Only: Users can post transactions but cannot view them.
* Admin Endpoint:
  * Retrieve all of a user's transactions.
  * Calculate and return the sum of the user's total balance.
  * Filter transactions by a date range.
## Requirements
To run the project locally, ensure you have the following installed:
* Python 3.8
* Django Rest Framework (DRF) 4.2
* SQLite
## Setup Instructions
  * Clone the repository:
      * `git clone git@github.com:bowenSteve/investment_account.git`
      * `cd investment_account`
  * Install dependencies and activate virtual environment:
      * `pipenv install`
      * `pipenv shell`
  * Configure database:
      * `python manage.py migrate`
  * Create Superuser:
      * `python manage.py createsuperuser`
  * Run the development server:
      * `python manage.py runserver`
## API endpoints:
### Authentication
* POST `/api/token/`: Obtain JWT access and refresh tokens.
* POST `/api/token/refresh/`: Refresh the JWT access token.
### Investment Accounts
* POST `/investment-accounts/`: Create a new investment account.
* GET `/investment-accounts/{id}/`: Retrieve details of an investment account.
* PUT/PATCH `/investment-accounts/{id}/`: Update an investment account.
* DELETE `/investment-accounts/{id}/`: Delete an investment account.
### Transactions
* POST `/investment-accounts/{id}/transactions/`: Create a new transaction.
* GET `/investment-accounts/{id}/transactions/`: Retrieve all transactions for an account.
* GET `/investment-accounts/{id}/transactions/{pk}/`: Retrieve details of a specific transaction.
* PUT/PATCH /investment-accounts/{id}/transactions/{pk}/`: Update a specific transaction.
* DELETE `/investment-accounts/{id}/transactions/{pk}/`: Delete a specific transaction.
### Admin
* GET `/admin/user-transactions/{user_id}/?start_date={YYYY-MM-DD}&end_date={YYYY-MM-DD}`: Retrieve all transactions for a user, with optional date range filtering. (Admin only)
### Permissions
Each user can have different permissions for different accounts:

* View Only `(view)`: The user can only view account details.
* Full CRUD `(crud)`: The user can create, read, update, and delete transactions.
* Post Only `(post_only)`: The user can post transactions but cannot view them.
* These permissions are managed through a ManyToMany relationship between users and accounts via the UserInvestmentAccount model.
## Conclusion
This API allows flexible user permissions on investment accounts, supports multiple accounts per user, 
and offers an admin endpoint for transaction management. The project includes unit tests and continuous integration with GitHub Actions.
