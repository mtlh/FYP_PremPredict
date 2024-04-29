class team:
    def __init__(self, id: int, tla: str, name: str, crest: str, shortName: str):
        self.id = id
        self.tla = tla
        self.name = name
        self.crest = crest
        self.shortName = shortName

class referee:
    def __init__(self, id: int, name: str, type: str, nationality: str):
        self.id = id
        self.name = name
        self.type = type
        self.nationality = nationality

class competition:
    def __init__(self, id: int, code: str, name: str, type: str, emblem: str):
        self.id = id
        self.code = code
        self.name = name
        self.type = type
        self.emblem = emblem