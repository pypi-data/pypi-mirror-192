"""
A sidebar section of the page.

https://schema.org/WPSideBar
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class WPSideBarInheritedProperties(TypedDict):
    """A sidebar section of the page.

    References:
        https://schema.org/WPSideBar
    Note:
        Model Depth 4
    Attributes:
        xpath: (Optional[Union[List[Union[str, SchemaOrgObj]], str, SchemaOrgObj]]): An XPath, e.g. of a [[SpeakableSpecification]] or [[WebPageElement]]. In the latter case, multiple matches within a page can constitute a single conceptual "Web page element".
        cssSelector: (Optional[Union[List[Union[str, SchemaOrgObj]], str, SchemaOrgObj]]): A CSS selector, e.g. of a [[SpeakableSpecification]] or [[WebPageElement]]. In the latter case, multiple matches within a page can constitute a single conceptual "Web page element".
    """

    xpath: NotRequired[Union[List[Union[str, SchemaOrgObj]], str, SchemaOrgObj]]
    cssSelector: NotRequired[Union[List[Union[str, SchemaOrgObj]], str, SchemaOrgObj]]
    


class WPSideBarProperties(TypedDict):
    """A sidebar section of the page.

    References:
        https://schema.org/WPSideBar
    Note:
        Model Depth 4
    Attributes:
    """

    

#WPSideBarInheritedPropertiesTd = WPSideBarInheritedProperties()
#WPSideBarPropertiesTd = WPSideBarProperties()


class AllProperties(WPSideBarInheritedProperties , WPSideBarProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[WPSideBarProperties, WPSideBarInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "WPSideBar"
    return model
    

WPSideBar = create_schema_org_model()