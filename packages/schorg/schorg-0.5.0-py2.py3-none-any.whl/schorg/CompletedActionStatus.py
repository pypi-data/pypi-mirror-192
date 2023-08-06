"""
An action that has already taken place.

https://schema.org/CompletedActionStatus
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class CompletedActionStatusInheritedProperties(TypedDict):
    """An action that has already taken place.

    References:
        https://schema.org/CompletedActionStatus
    Note:
        Model Depth 6
    Attributes:
    """

    


class CompletedActionStatusProperties(TypedDict):
    """An action that has already taken place.

    References:
        https://schema.org/CompletedActionStatus
    Note:
        Model Depth 6
    Attributes:
    """

    

#CompletedActionStatusInheritedPropertiesTd = CompletedActionStatusInheritedProperties()
#CompletedActionStatusPropertiesTd = CompletedActionStatusProperties()


class AllProperties(CompletedActionStatusInheritedProperties , CompletedActionStatusProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[CompletedActionStatusProperties, CompletedActionStatusInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "CompletedActionStatus"
    return model
    

CompletedActionStatus = create_schema_org_model()