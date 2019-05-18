from .api import api
from .keyboard import Keyboard

class Utils:
    def __init__(self, data):
        self.data = data
        self._kb = Keyboard()

    def sendMessage(self, peer_id, message, attachment = None, sticker_id = None, keyboard = None, **kwargs):
        return api(
            "messages.send",
            message = str(message),
            random_id = 0,
            peer_id = int(peer_id),
            attachment = attachment,
            sticker_id = sticker_id,
            keyboard = keyboard,
            **kwargs
        )

    def reply(self, message, **kwargs):
        return self.sendMessage(
            message = str(message),
            peer_id = int(self.data['peer_id']),
            **kwargs
        )
    
    def keyboard(self, buttons, one_time = False):
        return self._kb(
            buttons = buttons,
            one_time = one_time
        )

