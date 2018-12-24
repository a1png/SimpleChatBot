import json
import traceback
from channels.generic.websocket import WebsocketConsumer
from Users.models import UserInfo
from .ChatFlow import ChatFlow

GENDER_STATUS = {
    0: 'female',
    1: 'male',
    2: 'unknown'
}
SMOKER_STATUS = {
    0: 'non-smoker',
    1: 'smoker'
}
SUMMARIZE_SAFE_WORD = 'done'

class ChatConsumer(WebsocketConsumer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.chat_graph = ChatFlow()
        self.user_info = UserInfo()

    def connect(self):
        user = self.scope["user"]
        if user.is_authenticated:
            self.user_info.user_id = user.id
        self.accept()
        msg = self.chat_graph.current_chat.message
        self.send_msg(msg)
        self.chat_graph.get_next_chat()
        msg = self.chat_graph.current_chat.message
        self.send_msg(msg)

    def disconnect(self, close_code):
        try:
            # will need validation here
            self.user_info.save()
            # if save is done, send the info sentence.

        except Exception:
            traceback.print_exc()

    def receive(self, text_data):
        print(text_data)
        json_text_data = json.loads(text_data)
        message = json_text_data.get('message')
        if message == SUMMARIZE_SAFE_WORD:
            try:
                self.user_info.full_clean()
                self.send_msg(self.chat_graph.get_final_sentence().message %
                              (self.user_info.name, self.user_info.birth_date.strftime("%d-%m-%Y"),
                               GENDER_STATUS[self.user_info.gender], SMOKER_STATUS[self.user_info.smoker]))
            except:
                self.send_msg('bye')
            self.close()
        data = self.chat_graph.current_chat.parse_response(message)
        if data is None:
            if self.chat_graph.current_chat.to_record:
                msg = "Please input the correct data"
                self.send_msg(msg)
            else:
                self.chat_graph.get_next_chat()
        else:
            chat_phase = self.chat_graph.current_chat
            field = chat_phase.field
            if chat_phase.to_record:
                # if this is a field we want to record the msg, we save it to the data object
                setattr(self.user_info, field, data)
            self.chat_graph.get_next_chat()
        if self.chat_graph.current_chat is not None:
            msg = self.chat_graph.current_chat.message
            self.send_msg(msg)

    def send_msg(self, text):
        self.send(text_data=json.dumps({
            'message': text
        }))
