

def abstract(f):
    def _decorator(*_):
        raise NotImplementedError(f"Method '{f.__name__}' is abstract")
    return _decorator


class BaseSkill():

    intent = None
    samples = []    # some samples that can be used for training
    entities = {}   # the spacey entities that are parsed for optional parameters and their defaults
    responses = []  # the responses that the skill can take

    def getSamples(self) -> list:
        return {"intent": self.intent, "samples": self.samples}

    @abstract
    def actAndGetResponse(self, **kwargs) -> str:
        pass

    # by default we return an empty entity dictionary
    def parseEntities(self, doc) -> dict:
        return {}