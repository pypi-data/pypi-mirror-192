"""
Physical activity that is of high-intensity which utilizes the anaerobic metabolism of the body.

https://schema.org/AnaerobicActivity
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class AnaerobicActivityInheritedProperties(TypedDict):
    """Physical activity that is of high-intensity which utilizes the anaerobic metabolism of the body.

    References:
        https://schema.org/AnaerobicActivity
    Note:
        Model Depth 5
    Attributes:
    """

    


class AnaerobicActivityProperties(TypedDict):
    """Physical activity that is of high-intensity which utilizes the anaerobic metabolism of the body.

    References:
        https://schema.org/AnaerobicActivity
    Note:
        Model Depth 5
    Attributes:
    """

    

#AnaerobicActivityInheritedPropertiesTd = AnaerobicActivityInheritedProperties()
#AnaerobicActivityPropertiesTd = AnaerobicActivityProperties()


class AllProperties(AnaerobicActivityInheritedProperties , AnaerobicActivityProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[AnaerobicActivityProperties, AnaerobicActivityInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "AnaerobicActivity"
    return model
    

AnaerobicActivity = create_schema_org_model()