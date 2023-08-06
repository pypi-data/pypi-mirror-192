"""
Enumeration of considerations that make a product relevant or potentially restricted for adults only.

https://schema.org/AdultOrientedEnumeration
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class AdultOrientedEnumerationInheritedProperties(TypedDict):
    """Enumeration of considerations that make a product relevant or potentially restricted for adults only.

    References:
        https://schema.org/AdultOrientedEnumeration
    Note:
        Model Depth 4
    Attributes:
        supersededBy: (Optional[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]): Relates a term (i.e. a property, class or enumeration) to one that supersedes it.
    """

    supersededBy: NotRequired[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]
    


class AdultOrientedEnumerationProperties(TypedDict):
    """Enumeration of considerations that make a product relevant or potentially restricted for adults only.

    References:
        https://schema.org/AdultOrientedEnumeration
    Note:
        Model Depth 4
    Attributes:
    """

    

#AdultOrientedEnumerationInheritedPropertiesTd = AdultOrientedEnumerationInheritedProperties()
#AdultOrientedEnumerationPropertiesTd = AdultOrientedEnumerationProperties()


class AllProperties(AdultOrientedEnumerationInheritedProperties , AdultOrientedEnumerationProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[AdultOrientedEnumerationProperties, AdultOrientedEnumerationInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "AdultOrientedEnumeration"
    return model
    

AdultOrientedEnumeration = create_schema_org_model()