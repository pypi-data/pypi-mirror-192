"""
Completed.

https://schema.org/Completed
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class CompletedInheritedProperties(TypedDict):
    """Completed.

    References:
        https://schema.org/Completed
    Note:
        Model Depth 6
    Attributes:
    """

    


class CompletedProperties(TypedDict):
    """Completed.

    References:
        https://schema.org/Completed
    Note:
        Model Depth 6
    Attributes:
    """

    

#CompletedInheritedPropertiesTd = CompletedInheritedProperties()
#CompletedPropertiesTd = CompletedProperties()


class AllProperties(CompletedInheritedProperties , CompletedProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[CompletedProperties, CompletedInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "Completed"
    return model
    

Completed = create_schema_org_model()