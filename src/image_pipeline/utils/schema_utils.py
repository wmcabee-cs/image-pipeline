from image_pipeline.utils.exceptions import ValidationException


def get_schema_fields(schema):
    return frozenset(schema.__dataclass_fields__)


def validate_input_fields(skill, input):
    has_inputs = skill.required_inputs is not None
    if has_inputs:
        missing = get_schema_fields(skill.required_inputs) - frozenset(input)
        if len(missing) > 0:
            raise ValidationException(
                f"{skill} had required input fields not found in the input schema {sorted(missing)}")
    return None


def validate_output_fields(skill, output):
    has_outputs = skill.add_fields is not None
    if has_outputs:
        missing = get_schema_fields(skill.add_fields) - frozenset(output)
        if len(missing) > 0:
            raise ValidationException(
                f"Added fields {sorted(missing)} in {skill} were not found in output dataset")
    return None


def validate_request(schema, request):
    expected_parameters = get_schema_fields(schema)
    missing = expected_parameters - frozenset(request)
    if len(missing) > 0:
        raise ValidationException(
            f"Did not receive {sorted(missing)} in request. Expecting parameters {sorted(expected_parameters)}.")
    return None
