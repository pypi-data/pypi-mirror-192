"""
Results are not available.

https://schema.org/ResultsNotAvailable
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class ResultsNotAvailableInheritedProperties(TypedDict):
    """Results are not available.

    References:
        https://schema.org/ResultsNotAvailable
    Note:
        Model Depth 6
    Attributes:
    """

    


class ResultsNotAvailableProperties(TypedDict):
    """Results are not available.

    References:
        https://schema.org/ResultsNotAvailable
    Note:
        Model Depth 6
    Attributes:
    """

    

#ResultsNotAvailableInheritedPropertiesTd = ResultsNotAvailableInheritedProperties()
#ResultsNotAvailablePropertiesTd = ResultsNotAvailableProperties()


class AllProperties(ResultsNotAvailableInheritedProperties , ResultsNotAvailableProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[ResultsNotAvailableProperties, ResultsNotAvailableInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "ResultsNotAvailable"
    return model
    

ResultsNotAvailable = create_schema_org_model()