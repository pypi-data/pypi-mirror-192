"""
Book format: Paperback.

https://schema.org/Paperback
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class PaperbackInheritedProperties(TypedDict):
    """Book format: Paperback.

    References:
        https://schema.org/Paperback
    Note:
        Model Depth 5
    Attributes:
    """

    


class PaperbackProperties(TypedDict):
    """Book format: Paperback.

    References:
        https://schema.org/Paperback
    Note:
        Model Depth 5
    Attributes:
    """

    

#PaperbackInheritedPropertiesTd = PaperbackInheritedProperties()
#PaperbackPropertiesTd = PaperbackProperties()


class AllProperties(PaperbackInheritedProperties , PaperbackProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[PaperbackProperties, PaperbackInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "Paperback"
    return model
    

Paperback = create_schema_org_model()