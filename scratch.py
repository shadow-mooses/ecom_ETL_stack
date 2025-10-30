import random

def generate_customer_data(**context):
    """Generate random customer data"""
    first_names = ['John', 'Jane', 'Mike', 'Sarah', 'David', 'Emily', 'Chris', 'Lisa']
    last_names = ['Smith', 'Johnson', 'Williams', 'Brown', 'Jones', 'Garcia', 'Miller', 'Davis']
    cities = ['New York','Taiwan', 'London','Houston','Phoenix']
    randomnum = random.randint(1,10)
    
    first_name = random.choice(first_names)
    last_name = random.choice(last_names)
    email = f"{first_name.lower()}.{last_name.lower()}@example.com"
    username = f"{randomnum}{first_name[0].lower()}{last_name.lower()}"
    city = random.choice(cities)
    
    # Push data to XCom for the next task
    context['ti'].xcom_push(key='first_name', value=first_name)
    context['ti'].xcom_push(key='last_name', value=last_name)
    context['ti'].xcom_push(key='email', value=email)
    context['ti'].xcom_push(key='username', value=username)
    context['ti'].xcom_push(key='city', value=city)

generate_customer_data()