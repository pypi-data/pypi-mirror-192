"""
A file composed primarily of text.

https://schema.org/TextDigitalDocument
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class TextDigitalDocumentInheritedProperties(TypedDict):
    """A file composed primarily of text.

    References:
        https://schema.org/TextDigitalDocument
    Note:
        Model Depth 4
    Attributes:
        hasDigitalDocumentPermission: (Optional[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]): A permission related to the access to this document (e.g. permission to read or write an electronic document). For a public document, specify a grantee with an Audience with audienceType equal to "public".
    """

    hasDigitalDocumentPermission: NotRequired[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]
    


class TextDigitalDocumentProperties(TypedDict):
    """A file composed primarily of text.

    References:
        https://schema.org/TextDigitalDocument
    Note:
        Model Depth 4
    Attributes:
    """

    

#TextDigitalDocumentInheritedPropertiesTd = TextDigitalDocumentInheritedProperties()
#TextDigitalDocumentPropertiesTd = TextDigitalDocumentProperties()


class AllProperties(TextDigitalDocumentInheritedProperties , TextDigitalDocumentProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[TextDigitalDocumentProperties, TextDigitalDocumentInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "TextDigitalDocument"
    return model
    

TextDigitalDocument = create_schema_org_model()