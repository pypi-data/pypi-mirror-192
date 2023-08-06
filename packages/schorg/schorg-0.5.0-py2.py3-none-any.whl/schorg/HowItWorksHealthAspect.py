"""
Content that discusses and explains how a particular health-related topic works, e.g. in terms of mechanisms and underlying science.

https://schema.org/HowItWorksHealthAspect
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class HowItWorksHealthAspectInheritedProperties(TypedDict):
    """Content that discusses and explains how a particular health-related topic works, e.g. in terms of mechanisms and underlying science.

    References:
        https://schema.org/HowItWorksHealthAspect
    Note:
        Model Depth 5
    Attributes:
    """

    


class HowItWorksHealthAspectProperties(TypedDict):
    """Content that discusses and explains how a particular health-related topic works, e.g. in terms of mechanisms and underlying science.

    References:
        https://schema.org/HowItWorksHealthAspect
    Note:
        Model Depth 5
    Attributes:
    """

    

#HowItWorksHealthAspectInheritedPropertiesTd = HowItWorksHealthAspectInheritedProperties()
#HowItWorksHealthAspectPropertiesTd = HowItWorksHealthAspectProperties()


class AllProperties(HowItWorksHealthAspectInheritedProperties , HowItWorksHealthAspectProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[HowItWorksHealthAspectProperties, HowItWorksHealthAspectInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "HowItWorksHealthAspect"
    return model
    

HowItWorksHealthAspect = create_schema_org_model()