"""
Nonprofit501c25: Non-profit type referring to Real Property Title-Holding Corporations or Trusts with Multiple Parents.

https://schema.org/Nonprofit501c25
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class Nonprofit501c25InheritedProperties(TypedDict):
    """Nonprofit501c25: Non-profit type referring to Real Property Title-Holding Corporations or Trusts with Multiple Parents.

    References:
        https://schema.org/Nonprofit501c25
    Note:
        Model Depth 6
    Attributes:
    """

    


class Nonprofit501c25Properties(TypedDict):
    """Nonprofit501c25: Non-profit type referring to Real Property Title-Holding Corporations or Trusts with Multiple Parents.

    References:
        https://schema.org/Nonprofit501c25
    Note:
        Model Depth 6
    Attributes:
    """

    

#Nonprofit501c25InheritedPropertiesTd = Nonprofit501c25InheritedProperties()
#Nonprofit501c25PropertiesTd = Nonprofit501c25Properties()


class AllProperties(Nonprofit501c25InheritedProperties , Nonprofit501c25Properties, TypedDict):
    pass


def create_schema_org_model(type_: Union[Nonprofit501c25Properties, Nonprofit501c25InheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "Nonprofit501c25"
    return model
    

Nonprofit501c25 = create_schema_org_model()