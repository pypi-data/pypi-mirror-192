"""
UnincorporatedAssociationCharity: Non-profit type referring to a charitable company that is not incorporated (UK).

https://schema.org/UnincorporatedAssociationCharity
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class UnincorporatedAssociationCharityInheritedProperties(TypedDict):
    """UnincorporatedAssociationCharity: Non-profit type referring to a charitable company that is not incorporated (UK).

    References:
        https://schema.org/UnincorporatedAssociationCharity
    Note:
        Model Depth 6
    Attributes:
    """

    


class UnincorporatedAssociationCharityProperties(TypedDict):
    """UnincorporatedAssociationCharity: Non-profit type referring to a charitable company that is not incorporated (UK).

    References:
        https://schema.org/UnincorporatedAssociationCharity
    Note:
        Model Depth 6
    Attributes:
    """

    

#UnincorporatedAssociationCharityInheritedPropertiesTd = UnincorporatedAssociationCharityInheritedProperties()
#UnincorporatedAssociationCharityPropertiesTd = UnincorporatedAssociationCharityProperties()


class AllProperties(UnincorporatedAssociationCharityInheritedProperties , UnincorporatedAssociationCharityProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[UnincorporatedAssociationCharityProperties, UnincorporatedAssociationCharityInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "UnincorporatedAssociationCharity"
    return model
    

UnincorporatedAssociationCharity = create_schema_org_model()