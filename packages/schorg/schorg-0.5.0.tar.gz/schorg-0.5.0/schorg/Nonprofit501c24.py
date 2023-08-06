"""
Nonprofit501c24: Non-profit type referring to Section 4049 ERISA Trusts.

https://schema.org/Nonprofit501c24
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class Nonprofit501c24InheritedProperties(TypedDict):
    """Nonprofit501c24: Non-profit type referring to Section 4049 ERISA Trusts.

    References:
        https://schema.org/Nonprofit501c24
    Note:
        Model Depth 6
    Attributes:
    """

    


class Nonprofit501c24Properties(TypedDict):
    """Nonprofit501c24: Non-profit type referring to Section 4049 ERISA Trusts.

    References:
        https://schema.org/Nonprofit501c24
    Note:
        Model Depth 6
    Attributes:
    """

    

#Nonprofit501c24InheritedPropertiesTd = Nonprofit501c24InheritedProperties()
#Nonprofit501c24PropertiesTd = Nonprofit501c24Properties()


class AllProperties(Nonprofit501c24InheritedProperties , Nonprofit501c24Properties, TypedDict):
    pass


def create_schema_org_model(type_: Union[Nonprofit501c24Properties, Nonprofit501c24InheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "Nonprofit501c24"
    return model
    

Nonprofit501c24 = create_schema_org_model()