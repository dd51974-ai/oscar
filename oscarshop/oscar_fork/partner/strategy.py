from decimal import Decimal as D
from oscar.apps.partner import strategy

class Selector(object):
    def strategy(self, request=None, user=None, **kwargs):
        return JPStrategy()

class JP(strategy.FixedRateTax):
    rate = D('0.10')
    exponent = D('1.')

    def pricing_policy(self, product, stockrecord):
        if not stockrecord:
            return prices.Unavailable()
        rate = self.get_rate(product, stockrecord)
        exponent = self.get_exponent(stockrecord)
        tax = (stockrecord.price_excl_tax * rate).quantize(
            exponent, rounding=ROUND_DOWN)
        return prices.TaxInclusiveFixedPrice(
            currency=stockrecord.price_currency,
            excl_tax=stockrecord.price_excl_tax,
            tax=tax)

    def parent_pricing_policy(self, product, children_stock):
        stockrecords = [x[1] for x in children_stock if x[1] is not None]
        if not stockrecords:
            return prices.Unavailable()

        # We take price from first record
        stockrecord = stockrecords[0]
        rate = self.get_rate(product, stockrecord)
        exponent = self.get_exponent(stockrecord)
        tax = (stockrecord.price_excl_tax * rate).quantize(
            exponent, rounding=ROUND_DOWN)

        return prices.FixedPrice(
            currency=stockrecord.price_currency,
            excl_tax=stockrecord.price_excl_tax,
            tax=tax)

class JPStrategy(strategy.UseFirstStockRecord, strategy.StockRequired,
                 JP, strategy.Structured):
    pass
