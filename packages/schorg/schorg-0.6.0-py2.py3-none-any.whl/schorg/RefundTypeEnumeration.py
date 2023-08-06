"""
Enumerates several kinds of product return refund types.

https://schema.org/RefundTypeEnumeration
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class RefundTypeEnumerationInheritedProperties(TypedDict):
    """Enumerates several kinds of product return refund types.

    References:
        https://schema.org/RefundTypeEnumeration
    Note:
        Model Depth 4
    Attributes:
        supersededBy: (Optional[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]): Relates a term (i.e. a property, class or enumeration) to one that supersedes it.
    """

    supersededBy: NotRequired[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]
    


class RefundTypeEnumerationProperties(TypedDict):
    """Enumerates several kinds of product return refund types.

    References:
        https://schema.org/RefundTypeEnumeration
    Note:
        Model Depth 4
    Attributes:
    """

    

#RefundTypeEnumerationInheritedPropertiesTd = RefundTypeEnumerationInheritedProperties()
#RefundTypeEnumerationPropertiesTd = RefundTypeEnumerationProperties()


class AllProperties(RefundTypeEnumerationInheritedProperties , RefundTypeEnumerationProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[RefundTypeEnumerationProperties, RefundTypeEnumerationInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "RefundTypeEnumeration"
    return model
    

RefundTypeEnumeration = create_schema_org_model()