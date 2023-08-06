"""
A tennis complex.

https://schema.org/TennisComplex
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class TennisComplexInheritedProperties(TypedDict):
    """A tennis complex.

    References:
        https://schema.org/TennisComplex
    Note:
        Model Depth 5
    Attributes:
    """

    


class TennisComplexProperties(TypedDict):
    """A tennis complex.

    References:
        https://schema.org/TennisComplex
    Note:
        Model Depth 5
    Attributes:
    """

    

#TennisComplexInheritedPropertiesTd = TennisComplexInheritedProperties()
#TennisComplexPropertiesTd = TennisComplexProperties()


class AllProperties(TennisComplexInheritedProperties , TennisComplexProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[TennisComplexProperties, TennisComplexInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "TennisComplex"
    return model
    

TennisComplex = create_schema_org_model()