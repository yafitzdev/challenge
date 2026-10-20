from ._common import JavaEnum


class Address:
    class Type(JavaEnum):
        CUSTOM = 0
        HOME = 1
        WORK = 2
        OTHER = 3
        UNKNOWN = 4

        @classmethod
        def from_value(cls, value):
            # ContactsContract.CommonDataKinds.StructuredPostal TYPE_* constants
            return cls._from_mapping({0: "CUSTOM", 1: "HOME", 2: "WORK", 3: "OTHER"}, value)

        fromValue = from_value

    def __init__(self, address, street, city, region, postcode, country, type_or_label):
        self._formatted_address = address
        self._street = street
        self._city = city
        self._region = region
        self._postcode = postcode
        self._country = country
        if isinstance(type_or_label, Address.Type):
            self._type = type_or_label
            self._label = None
        else:
            self._type = Address.Type.CUSTOM
            self._label = type_or_label

    def getFormattedAddress(self):
        return self._formatted_address

    def getType(self):
        return self._type

    def getStreet(self):
        return self._street

    def getCity(self):
        return self._city

    def getRegion(self):
        return self._region

    def getPostcode(self):
        return self._postcode

    def getCountry(self):
        return self._country

    def getLabel(self):
        return self._label
