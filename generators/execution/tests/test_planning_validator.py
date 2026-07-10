import unittest
from aiodoo_datasets.generators.execution.validation.planning_validator import PlanningValidator
from aiodoo_datasets.generators.execution.planning.domain.execution_plan import PlannedExecution
from aiodoo_datasets.generators.execution.planning.domain.execution_schedule import ExecutionSchedule

class TestPlanningValidator(unittest.TestCase):
    def test_validation(self):
        plan = PlannedExecution(plan_id="p1", graph_id="g1", schedules=())
        violations = PlanningValidator.validate(plan)
        self.assertTrue(len(violations) > 0)
        self.assertIn("has no schedules", violations[0])
        
        sch = ExecutionSchedule(schedule_id="s1", strategy="seq", batches=())
        plan2 = PlannedExecution(plan_id="p1", graph_id="g1", schedules=(sch,))
        violations2 = PlanningValidator.validate(plan2)
        self.assertTrue(len(violations2) > 0)
        self.assertIn("has no batches", violations2[0])

if __name__ == '__main__':
    unittest.main()
