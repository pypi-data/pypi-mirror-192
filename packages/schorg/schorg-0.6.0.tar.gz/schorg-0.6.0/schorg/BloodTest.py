"""
A medical test performed on a sample of a patient's blood.

https://schema.org/BloodTest
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class BloodTestInheritedProperties(TypedDict):
    """A medical test performed on a sample of a patient's blood.

    References:
        https://schema.org/BloodTest
    Note:
        Model Depth 4
    Attributes:
        affectedBy: (Optional[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]): Drugs that affect the test's results.
        normalRange: (Optional[Union[List[Union[str, SchemaOrgObj]], str, SchemaOrgObj]]): Range of acceptable values for a typical patient, when applicable.
        signDetected: (Optional[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]): A sign detected by the test.
        usedToDiagnose: (Optional[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]): A condition the test is used to diagnose.
        usesDevice: (Optional[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]): Device used to perform the test.
    """

    affectedBy: NotRequired[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]
    normalRange: NotRequired[Union[List[Union[str, SchemaOrgObj]], str, SchemaOrgObj]]
    signDetected: NotRequired[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]
    usedToDiagnose: NotRequired[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]
    usesDevice: NotRequired[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]
    


class BloodTestProperties(TypedDict):
    """A medical test performed on a sample of a patient's blood.

    References:
        https://schema.org/BloodTest
    Note:
        Model Depth 4
    Attributes:
    """

    

#BloodTestInheritedPropertiesTd = BloodTestInheritedProperties()
#BloodTestPropertiesTd = BloodTestProperties()


class AllProperties(BloodTestInheritedProperties , BloodTestProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[BloodTestProperties, BloodTestInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "BloodTest"
    return model
    

BloodTest = create_schema_org_model()