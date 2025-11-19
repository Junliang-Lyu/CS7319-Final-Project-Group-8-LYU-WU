class PlayerState:
    def __init__(self):
        self.saw_poster = False
        self.talked_professor = False
        self.got_key = False
        self.items = []

    def add_item(self, name):
        if name not in self.items:
            self.items.append(name)

player = PlayerState()
