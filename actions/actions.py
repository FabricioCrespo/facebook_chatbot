import json
from typing import Any, Dict, List, Optional, Text

from rasa_sdk import Action, Tracker
from rasa_sdk.events import FollowupAction, Restarted, SlotSet
from rasa_sdk.executor import CollectingDispatcher


def select_laptop(price: int, purpose: Optional[str], brand: Optional[List[str]]) -> List[Dict[str, str]]:
    with open('actions/laptops.json') as f: 
        laptops = json.load(f) #carga el archivo .json
    laptops = [x for x in laptops if x['price'] <= price] #selecciona la laptops que son de menor o igual precio que el ingresado por el user.
    if purpose:
        laptops = [x for x in laptops if x['purpose'].lower() == purpose] #selecciona las laptops que coincidan con el proposito.
    if brand and 'no tengo preferencia' not in brand: #Si tengo una marca y "no tengo preferencia" no esta en la lista, retorno las laptops.
        laptops = [x for x in laptops if x['brand'] in brand]
    return laptops #retorna las laptops. 


class ActionGreet(Action):
    def name(self) -> Text:
        return 'action_greet'  # Dice que devuelve la accion action_greet definida en las acciones en domain.yml

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        dispatcher.utter_message(template='utter_greet') #Devuelve el mensaje pre-definido en domain.yml en la seccion de responses.
        dispatcher.utter_message(template='utter_price') #Devuelve el mensaje pre-definido en domain.yml en la seccion de responses.
        return []


class ActionSelectPrice(Action):
    def name(self) -> Text:
        return 'action_select_upper_price'

    def extract_price(self, message: str) -> int:
        #Llena una lista vacia con los valores enteros que encuentra en el mensaje.
        #Previamente elimina los $, separa a las palabras en una lista (split) y los agrega a la lista numerical_values
        # si es que son digitos, convirtiendolos a enteros primero
        numerical_values = [int(s) for s in message.replace('$', '').split() if s.isdigit()] #Extrae los enteros encontrados en el string de respuesta 
        if len(numerical_values) >= 1:
            return numerical_values[0] #Devuelve el primer entero (precio) que se encontro en el mensaje
        else:
            return -1   #retorna -1 como flag para saber que no hay un numero 

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        upper_price = tracker.latest_message['text'] #Posiblemente es un diccionario y con la clave text accede al ultimo mensaje completo
        extracted_price = self.extract_price(upper_price) #Se aplica el metodo extract_price para extraer el precio del mensaje
        if extracted_price != -1:
            dispatcher.utter_message(text=f'I will look for a laptop under ${extracted_price}.')
            dispatcher.utter_message(template='utter_service') #Devuelve los botones configurados en domain.yml - utter_purpose
            return [SlotSet('upper_price', extracted_price)] #Guarda el precio extraido en el slot extracted_price establecido en domain.yml
        else:
            dispatcher.utter_message(template='utter_default') #Si no se encontro un valor entero en el string, devuelve un mensaje por default
            return []

class ActionSelectService(Action):
    def name(self) -> Text:
        return 'action_select_service'

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        dispatcher.utter_message(template='utter_service') #Devuelve el mensaje pre-definido en domain.yml en la seccion de responses.
        #dispatcher.utter_message(template='utter_price') #Devuelve el mensaje pre-definido en domain.yml en la seccion de responses.
        return []

class ActionSelectPurpose(Action):
    def name(self) -> Text:
        return 'action_select_purpose'

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        purpose = tracker.slots['purpose']
        dispatcher.utter_message(template='utter_brand') #Devuelve un mensaje relacionado a la accion siguiente
        return [SlotSet('purpose', purpose)]


class ActionSelectBrand(Action):
    def name(self) -> Text:
        return 'action_select_brand'

    def reformat_brands(self, message: str) -> List[str]:
        return [x.strip() for x in message.split(',')] # Genera una lista con los strings utilizando la coma como separador y Strip elimina los espacios en blanco alrededor de la palabra 

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        brands = tracker.latest_message['text'] #Recupera el ultimo mensaje que contiene las marcas
        if brands.lower().strip() != 'no tengo preferencia': #si hay marcas ingresadas
            return [SlotSet('brand', self.reformat_brands(brands)), FollowupAction('action_recommend_laptop')] #setea el slot 'brand' como una lista de las marcas.
        return [SlotSet('brand', []), FollowupAction('action_recommend_laptop')] # si no se cumple el if, setea el slot brand a una lista vacia. 


class ActionRecommendLaptop(Action):
    def name(self) -> Text:
        return 'action_recommend_laptop'

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        laptops = select_laptop(tracker.slots['upper_price'], tracker.slots['purpose'], tracker.slots['brand']) #todas las laptops encontradas
        if laptops == []:
            dispatcher.utter_message(template='utter_no_recommendations') #dicen que no hay recomendacion
        else:
            dispatcher.utter_message(text=f'I have a few recommendations for you.') #dice q tiene algunas recomendaciones.
            for laptop in laptops[:3]: #retorna solo las tres primeras recomendaciones.
                dispatcher.utter_message(
                    text=f'{laptop["name"]} (${laptop["price"]})-- {laptop["description"]}.') #retorna cada una de las laptops con sus detalles.
        return [FollowupAction('action_goodbye')] #retorna la proxima accion que es despedirse.


class ActionGoodbye(Action):
    def name(self) -> Text:
        return 'action_goodbye'

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        dispatcher.utter_message(template='utter_goodbye')
        return [Restarted()] #Reinicia la conversacion y elimina los valores almacenados en memoria
