"""
A list of possible statuses for the legal force of a legislation.

https://schema.org/LegalForceStatus
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class LegalForceStatusInheritedProperties(TypedDict):
    """A list of possible statuses for the legal force of a legislation.

    References:
        https://schema.org/LegalForceStatus
    Note:
        Model Depth 5
    Attributes:
    """

    


class LegalForceStatusProperties(TypedDict):
    """A list of possible statuses for the legal force of a legislation.

    References:
        https://schema.org/LegalForceStatus
    Note:
        Model Depth 5
    Attributes:
    """

    

#LegalForceStatusInheritedPropertiesTd = LegalForceStatusInheritedProperties()
#LegalForceStatusPropertiesTd = LegalForceStatusProperties()


class AllProperties(LegalForceStatusInheritedProperties , LegalForceStatusProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[LegalForceStatusProperties, LegalForceStatusInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "LegalForceStatus"
    return model
    

LegalForceStatus = create_schema_org_model()