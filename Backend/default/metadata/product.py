# products storage functions
import uuid




class Product:

    def __init__(self, creator: str, responsible_supervisor: str = None, content: str = None) -> None:
        self.uuid = uuid.uuid4().hex
        self.creator = creator
        self.responsible_supervisor = responsible_supervisor
        self.content = content

    def to_dict(self):
        return {
            "uuid": self.uuid,
            "creator": self.creator,
            "responsible_supervisor": self.responsible_supervisor,
            "content": self.content,
        }
