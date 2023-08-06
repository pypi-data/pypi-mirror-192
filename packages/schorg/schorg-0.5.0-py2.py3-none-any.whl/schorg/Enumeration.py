"""
Lists or enumerations—for example, a list of cuisines or music genres, etc.

https://schema.org/Enumeration
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class EnumerationInheritedProperties(TypedDict):
    """Lists or enumerations—for example, a list of cuisines or music genres, etc.

    References:
        https://schema.org/Enumeration
    Note:
        Model Depth 3
    Attributes:
    """

    


class EnumerationProperties(TypedDict):
    """Lists or enumerations—for example, a list of cuisines or music genres, etc.

    References:
        https://schema.org/Enumeration
    Note:
        Model Depth 3
    Attributes:
        supersededBy: (Optional[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]): Relates a term (i.e. a property, class or enumeration) to one that supersedes it.
    """

    supersededBy: NotRequired[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]
    

#EnumerationInheritedPropertiesTd = EnumerationInheritedProperties()
#EnumerationPropertiesTd = EnumerationProperties()


class AllProperties(EnumerationInheritedProperties , EnumerationProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[EnumerationProperties, EnumerationInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "Enumeration"
    return model
    

Enumeration = create_schema_org_model()