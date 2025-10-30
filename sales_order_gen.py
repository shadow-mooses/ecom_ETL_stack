import random

def generate_order_data(num_records):
    order_statuses = ['pending', 'confirmed', 'processing', 'shipped', 'delivered', 'cancelled', 'refunded']
    
    i = 1
    while i <= num_records:
        user_id = random.randint(1, 172)
        store_id = random.randint(1, 7)
        order_id = random.randint(100000, 999999)
        product_id = random.randint(1, 25)
        order_status = random.choice(order_statuses)
        
        print(f"({user_id}, {store_id}, {order_id}, {product_id}, '{order_status}'),")
        i += 1

generate_order_data(1000)
