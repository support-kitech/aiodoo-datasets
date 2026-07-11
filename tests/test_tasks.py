"""Tests for the Protocol Task Dependency Graph Builder."""

from generators.planner.protocol.task_builder import build_tasks
from generators.planner.discovery.ast_parser import PythonKnowledge, OdooModelDef, OdooFieldDef, OdooMethodDef
from generators.planner.discovery.xml_parser import XMLKnowledge, OdooViewDef, OdooActionDef, OdooMenuDef, OdooSecurityDef

def test_task_topological_graph():
    # Setup mock data simulating a full module
    py_k = PythonKnowledge()
    py_k.models["my.model"] = OdooModelDef(
        name="my.model",
        model_type="models.Model",
        fields={"name": OdooFieldDef(name="name", type="Char")},
        methods={"my_method": OdooMethodDef(name="my_method")}
    )
    
    xml_k = XMLKnowledge()
    xml_k.security_rules.append(OdooSecurityDef(id="rule1", model="my.model"))
    xml_k.views.append(OdooViewDef(id="view1", model="my.model", view_type="form"))
    xml_k.actions.append(OdooActionDef(id="action1", action_type="ir.actions.act_window", model="my.model"))
    xml_k.menus.append(OdooMenuDef(id="menu1", action="action1"))
    
    tasks = build_tasks([py_k], [xml_k])
    
    # We expect: Model -> Fields -> Methods -> Security -> View -> Action -> Menu -> Test
    # Let's verify IDs and dependencies
    task_dict = {t.title: t for t in tasks}
    
    # 1. Model
    model_task = task_dict["Create Model: my.model"]
    assert model_task.dependencies == []
    
    # 2. Fields
    fields_task = task_dict["Create Fields for my.model"]
    assert model_task.id in fields_task.dependencies
    
    # 3. Methods (Business Logic)
    methods_task = task_dict["Implement Business Logic for my.model"]
    assert fields_task.id in methods_task.dependencies
    
    # 4. Security
    sec_task = task_dict["Configure Access Rights & Security Rules"]
    # Depends on model phase
    assert any(dep in sec_task.dependencies for dep in [model_task.id, fields_task.id, methods_task.id])
    
    # 5. View
    view_task = task_dict["Create Form View: my.model"]
    assert sec_task.id in view_task.dependencies
    
    # 6. Action
    action_task = task_dict["Create Window Action: action1"]
    assert view_task.id in action_task.dependencies
    
    # 7. Menu
    menu_task = task_dict["Create Menu Item: menu1"]
    assert action_task.id in menu_task.dependencies
    
    # 8. Test
    test_task = task_dict["Implement Unit Tests"]
    assert menu_task.id in test_task.dependencies
