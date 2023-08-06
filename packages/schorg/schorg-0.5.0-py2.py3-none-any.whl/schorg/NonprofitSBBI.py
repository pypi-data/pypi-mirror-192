"""
NonprofitSBBI: Non-profit type referring to a Social Interest Promoting Institution (NL).

https://schema.org/NonprofitSBBI
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class NonprofitSBBIInheritedProperties(TypedDict):
    """NonprofitSBBI: Non-profit type referring to a Social Interest Promoting Institution (NL).

    References:
        https://schema.org/NonprofitSBBI
    Note:
        Model Depth 6
    Attributes:
    """

    


class NonprofitSBBIProperties(TypedDict):
    """NonprofitSBBI: Non-profit type referring to a Social Interest Promoting Institution (NL).

    References:
        https://schema.org/NonprofitSBBI
    Note:
        Model Depth 6
    Attributes:
    """

    

#NonprofitSBBIInheritedPropertiesTd = NonprofitSBBIInheritedProperties()
#NonprofitSBBIPropertiesTd = NonprofitSBBIProperties()


class AllProperties(NonprofitSBBIInheritedProperties , NonprofitSBBIProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[NonprofitSBBIProperties, NonprofitSBBIInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "NonprofitSBBI"
    return model
    

NonprofitSBBI = create_schema_org_model()