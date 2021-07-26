import json
from typing import Any, Dict, List, Optional, Text

from rasa_sdk import Action, Tracker
from rasa_sdk.events import FollowupAction, Restarted, SlotSet
from rasa_sdk.executor import CollectingDispatcher


#========================GLOBAL VARIABLES===============================

topins={'Compras en Whatsapp':20,'Agendar citas':30, 'Banner animado':10}
plans={'Básico':200, 'Medio':350, 'Business':500}
selected_topins=[]
total=0

#=======================================================================


def select_laptop(price: int, purpose: Optional[str], brand: Optional[List[str]]) -> List[Dict[str, str]]:
    with open('actions/laptops.json') as f: 
        laptops = json.load(f) #carga el archivo .json
    laptops = [x for x in laptops if x['price'] <= price] #selecciona la laptops que son de menor o igual precio que el ingresado por el user.
    if purpose:
        laptops = [x for x in laptops if x['purpose'].lower() == purpose] #selecciona las laptops que coincidan con el proposito.
    if brand and 'no tengo preferencia' not in brand: #Si tengo una marca y "no tengo preferencia" no esta en la lista, retorno las laptops.
        laptops = [x for x in laptops if x['brand'] in brand]
    return laptops #retorna las laptops. 


""" class ActionGreet(Action):
    def name(self) -> Text:
        return 'action_greet'  # Dice que devuelve la accion action_greet definida en las acciones en domain.yml

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        dispatcher.utter_message(template='utter_greet') #Devuelve el mensaje pre-definido en domain.yml en la seccion de responses.
        dispatcher.utter_message(template='utter_price') #Devuelve el mensaje pre-definido en domain.yml en la seccion de responses.
        return [] """

""" Function to send a greet to the user when it write to the chatbot """
class ActionGreet(Action):
    def name(self) -> Text:
        return 'action_greet'  # Dice que devuelve la accion action_greet definida en las acciones en domain.yml

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        dispatcher.utter_message(template='utter_menu') #Devuelve el mensaje pre-definido en domain.yml en la seccion de responses.
        return []

"""  Function to capture the service choosen by the user"""
class ActionSelectMenu(Action):
    def name(self) -> Text:
        return 'action_select_menu'

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        menu = tracker.slots['menu']

        print('=========================================')
        print(f'It is the selected menu: {menu}')
        print('=========================================')
        #-----------------HERE GOES IF CODE DEPENDING ON THE SELECTION OF THE USER------------------#

        if tracker.slots['menu'] =="Servicios":
            dispatcher.utter_message(template='utter_servicios_menu') #Devuelve un mensaje relacionado a la accion siguiente
            return [SlotSet('menu', menu)]
        
        elif tracker.slots['menu'] =="Planifiquemos mi página web":
            dispatcher.utter_message(template='utter_website_plan') #Devuelve un mensaje relacionado a la accion siguiente
            return [SlotSet('menu', menu)]

        elif tracker.slots['menu'] =="Comunicarse con un representante":
            dispatcher.utter_message(template='utter_contacto_menu') #Devuelve un mensaje relacionado a la accion siguiente
            return [SlotSet('menu', menu)]

        else:
            dispatcher.utter_message(template='utter_default') #Si no se encontro un valor entero en el string, devuelve un mensaje por default
            return []

        #----------------------------------end code--------------------------------------------------#

