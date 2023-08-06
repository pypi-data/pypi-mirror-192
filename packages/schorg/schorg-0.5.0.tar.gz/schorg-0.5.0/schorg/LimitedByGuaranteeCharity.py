"""
LimitedByGuaranteeCharity: Non-profit type referring to a charitable company that is limited by guarantee (UK).

https://schema.org/LimitedByGuaranteeCharity
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class LimitedByGuaranteeCharityInheritedProperties(TypedDict):
    """LimitedByGuaranteeCharity: Non-profit type referring to a charitable company that is limited by guarantee (UK).

    References:
        https://schema.org/LimitedByGuaranteeCharity
    Note:
        Model Depth 6
    Attributes:
    """

    


class LimitedByGuaranteeCharityProperties(TypedDict):
    """LimitedByGuaranteeCharity: Non-profit type referring to a charitable company that is limited by guarantee (UK).

    References:
        https://schema.org/LimitedByGuaranteeCharity
    Note:
        Model Depth 6
    Attributes:
    """

    

#LimitedByGuaranteeCharityInheritedPropertiesTd = LimitedByGuaranteeCharityInheritedProperties()
#LimitedByGuaranteeCharityPropertiesTd = LimitedByGuaranteeCharityProperties()


class AllProperties(LimitedByGuaranteeCharityInheritedProperties , LimitedByGuaranteeCharityProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[LimitedByGuaranteeCharityProperties, LimitedByGuaranteeCharityInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "LimitedByGuaranteeCharity"
    return model
    

LimitedByGuaranteeCharity = create_schema_org_model()