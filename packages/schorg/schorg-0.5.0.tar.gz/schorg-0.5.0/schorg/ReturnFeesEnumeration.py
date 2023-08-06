"""
Enumerates several kinds of policies for product return fees.

https://schema.org/ReturnFeesEnumeration
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class ReturnFeesEnumerationInheritedProperties(TypedDict):
    """Enumerates several kinds of policies for product return fees.

    References:
        https://schema.org/ReturnFeesEnumeration
    Note:
        Model Depth 4
    Attributes:
        supersededBy: (Optional[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]): Relates a term (i.e. a property, class or enumeration) to one that supersedes it.
    """

    supersededBy: NotRequired[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]
    


class ReturnFeesEnumerationProperties(TypedDict):
    """Enumerates several kinds of policies for product return fees.

    References:
        https://schema.org/ReturnFeesEnumeration
    Note:
        Model Depth 4
    Attributes:
    """

    

#ReturnFeesEnumerationInheritedPropertiesTd = ReturnFeesEnumerationInheritedProperties()
#ReturnFeesEnumerationPropertiesTd = ReturnFeesEnumerationProperties()


class AllProperties(ReturnFeesEnumerationInheritedProperties , ReturnFeesEnumerationProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[ReturnFeesEnumerationProperties, ReturnFeesEnumerationInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "ReturnFeesEnumeration"
    return model
    

ReturnFeesEnumeration = create_schema_org_model()