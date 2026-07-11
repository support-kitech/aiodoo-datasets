from generators.execution.builders.results.verification_build_result import (
    VerificationBuildResult,
)


class VerificationValidator:
    """Validates ExecutionVerification domain objects."""

    @classmethod
    def validate(cls, result: VerificationBuildResult) -> None:
        pass
