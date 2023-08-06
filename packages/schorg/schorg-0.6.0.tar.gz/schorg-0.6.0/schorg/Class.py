"""
A class, also often called a 'Type'; equivalent to rdfs:Class.

https://schema.org/Class
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class ClassInheritedProperties(TypedDict):
    """A class, also often called a 'Type'; equivalent to rdfs:Class.

    References:
        https://schema.org/Class
    Note:
        Model Depth 3
    Attributes:
    """

    


class ClassProperties(TypedDict):
    """A class, also often called a 'Type'; equivalent to rdfs:Class.

    References:
        https://schema.org/Class
    Note:
        Model Depth 3
    Attributes:
        supersededBy: (Optional[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]): Relates a term (i.e. a property, class or enumeration) to one that supersedes it.
    """

    supersededBy: NotRequired[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]
    

#ClassInheritedPropertiesTd = ClassInheritedProperties()
#ClassPropertiesTd = ClassProperties()


class AllProperties(ClassInheritedProperties , ClassProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[ClassProperties, ClassInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "Class"
    return model
    

Class = create_schema_org_model()