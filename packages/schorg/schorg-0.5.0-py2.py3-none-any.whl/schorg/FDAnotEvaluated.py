"""
A designation that the drug in question has not been assigned a pregnancy category designation by the US FDA.

https://schema.org/FDAnotEvaluated
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class FDAnotEvaluatedInheritedProperties(TypedDict):
    """A designation that the drug in question has not been assigned a pregnancy category designation by the US FDA.

    References:
        https://schema.org/FDAnotEvaluated
    Note:
        Model Depth 6
    Attributes:
    """

    


class FDAnotEvaluatedProperties(TypedDict):
    """A designation that the drug in question has not been assigned a pregnancy category designation by the US FDA.

    References:
        https://schema.org/FDAnotEvaluated
    Note:
        Model Depth 6
    Attributes:
    """

    

#FDAnotEvaluatedInheritedPropertiesTd = FDAnotEvaluatedInheritedProperties()
#FDAnotEvaluatedPropertiesTd = FDAnotEvaluatedProperties()


class AllProperties(FDAnotEvaluatedInheritedProperties , FDAnotEvaluatedProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[FDAnotEvaluatedProperties, FDAnotEvaluatedInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "FDAnotEvaluated"
    return model
    

FDAnotEvaluated = create_schema_org_model()