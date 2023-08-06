"""
Nonprofit501c20: Non-profit type referring to Group Legal Services Plan Organizations.

https://schema.org/Nonprofit501c20
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class Nonprofit501c20InheritedProperties(TypedDict):
    """Nonprofit501c20: Non-profit type referring to Group Legal Services Plan Organizations.

    References:
        https://schema.org/Nonprofit501c20
    Note:
        Model Depth 6
    Attributes:
    """

    


class Nonprofit501c20Properties(TypedDict):
    """Nonprofit501c20: Non-profit type referring to Group Legal Services Plan Organizations.

    References:
        https://schema.org/Nonprofit501c20
    Note:
        Model Depth 6
    Attributes:
    """

    

#Nonprofit501c20InheritedPropertiesTd = Nonprofit501c20InheritedProperties()
#Nonprofit501c20PropertiesTd = Nonprofit501c20Properties()


class AllProperties(Nonprofit501c20InheritedProperties , Nonprofit501c20Properties, TypedDict):
    pass


def create_schema_org_model(type_: Union[Nonprofit501c20Properties, Nonprofit501c20InheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "Nonprofit501c20"
    return model
    

Nonprofit501c20 = create_schema_org_model()