"""
A table on a Web page.

https://schema.org/Table
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class TableInheritedProperties(TypedDict):
    """A table on a Web page.

    References:
        https://schema.org/Table
    Note:
        Model Depth 4
    Attributes:
        xpath: (Optional[Union[List[Union[str, SchemaOrgObj]], str, SchemaOrgObj]]): An XPath, e.g. of a [[SpeakableSpecification]] or [[WebPageElement]]. In the latter case, multiple matches within a page can constitute a single conceptual "Web page element".
        cssSelector: (Optional[Union[List[Union[str, SchemaOrgObj]], str, SchemaOrgObj]]): A CSS selector, e.g. of a [[SpeakableSpecification]] or [[WebPageElement]]. In the latter case, multiple matches within a page can constitute a single conceptual "Web page element".
    """

    xpath: NotRequired[Union[List[Union[str, SchemaOrgObj]], str, SchemaOrgObj]]
    cssSelector: NotRequired[Union[List[Union[str, SchemaOrgObj]], str, SchemaOrgObj]]
    


class TableProperties(TypedDict):
    """A table on a Web page.

    References:
        https://schema.org/Table
    Note:
        Model Depth 4
    Attributes:
    """

    

#TableInheritedPropertiesTd = TableInheritedProperties()
#TablePropertiesTd = TableProperties()


class AllProperties(TableInheritedProperties , TableProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[TableProperties, TableInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "Table"
    return model
    

Table = create_schema_org_model()