"""
A delivery method is a standardized procedure for transferring the product or service to the destination of fulfillment chosen by the customer. Delivery methods are characterized by the means of transportation used, and by the organization or group that is the contracting party for the sending organization or person.Commonly used values:* http://purl.org/goodrelations/v1#DeliveryModeDirectDownload* http://purl.org/goodrelations/v1#DeliveryModeFreight* http://purl.org/goodrelations/v1#DeliveryModeMail* http://purl.org/goodrelations/v1#DeliveryModeOwnFleet* http://purl.org/goodrelations/v1#DeliveryModePickUp* http://purl.org/goodrelations/v1#DHL* http://purl.org/goodrelations/v1#FederalExpress* http://purl.org/goodrelations/v1#UPS        

https://schema.org/DeliveryMethod
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class DeliveryMethodInheritedProperties(TypedDict):
    """A delivery method is a standardized procedure for transferring the product or service to the destination of fulfillment chosen by the customer. Delivery methods are characterized by the means of transportation used, and by the organization or group that is the contracting party for the sending organization or person.Commonly used values:* http://purl.org/goodrelations/v1#DeliveryModeDirectDownload* http://purl.org/goodrelations/v1#DeliveryModeFreight* http://purl.org/goodrelations/v1#DeliveryModeMail* http://purl.org/goodrelations/v1#DeliveryModeOwnFleet* http://purl.org/goodrelations/v1#DeliveryModePickUp* http://purl.org/goodrelations/v1#DHL* http://purl.org/goodrelations/v1#FederalExpress* http://purl.org/goodrelations/v1#UPS        

    References:
        https://schema.org/DeliveryMethod
    Note:
        Model Depth 4
    Attributes:
        supersededBy: (Optional[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]): Relates a term (i.e. a property, class or enumeration) to one that supersedes it.
    """

    supersededBy: NotRequired[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]
    


class DeliveryMethodProperties(TypedDict):
    """A delivery method is a standardized procedure for transferring the product or service to the destination of fulfillment chosen by the customer. Delivery methods are characterized by the means of transportation used, and by the organization or group that is the contracting party for the sending organization or person.Commonly used values:* http://purl.org/goodrelations/v1#DeliveryModeDirectDownload* http://purl.org/goodrelations/v1#DeliveryModeFreight* http://purl.org/goodrelations/v1#DeliveryModeMail* http://purl.org/goodrelations/v1#DeliveryModeOwnFleet* http://purl.org/goodrelations/v1#DeliveryModePickUp* http://purl.org/goodrelations/v1#DHL* http://purl.org/goodrelations/v1#FederalExpress* http://purl.org/goodrelations/v1#UPS        

    References:
        https://schema.org/DeliveryMethod
    Note:
        Model Depth 4
    Attributes:
    """

    

#DeliveryMethodInheritedPropertiesTd = DeliveryMethodInheritedProperties()
#DeliveryMethodPropertiesTd = DeliveryMethodProperties()


class AllProperties(DeliveryMethodInheritedProperties , DeliveryMethodProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[DeliveryMethodProperties, DeliveryMethodInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "DeliveryMethod"
    return model
    

DeliveryMethod = create_schema_org_model()