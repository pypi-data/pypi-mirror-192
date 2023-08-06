"""
The footer section of the page.

https://schema.org/WPFooter
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class WPFooterInheritedProperties(TypedDict):
    """The footer section of the page.

    References:
        https://schema.org/WPFooter
    Note:
        Model Depth 4
    Attributes:
        xpath: (Optional[Union[List[Union[str, SchemaOrgObj]], str, SchemaOrgObj]]): An XPath, e.g. of a [[SpeakableSpecification]] or [[WebPageElement]]. In the latter case, multiple matches within a page can constitute a single conceptual "Web page element".
        cssSelector: (Optional[Union[List[Union[str, SchemaOrgObj]], str, SchemaOrgObj]]): A CSS selector, e.g. of a [[SpeakableSpecification]] or [[WebPageElement]]. In the latter case, multiple matches within a page can constitute a single conceptual "Web page element".
    """

    xpath: NotRequired[Union[List[Union[str, SchemaOrgObj]], str, SchemaOrgObj]]
    cssSelector: NotRequired[Union[List[Union[str, SchemaOrgObj]], str, SchemaOrgObj]]
    


class WPFooterProperties(TypedDict):
    """The footer section of the page.

    References:
        https://schema.org/WPFooter
    Note:
        Model Depth 4
    Attributes:
    """

    

#WPFooterInheritedPropertiesTd = WPFooterInheritedProperties()
#WPFooterPropertiesTd = WPFooterProperties()


class AllProperties(WPFooterInheritedProperties , WPFooterProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[WPFooterProperties, WPFooterInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "WPFooter"
    return model
    

WPFooter = create_schema_org_model()