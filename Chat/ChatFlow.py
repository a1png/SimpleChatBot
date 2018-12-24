import json
import re
from enum import Enum
from dateutil.parser import parse
from Users.models import GenderEnum, SmokerEnum


RECORD_FIELDS = ['name', 'birth_date', 'smoker', 'gender']  # fields we want to record
FIELD_RULES = {
    'name': r"^[A-Za-z]+$",
}
FIELD_ENUMS = {
    'gender': GenderEnum,
    'smoker': SmokerEnum
}
CHAT_FLOW_FILE = 'Chat/chat_flow.json'


class ChatNode:
    def __init__(self, chat):
        self.field = chat.get('field')
        self.next = chat.get('next')
        self.default_next = None
        self.message = chat.get('message')
        self.response = None
        self.to_record = False
        if self.field in RECORD_FIELDS:
            self.to_record = True

    def parse_response(self, message):
        field_rule = FIELD_RULES.get(self.field)
        field_enum = FIELD_ENUMS.get(self.field)
        if self.field in ['birth_date']:
            try:
                message = parse(message, dayfirst=True)
            except:
                return None
        if field_rule is not None:
            if re.match(field_rule, message) is None:
                return None
        if field_enum is not None:
            try:
                message = getattr(field_enum, message.lower()).value
            except:
                return None

        return message


class ChatFlow:
    def __init__(self):
        with open(CHAT_FLOW_FILE) as flow:
            self.chat_flow = json.loads(flow.read())
        self.chat_graph = {}
        for chat_id, chat in self.chat_flow.items():
            # read each chat content in a dictionary with its id as key
            self.chat_graph[chat_id] = ChatNode(chat)

        self.current_chat = None
        self.reset_chat()
        del self.chat_flow

    def reset_chat(self):
        self.set_chat(0)

    def set_chat(self, chat_id):
        # set the current position in the flow to a given chat_id
        self.current_chat = self.chat_graph[str(chat_id)]

    def get_next_chat(self):
        # can extend to navigate by condition, not just default.
        next_chat_id = self.current_chat.next.get('default')
        if next_chat_id is not None:
            self.current_chat = self.get_chat_by_id(next_chat_id)

    def get_chat_by_id(self, chat_id):
        chat = self.chat_graph.get(chat_id)
        return chat

    def get_final_sentence(self):
        chat = self.chat_graph.get('999')
        return chat
