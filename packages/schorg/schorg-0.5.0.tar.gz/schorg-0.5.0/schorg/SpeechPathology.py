"""
The scientific study and treatment of defects, disorders, and malfunctions of speech and voice, as stuttering, lisping, or lalling, and of language disturbances, as aphasia or delayed language acquisition.

https://schema.org/SpeechPathology
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class SpeechPathologyInheritedProperties(TypedDict):
    """The scientific study and treatment of defects, disorders, and malfunctions of speech and voice, as stuttering, lisping, or lalling, and of language disturbances, as aphasia or delayed language acquisition.

    References:
        https://schema.org/SpeechPathology
    Note:
        Model Depth 6
    Attributes:
    """

    


class SpeechPathologyProperties(TypedDict):
    """The scientific study and treatment of defects, disorders, and malfunctions of speech and voice, as stuttering, lisping, or lalling, and of language disturbances, as aphasia or delayed language acquisition.

    References:
        https://schema.org/SpeechPathology
    Note:
        Model Depth 6
    Attributes:
    """

    

#SpeechPathologyInheritedPropertiesTd = SpeechPathologyInheritedProperties()
#SpeechPathologyPropertiesTd = SpeechPathologyProperties()


class AllProperties(SpeechPathologyInheritedProperties , SpeechPathologyProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[SpeechPathologyProperties, SpeechPathologyInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "SpeechPathology"
    return model
    

SpeechPathology = create_schema_org_model()