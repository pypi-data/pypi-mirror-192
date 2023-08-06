"""
The act of responding instinctively and emotionally to an object, expressing a sentiment.

https://schema.org/ReactAction
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class ReactActionInheritedProperties(TypedDict):
    """The act of responding instinctively and emotionally to an object, expressing a sentiment.

    References:
        https://schema.org/ReactAction
    Note:
        Model Depth 4
    Attributes:
    """

    


class ReactActionProperties(TypedDict):
    """The act of responding instinctively and emotionally to an object, expressing a sentiment.

    References:
        https://schema.org/ReactAction
    Note:
        Model Depth 4
    Attributes:
    """

    

#ReactActionInheritedPropertiesTd = ReactActionInheritedProperties()
#ReactActionPropertiesTd = ReactActionProperties()


class AllProperties(ReactActionInheritedProperties , ReactActionProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[ReactActionProperties, ReactActionInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "ReactAction"
    return model
    

ReactAction = create_schema_org_model()