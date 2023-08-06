"""
Content about contagion mechanisms and contagiousness information over the topic.

https://schema.org/ContagiousnessHealthAspect
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class ContagiousnessHealthAspectInheritedProperties(TypedDict):
    """Content about contagion mechanisms and contagiousness information over the topic.

    References:
        https://schema.org/ContagiousnessHealthAspect
    Note:
        Model Depth 5
    Attributes:
    """

    


class ContagiousnessHealthAspectProperties(TypedDict):
    """Content about contagion mechanisms and contagiousness information over the topic.

    References:
        https://schema.org/ContagiousnessHealthAspect
    Note:
        Model Depth 5
    Attributes:
    """

    

#ContagiousnessHealthAspectInheritedPropertiesTd = ContagiousnessHealthAspectInheritedProperties()
#ContagiousnessHealthAspectPropertiesTd = ContagiousnessHealthAspectProperties()


class AllProperties(ContagiousnessHealthAspectInheritedProperties , ContagiousnessHealthAspectProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[ContagiousnessHealthAspectProperties, ContagiousnessHealthAspectInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "ContagiousnessHealthAspect"
    return model
    

ContagiousnessHealthAspect = create_schema_org_model()