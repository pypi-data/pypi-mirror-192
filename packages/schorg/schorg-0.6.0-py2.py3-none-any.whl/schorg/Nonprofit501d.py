"""
Nonprofit501d: Non-profit type referring to Religious and Apostolic Associations.

https://schema.org/Nonprofit501d
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class Nonprofit501dInheritedProperties(TypedDict):
    """Nonprofit501d: Non-profit type referring to Religious and Apostolic Associations.

    References:
        https://schema.org/Nonprofit501d
    Note:
        Model Depth 6
    Attributes:
    """

    


class Nonprofit501dProperties(TypedDict):
    """Nonprofit501d: Non-profit type referring to Religious and Apostolic Associations.

    References:
        https://schema.org/Nonprofit501d
    Note:
        Model Depth 6
    Attributes:
    """

    

#Nonprofit501dInheritedPropertiesTd = Nonprofit501dInheritedProperties()
#Nonprofit501dPropertiesTd = Nonprofit501dProperties()


class AllProperties(Nonprofit501dInheritedProperties , Nonprofit501dProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[Nonprofit501dProperties, Nonprofit501dInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "Nonprofit501d"
    return model
    

Nonprofit501d = create_schema_org_model()