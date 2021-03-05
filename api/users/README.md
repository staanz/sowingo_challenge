# Users module documentation

This module contains all the logic for authentication management.
For this exercise, I have constructed a very basic JWT based authentication with only 3 functions:
* Signup a new `user` (email, password, employee type)
* Login a `user` and receive a token
* View a `user`'s own details by providing the right token

**Notes: I have not hashed the password, which would be required in a production setting**

#### Views Exposed
* `UserViewAPI`: `GET /users/` expects a `x-access-token` in header, returns user details corresponding to the token
* `UserSignupAPI`: `POST /users/signup` expects a JSON object with `email`, `password`, and/or `type` for a new `user` registration. If `type` is not provided, "employee" is set as default
* `UserLoginAPI`: `GET /users/login` expects a JSON object with `email` and `password` and returns a token valid for 14 days