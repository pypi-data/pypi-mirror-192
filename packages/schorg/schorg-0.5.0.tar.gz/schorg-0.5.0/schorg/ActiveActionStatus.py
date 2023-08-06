"""
An in-progress action (e.g., while watching the movie, or driving to a location).

https://schema.org/ActiveActionStatus
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class ActiveActionStatusInheritedProperties(TypedDict):
    """An in-progress action (e.g., while watching the movie, or driving to a location).

    References:
        https://schema.org/ActiveActionStatus
    Note:
        Model Depth 6
    Attributes:
    """

    


class ActiveActionStatusProperties(TypedDict):
    """An in-progress action (e.g., while watching the movie, or driving to a location).

    References:
        https://schema.org/ActiveActionStatus
    Note:
        Model Depth 6
    Attributes:
    """

    

#ActiveActionStatusInheritedPropertiesTd = ActiveActionStatusInheritedProperties()
#ActiveActionStatusPropertiesTd = ActiveActionStatusProperties()


class AllProperties(ActiveActionStatusInheritedProperties , ActiveActionStatusProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[ActiveActionStatusProperties, ActiveActionStatusInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "ActiveActionStatus"
    return model
    

ActiveActionStatus = create_schema_org_model()