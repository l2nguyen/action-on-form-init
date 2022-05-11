# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

from typing import Any, Text, Dict, List

import abc

from rasa_sdk import Action, Tracker, FormValidationAction, ValidationAction
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import EventType, SlotSet
from rasa_sdk.types import DomainDict

class ValidatePredefinedSlots(ValidationAction):
    def extract_form_initialized(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ):
        if not tracker.active_loop or not tracker.get_slot("form_initialized"):
            return {"form_initialized": False}
        else:
            return {"form_initialized": True}

class CustomFormValidationAction(FormValidationAction, metaclass=abc.ABCMeta):
    # Avoids registering this class as a custom action
    @abc.abstractmethod
    def name(self) -> Text:
        """Unique identifier of the CustomFormValidationAction"""

        raise NotImplementedError("A CustomFormValidationAction must implement a name")

    async def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> List[EventType]:
        events = []
        if not tracker.get_slot("form_initialized"):
            events.extend(await self.extra_run_logic(dispatcher, tracker, domain))
        events.extend(await super().run(dispatcher, tracker, domain))
        return events

    def validate_form_initialized(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ):
        return {"form_initialized": True}

    async def extra_run_logic(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ):
        return []

class ActionHelloWorld(Action):

    def name(self) -> Text:
        return "action_hello_world"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        dispatcher.utter_message(text="Hello World!")

        return []


class ValidateTestForm(CustomFormValidationAction):

    def name(self):
        return "validate_test_form"
    
    # extra logic to run at form initialization
    async def extra_run_logic(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ):
        form_init = tracker.get_slot("form_initialized")
        print(form_init)
        events = await super().extra_run_logic(dispatcher, tracker, domain)
        
        dispatcher.utter_message(text="I am the extra run logic and I should run at the beginning of a form!")
        # set example slot
        events.append(SlotSet("example_slot_to_set_on_form_entry", "my_test_value"))
        
        return events

    def validate_question1(
            self,
            value: Text,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any],
    ) -> Dict[Text, Any]:
        print("hello")
        return {"question1": value}


class ActionSubmitTestForm(Action):

    def name(self) -> Text:
        return "action_submit_test_form"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        dispatcher.utter_message(text="Submit test form")

        return []
