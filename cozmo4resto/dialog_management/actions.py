# This files contains your custom actions which can be used to run
# custom Python code.
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/core/actions/#custom-actions/

# from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet, FollowupAction, ConversationPaused, ConversationResumed, UserUtteranceReverted, ActionReverted
import os
import sys
import json
import requests
import random
from zomathon import ZomatoAPI #to get restaurant information near user
import geocoder #to get coordinates of location of user

#Ankara coordinates: lat='39.91987', lon='32.85427'
#London coordinates: lat='51.509865', lon='-0.118092'
#Istanbul coordinates: lat='41.02384', lon='28.94966'

def fetchCoordinates(username):
    #use open street map (OSM)
    with open('users.json') as f:
        userdata = json.load(f)
        for i in userdata:
            if i['user'] == username:
                profile_number = userdata.index(i)
                profile = userdata[profile_number]
                user_city = profile['properties']['city']
                user_street = profile['properties']['street']
                user_full = user_street + ", " + user_city
    results = geocoder.osm(user_full)

    coordinates = results.latlng
    print(coordinates)
    return(coordinates)

def zomatoFetchRestaurants(dispatcher):
    """function creates a list of restaurants nearby the fetched coordinates, using zomato API
    
    Args:
        dispatcher: sends message back to user
    """
    z = ZomatoAPI("2f8ef60545077e72777fff722a3b1e26")
    while True:
        userlocation = fetchCoordinates("papaya")
        nearby = z.search(coordinate=userlocation, count=100)
        restaurants = []
                            
        try :
            for restaurant in (nearby['restaurants']):
                restaurants.append('{name}'.format(
                    name=restaurant['restaurant']['name']))
        except :
            dispatcher.utter_message('Something went wrong when fetching nearby restaurant...')
        break
    return(restaurants)

def zomatoFetchAddresses(dispatcher):
    """function creates a list of addresses of the restaurants from FetchRestaurants, using zomato API
    
    Args:
        dispatcher: sends message back to user
    """
    z = ZomatoAPI("2f8ef60545077e72777fff722a3b1e26")
    while True:
        userlocation = fetchCoordinates("papaya")
        nearby = z.search(coordinate=userlocation, count=100)
        addresses = []
            
        try :
            for restaurant in (nearby['restaurants']):
                addresses.append('{addr}'.format(
                    addr=restaurant['restaurant']['location']['address']))
        except :
            dispatcher.utter_message('Something went wrong when fetching nearby restaurant...')
        break
    return(addresses)

def zomatoFetchCuisines(dispatcher):
    """function creates a list of cuisines of the restaurants from FetchRestaurants, using zomato API
    
    Args:
        dispatcher: sends message back to user
    """
    z = ZomatoAPI("2f8ef60545077e72777fff722a3b1e26")
    while True:
        userlocation = fetchCoordinates("papaya")
        nearby = z.search(coordinate=userlocation, count=100)
        cuisines = []
            
        try :
            for restaurant in (nearby['restaurants']):
                cuisines.append('{cuis}'.format(
                    cuis=restaurant['restaurant']['cuisines']).lower())        
        except :
            dispatcher.utter_message('Something went wrong when fetching nearby restaurant...')
        break
    return(cuisines)

class ActionSearchRestaurant(Action):
    """
    action that sets the bot to search for restaurants nearby the user and make a suggestion

    Args:
        Action: the action the bot needs to perform
    
    Returns:
        SlotSet: updates the cuisine slot
    """
    
    def name(self):
        return "action_search_restaurant"
        
    def run(self, dispatcher, tracker, domain):
        """this function...
        Step 1: first lets the user know that the bot is searching
        Step 2: then it creates the lists via the previous functions
        Step 3: then it looks whether the cuisine the user wants, is actually available
        Step 4a:if it is it gives the suggestion
        Step 4b:if not it says it could not find one
    
        Args:
            dispatcher: sends message back to user
            tracker: gets the values of the slots filled by the user
            domain (Dict): gets the right intents, actions and templates
        """
        cuisine = tracker.get_slot('cuisine')
        
        if cuisine == None:
            dispatcher.utter_message('Sorry, this type of restaurant is not in my database. Could you be more precise?')
            return[FollowupAction("utter_cuisine")]
        elif cuisine.lower == 'any':
            cuisine = cuisine.lower()
            restaurants = zomatoFetchRestaurants(dispatcher)
            cuisines = zomatoFetchCuisines(dispatcher)
            
            pick = random.randint(1,21)
            
            dispatcher.utter_message('What do you think of ' + restaurants[pick] + ', a restaurant that serves ' + cuisines[pick] + '?')
        else:
                   
            #step 1
            restaurants = zomatoFetchRestaurants(dispatcher)
            cuisines = zomatoFetchCuisines(dispatcher)
            cuisine = cuisine.lower()
            #step 2 (often multiple cuisines per restaurant, therefore it needs to look for substrings)
            fullcuisine = next((text for text in cuisines if cuisine in text), None)
            
            #step 3b
            if fullcuisine == None:
                dispatcher.utter_message('Sorry, I could not find this type of restaurant near you. Please choose another cuisine or be more precise.')
                return[FollowupAction("utter_cuisine")]
            #step 3a
            else:
                pick = cuisines.index(fullcuisine)
                restaurant = restaurants[pick]
                dispatcher.utter_message('What do you think of ' + restaurant + ', a restaurant that serves ' + cuisines[pick] + '?')

            return[SlotSet('cuisine', cuisine), SlotSet('restaurant', restaurant)]

