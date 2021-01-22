from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from datetime import datetime as date 
import requests
import urllib3

class ActionProductNum(Action):
    def name(self) -> Text:
        return "action_product_num"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        code = tracker.get_slot("productCode")
        print(code)
        if(code == None):
            dispatcher.utter_message(text = "Bạn vui lòng nhập đúng mã sản phẩm giúp shop ạ")
            return []
        quantity = 0
        for obj in listProduct:
            if obj['productCode'] == code:
                quantity = obj['amount']
                print(obj['amount'])
        print(quantity)
        if quantity == 0:
            dispatcher.utter_message(text = "Sản phẩm này hiện đã hết hàng. Anh chị vui lòng tham khảo mẫu sản phẩm khác nhé")            
        else:
            dispatcher.utter_message(text = "Sản phẩm này hiện vẫn còn hàng ạ")
        return []
        # dispatcher.utter_message(text = "Sản phẩm này hiện đã hết hàng. Anh chị vui lòng tham khảo mẫu sản phẩm khác nhé")
        # return []

class ActionProductPrice(Action):
    def name(self) -> Text:
        return "action_product_price"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        code = tracker.get_slot("productCode")
        if(code == None):
            dispatcher.utter_message(text = "Bạn vui lòng nhập đúng mã sản phẩm giúp shop ạ")
            return []
        for obj in listProduct:
            if obj['productCode'] == code:
                price = obj['price']        
        dispatcher.utter_message(text = "Sản phẩm {} có giá {} ".format(code, price))
        return []

class ActionConsultSize(Action):
    def name(self) -> Text:
        return "action_consult_size"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        height = tracker.get_slot("height")
        weight = tracker.get_slot("weight")
        if(height == None):
            dispatcher.utter_message(text = "Bạn vui lòng nhập chiều cao để shop tư vấn ạ")
            return []
        if(weight == None):
            dispatcher.utter_message(text = "Bạn vui lòng nhập cân nặng để shop tư vấn ạ")
            return []
        check = False
        for s in sizes:
            if (s['min-weight']< weight < s['max-weight']):
                check = True
                dispatcher.utter_message(text = "Bạn mặc vừa size {} nhé".format(s['size']))
                return []
            if(s['size'] == 'XL'):
                if ( weight > s['max-weight']):
                    check = True
                    dispatcher.utter_message(text = "Xin lỗi, shop không có size phù hợp với bạn rồi ạ :((")
                    return []
            if(s['size'] == 'S'):
                if ( weight < s['min-weight']):
                    check = True
                    dispatcher.utter_message(text = "Xin lỗi, shop không có size phù hợp với bạn rồi ạ :((")
                    return []
        if(check == False):
            dispatcher.utter_message(text = "Không biết trả lời thế nào hết")
            return []
