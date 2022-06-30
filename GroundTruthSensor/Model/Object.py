class Object():

    def __init__(self, location, rotation, type_id, id, bounding_box):
        self.location = location
        self.rotation = rotation
        self.type_id = type_id
        self.id = id
        self.bounding_box = bounding_box
        self.distance = 0
        self.distance_set = False

    def get_location(self):
        return self.location

    def get_rotation(self):
        return self.rotation
    