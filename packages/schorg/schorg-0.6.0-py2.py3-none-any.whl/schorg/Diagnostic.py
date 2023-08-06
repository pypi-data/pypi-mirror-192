"""
A medical device used for diagnostic purposes.

https://schema.org/Diagnostic
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class DiagnosticInheritedProperties(TypedDict):
    """A medical device used for diagnostic purposes.

    References:
        https://schema.org/Diagnostic
    Note:
        Model Depth 6
    Attributes:
    """

    


class DiagnosticProperties(TypedDict):
    """A medical device used for diagnostic purposes.

    References:
        https://schema.org/Diagnostic
    Note:
        Model Depth 6
    Attributes:
    """

    

#DiagnosticInheritedPropertiesTd = DiagnosticInheritedProperties()
#DiagnosticPropertiesTd = DiagnosticProperties()


class AllProperties(DiagnosticInheritedProperties , DiagnosticProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[DiagnosticProperties, DiagnosticInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "Diagnostic"
    return model
    

Diagnostic = create_schema_org_model()