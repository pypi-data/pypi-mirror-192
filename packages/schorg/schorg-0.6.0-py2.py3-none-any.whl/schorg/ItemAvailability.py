"""
A list of possible product availability options.

https://schema.org/ItemAvailability
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class ItemAvailabilityInheritedProperties(TypedDict):
    """A list of possible product availability options.

    References:
        https://schema.org/ItemAvailability
    Note:
        Model Depth 4
    Attributes:
        supersededBy: (Optional[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]): Relates a term (i.e. a property, class or enumeration) to one that supersedes it.
    """

    supersededBy: NotRequired[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]
    


class ItemAvailabilityProperties(TypedDict):
    """A list of possible product availability options.

    References:
        https://schema.org/ItemAvailability
    Note:
        Model Depth 4
    Attributes:
    """

    

#ItemAvailabilityInheritedPropertiesTd = ItemAvailabilityInheritedProperties()
#ItemAvailabilityPropertiesTd = ItemAvailabilityProperties()


class AllProperties(ItemAvailabilityInheritedProperties , ItemAvailabilityProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[ItemAvailabilityProperties, ItemAvailabilityInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "ItemAvailability"
    return model
    

ItemAvailability = create_schema_org_model()