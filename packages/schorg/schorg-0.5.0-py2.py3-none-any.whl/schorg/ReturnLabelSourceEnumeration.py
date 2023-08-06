"""
Enumerates several types of return labels for product returns.

https://schema.org/ReturnLabelSourceEnumeration
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class ReturnLabelSourceEnumerationInheritedProperties(TypedDict):
    """Enumerates several types of return labels for product returns.

    References:
        https://schema.org/ReturnLabelSourceEnumeration
    Note:
        Model Depth 4
    Attributes:
        supersededBy: (Optional[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]): Relates a term (i.e. a property, class or enumeration) to one that supersedes it.
    """

    supersededBy: NotRequired[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]
    


class ReturnLabelSourceEnumerationProperties(TypedDict):
    """Enumerates several types of return labels for product returns.

    References:
        https://schema.org/ReturnLabelSourceEnumeration
    Note:
        Model Depth 4
    Attributes:
    """

    

#ReturnLabelSourceEnumerationInheritedPropertiesTd = ReturnLabelSourceEnumerationInheritedProperties()
#ReturnLabelSourceEnumerationPropertiesTd = ReturnLabelSourceEnumerationProperties()


class AllProperties(ReturnLabelSourceEnumerationInheritedProperties , ReturnLabelSourceEnumerationProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[ReturnLabelSourceEnumerationProperties, ReturnLabelSourceEnumerationInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "ReturnLabelSourceEnumeration"
    return model
    

ReturnLabelSourceEnumeration = create_schema_org_model()