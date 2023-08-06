"""
Related topics may be treated by a Topic.

https://schema.org/MayTreatHealthAspect
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class MayTreatHealthAspectInheritedProperties(TypedDict):
    """Related topics may be treated by a Topic.

    References:
        https://schema.org/MayTreatHealthAspect
    Note:
        Model Depth 5
    Attributes:
    """

    


class MayTreatHealthAspectProperties(TypedDict):
    """Related topics may be treated by a Topic.

    References:
        https://schema.org/MayTreatHealthAspect
    Note:
        Model Depth 5
    Attributes:
    """

    

#MayTreatHealthAspectInheritedPropertiesTd = MayTreatHealthAspectInheritedProperties()
#MayTreatHealthAspectPropertiesTd = MayTreatHealthAspectProperties()


class AllProperties(MayTreatHealthAspectInheritedProperties , MayTreatHealthAspectProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[MayTreatHealthAspectProperties, MayTreatHealthAspectInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "MayTreatHealthAspect"
    return model
    

MayTreatHealthAspect = create_schema_org_model()