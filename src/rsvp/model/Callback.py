

class Callback:
    def __init__(self, request=None, data=None, key=None, result=None, is_next=None,
                 next_label=None, direction=None, error=None, is_static=None):
        self.request = request
        self.data = data
        self.key = key
        self.result = result
        self.is_next = is_next
        self.next_label = next_label
        self.direction = direction
        self.error = error
        self.is_static = is_static


def build_callback_error(callback, is_next, error):
    callback.result = False
    callback.is_next = is_next
    callback.error = error


def build_callback(callback, result, is_next, next_label, direction):
    callback.result = result
    callback.is_next = is_next
    callback.next_label = next_label
    callback.direction = direction
