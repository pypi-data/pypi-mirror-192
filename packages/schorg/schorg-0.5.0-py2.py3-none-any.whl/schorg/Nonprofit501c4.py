"""
Nonprofit501c4: Non-profit type referring to Civic Leagues, Social Welfare Organizations, and Local Associations of Employees.

https://schema.org/Nonprofit501c4
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class Nonprofit501c4InheritedProperties(TypedDict):
    """Nonprofit501c4: Non-profit type referring to Civic Leagues, Social Welfare Organizations, and Local Associations of Employees.

    References:
        https://schema.org/Nonprofit501c4
    Note:
        Model Depth 6
    Attributes:
    """

    


class Nonprofit501c4Properties(TypedDict):
    """Nonprofit501c4: Non-profit type referring to Civic Leagues, Social Welfare Organizations, and Local Associations of Employees.

    References:
        https://schema.org/Nonprofit501c4
    Note:
        Model Depth 6
    Attributes:
    """

    

#Nonprofit501c4InheritedPropertiesTd = Nonprofit501c4InheritedProperties()
#Nonprofit501c4PropertiesTd = Nonprofit501c4Properties()


class AllProperties(Nonprofit501c4InheritedProperties , Nonprofit501c4Properties, TypedDict):
    pass


def create_schema_org_model(type_: Union[Nonprofit501c4Properties, Nonprofit501c4InheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "Nonprofit501c4"
    return model
    

Nonprofit501c4 = create_schema_org_model()