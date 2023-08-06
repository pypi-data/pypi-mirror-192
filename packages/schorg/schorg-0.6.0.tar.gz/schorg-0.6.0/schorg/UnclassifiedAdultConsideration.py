"""
The item is suitable only for adults, without indicating why. Due to widespread use of "adult" as a euphemism for "sexual", many such items are likely suited also for the SexualContentConsideration code.

https://schema.org/UnclassifiedAdultConsideration
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class UnclassifiedAdultConsiderationInheritedProperties(TypedDict):
    """The item is suitable only for adults, without indicating why. Due to widespread use of "adult" as a euphemism for "sexual", many such items are likely suited also for the SexualContentConsideration code.

    References:
        https://schema.org/UnclassifiedAdultConsideration
    Note:
        Model Depth 5
    Attributes:
    """

    


class UnclassifiedAdultConsiderationProperties(TypedDict):
    """The item is suitable only for adults, without indicating why. Due to widespread use of "adult" as a euphemism for "sexual", many such items are likely suited also for the SexualContentConsideration code.

    References:
        https://schema.org/UnclassifiedAdultConsideration
    Note:
        Model Depth 5
    Attributes:
    """

    

#UnclassifiedAdultConsiderationInheritedPropertiesTd = UnclassifiedAdultConsiderationInheritedProperties()
#UnclassifiedAdultConsiderationPropertiesTd = UnclassifiedAdultConsiderationProperties()


class AllProperties(UnclassifiedAdultConsiderationInheritedProperties , UnclassifiedAdultConsiderationProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[UnclassifiedAdultConsiderationProperties, UnclassifiedAdultConsiderationInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "UnclassifiedAdultConsideration"
    return model
    

UnclassifiedAdultConsideration = create_schema_org_model()