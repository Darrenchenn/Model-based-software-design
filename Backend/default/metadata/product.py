# products storage functions
import json
import uuid




class Product:

    def __init__(self, 
                 creator_uuid: str = None, 
                 creator_name: str = None, 
                 responsible_supervisor_uuid: str = None, 
                 responsible_supervisor_name: str = None,
                 audition_status: str = "Unaudited",
                 audit_comment = None,
                 content = None) -> None:
        self.uuid = uuid.uuid4().hex
        self.creator_uuid = creator_uuid
        self.creator_name = creator_name
        self.responsible_supervisor_uuid = responsible_supervisor_uuid
        self.responsible_supervisor_name = responsible_supervisor_name
        self.audition_status = audition_status
        self.audit_comment = audit_comment
        self.content = content

    def to_dict(self) -> dict:
        return {
            "uuid": self.uuid,
            "creator_uuid": self.creator_uuid,
            "creator_name": self.creator_name,
            "responsible_supervisor_uuid": self.responsible_supervisor_uuid,
            "responsible_supervisor_name": self.responsible_supervisor_name,
            "audition_status": self.audition_status,
            "audit_comment": self.audit_comment,
            "content": self.content,
        }
    
    def from_result_to_product(self, result):
        self.uuid = result.get("uuid", uuid.uuid4().hex)
        self.creator_uuid = result.get("creator_uuid", "")
        self.creator_name = result.get("creator_name", "")
        self.responsible_supervisor_uuid = result.get("responsible_supervisor_uuid", "")
        self.responsible_supervisor_name = result.get("responsible_supervisor_name", "")
        self.audition_status = result.get("audition_status", "")
        self.audit_comment = result.get("audit_comment", "")
        self.content = result.get("content", "")
        return self
