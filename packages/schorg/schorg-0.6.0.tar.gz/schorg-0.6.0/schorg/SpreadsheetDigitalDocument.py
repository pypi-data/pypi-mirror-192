"""
A spreadsheet file.

https://schema.org/SpreadsheetDigitalDocument
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class SpreadsheetDigitalDocumentInheritedProperties(TypedDict):
    """A spreadsheet file.

    References:
        https://schema.org/SpreadsheetDigitalDocument
    Note:
        Model Depth 4
    Attributes:
        hasDigitalDocumentPermission: (Optional[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]): A permission related to the access to this document (e.g. permission to read or write an electronic document). For a public document, specify a grantee with an Audience with audienceType equal to "public".
    """

    hasDigitalDocumentPermission: NotRequired[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]
    


class SpreadsheetDigitalDocumentProperties(TypedDict):
    """A spreadsheet file.

    References:
        https://schema.org/SpreadsheetDigitalDocument
    Note:
        Model Depth 4
    Attributes:
    """

    

#SpreadsheetDigitalDocumentInheritedPropertiesTd = SpreadsheetDigitalDocumentInheritedProperties()
#SpreadsheetDigitalDocumentPropertiesTd = SpreadsheetDigitalDocumentProperties()


class AllProperties(SpreadsheetDigitalDocumentInheritedProperties , SpreadsheetDigitalDocumentProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[SpreadsheetDigitalDocumentProperties, SpreadsheetDigitalDocumentInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "SpreadsheetDigitalDocument"
    return model
    

SpreadsheetDigitalDocument = create_schema_org_model()