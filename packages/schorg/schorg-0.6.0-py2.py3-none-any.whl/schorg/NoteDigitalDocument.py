"""
A file containing a note, primarily for the author.

https://schema.org/NoteDigitalDocument
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class NoteDigitalDocumentInheritedProperties(TypedDict):
    """A file containing a note, primarily for the author.

    References:
        https://schema.org/NoteDigitalDocument
    Note:
        Model Depth 4
    Attributes:
        hasDigitalDocumentPermission: (Optional[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]): A permission related to the access to this document (e.g. permission to read or write an electronic document). For a public document, specify a grantee with an Audience with audienceType equal to "public".
    """

    hasDigitalDocumentPermission: NotRequired[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]
    


class NoteDigitalDocumentProperties(TypedDict):
    """A file containing a note, primarily for the author.

    References:
        https://schema.org/NoteDigitalDocument
    Note:
        Model Depth 4
    Attributes:
    """

    

#NoteDigitalDocumentInheritedPropertiesTd = NoteDigitalDocumentInheritedProperties()
#NoteDigitalDocumentPropertiesTd = NoteDigitalDocumentProperties()


class AllProperties(NoteDigitalDocumentInheritedProperties , NoteDigitalDocumentProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[NoteDigitalDocumentProperties, NoteDigitalDocumentInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "NoteDigitalDocument"
    return model
    

NoteDigitalDocument = create_schema_org_model()