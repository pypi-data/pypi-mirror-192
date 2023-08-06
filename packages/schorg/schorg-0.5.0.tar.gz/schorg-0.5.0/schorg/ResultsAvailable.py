"""
Results are available.

https://schema.org/ResultsAvailable
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class ResultsAvailableInheritedProperties(TypedDict):
    """Results are available.

    References:
        https://schema.org/ResultsAvailable
    Note:
        Model Depth 6
    Attributes:
    """

    


class ResultsAvailableProperties(TypedDict):
    """Results are available.

    References:
        https://schema.org/ResultsAvailable
    Note:
        Model Depth 6
    Attributes:
    """

    

#ResultsAvailableInheritedPropertiesTd = ResultsAvailableInheritedProperties()
#ResultsAvailablePropertiesTd = ResultsAvailableProperties()


class AllProperties(ResultsAvailableInheritedProperties , ResultsAvailableProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[ResultsAvailableProperties, ResultsAvailableInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "ResultsAvailable"
    return model
    

ResultsAvailable = create_schema_org_model()