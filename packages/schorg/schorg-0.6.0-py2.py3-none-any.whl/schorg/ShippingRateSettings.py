"""
A ShippingRateSettings represents re-usable pieces of shipping information. It is designed for publication on an URL that may be referenced via the [[shippingSettingsLink]] property of an [[OfferShippingDetails]]. Several occurrences can be published, distinguished and matched (i.e. identified/referenced) by their different values for [[shippingLabel]].

https://schema.org/ShippingRateSettings
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class ShippingRateSettingsInheritedProperties(TypedDict):
    """A ShippingRateSettings represents re-usable pieces of shipping information. It is designed for publication on an URL that may be referenced via the [[shippingSettingsLink]] property of an [[OfferShippingDetails]]. Several occurrences can be published, distinguished and matched (i.e. identified/referenced) by their different values for [[shippingLabel]].

    References:
        https://schema.org/ShippingRateSettings
    Note:
        Model Depth 4
    Attributes:
    """

    


class ShippingRateSettingsProperties(TypedDict):
    """A ShippingRateSettings represents re-usable pieces of shipping information. It is designed for publication on an URL that may be referenced via the [[shippingSettingsLink]] property of an [[OfferShippingDetails]]. Several occurrences can be published, distinguished and matched (i.e. identified/referenced) by their different values for [[shippingLabel]].

    References:
        https://schema.org/ShippingRateSettings
    Note:
        Model Depth 4
    Attributes:
        shippingDestination: (Optional[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]): indicates (possibly multiple) shipping destinations. These can be defined in several ways, e.g. postalCode ranges.
        shippingLabel: (Optional[Union[List[Union[str, SchemaOrgObj]], str, SchemaOrgObj]]): Label to match an [[OfferShippingDetails]] with a [[ShippingRateSettings]] (within the context of a [[shippingSettingsLink]] cross-reference).
        doesNotShip: (Optional[Union[List[Union[StrictBool, SchemaOrgObj, str]], StrictBool, SchemaOrgObj, str]]): Indicates when shipping to a particular [[shippingDestination]] is not available.
        freeShippingThreshold: (Optional[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]): A monetary value above (or at) which the shipping rate becomes free. Intended to be used via an [[OfferShippingDetails]] with [[shippingSettingsLink]] matching this [[ShippingRateSettings]].
        shippingRate: (Optional[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]): The shipping rate is the cost of shipping to the specified destination. Typically, the maxValue and currency values (of the [[MonetaryAmount]]) are most appropriate.
        isUnlabelledFallback: (Optional[Union[List[Union[StrictBool, SchemaOrgObj, str]], StrictBool, SchemaOrgObj, str]]): This can be marked 'true' to indicate that some published [[DeliveryTimeSettings]] or [[ShippingRateSettings]] are intended to apply to all [[OfferShippingDetails]] published by the same merchant, when referenced by a [[shippingSettingsLink]] in those settings. It is not meaningful to use a 'true' value for this property alongside a transitTimeLabel (for [[DeliveryTimeSettings]]) or shippingLabel (for [[ShippingRateSettings]]), since this property is for use with unlabelled settings.
    """

    shippingDestination: NotRequired[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]
    shippingLabel: NotRequired[Union[List[Union[str, SchemaOrgObj]], str, SchemaOrgObj]]
    doesNotShip: NotRequired[Union[List[Union[StrictBool, SchemaOrgObj, str]], StrictBool, SchemaOrgObj, str]]
    freeShippingThreshold: NotRequired[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]
    shippingRate: NotRequired[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]
    isUnlabelledFallback: NotRequired[Union[List[Union[StrictBool, SchemaOrgObj, str]], StrictBool, SchemaOrgObj, str]]
    

#ShippingRateSettingsInheritedPropertiesTd = ShippingRateSettingsInheritedProperties()
#ShippingRateSettingsPropertiesTd = ShippingRateSettingsProperties()


class AllProperties(ShippingRateSettingsInheritedProperties , ShippingRateSettingsProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[ShippingRateSettingsProperties, ShippingRateSettingsInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "ShippingRateSettings"
    return model
    

ShippingRateSettings = create_schema_org_model()