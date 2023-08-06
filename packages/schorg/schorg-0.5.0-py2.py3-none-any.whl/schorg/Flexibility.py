"""
Physical activity that is engaged in to improve joint and muscle flexibility.

https://schema.org/Flexibility
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class FlexibilityInheritedProperties(TypedDict):
    """Physical activity that is engaged in to improve joint and muscle flexibility.

    References:
        https://schema.org/Flexibility
    Note:
        Model Depth 5
    Attributes:
    """

    


class FlexibilityProperties(TypedDict):
    """Physical activity that is engaged in to improve joint and muscle flexibility.

    References:
        https://schema.org/Flexibility
    Note:
        Model Depth 5
    Attributes:
    """

    

#FlexibilityInheritedPropertiesTd = FlexibilityInheritedProperties()
#FlexibilityPropertiesTd = FlexibilityProperties()


class AllProperties(FlexibilityInheritedProperties , FlexibilityProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[FlexibilityProperties, FlexibilityInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "Flexibility"
    return model
    

Flexibility = create_schema_org_model()