"""
Nonprofit501c18: Non-profit type referring to Employee Funded Pension Trust (created before 25 June 1959).

https://schema.org/Nonprofit501c18
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class Nonprofit501c18InheritedProperties(TypedDict):
    """Nonprofit501c18: Non-profit type referring to Employee Funded Pension Trust (created before 25 June 1959).

    References:
        https://schema.org/Nonprofit501c18
    Note:
        Model Depth 6
    Attributes:
    """

    


class Nonprofit501c18Properties(TypedDict):
    """Nonprofit501c18: Non-profit type referring to Employee Funded Pension Trust (created before 25 June 1959).

    References:
        https://schema.org/Nonprofit501c18
    Note:
        Model Depth 6
    Attributes:
    """

    

#Nonprofit501c18InheritedPropertiesTd = Nonprofit501c18InheritedProperties()
#Nonprofit501c18PropertiesTd = Nonprofit501c18Properties()


class AllProperties(Nonprofit501c18InheritedProperties , Nonprofit501c18Properties, TypedDict):
    pass


def create_schema_org_model(type_: Union[Nonprofit501c18Properties, Nonprofit501c18InheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "Nonprofit501c18"
    return model
    

Nonprofit501c18 = create_schema_org_model()