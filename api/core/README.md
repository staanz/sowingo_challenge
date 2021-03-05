# Models & Database documentation

Models added in `database`:
* `class User`: All user object fields and class methods specific for user functionality
* `class Vacation`: All vacation object fields and class methods specific for vacation functionality
* `flask-marshmallow`: Serializing & Deserializing model objects

Class methods:
* `User` class has methods to:
    * return all `vacation` objects associated with user
    * calculate and return the remaining vacation days from total of 30 (logic used is for lifetime 30 days in interest of time)
* `Vacation` class has methods to:
    * return employee `user` that requested the vacation
    * return manager `user` that validated the request
    * calculate and return the number of days of the vacation request
    * return a string representation of the start and end of vacation period