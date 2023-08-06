"""
A Property value specification.

https://schema.org/PropertyValueSpecification
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class PropertyValueSpecificationInheritedProperties(TypedDict):
    """A Property value specification.

    References:
        https://schema.org/PropertyValueSpecification
    Note:
        Model Depth 3
    Attributes:
    """

    


class PropertyValueSpecificationProperties(TypedDict):
    """A Property value specification.

    References:
        https://schema.org/PropertyValueSpecification
    Note:
        Model Depth 3
    Attributes:
        valuePattern: (Optional[Union[List[Union[str, SchemaOrgObj]], str, SchemaOrgObj]]): Specifies a regular expression for testing literal values according to the HTML spec.
        readonlyValue: (Optional[Union[List[Union[StrictBool, SchemaOrgObj, str]], StrictBool, SchemaOrgObj, str]]): Whether or not a property is mutable.  Default is false. Specifying this for a property that also has a value makes it act similar to a "hidden" input in an HTML form.
        valueMinLength: (Optional[Union[List[Union[SchemaOrgObj, str, StrictInt, StrictFloat]], SchemaOrgObj, str, StrictInt, StrictFloat]]): Specifies the minimum allowed range for number of characters in a literal value.
        valueName: (Optional[Union[List[Union[str, SchemaOrgObj]], str, SchemaOrgObj]]): Indicates the name of the PropertyValueSpecification to be used in URL templates and form encoding in a manner analogous to HTML's input@name.
        maxValue: (Optional[Union[List[Union[SchemaOrgObj, str, StrictInt, StrictFloat]], SchemaOrgObj, str, StrictInt, StrictFloat]]): The upper value of some characteristic or property.
        valueMaxLength: (Optional[Union[List[Union[SchemaOrgObj, str, StrictInt, StrictFloat]], SchemaOrgObj, str, StrictInt, StrictFloat]]): Specifies the allowed range for number of characters in a literal value.
        valueRequired: (Optional[Union[List[Union[StrictBool, SchemaOrgObj, str]], StrictBool, SchemaOrgObj, str]]): Whether the property must be filled in to complete the action.  Default is false.
        stepValue: (Optional[Union[List[Union[SchemaOrgObj, str, StrictInt, StrictFloat]], SchemaOrgObj, str, StrictInt, StrictFloat]]): The stepValue attribute indicates the granularity that is expected (and required) of the value in a PropertyValueSpecification.
        defaultValue: (Optional[Union[List[Union[str, SchemaOrgObj]], str, SchemaOrgObj]]): The default value of the input.  For properties that expect a literal, the default is a literal value, for properties that expect an object, it's an ID reference to one of the current values.
        multipleValues: (Optional[Union[List[Union[StrictBool, SchemaOrgObj, str]], StrictBool, SchemaOrgObj, str]]): Whether multiple values are allowed for the property.  Default is false.
        minValue: (Optional[Union[List[Union[SchemaOrgObj, str, StrictInt, StrictFloat]], SchemaOrgObj, str, StrictInt, StrictFloat]]): The lower value of some characteristic or property.
    """

    valuePattern: NotRequired[Union[List[Union[str, SchemaOrgObj]], str, SchemaOrgObj]]
    readonlyValue: NotRequired[Union[List[Union[StrictBool, SchemaOrgObj, str]], StrictBool, SchemaOrgObj, str]]
    valueMinLength: NotRequired[Union[List[Union[SchemaOrgObj, str, StrictInt, StrictFloat]], SchemaOrgObj, str, StrictInt, StrictFloat]]
    valueName: NotRequired[Union[List[Union[str, SchemaOrgObj]], str, SchemaOrgObj]]
    maxValue: NotRequired[Union[List[Union[SchemaOrgObj, str, StrictInt, StrictFloat]], SchemaOrgObj, str, StrictInt, StrictFloat]]
    valueMaxLength: NotRequired[Union[List[Union[SchemaOrgObj, str, StrictInt, StrictFloat]], SchemaOrgObj, str, StrictInt, StrictFloat]]
    valueRequired: NotRequired[Union[List[Union[StrictBool, SchemaOrgObj, str]], StrictBool, SchemaOrgObj, str]]
    stepValue: NotRequired[Union[List[Union[SchemaOrgObj, str, StrictInt, StrictFloat]], SchemaOrgObj, str, StrictInt, StrictFloat]]
    defaultValue: NotRequired[Union[List[Union[str, SchemaOrgObj]], str, SchemaOrgObj]]
    multipleValues: NotRequired[Union[List[Union[StrictBool, SchemaOrgObj, str]], StrictBool, SchemaOrgObj, str]]
    minValue: NotRequired[Union[List[Union[SchemaOrgObj, str, StrictInt, StrictFloat]], SchemaOrgObj, str, StrictInt, StrictFloat]]
    

#PropertyValueSpecificationInheritedPropertiesTd = PropertyValueSpecificationInheritedProperties()
#PropertyValueSpecificationPropertiesTd = PropertyValueSpecificationProperties()


class AllProperties(PropertyValueSpecificationInheritedProperties , PropertyValueSpecificationProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[PropertyValueSpecificationProperties, PropertyValueSpecificationInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "PropertyValueSpecification"
    return model
    

PropertyValueSpecification = create_schema_org_model()