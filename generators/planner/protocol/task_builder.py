"""Generates Protocol V1 TaskSpec objects from structural knowledge."""

from typing import Sequence

from generators.planner.validation.schema import TaskSpec
from generators.common.discovery.ast_parser import PythonKnowledge
from generators.common.discovery.xml_parser import XMLKnowledge


def build_tasks(
    python_data: Sequence[PythonKnowledge], xml_data: Sequence[XMLKnowledge]
) -> list[TaskSpec]:
    """Deconstruct structural knowledge into topologically sorted executable tasks."""
    tasks = []
    task_id_counter = 1

    def next_id():  # type: ignore[no-untyped-def]
        nonlocal task_id_counter
        val = task_id_counter
        task_id_counter += 1
        return f"t{val}"

    # Phase 1: Models & Business Logic
    model_task_ids = []
    for py_k in python_data:
        for model_name, model_def in py_k.models.items():
            if model_def.model_type == "models.TransientModel":
                title = f"Define Wizard Model: {model_name}"
            elif model_def.inherit and model_name in model_def.inherit:
                title = f"Extend Existing Model: {model_name}"
            else:
                title = f"Create Model: {model_name}"

            tid = next_id()  # type: ignore[no-untyped-call]
            tasks.append(
                TaskSpec(
                    id=tid,
                    title=title,
                    description=f"Define the {model_def.model_type} architecture for {model_name}.",
                    complexity=3,
                    dependencies=[],
                    estimated_files=1,
                    estimated_time=15,
                )
            )
            model_task_ids.append(tid)

            if model_def.fields:
                ftid = next_id()  # type: ignore[no-untyped-call]
                tasks.append(
                    TaskSpec(
                        id=ftid,
                        title=f"Create Fields for {model_name}",
                        description=f"Implement {len(model_def.fields)} fields for {model_name}.",
                        complexity=2,
                        dependencies=[tid],
                        estimated_files=1,
                        estimated_time=15,
                    )
                )
                model_task_ids.append(ftid)

            if model_def.methods:
                mtid = next_id()  # type: ignore[no-untyped-call]
                tasks.append(
                    TaskSpec(
                        id=mtid,
                        title=f"Implement Business Logic for {model_name}",
                        description=f"Implement {len(model_def.methods)} methods for {model_name}.",
                        complexity=4,
                        dependencies=[ftid if model_def.fields else tid],
                        estimated_files=1,
                        estimated_time=30,
                    )
                )
                model_task_ids.append(mtid)

    # Phase 2: Security Rules
    security_task_ids = []
    for xml_k in xml_data:
        if xml_k.security_rules:
            tid = next_id()  # type: ignore[no-untyped-call]
            tasks.append(
                TaskSpec(
                    id=tid,
                    title="Configure Access Rights & Security Rules",
                    description=f"Define {len(xml_k.security_rules)} security definitions.",
                    complexity=2,
                    dependencies=model_task_ids.copy(),
                    estimated_files=1,
                    estimated_time=15,
                )
            )
            security_task_ids.append(tid)

    # Phase 3: Views
    view_deps = model_task_ids + security_task_ids
    view_task_ids = []
    for xml_k in xml_data:
        for view in xml_k.views:
            tid = next_id()  # type: ignore[no-untyped-call]
            tasks.append(
                TaskSpec(
                    id=tid,
                    title=f"Create {view.view_type.capitalize()} View: {view.model}",
                    description=f"Implement XML architecture for {view.id}.",
                    complexity=2,
                    dependencies=view_deps.copy(),
                    estimated_files=1,
                    estimated_time=20,
                )
            )
            view_task_ids.append(tid)

    # Phase 4: Actions
    action_deps = view_task_ids.copy()
    if not action_deps:
        action_deps = view_deps.copy()

    action_task_ids = []
    for xml_k in xml_data:
        for action in xml_k.actions:
            tid = next_id()  # type: ignore[no-untyped-call]
            tasks.append(
                TaskSpec(
                    id=tid,
                    title=f"Create Window Action: {action.id}",
                    description=f"Define {action.action_type} for {action.model}.",
                    complexity=1,
                    dependencies=action_deps.copy(),
                    estimated_files=1,
                    estimated_time=10,
                )
            )
            action_task_ids.append(tid)

    # Phase 5: Menus
    menu_deps = action_task_ids.copy()
    if not menu_deps:
        menu_deps = action_deps.copy()

    menu_task_ids = []
    for xml_k in xml_data:
        for menu in xml_k.menus:
            tid = next_id()  # type: ignore[no-untyped-call]
            tasks.append(
                TaskSpec(
                    id=tid,
                    title=f"Create Menu Item: {menu.name or menu.id}",
                    description=f"Link menu {menu.id} to its corresponding action.",
                    complexity=1,
                    dependencies=menu_deps.copy(),
                    estimated_files=1,
                    estimated_time=5,
                )
            )
            menu_task_ids.append(tid)

    # Phase 6: HTTP Routes/Controllers
    controller_task_ids = []
    for py_k in python_data:
        for route_name, route_def in py_k.routes.items():
            tid = next_id()  # type: ignore[no-untyped-call]
            tasks.append(
                TaskSpec(
                    id=tid,
                    title=f"Implement HTTP Route: {route_def.route}",
                    description=f"Create controller route with auth={route_def.auth}",
                    complexity=3,
                    dependencies=model_task_ids.copy(),
                    estimated_files=1,
                    estimated_time=45,
                )
            )
            controller_task_ids.append(tid)

    # Phase 7: Tests
    all_previous_ids = [t.id for t in tasks]
    if all_previous_ids:
        tid = next_id()  # type: ignore[no-untyped-call]
        tasks.append(
            TaskSpec(
                id=tid,
                title="Implement Unit Tests",
                description="Create test coverage for the implemented logic.",
                complexity=3,
                dependencies=all_previous_ids,
                estimated_files=1,
                estimated_time=30,
            )
        )

    # Fallback task if absolutely nothing was extracted
    if not tasks:
        tasks.append(
            TaskSpec(
                id="t1",
                title="Scaffold Module Architecture",
                description="Initialize standard module files and structure.",
                complexity=1,
                dependencies=[],
                estimated_files=2,
                estimated_time=10,
            )
        )

    return tasks
