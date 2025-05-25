from enum import Enum

class IntentCategoryEnum(str, Enum):
   DINING = "dining"
   TRAVEL = "travel"
   GIFTING = "gifting"
   CAB_BOOKING = "cab booking"
   OTHER = "other"

class CuisineTypeEnum(str, Enum):
    """Common cuisine types"""
    ITALIAN = "italian"
    CHINESE = "chinese"
    INDIAN = "indian"
    MEXICAN = "mexican"
    JAPANESE = "japanese"
    THAI = "thai"
    FRENCH = "french"
    AMERICAN = "american"
    MEDITERRANEAN = "mediterranean"
    VEGETARIAN = "vegetarian"
    VEGAN = "vegan"
    GLUTEN_FREE = "gluten_free"

class ModeOfTransportEnum(str, Enum):
    FLIGHT = "flight"
    TRAIN = "train"
    BUS = "bus"
    CAR = "car"
    BIKE = "bike"
    SHIP = "ship"
    TAXI = "taxi"


class GiftTypeEnum(str, Enum):
    FLOWERS = "flowers"
    CHOCOLATES = "chocolates"
    GADGETS = "gadgets"
    BOOKS = "books"
    CLOTHING = "clothing"
    JEWELRY = "jewelry"
    PERFUMES = "perfumes"
    TOYS = "toys"
    GIFT_CARD = "gift_card"
    HOME_DECOR = "home_decor"
    PERSONALIZED = "personalized"
    EXPERIENCES = "experiences"


class CabTypeEnum(str, Enum):
    STANDARD = "standard"
    SUV = "suv"
    LUXURY = "luxury"
    MINI = "mini"
    SEDAN = "sedan"
    ELECTRIC = "electric"
    SHARED = "shared"