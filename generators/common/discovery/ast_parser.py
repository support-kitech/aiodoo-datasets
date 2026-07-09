"""Parses Python AST to extract comprehensive structural Odoo knowledge."""

import ast
import logging
from dataclasses import dataclass, field
from pathlib import Path

logger = logging.getLogger(__name__)

@dataclass(slots=True)
class OdooFieldDef:
    name: str
    type: str
    args: list[str] = field(default_factory=list)
    kwargs: dict[str, str] = field(default_factory=dict)
    computed: bool = False
    related: str = ""

@dataclass(slots=True)
class OdooMethodDef:
    name: str
    decorators: list[str] = field(default_factory=list)
    raises: list[str] = field(default_factory=list)

@dataclass(slots=True)
class OdooRouteDef:
    route: str
    auth: str = "user"
    methods: list[str] = field(default_factory=list)
    csrf: bool = True

@dataclass(slots=True)
class OdooModelDef:
    name: str
    inherit: list[str] = field(default_factory=list)
    model_type: str = "models.Model"
    fields: dict[str, OdooFieldDef] = field(default_factory=dict)
    methods: dict[str, OdooMethodDef] = field(default_factory=dict)
    sql_constraints: list[str] = field(default_factory=list)

@dataclass(slots=True)
class PythonKnowledge:
    """Represents extracted structural knowledge from a Python module."""
    models: dict[str, OdooModelDef] = field(default_factory=dict)
    routes: dict[str, OdooRouteDef] = field(default_factory=dict)
    imports: list[str] = field(default_factory=list)


