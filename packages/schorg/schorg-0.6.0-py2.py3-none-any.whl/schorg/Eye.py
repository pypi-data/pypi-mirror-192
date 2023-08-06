"""
Eye or ophthalmological function assessment with clinical examination.

https://schema.org/Eye
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class EyeInheritedProperties(TypedDict):
    """Eye or ophthalmological function assessment with clinical examination.

    References:
        https://schema.org/Eye
    Note:
        Model Depth 5
    Attributes:
    """

    


class EyeProperties(TypedDict):
    """Eye or ophthalmological function assessment with clinical examination.

    References:
        https://schema.org/Eye
    Note:
        Model Depth 5
    Attributes:
    """

    

#EyeInheritedPropertiesTd = EyeInheritedProperties()
#EyePropertiesTd = EyeProperties()


class AllProperties(EyeInheritedProperties , EyeProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[EyeProperties, EyeInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "Eye"
    return model
    

Eye = create_schema_org_model()