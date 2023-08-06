"""
Permission to add comments to the document.

https://schema.org/CommentPermission
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class CommentPermissionInheritedProperties(TypedDict):
    """Permission to add comments to the document.

    References:
        https://schema.org/CommentPermission
    Note:
        Model Depth 5
    Attributes:
    """

    


class CommentPermissionProperties(TypedDict):
    """Permission to add comments to the document.

    References:
        https://schema.org/CommentPermission
    Note:
        Model Depth 5
    Attributes:
    """

    

#CommentPermissionInheritedPropertiesTd = CommentPermissionInheritedProperties()
#CommentPermissionPropertiesTd = CommentPermissionProperties()


class AllProperties(CommentPermissionInheritedProperties , CommentPermissionProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[CommentPermissionProperties, CommentPermissionInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "CommentPermission"
    return model
    

CommentPermission = create_schema_org_model()