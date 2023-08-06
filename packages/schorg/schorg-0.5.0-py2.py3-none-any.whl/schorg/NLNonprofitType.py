"""
NLNonprofitType: Non-profit organization type originating from the Netherlands.

https://schema.org/NLNonprofitType
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class NLNonprofitTypeInheritedProperties(TypedDict):
    """NLNonprofitType: Non-profit organization type originating from the Netherlands.

    References:
        https://schema.org/NLNonprofitType
    Note:
        Model Depth 5
    Attributes:
    """

    


class NLNonprofitTypeProperties(TypedDict):
    """NLNonprofitType: Non-profit organization type originating from the Netherlands.

    References:
        https://schema.org/NLNonprofitType
    Note:
        Model Depth 5
    Attributes:
    """

    

#NLNonprofitTypeInheritedPropertiesTd = NLNonprofitTypeInheritedProperties()
#NLNonprofitTypePropertiesTd = NLNonprofitTypeProperties()


class AllProperties(NLNonprofitTypeInheritedProperties , NLNonprofitTypeProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[NLNonprofitTypeProperties, NLNonprofitTypeInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "NLNonprofitType"
    return model
    

NLNonprofitType = create_schema_org_model()