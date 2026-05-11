def classify_ticket(message: str) -> str:
    message = message.lower()

    if 'refund' in message or 'return' in message:
        return 'refund_request'

    if 'where is my order' in message or 'tracking' in message:
        return 'order_tracking'

    if 'damaged' in message or 'broken' in message:
        return 'damaged_product'

    return 'general_support'
