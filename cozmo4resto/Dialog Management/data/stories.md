## dinner-simple-italian
* greet
  - utter_greet
* wantdinner
  - utter_cuisine
* cuisine{"cuisine": "italian"}
  - utter_look
  - action_search_restaurant
  - slot{"cuisine": "italian"}
* affirm_yes
  - utter_ask_address
* affirm_need
  - action_give_address
  - slot{"cuisine": "italian"}
* affirm_yes
  - utter_goodbye
* goodbye
* greet

## give-address
* cuisine{"cuisine": "kebab"}
  - utter_look
  - action_search_restaurant
  - slot{"cuisine": "kebab"}
* affirm_yes
  - utter_ask_address
* affirm_need
  - action_give_address
  - slot{"cuisine": "kebab"}
* affirm_yes
  - utter_goodbye
* goodbye
* greet

## give-address-2
  - action_search_restaurant
  - slot{"cuisine": "italian"}
* affirm_yes
  - utter_ask_address
* affirm_need
  - action_give_address
  - slot{"cuisine": "italian"}
* affirm_yes
  - utter_goodbye
* goodbye

## give-address-small
  - action_search_restaurant
  - slot{"cuisine": "italian"}
* affirm_yes
  - utter_ask_address
* affirm_need
  - action_give_address
  - slot{"cuisine": "italian"}

## no-resto
* greet
  - utter_greet
* wantdinner
  - utter_cuisine
* cuisine{"cuisine": "american"}
  - utter_look
  - action_search_restaurant
  - slot{"cuisine": "american"}
* deny
  - action_other_suggest
  - slot{"cuisine": "american"}
* affirm_yes
  - utter_ask_address
* affirm_need

## no-no-resto-cuisine
* cuisine{"cuisine": "asian"}
  - utter_look
  - action_search_restaurant
  - slot{"cuisine": "asian"}
* deny
  - action_other_suggest
  - slot{"cuisine": "asian"}
* deny
  - action_other_suggest
  - slot{"cuisine": "asian"}
* affirm_yes
  - utter_ask_address
* affirm_need

## no-resto-yes-address
* affirm_yes
  - utter_ask_address
* affirm_need
  - action_give_address
  - slot{"cuisine": "dessert"}

## no-no-resto-address
* deny
  - action_other_suggest
  - slot{"cuisine": "asian"}
* affirm_yes
  - utter_ask_address
* affirm_need
  - action_give_address
  - slot{"cuisine": "asian"}
* affirm_yes
  - utter_goodbye
* goodbye
* greet

## no-no-resto-no-address
* deny
  - action_other_suggest
  - slot{"cuisine": "asian"}
* affirm_yes
  - utter_ask_address
* deny
  - utter_bon_appetit
* goodbye
* greet

## nogreet-simple-italian
* wantdinner
  - utter_cuisine
* cuisine{"cuisine": "italian"}
  - utter_look
  - action_search_restaurant
  - slot{"cuisine": "italian"}
* affirm_yes
  - utter_ask_address
* affirm_need
  - action_give_address
  - slot{"cuisine": "italian"}
* affirm_yes
  - utter_goodbye
* goodbye
* greet

## need-address
* affirm_yes
  - utter_ask_address
* affirm_need
  - action_give_address
  - slot{"cuisine": "indian"}
* affirm_yes
  - utter_goodbye
* goodbye
* greet

## no-resto-thai
* wantdinner
  - utter_cuisine
* cuisine{"cuisine": "thai"}
  - utter_look
  - action_search_restaurant
  - slot{"cuisine": "thai"}
* deny
  - action_other_suggest
  - slot{"cuisine": "thai"}
* affirm_yes
  - utter_ask_address
* deny
  - utter_goodbye
* goodbye
* greet

## cuisine-simple-italian
* cuisine{"cuisine": "italian"}
  - utter_look
  - action_search_restaurant
  - slot{"cuisine": "italian"}
* affirm_yes
  - utter_ask_address
* affirm_need
  - action_give_address
  - slot{"cuisine": "italian"}
* affirm_yes
  - utter_goodbye
* goodbye
* greet

## greet-cuisine-simple-kebab
* greet
  - utter_greet
* cuisine{"cuisine": "kebab"}
  - utter_look
  - action_search_restaurant
  - slot{"cuisine": "kebab"}
* affirm_yes
  - utter_ask_address
* affirm_need
  - action_give_address
  - slot{"cuisine": "kebab"}
* affirm_yes
  - utter_goodbye
* goodbye
* greet

## greet-no-resto-thai
* greet
  - utter_greet
* cuisine{"cuisine": "thai"}
  - utter_look
  - action_search_restaurant
  - slot{"cuisine": "thai"}
* deny
  - action_other_suggest
  - slot{"cuisine": "thai"}
* affirm_yes
  - utter_ask_address
* deny
  - utter_goodbye
* goodbye
* greet

## no-cuisine
* greet
  - utter_greet
* cuisine{"cuisine": "None"}
  - utter_no_options
* cuisine{"cuisine": "italian"}
  - utter_look
  - action_search_restaurant
  - slot{"cuisine": "italian"}
* affirm_yes

## dinner-simple-italian-1
* greet
  - utter_greet
