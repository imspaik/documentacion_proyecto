from django.conf import settings
from oscar.apps.payment.exceptions import UnableToTakePayment, InvalidGatewayRequestError

import stripe


class Facade(object):
    def __init__(self):
        stripe.api_key = settings.STRIPE_SECRET_KEY

    @staticmethod
    def get_friendly_decline_message(error):
        return 'La transaccíon ha sido rechazada por tu banco - Revisa tus datos bancarios y vuelve a intentarlo'

    @staticmethod
    def get_friendly_error_message(error):
        return 'Ha ocurrido un error con la plataforma de pagos.'

    def charge(self,
        order_number,
        total,
        card,
        currency=settings.STRIPE_CURRENCY,
        description=None,
        metadata=None,
        **kwargs):
        try:
            return stripe.Charge.create(
                amount=(total.incl_tax * 100).to_integral_value(),
                currency=currency,
                card=card,
                description=description,
                metadata=(metadata or {'order_number': order_number}),
                **kwargs).id
        except stripe.error.CardError:
            raise UnableToTakePayment(self.get_friendly_decline_message)
        except stripe.error.StripeError:
            raise InvalidGatewayRequestError(self.get_friendly_error_message)