"""  Function to capture the action if the user selects services option"""
class ActionSelectService(Action):
    def name(self) -> Text:
        return 'action_select_service'

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        service = tracker.slots['service']

        print('=========================================')
        print(f'It is the selected service: {service}')
        print('=========================================')
        #-----------------HERE GOES IF CODE DEPENDING ON THE SELECTION OF THE USER------------------#

        # Return info about marketing plans.
        if tracker.slots['service'] == "Marketing Digital":
            dispatcher.utter_message(template='utter_marketing') #Devuelve un mensaje relacionado a la accion siguiente
            dispatcher.utter_message(template='utter_goodbye')
            return [Restarted()] #Reinicia la conversacion y elimina los valores almacenados en memoria
            #return [SlotSet('service', service)]
        
        # Return info about Websites service
        elif tracker.slots['service'] == "Websites":
            dispatcher.utter_message(template='utter_websites') #Devuelve un mensaje relacionado a la accion siguiente
            dispatcher.utter_message(template='utter_goodbye')
            return [Restarted()] #Reinicia la conversacion y elimina los valores almacenados en memoria
            #return [SlotSet('service', service)]
        
        # Return info about Apps service
        elif tracker.slots['service'] == "Apps":
            dispatcher.utter_message(template='utter_apps') #Devuelve un mensaje relacionado a la accion siguiente
            dispatcher.utter_message(template='utter_goodbye')
            return [Restarted()] #Reinicia la conversacion y elimina los valores almacenados en memoria
            #return [SlotSet('service', service)]
        
        else:
            dispatcher.utter_message(template='utter_default') #Si no se encontro un valor entero en el string, devuelve un mensaje por default
            return []

        #----------------------------------end code--------------------------------------------------#

"""  Function to capture the action if the user select diseñar my website option"""
class ActionSelectPlan(Action):
    def name(self) -> Text:
        return 'action_select_plan'

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        #Retrive total global variable
        global total
        global plans

        plan= tracker.slots['plan']

        print('=========================================')
        print(f'It is the selected service: {plan}')
        print('=========================================')
        #-----------------HERE GOES IF CODE DEPENDING ON THE SELECTION OF THE USER------------------#

        # Return info about marketing plans.
        if tracker.slots['plan'] == "Básico":
            #Increase total
            total+=plans['Básico']

            dispatcher.utter_message(template='utter_topins') #Devuelve un mensaje relacionado a la accion siguiente
            return [SlotSet('plan', plan)]
        
        # Return info about Websites service
        elif tracker.slots['plan'] == "Medio":
            #Increase total
            total+=plans['Medio']

            dispatcher.utter_message(template='utter_topins') #Devuelve un mensaje relacionado a la accion siguiente
            return [SlotSet('plan', plan)]
        
        # Return info about Apps service
        elif tracker.slots['plan'] == "Business":
            #Increase total
            total+=plans['Business']

            dispatcher.utter_message(template='utter_topins') #Devuelve un mensaje relacionado a la accion siguiente
            return [SlotSet('plan', plan)]
        
        else:
            dispatcher.utter_message(template='utter_default') #Si no se encontro un valor entero en el string, devuelve un mensaje por default
            return []

        #----------------------------------end code--------------------------------------------------#

