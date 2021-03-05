# Strategy for APIs

### Worker (Employee) tasks
* See vacation requests
    * Filter by status (approved, pending, rejected)
* See number of remaining vacation days
* make new request if not already exhausted total limit of 30 per year

### Manager tasks
* See overview of all requests
    * Filter by status (pending, approved)
* See overview of each individual employee
* See overview of overlapping requests
* Process individual request: approve or reject

### Resources
* User Model
* Vacation Model

### DB Structure
##### User
* `id` | integer | pk
* `email` | string | unique
* `password` | string | *this is not hashed for convenience of exercise*
* `permission_class` | string | `default=employee`

##### Vacation
* `id` | integer | pk
* `vacation_start` | datetime | -
* `vacation_ end` | datetime | -
* `status` | string | `default=pending`
* `requester_id` | foreign key | users table
* `validator_id` | foreign key | user table

### APIs
##### Users
* `GET /users/` | returns data of logged in user
* `GET /users/signup` | creates a new user
* `GET /users/login` | returns a user token valid for 14 days
##### Vacations - employees
* `GET /vacations/` | options: `id=ID`, `status=STATUS` | employee sees all or single of own requests + remaining vacation days, can filter by status
* `POST /vacations/new` | creates a new vacation request if **conditions** meet
##### Vacations - managers
* `GET /vacations/overview` | options: `email=EMAIL`, `status=STATUS` | manager sees all vacation requests from all employees, can filter by status and employee email
* `GET /vacations/overlaps` | gets a list of **pairs of overlaps** with details of overlapping vacation
* `POST /vacations/validate` | validates (or revalidates) a vacation request with a new status: `approved` or `rejected`

### Instructions
#### Database
* Database is as instructed in the exercise instructions document with a docker instance on port `5432`, DB is named `sowingo_varma`, as indicated in the `.env` file
##### Configuration
* I am using Flask-migrate to run my alembic migrations with the command `flask db *`
##### Migrations
* `flask db init`
* `flask db migrate`
* `flask db upgrade`
##### Seed Data
* Install all additional packages (pandas for loading to sql)
* `python tests/seed_data.py`
* This script will load the Database with a randomized dataset of employees, managers, and vacation requests 
#### Web Server
* `pip install -r requirements.txt`
* `honcho start webdev` on port `5000`
#### Routes and Sample Requests
* Included in the root folder: `insomnia_rest_apis_collection.json`