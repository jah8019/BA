class Plotpoints:

    def __init__(self, id, x, y, type_id):
        self.id = id
        self.x = [x]
        self.y = [y]
        self.type_id = type_id

    def add_point(self, actor):
        location = actor.get_location()
        self.x.append(location.x)
        self.y.append(location.y)