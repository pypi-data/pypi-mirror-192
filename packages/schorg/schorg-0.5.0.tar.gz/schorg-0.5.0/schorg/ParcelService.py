"""
A private parcel service as the delivery mode available for a certain offer.Commonly used values:* http://purl.org/goodrelations/v1#DHL* http://purl.org/goodrelations/v1#FederalExpress* http://purl.org/goodrelations/v1#UPS      

https://schema.org/ParcelService
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class ParcelServiceInheritedProperties(TypedDict):
    """A private parcel service as the delivery mode available for a certain offer.Commonly used values:* http://purl.org/goodrelations/v1#DHL* http://purl.org/goodrelations/v1#FederalExpress* http://purl.org/goodrelations/v1#UPS      

    References:
        https://schema.org/ParcelService
    Note:
        Model Depth 5
    Attributes:
    """

    


class ParcelServiceProperties(TypedDict):
    """A private parcel service as the delivery mode available for a certain offer.Commonly used values:* http://purl.org/goodrelations/v1#DHL* http://purl.org/goodrelations/v1#FederalExpress* http://purl.org/goodrelations/v1#UPS      

    References:
        https://schema.org/ParcelService
    Note:
        Model Depth 5
    Attributes:
    """

    

#ParcelServiceInheritedPropertiesTd = ParcelServiceInheritedProperties()
#ParcelServicePropertiesTd = ParcelServiceProperties()


class AllProperties(ParcelServiceInheritedProperties , ParcelServiceProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[ParcelServiceProperties, ParcelServiceInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "ParcelService"
    return model
    

ParcelService = create_schema_org_model()