"""
Treatments or related therapies for a Topic.

https://schema.org/TreatmentsHealthAspect
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class TreatmentsHealthAspectInheritedProperties(TypedDict):
    """Treatments or related therapies for a Topic.

    References:
        https://schema.org/TreatmentsHealthAspect
    Note:
        Model Depth 5
    Attributes:
    """

    


class TreatmentsHealthAspectProperties(TypedDict):
    """Treatments or related therapies for a Topic.

    References:
        https://schema.org/TreatmentsHealthAspect
    Note:
        Model Depth 5
    Attributes:
    """

    

#TreatmentsHealthAspectInheritedPropertiesTd = TreatmentsHealthAspectInheritedProperties()
#TreatmentsHealthAspectPropertiesTd = TreatmentsHealthAspectProperties()


class AllProperties(TreatmentsHealthAspectInheritedProperties , TreatmentsHealthAspectProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[TreatmentsHealthAspectProperties, TreatmentsHealthAspectInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "TreatmentsHealthAspect"
    return model
    

TreatmentsHealthAspect = create_schema_org_model()