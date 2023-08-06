"""
This type covers computer programming languages such as Scheme and Lisp, as well as other language-like computer representations. Natural languages are best represented with the [[Language]] type.

https://schema.org/ComputerLanguage
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class ComputerLanguageInheritedProperties(TypedDict):
    """This type covers computer programming languages such as Scheme and Lisp, as well as other language-like computer representations. Natural languages are best represented with the [[Language]] type.

    References:
        https://schema.org/ComputerLanguage
    Note:
        Model Depth 3
    Attributes:
    """

    


class ComputerLanguageProperties(TypedDict):
    """This type covers computer programming languages such as Scheme and Lisp, as well as other language-like computer representations. Natural languages are best represented with the [[Language]] type.

    References:
        https://schema.org/ComputerLanguage
    Note:
        Model Depth 3
    Attributes:
    """

    

#ComputerLanguageInheritedPropertiesTd = ComputerLanguageInheritedProperties()
#ComputerLanguagePropertiesTd = ComputerLanguageProperties()


class AllProperties(ComputerLanguageInheritedProperties , ComputerLanguageProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[ComputerLanguageProperties, ComputerLanguageInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "ComputerLanguage"
    return model
    

ComputerLanguage = create_schema_org_model()