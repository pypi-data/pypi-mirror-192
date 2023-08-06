"""
A medical test performed by a laboratory that typically involves examination of a tissue sample by a pathologist.

https://schema.org/PathologyTest
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class PathologyTestInheritedProperties(TypedDict):
    """A medical test performed by a laboratory that typically involves examination of a tissue sample by a pathologist.

    References:
        https://schema.org/PathologyTest
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
    


class PathologyTestProperties(TypedDict):
    """A medical test performed by a laboratory that typically involves examination of a tissue sample by a pathologist.

    References:
        https://schema.org/PathologyTest
    Note:
        Model Depth 4
    Attributes:
        tissueSample: (Optional[Union[List[Union[str, SchemaOrgObj]], str, SchemaOrgObj]]): The type of tissue sample required for the test.
    """

    tissueSample: NotRequired[Union[List[Union[str, SchemaOrgObj]], str, SchemaOrgObj]]
    

#PathologyTestInheritedPropertiesTd = PathologyTestInheritedProperties()
#PathologyTestPropertiesTd = PathologyTestProperties()


class AllProperties(PathologyTestInheritedProperties , PathologyTestProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[PathologyTestProperties, PathologyTestInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "PathologyTest"
    return model
    

PathologyTest = create_schema_org_model()