* wantdinner
  - utter_cuisine
* cuisine{"cuisine": "italian"}
  - utter_look
  - action_search_restaurant
  - slot{"cuisine": "italian"}
* affirm_yes
  - utter_ask_address
* deny
  - utter_bon_appetit
* goodbye
* greet

## nogreet-simple-italian-2
* wantdinner
  - utter_cuisine
* cuisine{"cuisine": "italian"}
  - utter_look
  - action_search_restaurant
  - slot{"cuisine": "italian"}
* affirm_yes
  - utter_ask_address
* deny
  - utter_bon_appetit
* goodbye
* greet

## cuisine-simple-turkish
* cuisine{"cuisine": "turkish"}
  - utter_look
  - action_search_restaurant
  - slot{"cuisine": "turkish"}
* affirm_yes
  - utter_ask_address
* deny
  - utter_bon_appetit
* goodbye
* greet

## greet-cuisine-simple-turkish
* greet
  - utter_greet
* cuisine{"cuisine": "turkish"}
  - utter_look
  - action_search_restaurant
  - slot{"cuisine": "turkish"}
* affirm_yes
  - utter_ask_address
* deny
  - utter_bon_appetit
* goodbye
* greet

## search-resto
  - action_search_restaurant
  - slot{"cuisine": "italian"}
* affirm_yes
  - utter_ask_address
* deny
  - utter_bon_appetit
* goodbye
* greet

## dinner-simple-kebab-2
* greet
  - utter_greet
* wantdinner
  - utter_cuisine
* cuisine{"cuisine": "kebab"}
  - utter_look
  - action_search_restaurant
  - slot{"cuisine": "kebab"}
* affirm_yes
  - utter_ask_address
* affirm_need
  - action_give_address
  - slot{"cuisine": "kebab"}
* affirm_yes
  - utter_goodbye
* goodbye
* greet

## nogreet-simple-american-2
* wantdinner
  - utter_cuisine
* cuisine{"cuisine": "american"}
  - utter_look
  - action_search_restaurant
  - slot{"cuisine": "american"}
* affirm_yes
  - utter_ask_address
* affirm_need
  - action_give_address
  - slot{"cuisine": "american"}
* affirm_yes
  - utter_goodbye
* goodbye
* greet

## cuisine-simple-sushi
* cuisine{"cuisine": "sushi"}
  - utter_look
  - action_search_restaurant
  - slot{"cuisine": "sushi"}
* affirm_yes
  - utter_ask_address
* affirm_need
  - action_give_address
  - slot{"cuisine": "sushi"}
* affirm_yes
  - utter_goodbye
* goodbye
* greet

## greet-cuisine-simple-italian-2
* greet
  - utter_greet
* cuisine{"cuisine": "italian"}
  - utter_look
  - action_search_restaurant
  - slot{"cuisine": "italian"}
* affirm_yes
  - utter_ask_address
* affirm_need
  - action_give_address
  - slot{"cuisine": "italian"}
* affirm_yes
  - utter_goodbye
* goodbye
* greet

## greet-next-step
* goodbye
* greet
  - utter_greet
* cuisine{"cuisine": "french"}
  - utter_look
  - action_search_restaurant
  - slot{"cuisine": "french"}
* deny
  - action_other_suggest
  - slot{"cuisine": "thai"}
* affirm_yes
  - utter_ask_address
* deny
  - utter_goodbye
* goodbye

## goodbye
  - utter_goodbye
* goodbye
* greet

## goodbye-bon-appetit
  - utter_bon_appetit
* goodbye
* greet

## kevin-greet
* kevin
  - utter_kevin
* greet

## kevin-resto
* kevin
  - utter_kevin
* cuisine{"cuisine": "asian"}

## address-need
  - utter_ask_address
* affirm_need
  - action_give_address
  - slot{"cuisine": "dessert"}
* thank

## thanks
* thank
  - utter_welcome
* goodbye
* greet

## thanks-address
* affirm_need
  - action_give_address
  - slot{"cuisine": "italian"}
* thank
  - utter_welcome
* goodbye
* greet

## bye-address
* affirm_need
  - action_give_address
  - slot{"cuisine": "italian"}
* goodbye
  - utter_goodbye

## ok-address
* affirm_need
  - action_give_address
  - slot{"cuisine": "italian"}
* affirm_yes
  - utter_goodbye
* goodbye
* greet

## thanks-simple
* thank
  - utter_welcome

## affirm-after-suggest
  - action_search_restaurant
  - slot{"cuisine": "french"}
* affirm_yes
  - utter_ask_address
* affirm_need

## affirm-after-suggest-2
  - action_search_restaurant
  - slot{"cuisine": "french"}
* deny
  - action_other_suggest
  - slot{"cuisine": "dessert"}
* affirm_yes
  - utter_ask_address
* affirm_need

## after-need-give-address
* affirm_need
  - action_give_address
  - slot{"cuisine": "any"}
* thank
  - utter_welcome
* goodbye
* greet

## after-yes-give-address
* affirm_yes
  - action_give_address
  - slot{"cuisine": "portuguese"}
* thank

## goodbye
* goodbye
  - utter_goodbye
* greet
