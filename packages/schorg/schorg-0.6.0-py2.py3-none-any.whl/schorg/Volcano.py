"""
A volcano, like Fujisan.

https://schema.org/Volcano
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class VolcanoInheritedProperties(TypedDict):
    """A volcano, like Fujisan.

    References:
        https://schema.org/Volcano
    Note:
        Model Depth 4
    Attributes:
    """

    


class VolcanoProperties(TypedDict):
    """A volcano, like Fujisan.

    References:
        https://schema.org/Volcano
    Note:
        Model Depth 4
    Attributes:
    """

    

#VolcanoInheritedPropertiesTd = VolcanoInheritedProperties()
#VolcanoPropertiesTd = VolcanoProperties()


class AllProperties(VolcanoInheritedProperties , VolcanoProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[VolcanoProperties, VolcanoInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "Volcano"
    return model
    

Volcano = create_schema_org_model()