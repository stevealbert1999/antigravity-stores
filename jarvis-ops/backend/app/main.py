from fastapi import FastAPI
from app.schemas import TicketPayload
from app.workflows.support_workflow import process_support_ticket

app = FastAPI(title='Jarvis Ops API')

@app.get('/')
def healthcheck():
    return {'status': 'ok', 'service': 'jarvis-ops'}

@app.post('/support/process')
def process_ticket(payload: TicketPayload):
    result = process_support_ticket(payload)
    return result
