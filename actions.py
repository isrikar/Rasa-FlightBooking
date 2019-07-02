# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/core/actions/#custom-actions/


# This is a simple example for a custom action which utters "Hello World!"

from typing import Any, Text, Dict, List
import dateutil.parser
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
import json
from rasa_sdk.forms import FormAction
from rasa_sdk.events import SlotSet
from rasa.core.events import FollowupAction
# from rasa.core.events import SlotSet
from rasa.core.events import UserUtteranceReverted
with open('./data/ticket.json') as json_file:  
            data = json.load(json_file)

class ActionSearchFlights(Action):
    def name(self):
        return "action_search_flights"

    def run(self, dispatcher, tracker, domain):
        dispatcher.utter_message("Searching for flights")
        source=tracker.get_slot("source")
        destination=tracker.get_slot("destination")
        dt=tracker.get_slot("time")
        d = dateutil.parser.parse(dt).date()
        date=d.strftime("%d/%m/%Y")
        # print("Data: ",source,destination,date)
        # message="Sou you said: Source:"+source+" Destination: "+destination+" Date: "+date
        # dispatcher.utter_message(message)
        
        
        
        sourceFlag=False
        destinationFlag=False
        dateFlag=False
        message="Flights found:"
        
        for i in range(0,len(data["inst"])):
            if(source.lower()==data["inst"][i]["From"].lower() and destination.lower()==data["inst"][i]["To"].lower() and date.lower()==data["inst"][i]["Date"].lower()):
                sourceFlag=True
                destinationFlag=True
                dateFlag=True
                flightNo=data["inst"][i]["FlightNo"]
                airLines=data["inst"][i]["Airlines"]
                message+="\nFlightNo.: {}\nAirLines: {}\nSource: {}\nDestination: {}\n Date: {}\n".format(flightNo,airLines,source,destination,date)
               
        if(sourceFlag==True and destinationFlag==True and dateFlag==True):
             flights=message
             print(flights)
             dispatcher.utter_message(flights)
        else:
            message="Flights not found"
            dispatcher.utter_message(message)        
        
        
        return []
        
class ActionSearchDirectFlights(Action):
    def name(self):
        return "action_search_direct_flights"

    def run(self, dispatcher, tracker, domain):
        # dispatcher.utter_message("Searching for flights")
        source=tracker.get_slot("source")
        destination=tracker.get_slot("destination")
        dt=tracker.get_slot("time")
        d = dateutil.parser.parse(dt).date()
        date=d.strftime("%d/%m/%Y")
        # print("Data: ",source,destination,date)
        # message="Sou you said: Source:"+source+" Destination: "+destination+" Date: "+date
        # dispatcher.utter_message(message)
        connection="True"
        

        sourceFlag=False
        destinationFlag=False
        dateFlag=False
        message=""
        for i in range(0,len(data["inst"])):
            if(connection.lower()==data["inst"][i]["Connection"].lower() and source.lower()==data["inst"][i]["From"].lower() and destination.lower()==data["inst"][i]["To"].lower() and date.lower()==data["inst"][i]["Date"].lower()):
                sourceFlag=True
                destinationFlag=True
                dateFlag=True
                flightNo=data["inst"][i]["FlightNo"]
                airLines=data["inst"][i]["Airlines"]
                message+="FlightNo.: {}\nAirLines: {}\nSource: {}\nDestination: {}\n Date: {}".format(flightNo,airLines,source,destination,date)
               
        if(sourceFlag==True and destinationFlag==True and dateFlag==True):
            
             flights=message
             print(flights)
             dispatcher.utter_message(flights)
        
        # if(sourceFlag==True and destinationFlag==True and dateFlag==True):
        #     message="Flight found:\nFlightNo.: {}\nAirLines: {}\nSource: {}\nDestination: {}\n Date: {}".format(flightNo,airLines,source,destination,date)
        else:
            message="Flights not found"
                    
        # dispatcher.utter_message(message)
        
        return []
        
class ActionMakeReservation(Action):
    def name(self):
        return "action_ack_makereservation"

    def run(self, dispatcher, tracker, domain):
        source=tracker.get_slot("source")
        destination=tracker.get_slot("destination")
        flightNo=tracker.get_slot("flightCode")
        dt=tracker.get_slot("time")
        d = dateutil.parser.parse(dt).date()
        date=d.strftime("%d/%m/%Y")
        
        for i in range(0,len(data["inst"])):
            if(flightNo==data["inst"][i]["FlightNo"]):
                message=data["inst"][i]["Airlines"]+" Flight No :"+data["inst"][i]["FlightNo"]+" has been booked.Your ticket has been booked on ref number YM45FH"
        
        dispatcher.utter_message(message)
        return []

class FlightForm(FormAction):
    """Example of a custom form action"""

    def name(self):
        """Unique identifier of the form"""

        return "flight_form"
    
    @staticmethod
    def required_slots(tracker):
        """A list of required slots that the form has to fill"""

        return ["location", "to", "time"]
    
 
    # @staticmethod
    def submit(self, dispatcher, tracker, domain):
        """Define what the form has to do
            after all required slots are filled"""
        print("####Came here")
        # utter submit template
        # dispatcher.utter_template("utter_submit", tracker)
        # tracker.trigger_followup_action('action_ack_makereservation')
        FollowupAction('action_search_flights')
        return []

 
class SaveOrigin(Action):
	def name(self):
		return 'action_save_origin'
		
	def run(self, dispatcher, tracker, domain):
		orig = next(tracker.get_latest_entity_values("location"), None)
		if not orig:
			dispatcher.utter_message("Please enter source")
			return [UserUtteranceReverted()]
		return [SlotSet('source',orig)]
	


class SaveDestination(Action):
	def name(self):
		return 'action_save_destination'
		
	def run(self, dispatcher, tracker, domain):
		dest = next(tracker.get_latest_entity_values("location"), None)
		if not dest:
			dispatcher.utter_message("Please enter destination")
			return [UserUtteranceReverted()]
		return [SlotSet('destination',dest)]
		
		
class SaveDate(Action):
	def name(self):
		return 'action_save_date'
		
	def run(self, dispatcher, tracker, domain):
		inp = next(tracker.get_latest_entity_values("time"), None)
		if not inp:
			dispatcher.utter_message("Please enter a valid date")
			return [UserUtteranceReverted()]
		return [SlotSet('time',inp)]    
		
class SaveID(Action):
	def name(self):
		return 'action_save_id'
		
	def run(self, dispatcher, tracker, domain):
		inp = next(tracker.get_latest_entity_values("ID"), None)
		if not inp:
			dispatcher.utter_message("Please enter a valid id")
			return [UserUtteranceReverted()]
		return [SlotSet('ID',inp)]    

class SaveContact(Action):
	def name(self):
		return 'action_save_contact'
		
	def run(self, dispatcher, tracker, domain):
		inp = next(tracker.get_latest_entity_values("phone-number"), None)
		if not inp:
			dispatcher.utter_message("Please enter a valid contact")
			return [UserUtteranceReverted()]
		return [SlotSet('phone-number',inp)]    
        
    
class SaveName(Action):
	def name(self):
		return 'action_save_name'
		
	def run(self, dispatcher, tracker, domain):
		inp = next(tracker.get_latest_entity_values("username"), None)
		if not inp:
			dispatcher.utter_message("Please enter your name")
			return [UserUtteranceReverted()]
		return [SlotSet('username',inp)]    
        
    