

class Callback:
    def __init__(self, request=None, data=None, key=None, result=None, is_next=None,
                 next_label=None, direction=None, error=None):
        self.request = request
        self.data = data
        self.key = key
        self.result = result
        self.is_next = is_next
        self.next_label = next_label
        self.direction = direction
        self.error = error
