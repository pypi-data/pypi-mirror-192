"""
A permission for a particular person or group to access a particular file.

https://schema.org/DigitalDocumentPermission
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class DigitalDocumentPermissionInheritedProperties(TypedDict):
    """A permission for a particular person or group to access a particular file.

    References:
        https://schema.org/DigitalDocumentPermission
    Note:
        Model Depth 3
    Attributes:
    """

    


class DigitalDocumentPermissionProperties(TypedDict):
    """A permission for a particular person or group to access a particular file.

    References:
        https://schema.org/DigitalDocumentPermission
    Note:
        Model Depth 3
    Attributes:
        grantee: (Optional[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]): The person, organization, contact point, or audience that has been granted this permission.
        permissionType: (Optional[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]): The type of permission granted the person, organization, or audience.
    """

    grantee: NotRequired[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]
    permissionType: NotRequired[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]
    

#DigitalDocumentPermissionInheritedPropertiesTd = DigitalDocumentPermissionInheritedProperties()
#DigitalDocumentPermissionPropertiesTd = DigitalDocumentPermissionProperties()


class AllProperties(DigitalDocumentPermissionInheritedProperties , DigitalDocumentPermissionProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[DigitalDocumentPermissionProperties, DigitalDocumentPermissionInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "DigitalDocumentPermission"
    return model
    

DigitalDocumentPermission = create_schema_org_model()