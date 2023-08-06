"""
A specific branch of medical science that pertains to diagnosis and treatment of disorders of endocrine glands and their secretions.

https://schema.org/Endocrine
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class EndocrineInheritedProperties(TypedDict):
    """A specific branch of medical science that pertains to diagnosis and treatment of disorders of endocrine glands and their secretions.

    References:
        https://schema.org/Endocrine
    Note:
        Model Depth 6
    Attributes:
    """

    


class EndocrineProperties(TypedDict):
    """A specific branch of medical science that pertains to diagnosis and treatment of disorders of endocrine glands and their secretions.

    References:
        https://schema.org/Endocrine
    Note:
        Model Depth 6
    Attributes:
    """

    

#EndocrineInheritedPropertiesTd = EndocrineInheritedProperties()
#EndocrinePropertiesTd = EndocrineProperties()


class AllProperties(EndocrineInheritedProperties , EndocrineProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[EndocrineProperties, EndocrineInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "Endocrine"
    return model
    

Endocrine = create_schema_org_model()