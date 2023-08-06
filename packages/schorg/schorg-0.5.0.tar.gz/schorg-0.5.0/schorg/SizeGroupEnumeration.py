"""
Enumerates common size groups for various product categories.

https://schema.org/SizeGroupEnumeration
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class SizeGroupEnumerationInheritedProperties(TypedDict):
    """Enumerates common size groups for various product categories.

    References:
        https://schema.org/SizeGroupEnumeration
    Note:
        Model Depth 4
    Attributes:
        supersededBy: (Optional[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]): Relates a term (i.e. a property, class or enumeration) to one that supersedes it.
    """

    supersededBy: NotRequired[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]
    


class SizeGroupEnumerationProperties(TypedDict):
    """Enumerates common size groups for various product categories.

    References:
        https://schema.org/SizeGroupEnumeration
    Note:
        Model Depth 4
    Attributes:
    """

    

#SizeGroupEnumerationInheritedPropertiesTd = SizeGroupEnumerationInheritedProperties()
#SizeGroupEnumerationPropertiesTd = SizeGroupEnumerationProperties()


class AllProperties(SizeGroupEnumerationInheritedProperties , SizeGroupEnumerationProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[SizeGroupEnumerationProperties, SizeGroupEnumerationInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "SizeGroupEnumeration"
    return model
    

SizeGroupEnumeration = create_schema_org_model()