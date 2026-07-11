"""Registry of all active Context Protocol validators."""

from generators.context.validation.schema_validator import SchemaValidator
from generators.context.validation.protocol_validator import ProtocolValidator
from generators.context.validation.core_validator import CoreValidator

REGISTERED_VALIDATORS = (
    SchemaValidator,
    ProtocolValidator,
    CoreValidator,
)
