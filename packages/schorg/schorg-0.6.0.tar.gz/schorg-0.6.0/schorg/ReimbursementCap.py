"""
The drug's cost represents the maximum reimbursement paid by an insurer for the drug.

https://schema.org/ReimbursementCap
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class ReimbursementCapInheritedProperties(TypedDict):
    """The drug's cost represents the maximum reimbursement paid by an insurer for the drug.

    References:
        https://schema.org/ReimbursementCap
    Note:
        Model Depth 6
    Attributes:
    """

    


class ReimbursementCapProperties(TypedDict):
    """The drug's cost represents the maximum reimbursement paid by an insurer for the drug.

    References:
        https://schema.org/ReimbursementCap
    Note:
        Model Depth 6
    Attributes:
    """

    

#ReimbursementCapInheritedPropertiesTd = ReimbursementCapInheritedProperties()
#ReimbursementCapPropertiesTd = ReimbursementCapProperties()


class AllProperties(ReimbursementCapInheritedProperties , ReimbursementCapProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[ReimbursementCapProperties, ReimbursementCapInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "ReimbursementCap"
    return model
    

ReimbursementCap = create_schema_org_model()