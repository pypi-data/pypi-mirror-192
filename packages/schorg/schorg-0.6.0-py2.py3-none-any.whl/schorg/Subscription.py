"""
Represents the subscription pricing component of the total price for an offered product.

https://schema.org/Subscription
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class SubscriptionInheritedProperties(TypedDict):
    """Represents the subscription pricing component of the total price for an offered product.

    References:
        https://schema.org/Subscription
    Note:
        Model Depth 5
    Attributes:
    """

    


class SubscriptionProperties(TypedDict):
    """Represents the subscription pricing component of the total price for an offered product.

    References:
        https://schema.org/Subscription
    Note:
        Model Depth 5
    Attributes:
    """

    

#SubscriptionInheritedPropertiesTd = SubscriptionInheritedProperties()
#SubscriptionPropertiesTd = SubscriptionProperties()


class AllProperties(SubscriptionInheritedProperties , SubscriptionProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[SubscriptionProperties, SubscriptionInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "Subscription"
    return model
    

Subscription = create_schema_org_model()