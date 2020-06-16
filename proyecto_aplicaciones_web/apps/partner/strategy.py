from collections import namedtuple
from decimal import Decimal as D

from oscar.core.loading import get_class
from oscar.apps.partner import strategy, prices

Unavailable = get_class('partner.availability', 'Unavailable')
Available = get_class('partner.availability', 'Available')
StockRequiredAvailability = get_class('partner.availability', 'StockRequired')
UnavailablePrice = get_class('partner.prices', 'Unavailable')
FixedPrice = get_class('partner.prices', 'FixedPrice')
TaxInclusiveFixedPrice = get_class('partner.prices', 'TaxInclusiveFixedPrice')

# A container for policies
PurchaseInfo = namedtuple(
    'PurchaseInfo', ['price', 'availability', 'stockrecord'])


class Selector(object):


    def strategy(self, request=None, user=None, **kwargs):
        """
        Return an instantiated strategy instance
        """
        # Default to the backwards-compatible strategy of picking the first
        # stockrecord but charging zero tax.
        return ESStrategy()

class IncludingVAT(strategy.FixedRateTax):
    """
    Price policy to charge VAT on the base price
    """
    rate = D('0.21')


class ESStrategy(strategy.UseFirstStockRecord, IncludingVAT,
                 strategy.StockRequired, strategy.Structured):

