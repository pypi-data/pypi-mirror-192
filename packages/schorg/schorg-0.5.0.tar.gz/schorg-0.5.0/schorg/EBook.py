"""
Book format: Ebook.

https://schema.org/EBook
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class EBookInheritedProperties(TypedDict):
    """Book format: Ebook.

    References:
        https://schema.org/EBook
    Note:
        Model Depth 5
    Attributes:
    """

    


class EBookProperties(TypedDict):
    """Book format: Ebook.

    References:
        https://schema.org/EBook
    Note:
        Model Depth 5
    Attributes:
    """

    

#EBookInheritedPropertiesTd = EBookInheritedProperties()
#EBookPropertiesTd = EBookProperties()


class AllProperties(EBookInheritedProperties , EBookProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[EBookProperties, EBookInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "EBook"
    return model
    

EBook = create_schema_org_model()