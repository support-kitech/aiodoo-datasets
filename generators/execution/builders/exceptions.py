class BuilderError(Exception):
    """Base exception for all Builder-related execution failures."""
    pass

class InvalidKnowledgeError(BuilderError):
    """Raised when upstream Knowledge is fundamentally malformed or missing."""
    pass

class FactoryError(BuilderError):
    """Raised when a Factory fails to instantiate an immutable Domain Object."""
    pass

class BuilderValidationError(BuilderError):
    """Raised when a Validator detects anomalous or corrupted Domain states post-build."""
    pass