class OdooASTVisitor(ast.NodeVisitor):
    def __init__(self):
        self.knowledge = PythonKnowledge()
        self.current_class = None
        self.current_method = None

    def visit_Import(self, node: ast.Import):
        for alias in node.names:
            self.knowledge.imports.append(alias.name)
        self.generic_visit(node)

    def visit_ImportFrom(self, node: ast.ImportFrom):
        if node.module:
            self.knowledge.imports.append(node.module)
        self.generic_visit(node)

    def visit_ClassDef(self, node: ast.ClassDef):
        model_type = "PythonClass"
        inherit = []
        for base in node.bases:
            if isinstance(base, ast.Attribute) and isinstance(base.value, ast.Name):
                if base.value.id == "models":
                    model_type = f"models.{base.attr}"
            elif isinstance(base, ast.Name):
                if base.id in ("Model", "TransientModel", "AbstractModel"):
                    model_type = f"models.{base.id}"
                elif base.id == "Controller":
                    model_type = "http.Controller"
            elif isinstance(base, ast.Attribute) and base.attr == "Controller":
                model_type = "http.Controller"

        model_def = OdooModelDef(name=node.name, model_type=model_type)
        
        for item in node.body:
            if isinstance(item, ast.Assign):
                for target in item.targets:
                    if isinstance(target, ast.Name):
                        if target.id == "_name" and isinstance(item.value, ast.Constant):
                            model_def.name = str(item.value.value)
                        elif target.id == "_inherit":
                            if isinstance(item.value, ast.Constant):
                                model_def.inherit.append(str(item.value.value))
                            elif isinstance(item.value, ast.List):
                                for elt in item.value.elts:
                                    if isinstance(elt, ast.Constant):
                                        model_def.inherit.append(str(elt.value))
                        elif target.id == "_sql_constraints" and isinstance(item.value, ast.List):
                            for elt in item.value.elts:
                                if isinstance(elt, ast.Tuple) and len(elt.elts) >= 1:
                                    if isinstance(elt.elts[0], ast.Constant):
                                        model_def.sql_constraints.append(str(elt.elts[0].value))

        self.knowledge.models[model_def.name] = model_def
        self.current_class = model_def
        self.generic_visit(node)
        self.current_class = None

    def visit_FunctionDef(self, node: ast.FunctionDef):
        if self.current_class:
            decorators = []
            for dec in node.decorator_list:
                if isinstance(dec, ast.Attribute) and isinstance(dec.value, ast.Name) and dec.value.id == "api":
                    decorators.append(f"api.{dec.attr}")
                elif isinstance(dec, ast.Call) and isinstance(dec.func, ast.Attribute) and isinstance(dec.func.value, ast.Name):
                    if dec.func.value.id == "api":
                        decorators.append(f"api.{dec.func.attr}")
                    elif dec.func.value.id == "http" and dec.func.attr == "route":
                        decorators.append("http.route")
                        self._extract_route(dec, node.name)

            method_def = OdooMethodDef(name=node.name, decorators=decorators)
            self.current_class.methods[node.name] = method_def
            self.current_method = method_def
            
        self.generic_visit(node)
        self.current_method = None

    def visit_Raise(self, node: ast.Raise):
        if self.current_method and node.exc:
            if isinstance(node.exc, ast.Call) and isinstance(node.exc.func, ast.Name):
                self.current_method.raises.append(node.exc.func.id)
            elif isinstance(node.exc, ast.Name):
                self.current_method.raises.append(node.exc.id)
        self.generic_visit(node)

    def visit_Assign(self, node: ast.Assign):
        if self.current_class and isinstance(node.value, ast.Call):
            func = node.value.func
            if isinstance(func, ast.Attribute) and isinstance(func.value, ast.Name) and func.value.id == "fields":
                field_type = func.attr
                computed = False
                related = ""
                for kw in node.value.keywords:
                    if kw.arg == "compute":
                        computed = True
                    elif kw.arg == "related" and isinstance(kw.value, ast.Constant):
                        related = str(kw.value.value)
                        
                for target in node.targets:
                    if isinstance(target, ast.Name):
                        self.current_class.fields[target.id] = OdooFieldDef(
                            name=target.id, 
                            type=field_type,
                            computed=computed,
                            related=related
                        )
        self.generic_visit(node)

    def _extract_route(self, call_node: ast.Call, method_name: str) -> None:
        """Extract HTTP route details from the decorator."""
        route_path = "unknown"
        if call_node.args and isinstance(call_node.args[0], ast.Constant):
            route_path = str(call_node.args[0].value)
            
        route_def = OdooRouteDef(route=route_path)
        for kw in call_node.keywords:
            if kw.arg == "auth" and isinstance(kw.value, ast.Constant):
                route_def.auth = str(kw.value.value)
            elif kw.arg == "csrf" and isinstance(kw.value, ast.Constant):
                route_def.csrf = bool(kw.value.value)
            elif kw.arg == "methods" and isinstance(kw.value, ast.List):
                route_def.methods = [str(e.value) for e in kw.value.elts if isinstance(e, ast.Constant)]
                
        self.knowledge.routes[method_name] = route_def


class ModuleKnowledgeList(list):
    """Backwards compatible list that also holds a .files attribute mapping path -> knowledge."""
    def __init__(self, items=None, files_dict=None):
        super().__init__(items or [])
        self.files = files_dict or {}

class OdooASTParser:
    """Parses Odoo Python files using the abstract syntax tree."""

    def parse_module(self, module_path: Path):
        results = []
        files_dict = {}
        if not module_path.is_dir():
            return ModuleKnowledgeList(results, files_dict)

        for py_file in module_path.rglob("*.py"):
            try:
                with open(py_file, "r", encoding="utf-8") as f:
                    content = f.read()
                tree = ast.parse(content, filename=str(py_file))
                visitor = OdooASTVisitor()
                visitor.visit(tree)
                if visitor.knowledge.models or visitor.knowledge.routes:
                    results.append(visitor.knowledge)
                    rel_path = str(py_file.relative_to(module_path))
                    files_dict[rel_path] = visitor.knowledge
            except SyntaxError as exc:
                logger.debug("Syntax error in %s: %s", py_file, exc)
            except Exception as exc:
                logger.debug("Failed to parse %s: %s", py_file, exc)
        return ModuleKnowledgeList(results, files_dict)
