"""
Enumerates several types of product return methods.

https://schema.org/ReturnMethodEnumeration
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class ReturnMethodEnumerationInheritedProperties(TypedDict):
    """Enumerates several types of product return methods.

    References:
        https://schema.org/ReturnMethodEnumeration
    Note:
        Model Depth 4
    Attributes:
        supersededBy: (Optional[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]): Relates a term (i.e. a property, class or enumeration) to one that supersedes it.
    """

    supersededBy: NotRequired[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]
    


class ReturnMethodEnumerationProperties(TypedDict):
    """Enumerates several types of product return methods.

    References:
        https://schema.org/ReturnMethodEnumeration
    Note:
        Model Depth 4
    Attributes:
    """

    

#ReturnMethodEnumerationInheritedPropertiesTd = ReturnMethodEnumerationInheritedProperties()
#ReturnMethodEnumerationPropertiesTd = ReturnMethodEnumerationProperties()


class AllProperties(ReturnMethodEnumerationInheritedProperties , ReturnMethodEnumerationProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[ReturnMethodEnumerationProperties, ReturnMethodEnumerationInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "ReturnMethodEnumeration"
    return model
    

ReturnMethodEnumeration = create_schema_org_model()