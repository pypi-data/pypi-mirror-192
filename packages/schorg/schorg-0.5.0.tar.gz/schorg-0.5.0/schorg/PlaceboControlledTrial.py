"""
A placebo-controlled trial design.

https://schema.org/PlaceboControlledTrial
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class PlaceboControlledTrialInheritedProperties(TypedDict):
    """A placebo-controlled trial design.

    References:
        https://schema.org/PlaceboControlledTrial
    Note:
        Model Depth 6
    Attributes:
    """

    


class PlaceboControlledTrialProperties(TypedDict):
    """A placebo-controlled trial design.

    References:
        https://schema.org/PlaceboControlledTrial
    Note:
        Model Depth 6
    Attributes:
    """

    

#PlaceboControlledTrialInheritedPropertiesTd = PlaceboControlledTrialInheritedProperties()
#PlaceboControlledTrialPropertiesTd = PlaceboControlledTrialProperties()


class AllProperties(PlaceboControlledTrialInheritedProperties , PlaceboControlledTrialProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[PlaceboControlledTrialProperties, PlaceboControlledTrialInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "PlaceboControlledTrial"
    return model
    

PlaceboControlledTrial = create_schema_org_model()