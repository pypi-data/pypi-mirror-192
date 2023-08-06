"""
Nonprofit501c8: Non-profit type referring to Fraternal Beneficiary Societies and Associations.

https://schema.org/Nonprofit501c8
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class Nonprofit501c8InheritedProperties(TypedDict):
    """Nonprofit501c8: Non-profit type referring to Fraternal Beneficiary Societies and Associations.

    References:
        https://schema.org/Nonprofit501c8
    Note:
        Model Depth 6
    Attributes:
    """

    


class Nonprofit501c8Properties(TypedDict):
    """Nonprofit501c8: Non-profit type referring to Fraternal Beneficiary Societies and Associations.

    References:
        https://schema.org/Nonprofit501c8
    Note:
        Model Depth 6
    Attributes:
    """

    

#Nonprofit501c8InheritedPropertiesTd = Nonprofit501c8InheritedProperties()
#Nonprofit501c8PropertiesTd = Nonprofit501c8Properties()


class AllProperties(Nonprofit501c8InheritedProperties , Nonprofit501c8Properties, TypedDict):
    pass


def create_schema_org_model(type_: Union[Nonprofit501c8Properties, Nonprofit501c8InheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "Nonprofit501c8"
    return model
    

Nonprofit501c8 = create_schema_org_model()