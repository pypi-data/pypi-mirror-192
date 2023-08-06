"""
Indicates a document for which the text is conclusively what the law says and is legally binding. (E.g. the digitally signed version of an Official Journal.)  Something "Definitive" is considered to be also [[AuthoritativeLegalValue]].

https://schema.org/DefinitiveLegalValue
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class DefinitiveLegalValueInheritedProperties(TypedDict):
    """Indicates a document for which the text is conclusively what the law says and is legally binding. (E.g. the digitally signed version of an Official Journal.)  Something "Definitive" is considered to be also [[AuthoritativeLegalValue]].

    References:
        https://schema.org/DefinitiveLegalValue
    Note:
        Model Depth 5
    Attributes:
    """

    


class DefinitiveLegalValueProperties(TypedDict):
    """Indicates a document for which the text is conclusively what the law says and is legally binding. (E.g. the digitally signed version of an Official Journal.)  Something "Definitive" is considered to be also [[AuthoritativeLegalValue]].

    References:
        https://schema.org/DefinitiveLegalValue
    Note:
        Model Depth 5
    Attributes:
    """

    

#DefinitiveLegalValueInheritedPropertiesTd = DefinitiveLegalValueInheritedProperties()
#DefinitiveLegalValuePropertiesTd = DefinitiveLegalValueProperties()


class AllProperties(DefinitiveLegalValueInheritedProperties , DefinitiveLegalValueProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[DefinitiveLegalValueProperties, DefinitiveLegalValueInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "DefinitiveLegalValue"
    return model
    

DefinitiveLegalValue = create_schema_org_model()