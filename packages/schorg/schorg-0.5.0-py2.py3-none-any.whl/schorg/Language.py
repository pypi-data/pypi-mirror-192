"""
Natural languages such as Spanish, Tamil, Hindi, English, etc. Formal language code tags expressed in [BCP 47](https://en.wikipedia.org/wiki/IETF_language_tag) can be used via the [[alternateName]] property. The Language type previously also covered programming languages such as Scheme and Lisp, which are now best represented using [[ComputerLanguage]].

https://schema.org/Language
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class LanguageInheritedProperties(TypedDict):
    """Natural languages such as Spanish, Tamil, Hindi, English, etc. Formal language code tags expressed in [BCP 47](https://en.wikipedia.org/wiki/IETF_language_tag) can be used via the [[alternateName]] property. The Language type previously also covered programming languages such as Scheme and Lisp, which are now best represented using [[ComputerLanguage]].

    References:
        https://schema.org/Language
    Note:
        Model Depth 3
    Attributes:
    """

    


class LanguageProperties(TypedDict):
    """Natural languages such as Spanish, Tamil, Hindi, English, etc. Formal language code tags expressed in [BCP 47](https://en.wikipedia.org/wiki/IETF_language_tag) can be used via the [[alternateName]] property. The Language type previously also covered programming languages such as Scheme and Lisp, which are now best represented using [[ComputerLanguage]].

    References:
        https://schema.org/Language
    Note:
        Model Depth 3
    Attributes:
    """

    

#LanguageInheritedPropertiesTd = LanguageInheritedProperties()
#LanguagePropertiesTd = LanguageProperties()


class AllProperties(LanguageInheritedProperties , LanguageProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[LanguageProperties, LanguageInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "Language"
    return model
    

Language = create_schema_org_model()