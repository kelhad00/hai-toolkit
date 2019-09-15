# import dependencies 
      from __future__ import absolute_import
      from __future__ import division
      from __future__ import print_function
      from __future__ import unicode_literals
      
      import logging
      
      from flask import Flask, Response, Blueprint, request, jsonify
      from rasa_core.channels.channel import UserMessage, OutputChannel
      from rasa_core.channels.channel import InputChannel
      from rasa_core.channels.channel import CollectingOutputChannel
      import json
      
      logger = logging.getLogger(__name__)
      
      # create connector class. Inherits InputChannel class from Rasa Core
      class GoogleConnector(InputChannel):
      
         @classmethod  ## define webhook url prefix
         def name(cls):
             return "Google_home"
      
         def blueprint(self, on_new_message):  # define webhook for Google Assistant
      
             Google_webhook = Blueprint('Google_webhook', __name__)
      
             @Google_webhook.route("/", methods=['GET']) # define health route
             def health():
                 return jsonify({"status": "ok"})
      
             @Google_webhook.route("/webhook", methods=['POST']) # define webhook route
             def receive():
                 payload = json.loads(request.data)
                 sender_id = payload['user']['userId']
                 intent = payload['inputs'][0]['intent']
                 text = payload['inputs'][0]['rawInputs'][0]['query']
                 if intent == 'actions.intent.MAIN': ## send bot response on connection
                     message = "<speak>Hey! <break time=\"1\"/>How can I help you?"
                 Else: ## send casual bot response regarding user messages
                     out = CollectingOutputChannel()
                     on_new_message(UserMessage(text, out, sender_id))
                     responses = [m["text"] for m in out.messages]
                     message = responses[0]
                 r = json.dumps(
                     {
                       "conversationToken": "{\"state\":null,\"data\":{}}",
                       "expectUserResponse": 'true',
                       "expectedInputs": [
                         {
                           "inputPrompt": {
                            "initialPrompts": [
                             {
                               "ssml": message
                             }
                           ]
                          },
                         "possibleIntents": [
                         {
                           "intent": "actions.intent.TEXT"
                         }
                        ]
                       }
                      ]
                    })
                 return r
      
             return Google_webhook