import json
import random
import string
import phonenumbers
from phonenumbers import geocoder, region_code_for_country_code
from django.utils.text import slugify


def random_string_generator(size=10, chars=string.ascii_lowercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


def unique_slug_generator(instance, new_slug=None):
    """
    This is for a Django project and it assumes your instance
    has a model with a slug field and a title character (char) field.
    """
    slug = new_slug if new_slug is not None else slugify(instance.name)
    Klass = instance.__class__
    if qs_exists := Klass.objects.filter(slug=slug).exists():
        new_slug = "{slug}-{randstr}".format(
            slug=slug,
            randstr=random_string_generator(size=4)
        )
        return unique_slug_generator(instance, new_slug=new_slug)
    return slug


def get_phone_country(phone_number):
    i = phonenumbers.parse(phone_number)
    return region_code_for_country_code(i.country_code)


def get_countries(json_file_dir):
    with open(json_file_dir, encoding='utf-8') as f:
        data = json.load(f)
    # print([country['name'] for country in data])
    return [country['name'] for country in data]


def get_states(json_file_dir, country):
    with open(json_file_dir, encoding='utf-8') as f:
        data = json.load(f)
        states = []
        for item in data:
            if item['name'] == country:
                states.extend(state['name'] for state in item['states'])
        return states


def get_cities_only(json_file_dir, country, state):
    with open(json_file_dir, 'r', encoding='utf-8') as f:
        data = json.load(f)
    for c in data:
        if c['name'] == country:
            for s in c['states']:
                if s['name'] == state:
                    return [city['name'] for city in s['cities']]
    return []


def generate_username(org_name, volantBA_user, Klass):
    username = org_name[:5] + volantBA_user[:5]
    count = 1
    while True:
        if Klass.objects.filter(username=username + str(count).zfill(2)).exists():
            count += 1
        else:
            break
    return username + str(count).zfill(2)


def generate_password(org_name, volantBA_user):
    return org_name[:5] + volantBA_user[:5] + str(random.randint(100, 999))


def get_car_brands(json_file_dir):
    with open(json_file_dir, encoding='utf-8') as f:
        data = json.load(f)
    # print([car['brand'] for car in data])
    return [car['brand'] for car in data]


# def get_car_brand_models(json_file_dir, brand):
#     with open(json_file_dir, encoding='utf-8') as f:
#         data = json.load(f)
#         models = []
#         for item in data:
#             if item['brand'] == brand:
#                 models.extend(model['name'] for model in item['models'])
#         return models

def get_car_brand_models(json_file_dir, brand):
    with open(json_file_dir, encoding='utf-8') as f:
        try:
            data = json.load(f)
            models = []
            for item in data:
                if 'brand' in item and 'models' in item and item['brand'] == brand:
                    models.extend(iter(item['models']))
            return models
        except json.JSONDecodeError as e:
            print(f"Error decoding JSON: {e}")
            return []


def get_car_logo(json_file_dir, brand):
    try:
        with open(json_file_dir, encoding='utf-8') as f:
            data = json.load(f)
            for item in data:
                if 'brand' in item and 'logo' in item and item['brand'] == brand:
                    return item['logo']
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON: {e}")
    return None


# Get nested states by names
def get_states_only(json_file_dir):
    file_path = json_file_dir
    with open(file_path, 'r') as json_file:
        data = json.load(json_file)
        return [b["name"] for b in data]


def get_cities_only_v2(json_file_dir, state):
    file_path = json_file_dir
    with open(file_path, 'r') as json_file:
        data = json.load(json_file)
        return next(b['cities'] for b in data if b["name"] == state)
