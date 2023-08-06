"""
A golf course.

https://schema.org/GolfCourse
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class GolfCourseInheritedProperties(TypedDict):
    """A golf course.

    References:
        https://schema.org/GolfCourse
    Note:
        Model Depth 5
    Attributes:
    """

    


class GolfCourseProperties(TypedDict):
    """A golf course.

    References:
        https://schema.org/GolfCourse
    Note:
        Model Depth 5
    Attributes:
    """

    

#GolfCourseInheritedPropertiesTd = GolfCourseInheritedProperties()
#GolfCoursePropertiesTd = GolfCourseProperties()


class AllProperties(GolfCourseInheritedProperties , GolfCourseProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[GolfCourseProperties, GolfCourseInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "GolfCourse"
    return model
    

GolfCourse = create_schema_org_model()