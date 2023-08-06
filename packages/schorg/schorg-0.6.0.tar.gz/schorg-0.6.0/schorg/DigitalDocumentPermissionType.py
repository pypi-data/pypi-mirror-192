"""
A type of permission which can be granted for accessing a digital document.

https://schema.org/DigitalDocumentPermissionType
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class DigitalDocumentPermissionTypeInheritedProperties(TypedDict):
    """A type of permission which can be granted for accessing a digital document.

    References:
        https://schema.org/DigitalDocumentPermissionType
    Note:
        Model Depth 4
    Attributes:
        supersededBy: (Optional[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]): Relates a term (i.e. a property, class or enumeration) to one that supersedes it.
    """

    supersededBy: NotRequired[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]
    


class DigitalDocumentPermissionTypeProperties(TypedDict):
    """A type of permission which can be granted for accessing a digital document.

    References:
        https://schema.org/DigitalDocumentPermissionType
    Note:
        Model Depth 4
    Attributes:
    """

    

#DigitalDocumentPermissionTypeInheritedPropertiesTd = DigitalDocumentPermissionTypeInheritedProperties()
#DigitalDocumentPermissionTypePropertiesTd = DigitalDocumentPermissionTypeProperties()


class AllProperties(DigitalDocumentPermissionTypeInheritedProperties , DigitalDocumentPermissionTypeProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[DigitalDocumentPermissionTypeProperties, DigitalDocumentPermissionTypeInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "DigitalDocumentPermissionType"
    return model
    

DigitalDocumentPermissionType = create_schema_org_model()