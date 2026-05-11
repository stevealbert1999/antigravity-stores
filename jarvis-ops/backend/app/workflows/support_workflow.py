from app.agents.ticket_classifier import classify_ticket
from app.agents.response_drafter import draft_response
from app.integrations.shopify import get_customer_order


def process_support_ticket(payload):
    category = classify_ticket(payload.message)

    order_context = get_customer_order(payload.customer_email)

    suggested_response = draft_response(
        category=category,
        customer_email=payload.customer_email
    )

    return {
        'category': category,
        'order_context': order_context,
        'suggested_response': suggested_response,
        'requires_approval': True,
        'status': 'pending_human_approval'
    }
