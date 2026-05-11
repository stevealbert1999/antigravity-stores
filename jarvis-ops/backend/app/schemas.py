from pydantic import BaseModel

class TicketPayload(BaseModel):
    customer_email: str
    subject: str
    message: str

class WorkflowResult(BaseModel):
    category: str
    suggested_response: str
    requires_approval: bool
