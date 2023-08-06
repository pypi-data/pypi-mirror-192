"""
A dentist.

https://schema.org/Dentist
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class DentistInheritedProperties(TypedDict):
    """A dentist.

    References:
        https://schema.org/Dentist
    Note:
        Model Depth 4
    Attributes:
        healthPlanNetworkId: (Optional[Union[List[Union[str, SchemaOrgObj]], str, SchemaOrgObj]]): Name or unique ID of network. (Networks are often reused across different insurance plans.)
        medicalSpecialty: (Optional[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]): A medical specialty of the provider.
        isAcceptingNewPatients: (Optional[Union[List[Union[StrictBool, SchemaOrgObj, str]], StrictBool, SchemaOrgObj, str]]): Whether the provider is accepting new patients.
        priceRange: (Optional[Union[List[Union[str, SchemaOrgObj]], str, SchemaOrgObj]]): The price range of the business, for example ```$$$```.
        currenciesAccepted: (Optional[Union[List[Union[str, SchemaOrgObj]], str, SchemaOrgObj]]): The currency accepted.Use standard formats: [ISO 4217 currency format](http://en.wikipedia.org/wiki/ISO_4217), e.g. "USD"; [Ticker symbol](https://en.wikipedia.org/wiki/List_of_cryptocurrencies) for cryptocurrencies, e.g. "BTC"; well known names for [Local Exchange Trading Systems](https://en.wikipedia.org/wiki/Local_exchange_trading_system) (LETS) and other currency types, e.g. "Ithaca HOUR".
        branchOf: (Optional[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]): The larger organization that this local business is a branch of, if any. Not to be confused with (anatomical) [[branch]].
        paymentAccepted: (Optional[Union[List[Union[str, SchemaOrgObj]], str, SchemaOrgObj]]): Cash, Credit Card, Cryptocurrency, Local Exchange Tradings System, etc.
        openingHours: (Optional[Union[List[Union[str, SchemaOrgObj]], str, SchemaOrgObj]]): The general opening hours for a business. Opening hours can be specified as a weekly time range, starting with days, then times per day. Multiple days can be listed with commas ',' separating each day. Day or time ranges are specified using a hyphen '-'.* Days are specified using the following two-letter combinations: ```Mo```, ```Tu```, ```We```, ```Th```, ```Fr```, ```Sa```, ```Su```.* Times are specified using 24:00 format. For example, 3pm is specified as ```15:00```, 10am as ```10:00```. * Here is an example: <code>&lt;time itemprop="openingHours" datetime=&quot;Tu,Th 16:00-20:00&quot;&gt;Tuesdays and Thursdays 4-8pm&lt;/time&gt;</code>.* If a business is open 7 days a week, then it can be specified as <code>&lt;time itemprop=&quot;openingHours&quot; datetime=&quot;Mo-Su&quot;&gt;Monday through Sunday, all day&lt;/time&gt;</code>.
    """

    healthPlanNetworkId: NotRequired[Union[List[Union[str, SchemaOrgObj]], str, SchemaOrgObj]]
    medicalSpecialty: NotRequired[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]
    isAcceptingNewPatients: NotRequired[Union[List[Union[StrictBool, SchemaOrgObj, str]], StrictBool, SchemaOrgObj, str]]
    priceRange: NotRequired[Union[List[Union[str, SchemaOrgObj]], str, SchemaOrgObj]]
    currenciesAccepted: NotRequired[Union[List[Union[str, SchemaOrgObj]], str, SchemaOrgObj]]
    branchOf: NotRequired[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]
    paymentAccepted: NotRequired[Union[List[Union[str, SchemaOrgObj]], str, SchemaOrgObj]]
    openingHours: NotRequired[Union[List[Union[str, SchemaOrgObj]], str, SchemaOrgObj]]
    


class DentistProperties(TypedDict):
    """A dentist.

    References:
        https://schema.org/Dentist
    Note:
        Model Depth 4
    Attributes:
    """

    

#DentistInheritedPropertiesTd = DentistInheritedProperties()
#DentistPropertiesTd = DentistProperties()


class AllProperties(DentistInheritedProperties , DentistProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[DentistProperties, DentistInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "Dentist"
    return model
    

Dentist = create_schema_org_model()