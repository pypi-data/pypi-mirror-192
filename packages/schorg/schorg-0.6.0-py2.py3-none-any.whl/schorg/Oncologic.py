"""
A specific branch of medical science that deals with benign and malignant tumors, including the study of their development, diagnosis, treatment and prevention.

https://schema.org/Oncologic
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class OncologicInheritedProperties(TypedDict):
    """A specific branch of medical science that deals with benign and malignant tumors, including the study of their development, diagnosis, treatment and prevention.

    References:
        https://schema.org/Oncologic
    Note:
        Model Depth 5
    Attributes:
    """

    


class OncologicProperties(TypedDict):
    """A specific branch of medical science that deals with benign and malignant tumors, including the study of their development, diagnosis, treatment and prevention.

    References:
        https://schema.org/Oncologic
    Note:
        Model Depth 5
    Attributes:
    """

    

#OncologicInheritedPropertiesTd = OncologicInheritedProperties()
#OncologicPropertiesTd = OncologicProperties()


class AllProperties(OncologicInheritedProperties , OncologicProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[OncologicProperties, OncologicInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "Oncologic"
    return model
    

Oncologic = create_schema_org_model()