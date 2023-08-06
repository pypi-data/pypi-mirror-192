"""
Indicated that a return label must be downloaded and printed by the customer.

https://schema.org/ReturnLabelDownloadAndPrint
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class ReturnLabelDownloadAndPrintInheritedProperties(TypedDict):
    """Indicated that a return label must be downloaded and printed by the customer.

    References:
        https://schema.org/ReturnLabelDownloadAndPrint
    Note:
        Model Depth 5
    Attributes:
    """

    


class ReturnLabelDownloadAndPrintProperties(TypedDict):
    """Indicated that a return label must be downloaded and printed by the customer.

    References:
        https://schema.org/ReturnLabelDownloadAndPrint
    Note:
        Model Depth 5
    Attributes:
    """

    

#ReturnLabelDownloadAndPrintInheritedPropertiesTd = ReturnLabelDownloadAndPrintInheritedProperties()
#ReturnLabelDownloadAndPrintPropertiesTd = ReturnLabelDownloadAndPrintProperties()


class AllProperties(ReturnLabelDownloadAndPrintInheritedProperties , ReturnLabelDownloadAndPrintProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[ReturnLabelDownloadAndPrintProperties, ReturnLabelDownloadAndPrintInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "ReturnLabelDownloadAndPrint"
    return model
    

ReturnLabelDownloadAndPrint = create_schema_org_model()