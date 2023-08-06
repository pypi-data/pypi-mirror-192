"""
Nonprofit501c1: Non-profit type referring to Corporations Organized Under Act of Congress, including Federal Credit Unions and National Farm Loan Associations.

https://schema.org/Nonprofit501c1
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class Nonprofit501c1InheritedProperties(TypedDict):
    """Nonprofit501c1: Non-profit type referring to Corporations Organized Under Act of Congress, including Federal Credit Unions and National Farm Loan Associations.

    References:
        https://schema.org/Nonprofit501c1
    Note:
        Model Depth 6
    Attributes:
    """

    


class Nonprofit501c1Properties(TypedDict):
    """Nonprofit501c1: Non-profit type referring to Corporations Organized Under Act of Congress, including Federal Credit Unions and National Farm Loan Associations.

    References:
        https://schema.org/Nonprofit501c1
    Note:
        Model Depth 6
    Attributes:
    """

    

#Nonprofit501c1InheritedPropertiesTd = Nonprofit501c1InheritedProperties()
#Nonprofit501c1PropertiesTd = Nonprofit501c1Properties()


class AllProperties(Nonprofit501c1InheritedProperties , Nonprofit501c1Properties, TypedDict):
    pass


def create_schema_org_model(type_: Union[Nonprofit501c1Properties, Nonprofit501c1InheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "Nonprofit501c1"
    return model
    

Nonprofit501c1 = create_schema_org_model()