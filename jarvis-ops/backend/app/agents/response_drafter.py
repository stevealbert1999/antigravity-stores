def draft_response(category: str, customer_email: str) -> str:
    responses = {
        'refund_request': 'We received your refund request and our support team is reviewing it.',
        'order_tracking': 'We are checking your tracking information and will update you shortly.',
        'damaged_product': 'We are sorry your product arrived damaged. We are reviewing replacement options.',
        'general_support': 'Thanks for contacting support. We are reviewing your request.'
    }

    return responses.get(category, responses['general_support'])
