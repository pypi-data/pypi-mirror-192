"""
Permission to write or edit the document.

https://schema.org/WritePermission
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class WritePermissionInheritedProperties(TypedDict):
    """Permission to write or edit the document.

    References:
        https://schema.org/WritePermission
    Note:
        Model Depth 5
    Attributes:
    """

    


class WritePermissionProperties(TypedDict):
    """Permission to write or edit the document.

    References:
        https://schema.org/WritePermission
    Note:
        Model Depth 5
    Attributes:
    """

    

#WritePermissionInheritedPropertiesTd = WritePermissionInheritedProperties()
#WritePermissionPropertiesTd = WritePermissionProperties()


class AllProperties(WritePermissionInheritedProperties , WritePermissionProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[WritePermissionProperties, WritePermissionInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "WritePermission"
    return model
    

WritePermission = create_schema_org_model()