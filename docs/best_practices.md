# Best Practices

* Group elements as per the following rule:
> Things that change at the same time or for the same reasons remain together. Things that change at different times or for different reasons are separated.

In practice:
* Not to split components by main role; so for example avoid having a controllers folder, a gateways folder, etc.
* Keep elements related to the same business flow in the same folder; so for example a `users` module will contain `users.controller.py`, `users.gateway.py`, etc.
* Keep the unit test files besides the file being tested, so in the `users` module you might find the `users.controller.py` but also `users.controller.test.py`; basically because the unit test changes at the same time the controller changes.


