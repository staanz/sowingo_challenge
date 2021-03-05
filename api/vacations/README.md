# Vacations module documentation

This module contains all the logic for vacation request management functions.
* `user` can view remaining vacation days and all `vacation` requests created by self, filter by status if needed
* `user` can request a new `vacation` if the requested number of days is less than or equal to the remaining vacation days
* Manager type `users` can view `vacations` of all `users` or single `user`, filter by status of request
* Manager type `users` can view list of `vacations` that are overlapping with one another
* Manager type `users` can process individual `vacation` requests as either "approved" or "rejected"

#### Views Exposed
* `VacationViewAPI`: `GET /vacations` expects a `x-access-token` in header, returns user's own vacation records; optionally include `status_filter` in JSON object to filter (possible values: pending, approved, rejected)
* `VacationViewAPI`: `POST /vacations` expects a `x-access-token` in header and JSON object with vacation data and returns confirmation on successful creation
* `VacationOverviewAPI`: `GET /vacations/overview` expects a `x-access-token` in header belonging to MANAGER type user object, returns all vacation records; optionally include `email_filter` and / or `status_filter`
* `VacationOverlapsAPI`: `GET /vacations/overlaps` expects a `x-access-token` in header belonging to MANAGER type user object, returns pairs of vacation records that are overlapping with each other
* `VacationValidateAPI`: `PUT /vacations/validate` expects a `x-access-token` in header belonging to MANAGER type user object and JSON object with vacation id and validation choice (approved or rejected) and returns a confirmation of action 