"""
A trial that takes place at a single center.

https://schema.org/SingleCenterTrial
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class SingleCenterTrialInheritedProperties(TypedDict):
    """A trial that takes place at a single center.

    References:
        https://schema.org/SingleCenterTrial
    Note:
        Model Depth 6
    Attributes:
    """

    


class SingleCenterTrialProperties(TypedDict):
    """A trial that takes place at a single center.

    References:
        https://schema.org/SingleCenterTrial
    Note:
        Model Depth 6
    Attributes:
    """

    

#SingleCenterTrialInheritedPropertiesTd = SingleCenterTrialInheritedProperties()
#SingleCenterTrialPropertiesTd = SingleCenterTrialProperties()


class AllProperties(SingleCenterTrialInheritedProperties , SingleCenterTrialProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[SingleCenterTrialProperties, SingleCenterTrialInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "SingleCenterTrial"
    return model
    

SingleCenterTrial = create_schema_org_model()