# action-on-form-init
This is a simple bot in Rasa 3.x that provides a workaround for running actions on form initialisation because form validation is now only run after the form is active. See this [issue](https://github.com/RasaHQ/rasa/issues/10913) for more details.

This is inspired by this solution [here](https://github.com/melindaloubser1/moodbot/tree/form_initial_logic_3.x) and Rasa's [financial demo](https://github.com/RasaHQ/financial-demo/blob/main/actions/custom_forms.py).

The workaround is acheived by:
1. Add a slot `form_initialized` with a custom type mapping as the first required slot for every form that needs initialization logic.

2. Add a custom slot extraction method for `form_initialized`. This will run on every user turn. It will set the slot to `False` unless the slot is both currently set (it's set by the form below) and the form is still active. This takes care of resetting the slot once a form is closed.

3. Create a form validation base class that runs extra logic when `form_initialized` is `False`, and includes a validation method for `form_initialized` that just sets the slot to `True`. The validation method will only run after the form was initialized.

4. Subclass the custom form validation action for any forms requiring initialization logic.
