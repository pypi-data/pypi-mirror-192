"""
A seasonal override of a return policy, for example used for holidays.

https://schema.org/MerchantReturnPolicySeasonalOverride
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class MerchantReturnPolicySeasonalOverrideInheritedProperties(TypedDict):
    """A seasonal override of a return policy, for example used for holidays.

    References:
        https://schema.org/MerchantReturnPolicySeasonalOverride
    Note:
        Model Depth 3
    Attributes:
    """

    


class MerchantReturnPolicySeasonalOverrideProperties(TypedDict):
    """A seasonal override of a return policy, for example used for holidays.

    References:
        https://schema.org/MerchantReturnPolicySeasonalOverride
    Note:
        Model Depth 3
    Attributes:
        returnPolicyCategory: (Optional[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]): Specifies an applicable return policy (from an enumeration).
        merchantReturnDays: (Optional[Union[List[Union[datetime, str, SchemaOrgObj, int, date]], datetime, str, SchemaOrgObj, int, date]]): Specifies either a fixed return date or the number of days (from the delivery date) that a product can be returned. Used when the [[returnPolicyCategory]] property is specified as [[MerchantReturnFiniteReturnWindow]].
        startDate: (Optional[Union[List[Union[datetime, SchemaOrgObj, str, date]], datetime, SchemaOrgObj, str, date]]): The start date and time of the item (in [ISO 8601 date format](http://en.wikipedia.org/wiki/ISO_8601)).
        endDate: (Optional[Union[List[Union[datetime, SchemaOrgObj, str, date]], datetime, SchemaOrgObj, str, date]]): The end date and time of the item (in [ISO 8601 date format](http://en.wikipedia.org/wiki/ISO_8601)).
    """

    returnPolicyCategory: NotRequired[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]
    merchantReturnDays: NotRequired[Union[List[Union[datetime, str, SchemaOrgObj, int, date]], datetime, str, SchemaOrgObj, int, date]]
    startDate: NotRequired[Union[List[Union[datetime, SchemaOrgObj, str, date]], datetime, SchemaOrgObj, str, date]]
    endDate: NotRequired[Union[List[Union[datetime, SchemaOrgObj, str, date]], datetime, SchemaOrgObj, str, date]]
    

#MerchantReturnPolicySeasonalOverrideInheritedPropertiesTd = MerchantReturnPolicySeasonalOverrideInheritedProperties()
#MerchantReturnPolicySeasonalOverridePropertiesTd = MerchantReturnPolicySeasonalOverrideProperties()


class AllProperties(MerchantReturnPolicySeasonalOverrideInheritedProperties , MerchantReturnPolicySeasonalOverrideProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[MerchantReturnPolicySeasonalOverrideProperties, MerchantReturnPolicySeasonalOverrideInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "MerchantReturnPolicySeasonalOverride"
    return model
    

MerchantReturnPolicySeasonalOverride = create_schema_org_model()