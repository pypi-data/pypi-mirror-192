"""
Content about how, when, frequency and dosage of a topic.

https://schema.org/UsageOrScheduleHealthAspect
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class UsageOrScheduleHealthAspectInheritedProperties(TypedDict):
    """Content about how, when, frequency and dosage of a topic.

    References:
        https://schema.org/UsageOrScheduleHealthAspect
    Note:
        Model Depth 5
    Attributes:
    """

    


class UsageOrScheduleHealthAspectProperties(TypedDict):
    """Content about how, when, frequency and dosage of a topic.

    References:
        https://schema.org/UsageOrScheduleHealthAspect
    Note:
        Model Depth 5
    Attributes:
    """

    

#UsageOrScheduleHealthAspectInheritedPropertiesTd = UsageOrScheduleHealthAspectInheritedProperties()
#UsageOrScheduleHealthAspectPropertiesTd = UsageOrScheduleHealthAspectProperties()


class AllProperties(UsageOrScheduleHealthAspectInheritedProperties , UsageOrScheduleHealthAspectProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[UsageOrScheduleHealthAspectProperties, UsageOrScheduleHealthAspectInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "UsageOrScheduleHealthAspect"
    return model
    

UsageOrScheduleHealthAspect = create_schema_org_model()