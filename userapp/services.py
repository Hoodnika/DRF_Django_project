import stripe
from django.urls import reverse

from config.settings import STRIPE_API_KEY

stripe.api_key = STRIPE_API_KEY


def create_stripe_price(price, product_title):
    return stripe.Price.create(
        currency="rub",
        unit_amount=price * 100,
        product_data={"name": product_title},
    )


def create_stripe_session(price):
    session = stripe.checkout.Session.create(
        success_url='http://127.0.0.1:8000/payment_success/',
        line_items=[{"price": price.get('id'), "quantity": 1}],
        mode="payment",
    )
    return session.get('id'), session.get('url')


def create_stripe_product(product):
    """без default_price_data.currency_options.<currency>.unit_amount, потому что потому"""
    stripe_product = stripe.Product.create(
        name=product.title,
        description=product.description,
        active=True,
    )
    return stripe_product.get('id')
