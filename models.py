class Location:
    def __init__(self, id, name, country, type, visited=False):
        self.id = id
        self.name = name
        self.country = country
        self.type = type
        self.visited = visited

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "country": self.country,
            "type": self.type,
            "visited": self.visited
        }