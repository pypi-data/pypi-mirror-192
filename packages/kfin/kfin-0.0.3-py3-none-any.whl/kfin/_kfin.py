from enum import Enum
from kfin.koreaexim.exchange_rate import *


class Currency(Enum):
    AED = "AED"
    AUD = "AUD"
    BHD = "BHD"
    BND = "BND"
    CAD = "CAD"
    CHF = "CHF"
    CNY = "CNH"
    DKK = "DKK"
    EUR = "EUR"
    GBP = "GBP"
    HKD = "HKD"
    IDR = "IDR(100)"
    JPY = "JPY(100)"
    KRW = "KRW"
    KWD = "KWD"
    MYR = "MYR"
    NOK = "NOK"
    NZD = "NZD"
    SAR = "SAR"
    SEK = "SEK"
    SGD = "SGD"
    THB = "THB"
    USD = "USD"


def get_exchange_rate(cur_unit):
    return [item for item in get_exchange_rates() if item.cur_unit == cur_unit.value]