class ActionOtherSuggest(Action):

    def name(self):
        return "action_other_suggest"
    
    def run(self, dispatcher, tracker, domain):
        cuisine = tracker.get_slot('cuisine')
        cuisine = cuisine.lower()
        restaurant = tracker.get_slot('restaurant')

        restaurants = zomatoFetchRestaurants(dispatcher)
        cuisines = zomatoFetchCuisines(dispatcher)
        if restaurant == None:
            dispatcher.utter_message('Sorry, something went wrong.')
            return[FollowupAction("utter_cuisine")]
        else:
            indexresto = restaurants.index(restaurant)
            fromindex = indexresto + 1
            restaurants = restaurants[fromindex:]
            cuisines = cuisines[fromindex:]

            fullcuisine = next((text for text in cuisines if cuisine in text), None)
            
            if fullcuisine == None:
                dispatcher.utter_message('Sorry, I could not find another ' + cuisine + ' restaurant near you. Please choose another cuisine.')
                return[FollowupAction("utter_cuisine")]

            else:
                pick = cuisines.index(fullcuisine)
                restaurant = restaurants[pick]
                dispatcher.utter_message('What about ' + restaurant + ', a restaurant that serves ' + cuisines[pick] + '?')

                return[SlotSet('cuisine', cuisine), SlotSet('restaurant', restaurant)]


class ActionGiveAddress(Action):
    """action that sets the bot to give the address for the suggested restaurant
    
    Args:
        Action: the action the bot needs to perform
    
    Returns:
        SlotSet: updates the cuisine slot
    """
    def name(self):
        return "action_give_address"
        
    def run(self, dispatcher, tracker, domain):
        """this function finds the corresponding address of the suggested restaurant via index
           Step 1:it creates the lists again
           Step 2:then gives the address    
        
        Args:
            dispatcher: sends message back to user
            tracker: gets the values of the slots filled by the user
            domain (Dict): gets the right intents, actions and templates
        """
        cuisine = tracker.get_slot('cuisine')
        
        restaurant = tracker.get_slot('restaurant')
        #step 1
        restaurants = zomatoFetchRestaurants(dispatcher)
        addresses = zomatoFetchAddresses(dispatcher)
        
        #step 2
        if cuisine == None:
            dispatcher.utter_message('Sorry, something went wrong.')
            return[FollowupAction("utter_cuisine")]
        elif restaurant == None:
            dispatcher.utter_message('Sorry, something went wrong.')
            return[FollowupAction("utter_cuisine")]
        else:
            cuisine = cuisine.lower()
            pick = restaurants.index(restaurant)
            dispatcher.utter_message('The address is ' + addresses[pick] + '. Bon appetit!')
            return[SlotSet('cuisine', cuisine), SlotSet('restaurant', restaurant)]

#class Action_Pause(Action):
#    #this function pauses the conversation when it is finished
#    def name(self):
#        return "action_pause"
#    
#    def run(self, dispatcher, tracker, domain):
#        return[ConversationPaused()]

class ActionCustomFallback(Action):
    #this function causes the bot to have a fallback utterance when it doesn't understand the user
    #ideally, it returns to the previous state so that the user can continue its conversation
    def name(self):
        return "action_custom_fallback"

    def run(self, dispatcher, tracker, domain):
        
        dispatcher.utter_template("utter_default", tracker, silent_fail=True)
        return [UserUtteranceReverted()]