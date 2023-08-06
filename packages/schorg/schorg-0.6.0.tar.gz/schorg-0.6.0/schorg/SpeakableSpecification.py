"""
A SpeakableSpecification indicates (typically via [[xpath]] or [[cssSelector]]) sections of a document that are highlighted as particularly [[speakable]]. Instances of this type are expected to be used primarily as values of the [[speakable]] property.

https://schema.org/SpeakableSpecification
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class SpeakableSpecificationInheritedProperties(TypedDict):
    """A SpeakableSpecification indicates (typically via [[xpath]] or [[cssSelector]]) sections of a document that are highlighted as particularly [[speakable]]. Instances of this type are expected to be used primarily as values of the [[speakable]] property.

    References:
        https://schema.org/SpeakableSpecification
    Note:
        Model Depth 3
    Attributes:
    """

    


class SpeakableSpecificationProperties(TypedDict):
    """A SpeakableSpecification indicates (typically via [[xpath]] or [[cssSelector]]) sections of a document that are highlighted as particularly [[speakable]]. Instances of this type are expected to be used primarily as values of the [[speakable]] property.

    References:
        https://schema.org/SpeakableSpecification
    Note:
        Model Depth 3
    Attributes:
        xpath: (Optional[Union[List[Union[str, SchemaOrgObj]], str, SchemaOrgObj]]): An XPath, e.g. of a [[SpeakableSpecification]] or [[WebPageElement]]. In the latter case, multiple matches within a page can constitute a single conceptual "Web page element".
        cssSelector: (Optional[Union[List[Union[str, SchemaOrgObj]], str, SchemaOrgObj]]): A CSS selector, e.g. of a [[SpeakableSpecification]] or [[WebPageElement]]. In the latter case, multiple matches within a page can constitute a single conceptual "Web page element".
    """

    xpath: NotRequired[Union[List[Union[str, SchemaOrgObj]], str, SchemaOrgObj]]
    cssSelector: NotRequired[Union[List[Union[str, SchemaOrgObj]], str, SchemaOrgObj]]
    

#SpeakableSpecificationInheritedPropertiesTd = SpeakableSpecificationInheritedProperties()
#SpeakableSpecificationPropertiesTd = SpeakableSpecificationProperties()


class AllProperties(SpeakableSpecificationInheritedProperties , SpeakableSpecificationProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[SpeakableSpecificationProperties, SpeakableSpecificationInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "SpeakableSpecification"
    return model
    

SpeakableSpecification = create_schema_org_model()