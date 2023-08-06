"""
Permission to read or view the document.

https://schema.org/ReadPermission
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class ReadPermissionInheritedProperties(TypedDict):
    """Permission to read or view the document.

    References:
        https://schema.org/ReadPermission
    Note:
        Model Depth 5
    Attributes:
    """

    


class ReadPermissionProperties(TypedDict):
    """Permission to read or view the document.

    References:
        https://schema.org/ReadPermission
    Note:
        Model Depth 5
    Attributes:
    """

    

#ReadPermissionInheritedPropertiesTd = ReadPermissionInheritedProperties()
#ReadPermissionPropertiesTd = ReadPermissionProperties()


class AllProperties(ReadPermissionInheritedProperties , ReadPermissionProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[ReadPermissionProperties, ReadPermissionInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "ReadPermission"
    return model
    

ReadPermission = create_schema_org_model()