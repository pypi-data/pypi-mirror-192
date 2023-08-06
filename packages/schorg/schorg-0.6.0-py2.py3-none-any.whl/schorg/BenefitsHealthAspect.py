"""
Content about the benefits and advantages of usage or utilization of topic.

https://schema.org/BenefitsHealthAspect
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class BenefitsHealthAspectInheritedProperties(TypedDict):
    """Content about the benefits and advantages of usage or utilization of topic.

    References:
        https://schema.org/BenefitsHealthAspect
    Note:
        Model Depth 5
    Attributes:
    """

    


class BenefitsHealthAspectProperties(TypedDict):
    """Content about the benefits and advantages of usage or utilization of topic.

    References:
        https://schema.org/BenefitsHealthAspect
    Note:
        Model Depth 5
    Attributes:
    """

    

#BenefitsHealthAspectInheritedPropertiesTd = BenefitsHealthAspectInheritedProperties()
#BenefitsHealthAspectPropertiesTd = BenefitsHealthAspectProperties()


class AllProperties(BenefitsHealthAspectInheritedProperties , BenefitsHealthAspectProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[BenefitsHealthAspectProperties, BenefitsHealthAspectInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "BenefitsHealthAspect"
    return model
    

BenefitsHealthAspect = create_schema_org_model()