"""
A file containing slides or used for a presentation.

https://schema.org/PresentationDigitalDocument
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class PresentationDigitalDocumentInheritedProperties(TypedDict):
    """A file containing slides or used for a presentation.

    References:
        https://schema.org/PresentationDigitalDocument
    Note:
        Model Depth 4
    Attributes:
        hasDigitalDocumentPermission: (Optional[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]): A permission related to the access to this document (e.g. permission to read or write an electronic document). For a public document, specify a grantee with an Audience with audienceType equal to "public".
    """

    hasDigitalDocumentPermission: NotRequired[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]
    


class PresentationDigitalDocumentProperties(TypedDict):
    """A file containing slides or used for a presentation.

    References:
        https://schema.org/PresentationDigitalDocument
    Note:
        Model Depth 4
    Attributes:
    """

    

#PresentationDigitalDocumentInheritedPropertiesTd = PresentationDigitalDocumentInheritedProperties()
#PresentationDigitalDocumentPropertiesTd = PresentationDigitalDocumentProperties()


class AllProperties(PresentationDigitalDocumentInheritedProperties , PresentationDigitalDocumentProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[PresentationDigitalDocumentProperties, PresentationDigitalDocumentInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "PresentationDigitalDocument"
    return model
    

PresentationDigitalDocument = create_schema_org_model()