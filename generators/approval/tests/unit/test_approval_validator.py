"""Unit tests for ApprovalValidator."""

import unittest
from aiodoo_datasets.generators.approval.validation.approval_validator import ApprovalValidator
from aiodoo_datasets.generators.approval.exceptions import ApprovalValidationError


class TestApprovalValidator(unittest.TestCase):
    def test_validate_all_fails_fast_on_review(self) -> None:
        # We can test that passing None or invalid types raises ApprovalValidationError
        with self.assertRaises(ApprovalValidationError):
            ApprovalValidator.validate_all(None, None)
