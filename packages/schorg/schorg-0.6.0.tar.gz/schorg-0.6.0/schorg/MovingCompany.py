"""
A moving company.

https://schema.org/MovingCompany
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class MovingCompanyInheritedProperties(TypedDict):
    """A moving company.

    References:
        https://schema.org/MovingCompany
    Note:
        Model Depth 5
    Attributes:
    """

    


class MovingCompanyProperties(TypedDict):
    """A moving company.

    References:
        https://schema.org/MovingCompany
    Note:
        Model Depth 5
    Attributes:
    """

    

#MovingCompanyInheritedPropertiesTd = MovingCompanyInheritedProperties()
#MovingCompanyPropertiesTd = MovingCompanyProperties()


class AllProperties(MovingCompanyInheritedProperties , MovingCompanyProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[MovingCompanyProperties, MovingCompanyInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "MovingCompany"
    return model
    

MovingCompany = create_schema_org_model()