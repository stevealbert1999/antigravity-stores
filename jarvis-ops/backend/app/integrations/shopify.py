def get_customer_order(customer_email: str):
    return {
        'customer_email': customer_email,
        'last_order_id': 'ORD-1001',
        'status': 'in_transit'
    }
