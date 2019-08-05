import logging
import json
import zmq
from sanic import Blueprint, response
from sanic.request import Request
from typing import Text, Optional, List, Dict, Any

from rasa.core.channels.channel import UserMessage, OutputChannel
from rasa.core.channels.channel import InputChannel
from rasa.core.channels.channel import CollectingOutputChannel



logger = logging.getLogger(__name__)


		
class CozmoConnect(InputChannel):
    """A custom http input channel.
    This implementation is the basis for a custom implementation of a chat
    frontend. You can customize this to send messages to Rasa Core and
    retrieve responses from the agent."""

    @classmethod
    def name(cls):
        return "cozmo"

    def get_text():
        context = zmq.Context()
        socket = context.socket(zmq.REQ)
        socket.connect("tcp://127.0.0.1:5000")

        socket.send()
        msg = socket.recv_string()
        text = json.loads(msg)['data']
        print('User said:{}'.format(text))
        return text

    def blueprint(self, on_new_message):
	    
        custom_webhook = Blueprint('custom_webhook', __name__)

        @custom_webhook.route("/", methods=['GET'])
        async def health(request):
            return response.json({"status": "ok"})

        @custom_webhook.route("/webhook", methods=['POST'])
        async def receive():
            text = get_text() #grab message from user
            with open('users.json') as f:
                userdata = json.load(f)
            sender_id = userdata['user']['papaya']
            output = CollectingOutputChannel() #sets the output channel to just collect the messages from Core
            on_new_message(UserMessage(text, output, sender_id)) #this will tell Rasa Core to handle this user message
            responses = [m["text"] for m in out.messages] #out.messages = list of dictionaries with id & response message
            #grab response for bot:
            message = ' '.join(responses) #if dispatcher sends multiple messages these are all put in 'message'
            r = {
                  "Username": sender_id,
                  "Convo": {
                       "UserInput": text,
                       "BotOutput": message
                  }
            }

            return response.json(r)				
          		
        return custom_webhook
