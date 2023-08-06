"""
An action that failed to complete. The action's error property and the HTTP return code contain more information about the failure.

https://schema.org/FailedActionStatus
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class FailedActionStatusInheritedProperties(TypedDict):
    """An action that failed to complete. The action's error property and the HTTP return code contain more information about the failure.

    References:
        https://schema.org/FailedActionStatus
    Note:
        Model Depth 6
    Attributes:
    """

    


class FailedActionStatusProperties(TypedDict):
    """An action that failed to complete. The action's error property and the HTTP return code contain more information about the failure.

    References:
        https://schema.org/FailedActionStatus
    Note:
        Model Depth 6
    Attributes:
    """

    

#FailedActionStatusInheritedPropertiesTd = FailedActionStatusInheritedProperties()
#FailedActionStatusPropertiesTd = FailedActionStatusProperties()


class AllProperties(FailedActionStatusInheritedProperties , FailedActionStatusProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[FailedActionStatusProperties, FailedActionStatusInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "FailedActionStatus"
    return model
    

FailedActionStatus = create_schema_org_model()