from .utils import Utils
from objdict import ObjDict

class Handler:
    def __init__(self):
        self._msg_command_handler_list = []
        self._event_handler_list = []

    def _msg_parser(self, obj):
        object = dict(object = obj)
        utils = Utils(obj)

        available_methods = [m for m in dir(utils) if callable(getattr(utils, m)) and not m.startswith("_")]

        for method in available_methods:
            object[method] = getattr(utils, method)

        return ObjDict(object)

    def _msg_command_handler(self, object):
        if not self._msg_command_handler_list:
            return ()
            
        for update in self._msg_command_handler_list:
            command = object['text'].split(" ").pop(0)
            if command in update['commands']:
                return update['object']

    def _event_handler(self, object):
        for update in self._event_handler_list:
            if object['type'] in update['events']:
                return update['object']

    def _update_handler(self, update):
        if update['type'] == "message_new" and self._msg_command_handler_list:
            return self._msg_command_handler(update['object'])
        else:
            return self._event_handler(update)
        
    def command(self, commands = None):
        def decorator(object):
            def wrapper():
                self._msg_command_handler_list.append(
                    dict(
                        commands = commands,
                        object = object
                    )
                )
                
                return object
            return wrapper()
        return decorator

    def event(self, events = None):
        def decorator(object):
            def wrapper():
                self._event_handler_list.append(
                    dict(
                        events = events,
                        object = object
                    )
                )

                return object
            return wrapper()
        return decorator