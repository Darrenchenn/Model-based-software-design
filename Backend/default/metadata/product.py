# products storage functions
import uuid




class Product:

    def __init__(self, 
                 creator_uuid: str,
                 creator_name: str, 
                 responsible_supervisor_uuid: str = None, 
                 responsible_supervisor_name: str = None,
                 audition_status: str = "Unaudited",
                 content: str = None) -> None:
        self.uuid = uuid.uuid4().hex
        self.creator_uuid = creator_uuid
        self.creator_name = creator_name
        self.responsible_supervisor_uuid = responsible_supervisor_uuid
        self.responsible_supervisor_name = responsible_supervisor_name
        self.audition_status = audition_status
        self.content = content

    def to_dict(self):
        return {
            "uuid": self.uuid,
            "creator_uuid": self.creator_uuid,
            "creator_name": self.creator_name,
            "responsible_supervisor_uuid": self.responsible_supervisor_uuid,
            "responsible_supervisor_name": self.responsible_supervisor_name,
            "audition_status": self.audition_status,
            "content": self.content,
        }
