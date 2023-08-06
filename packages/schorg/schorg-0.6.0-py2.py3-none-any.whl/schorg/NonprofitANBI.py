"""
NonprofitANBI: Non-profit type referring to a Public Benefit Organization (NL).

https://schema.org/NonprofitANBI
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class NonprofitANBIInheritedProperties(TypedDict):
    """NonprofitANBI: Non-profit type referring to a Public Benefit Organization (NL).

    References:
        https://schema.org/NonprofitANBI
    Note:
        Model Depth 6
    Attributes:
    """

    


class NonprofitANBIProperties(TypedDict):
    """NonprofitANBI: Non-profit type referring to a Public Benefit Organization (NL).

    References:
        https://schema.org/NonprofitANBI
    Note:
        Model Depth 6
    Attributes:
    """

    

#NonprofitANBIInheritedPropertiesTd = NonprofitANBIInheritedProperties()
#NonprofitANBIPropertiesTd = NonprofitANBIProperties()


class AllProperties(NonprofitANBIInheritedProperties , NonprofitANBIProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[NonprofitANBIProperties, NonprofitANBIInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "NonprofitANBI"
    return model
    

NonprofitANBI = create_schema_org_model()