"""
The male gender.

https://schema.org/Male
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class MaleInheritedProperties(TypedDict):
    """The male gender.

    References:
        https://schema.org/Male
    Note:
        Model Depth 5
    Attributes:
    """

    


class MaleProperties(TypedDict):
    """The male gender.

    References:
        https://schema.org/Male
    Note:
        Model Depth 5
    Attributes:
    """

    

#MaleInheritedPropertiesTd = MaleInheritedProperties()
#MalePropertiesTd = MaleProperties()


class AllProperties(MaleInheritedProperties , MaleProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[MaleProperties, MaleInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "Male"
    return model
    

Male = create_schema_org_model()