"""
HealthAspectEnumeration enumerates several aspects of health content online, each of which might be described using [[hasHealthAspect]] and [[HealthTopicContent]].

https://schema.org/HealthAspectEnumeration
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class HealthAspectEnumerationInheritedProperties(TypedDict):
    """HealthAspectEnumeration enumerates several aspects of health content online, each of which might be described using [[hasHealthAspect]] and [[HealthTopicContent]].

    References:
        https://schema.org/HealthAspectEnumeration
    Note:
        Model Depth 4
    Attributes:
        supersededBy: (Optional[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]): Relates a term (i.e. a property, class or enumeration) to one that supersedes it.
    """

    supersededBy: NotRequired[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]
    


class HealthAspectEnumerationProperties(TypedDict):
    """HealthAspectEnumeration enumerates several aspects of health content online, each of which might be described using [[hasHealthAspect]] and [[HealthTopicContent]].

    References:
        https://schema.org/HealthAspectEnumeration
    Note:
        Model Depth 4
    Attributes:
    """

    

#HealthAspectEnumerationInheritedPropertiesTd = HealthAspectEnumerationInheritedProperties()
#HealthAspectEnumerationPropertiesTd = HealthAspectEnumerationProperties()


class AllProperties(HealthAspectEnumerationInheritedProperties , HealthAspectEnumerationProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[HealthAspectEnumerationProperties, HealthAspectEnumerationInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "HealthAspectEnumeration"
    return model
    

HealthAspectEnumeration = create_schema_org_model()