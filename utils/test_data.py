from faker import Faker

fake = Faker()

def generate_account_data(fields):
    password = fake.password()
    data = {
        'firstname': fake.first_name(),
        'lastname': fake.last_name(),
        'email': fake.email(),
        'password': password,
        'password-confirmation': password
    }
    if fields:
        return {key: value if fields.get(key, True) else '' for key, value in data.items()}
    else:
        data['password-confirmation'] += 'fakestring'
        return data
