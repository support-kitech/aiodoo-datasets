"""Registry of all active Context Protocol validators."""

from aiodoo_datasets.generators.context.validation.schema_validator import SchemaValidator
from aiodoo_datasets.generators.context.validation.protocol_validator import ProtocolValidator
from aiodoo_datasets.generators.context.validation.core_validator import CoreValidator

REGISTERED_VALIDATORS = (
    SchemaValidator,
    ProtocolValidator,
    CoreValidator,
)
