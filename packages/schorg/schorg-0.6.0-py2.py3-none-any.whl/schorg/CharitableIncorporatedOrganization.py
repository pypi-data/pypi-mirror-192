"""
CharitableIncorporatedOrganization: Non-profit type referring to a Charitable Incorporated Organization (UK).

https://schema.org/CharitableIncorporatedOrganization
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class CharitableIncorporatedOrganizationInheritedProperties(TypedDict):
    """CharitableIncorporatedOrganization: Non-profit type referring to a Charitable Incorporated Organization (UK).

    References:
        https://schema.org/CharitableIncorporatedOrganization
    Note:
        Model Depth 6
    Attributes:
    """

    


class CharitableIncorporatedOrganizationProperties(TypedDict):
    """CharitableIncorporatedOrganization: Non-profit type referring to a Charitable Incorporated Organization (UK).

    References:
        https://schema.org/CharitableIncorporatedOrganization
    Note:
        Model Depth 6
    Attributes:
    """

    

#CharitableIncorporatedOrganizationInheritedPropertiesTd = CharitableIncorporatedOrganizationInheritedProperties()
#CharitableIncorporatedOrganizationPropertiesTd = CharitableIncorporatedOrganizationProperties()


class AllProperties(CharitableIncorporatedOrganizationInheritedProperties , CharitableIncorporatedOrganizationProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[CharitableIncorporatedOrganizationProperties, CharitableIncorporatedOrganizationInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "CharitableIncorporatedOrganization"
    return model
    

CharitableIncorporatedOrganization = create_schema_org_model()