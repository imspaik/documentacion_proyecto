from decimal import Decimal as D

from oscar.apps.shipping.methods import Free, FixedPrice
from oscar.apps.shipping.repository import Repository as CoreRepository


class Repository(CoreRepository):
    """
    This class is included so that there is a choice of shipping methods.
    Oscar's default behaviour is to only have one which means you can't test
    the shipping features of PayPal.
    """
    methods = [Free(), FixedPrice(D('5.00'), D('5.00'))]

class Free(Base):
    """
    This shipping method specifies that shipping is free.
    """
    code = 'free-shipping'
    name = _('Envío gratuito')
    description = 'Entrega en 2-5 días hábiles'

    def calculate(self, basket):
        # If the charge is free then tax must be free (musn't it?) and so we
        # immediately set the tax to zero
        return prices.Price(
            currency=basket.currency,
            excl_tax=D('0.00'), tax=D('0.00'))


class NoShippingRequired(Free):
    """
    This is a special shipping method that indicates that no shipping is
    actually required (e.g. for digital goods).
    """
    code = 'no-shipping-required'
    name = _('No shipping required')
    


class FixedPrice(Base):
    """
    This shipping method indicates that shipping costs a fixed price and
    requires no special calculation.
    """
    code = 'fixed-price-shipping'
    name = _('Envío urgente')
    description = 'Entrega en 1-2 días hábiles'

    # Charges can be either declared by subclassing and overriding the
    # class attributes or by passing them to the constructor
    charge_excl_tax = None
    charge_incl_tax = None

    def __init__(self, charge_excl_tax=None, charge_incl_tax=None):
        if charge_excl_tax is not None:
            self.charge_excl_tax = charge_excl_tax
        if charge_incl_tax is not None:
            self.charge_incl_tax = charge_incl_tax

    def calculate(self, basket):
        return prices.Price(
            currency=basket.currency,
            excl_tax=self.charge_excl_tax,
            incl_tax=self.charge_incl_tax)