"""  Function to capture the action if the user select diseñar my website option"""
class ActionSelectTopin(Action):
    def name(self) -> Text:
        return 'action_select_topin'

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        #Retrive total global variable
        global total
        global topins
        global selected_topins

        topin= tracker.slots['topin']

        print('=========================================')
        print(f'It is the selected topin: {topin}')
        print('=========================================')
        #-----------------HERE GOES IF CODE DEPENDING ON THE SELECTION OF THE USER------------------#

        # Return info about marketing plans.
        if tracker.slots['topin'] == "WhatsApp":
            if "WhatsApp" in selected_topins:
                dispatcher.utter_message(template='utter_exist_topin') #Si no se encontro un valor entero en el string, devuelve un mensaje por default
                dispatcher.utter_message(template='utter_topins') #Devuelve un mensaje relacionado a la accion siguiente
                return []
            else:
                #Increase total
                total+=topins['Compras en Whatsapp']

                selected_topins.append("WhatsApp")

                dispatcher.utter_message(template='utter_topins') #Devuelve un mensaje relacionado a la accion siguiente
                return [SlotSet('topin', topin)]
        
        # Return info about Websites service
        elif tracker.slots['topin'] == "Citas":
            if "Citas" in selected_topins:
                dispatcher.utter_message(template='utter_exist_topin') #Si no se encontro un valor entero en el string, devuelve un mensaje por default
                dispatcher.utter_message(template='utter_topins') #Devuelve un mensaje relacionado a la accion siguiente
                return []
            else: 
                #Increase total
                total+=topins['Agendar citas']
                
                selected_topins.append("Citas")

                dispatcher.utter_message(template='utter_topins') #Devuelve un mensaje relacionado a la accion siguiente
                return [SlotSet('topin', topin)]
        
        # Return info about Apps service
        elif tracker.slots['topin'] == "Banner":
            if "Banner" in selected_topins:
                dispatcher.utter_message(template='utter_exist_topin') #Si no se encontro un valor entero en el string, devuelve un mensaje por default
                dispatcher.utter_message(template='utter_topins') #Devuelve un mensaje relacionado a la accion siguiente
                return []
            else: 
                #Increase total
                total+=topins['Banner animado']
                
                selected_topins.append("Banner")

                dispatcher.utter_message(template='utter_topins') #Devuelve un mensaje relacionado a la accion siguiente
                return [SlotSet('topin', topin)]

        elif tracker.slots['topin'] == "Cotizar":
            dispatcher.utter_message(text=f'El precio de tu website es ${total} +IVA.')
            dispatcher.utter_message(template='utter_goodbye')
            return [Restarted()] #Reinicia la conversacion y elimina los valores almacenados en memoria
            #return [SlotSet('service', service)]
        
        else:
            dispatcher.utter_message(template='utter_default') #Si no se encontro un valor entero en el string, devuelve un mensaje por default
            return []

        #----------------------------------end code--------------------------------------------------#

"""  Function to capture the action if the user selects comunicarse option"""
class ActionSelectContacto(Action):
    def name(self) -> Text:
        return 'action_select_contacto'

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        contacto = tracker.slots['contacto']

        print('=========================================')
        print(f'It is the selected service: {contacto}')
        print('=========================================')
        #-----------------HERE GOES IF CODE DEPENDING ON THE SELECTION OF THE USER------------------#

        # Return info about marketing plans.
        if tracker.slots['contacto'] == "WhatsApp":
            dispatcher.utter_message(template='utter_whatsapp') #Devuelve un mensaje relacionado a la accion siguiente
            dispatcher.utter_message(template='utter_goodbye')
            return [Restarted()] #Reinicia la conversacion y elimina los valores almacenados en memoria
            #return [SlotSet('service', service)]
        
        # Return info about Websites service
        elif tracker.slots['contacto'] == "Messenger":
            dispatcher.utter_message(template='utter_messenger') #Devuelve un mensaje relacionado a la accion siguiente
            dispatcher.utter_message(template='utter_goodbye')
            return [Restarted()] #Reinicia la conversacion y elimina los valores almacenados en memoria
            #return [SlotSet('service', service)]
        
        # Return info about Apps service
        elif tracker.slots['contacto'] == "Llamada":
            dispatcher.utter_message(template='utter_llamada') #Devuelve un mensaje relacionado a la accion siguiente
            dispatcher.utter_message(template='utter_goodbye')
            return [Restarted()] #Reinicia la conversacion y elimina los valores almacenados en memoria
            #return [SlotSet('service', service)]
        
        else:
            dispatcher.utter_message(template='utter_default') #Si no se encontro un valor entero en el string, devuelve un mensaje por default
            return []

        #----------------------------------end code--------------------------------------------------#


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
            dispatcher.utter_message(template='utter_purpose') #Devuelve los botones configurados en domain.yml - utter_purpose
            return [SlotSet('upper_price', extracted_price)] #Guarda el precio extraido en el slot extracted_price establecido en domain.yml
        else:
            dispatcher.utter_message(template='utter_default') #Si no se encontro un valor entero en el string, devuelve un mensaje por default
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
