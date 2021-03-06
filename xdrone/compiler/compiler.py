import copy
from typing import List, Optional, Dict

from antlr.xDroneParser import xDroneParser
from antlr.xDroneParserVisitor import xDroneParserVisitor
from xdrone.compiler.compiler_utils.drones import NullDrone, Drone
from xdrone.compiler.compiler_utils.expressions import Identifier, ListElem, VectorElem, Expression
from xdrone.compiler.compiler_utils.functions import FunctionTable, Function, Parameter, FunctionIdentifier
from xdrone.compiler.compiler_utils.symbol_table import SymbolTable
from xdrone.compiler.compiler_utils.type import Type, ListType, EmptyList
from xdrone.shared.command import Command, SingleDroneCommand, ParallelDroneCommands, AbstractDroneCommand, \
    RepeatDroneNameException
from xdrone.shared.compile_error import CompileError
from xdrone.shared.drone_config import DroneConfig


class Compiler(xDroneParserVisitor):

    def __init__(self, drone_config_map: Dict[str, DroneConfig],
                 symbol_table: SymbolTable, function_table: FunctionTable):
        super().__init__()

        self.drones = {name: Drone(name, config) for name, config in drone_config_map.items()}  # global constant table
        self.symbol_table = [symbol_table]
        self.function_table = function_table

        self.returned = [False]
        self.returned_value = []

        self.commands = [[]]

    def _get_latest_symbol_table(self):
        return self.symbol_table[-1]

    def _get_latest_commands(self):
        return self.commands[-1]

    ######## prog ########

    def visitProg(self, ctx: xDroneParser.ProgContext) -> List[AbstractDroneCommand]:
        for func in ctx.func():
            self.visit(func)
        self.visit(ctx.commands())
        assert len(self.commands) == 1
        commands = self.commands[0]
        return commands

    ######## commands ########

    def visitCommands(self, ctx: xDroneParser.CommandsContext) -> None:
        for command in ctx.command():
            if self.returned[-1]:
                break
            self.visit(command)

    ######## command ########

    def _get_drone_name(self, expr: Optional[Expression]):
        if expr is not None:
            if expr.type != Type.drone():
                raise CompileError("Expression {} should have type drone, but is {}".format(expr, expr.type))
            if isinstance(expr.value, NullDrone):
                raise CompileError("Drone has not been assigned".format(expr, expr.type))

            drone_name = expr.value.name
        elif expr is None and len(self.drones) == 1:
            drone_name = list(self.drones.keys())[0]
        else:
            raise CompileError("Drone should be specified if there are multiple drones in config")
        return drone_name

    def visitTakeoff(self, ctx: xDroneParser.TakeoffContext) -> None:
        expr = self.visit(ctx.expr()) if ctx.expr() else None
        drone_name = self._get_drone_name(expr)
        self._get_latest_commands().append(SingleDroneCommand(drone_name, Command.takeoff()))

    def visitLand(self, ctx: xDroneParser.LandContext) -> None:
        exprs = self.visit(ctx.expr()) if ctx.expr() else None
        drone_name = self._get_drone_name(exprs)
        self._get_latest_commands().append(SingleDroneCommand(drone_name, Command.land()))

    def visitUp(self, ctx: xDroneParser.UpContext) -> None:
        exprs = [self.visit(expr) for expr in ctx.expr()]
        if ctx.DOT():
            drone_expr, expr = exprs
        else:
            drone_expr, expr = None, exprs[0]
        if expr.type != Type.int() and expr.type != Type.decimal():
            raise CompileError("Expression {} should have type int or decimal, but is {}".format(expr, expr.type))
        drone_name = self._get_drone_name(drone_expr)
        self._get_latest_commands().append(SingleDroneCommand(drone_name, Command.up(expr.value)))

    def visitDown(self, ctx: xDroneParser.DownContext) -> None:
        exprs = [self.visit(expr) for expr in ctx.expr()]
        if ctx.DOT():
            drone_expr, expr = exprs
        else:
            drone_expr, expr = None, exprs[0]
        if expr.type != Type.int() and expr.type != Type.decimal():
            raise CompileError("Expression {} should have type int or decimal, but is {}".format(expr, expr.type))
        drone_name = self._get_drone_name(drone_expr)
        self._get_latest_commands().append(SingleDroneCommand(drone_name, Command.down(expr.value)))

    def visitLeft(self, ctx: xDroneParser.LeftContext) -> None:
        exprs = [self.visit(expr) for expr in ctx.expr()]
        if ctx.DOT():
            drone_expr, expr = exprs
        else:
            drone_expr, expr = None, exprs[0]
        if expr.type != Type.int() and expr.type != Type.decimal():
            raise CompileError("Expression {} should have type int or decimal, but is {}".format(expr, expr.type))
        drone_name = self._get_drone_name(drone_expr)
        self._get_latest_commands().append(SingleDroneCommand(drone_name, Command.left(expr.value)))

    def visitRight(self, ctx: xDroneParser.RightContext) -> None:
        exprs = [self.visit(expr) for expr in ctx.expr()]
        if ctx.DOT():
            drone_expr, expr = exprs
        else:
            drone_expr, expr = None, exprs[0]
        if expr.type != Type.int() and expr.type != Type.decimal():
            raise CompileError("Expression {} should have type int or decimal, but is {}".format(expr, expr.type))
        drone_name = self._get_drone_name(drone_expr)
        self._get_latest_commands().append(SingleDroneCommand(drone_name, Command.right(expr.value)))

    def visitForward(self, ctx: xDroneParser.ForwardContext) -> None:
        exprs = [self.visit(expr) for expr in ctx.expr()]
        if ctx.DOT():
            drone_expr, expr = exprs
        else:
            drone_expr, expr = None, exprs[0]
        if expr.type != Type.int() and expr.type != Type.decimal():
            raise CompileError("Expression {} should have type int or decimal, but is {}".format(expr, expr.type))
        drone_name = self._get_drone_name(drone_expr)
        self._get_latest_commands().append(SingleDroneCommand(drone_name, Command.forward(expr.value)))

    def visitBackward(self, ctx: xDroneParser.BackwardContext) -> None:
        exprs = [self.visit(expr) for expr in ctx.expr()]
        if ctx.DOT():
            drone_expr, expr = exprs
        else:
            drone_expr, expr = None, exprs[0]
        if expr.type != Type.int() and expr.type != Type.decimal():
            raise CompileError("Expression {} should have type int or decimal, but is {}".format(expr, expr.type))
        drone_name = self._get_drone_name(drone_expr)
        self._get_latest_commands().append(SingleDroneCommand(drone_name, Command.backward(expr.value)))

    def visitRotateLeft(self, ctx: xDroneParser.RotateLeftContext) -> None:
        exprs = [self.visit(expr) for expr in ctx.expr()]
        if ctx.DOT():
            drone_expr, expr = exprs
        else:
            drone_expr, expr = None, exprs[0]
        if expr.type != Type.int() and expr.type != Type.decimal():
            raise CompileError("Expression {} should have type int or decimal, but is {}".format(expr, expr.type))
        drone_name = self._get_drone_name(drone_expr)
        self._get_latest_commands().append(SingleDroneCommand(drone_name, Command.rotate_left(expr.value)))

    def visitRotateRight(self, ctx: xDroneParser.RotateRightContext) -> None:
        exprs = [self.visit(expr) for expr in ctx.expr()]
        if ctx.DOT():
            drone_expr, expr = exprs
        else:
            drone_expr, expr = None, exprs[0]
        if expr.type != Type.int() and expr.type != Type.decimal():
            raise CompileError("Expression {} should have type int or decimal, but is {}".format(expr, expr.type))
        drone_name = self._get_drone_name(drone_expr)
        self._get_latest_commands().append(SingleDroneCommand(drone_name, Command.rotate_right(expr.value)))

    def visitWait(self, ctx: xDroneParser.WaitContext) -> None:
        exprs = [self.visit(expr) for expr in ctx.expr()]
        if ctx.DOT():
            drone_expr, expr = exprs
        else:
            drone_expr, expr = None, exprs[0]
        if expr.type != Type.int() and expr.type != Type.decimal():
            raise CompileError("Expression {} should have type int or decimal, but is {}".format(expr, expr.type))
        drone_name = self._get_drone_name(drone_expr)
        self._get_latest_commands().append(SingleDroneCommand(drone_name, Command.wait(expr.value)))

    def visitDeclare(self, ctx: xDroneParser.DeclareContext) -> None:
        type, identifier = self.visit(ctx.type_()), self.visit(ctx.ident())
        ident = identifier.ident
        if ident in self._get_latest_symbol_table() or ident in self.drones:
            raise CompileError("Identifier {} already declared".format(ident))
        self._get_latest_symbol_table().store(ident, Expression(type, type.default_value, ident=ident))

    def visitDeclareAssign(self, ctx: xDroneParser.DeclareAssignContext) -> None:
        type, identifier, expr = self.visit(ctx.type_()), self.visit(ctx.ident()), self.visit(ctx.expr())
        ident = identifier.ident
        if ident in self._get_latest_symbol_table() or identifier.ident in self.drones:
            raise CompileError("Identifier {} already declared".format(ident))
        if expr.type != type:
            raise CompileError("Identifier {} has been declared as {}, but assigned as {}"
                               .format(ident, type, expr.type))
        expr_with_ident = Expression(type, expr.value, ident)
        self._get_latest_symbol_table().store(ident, expr_with_ident)

    def _unfold_nested_list(self, ident: str) -> (str, list, list):
        if "[" in ident:
            tokens = ident.split("[")
            ident = tokens[0]
            indices = [int(token.replace("]", "")) for token in tokens[1:]]
        else:
            indices = []
        assert ident in self._get_latest_symbol_table()
        new_list = self._get_latest_symbol_table().get_expression(ident).value
        inner = new_list
        for i in indices:
            inner = inner[i]
        return ident, new_list, inner

    def _insert_nested_ident(self, ident: Optional[str], expr: Expression, index: int) -> None:
        if ident is not None:
            new_ident, new_list, inner = self._unfold_nested_list(ident)
            inner.insert(index, expr.value)
            self._get_latest_symbol_table().update(new_ident, new_list)

    def _remove_nested_ident(self, ident: Optional[str], index: int) -> None:
        if ident is not None:
            new_ident, new_list, inner = self._unfold_nested_list(ident)
            inner.pop(index)
            self._get_latest_symbol_table().update(new_ident, new_list)

    def _update_nested_ident(self, ident: Optional[str], expr: Expression, index: int) -> None:
        if ident is not None:
            new_ident, new_list, inner = self._unfold_nested_list(ident)
            inner[index] = expr.value
            self._get_latest_symbol_table().update(new_ident, new_list)

    def visitAssignVectorElem(self, ctx: xDroneParser.AssignVectorElemContext) -> None:
        vector_elem, expr = self.visit(ctx.vectorElem()), self.visit(ctx.expr())
        ident = vector_elem.ident
        vector = vector_elem.container
        index = vector_elem.index
        if expr.type != Type.int() and expr.type != Type.decimal():
            raise CompileError("Assigned value {} should have type int or decimal, but is {}".format(expr, expr.type))
        decimal_expr = Expression(Type.decimal(), float(expr.value), ident=expr.ident)
        self._update_nested_ident(ident, decimal_expr, index)

    def visitAssignListElem(self, ctx: xDroneParser.AssignListElemContext) -> None:
        list_elem, expr = self.visit(ctx.listElem()), self.visit(ctx.expr())
        ident = list_elem.ident
        list = list_elem.container
        index = list_elem.index
        assigned_type = expr.type
        declared_type = list.type.elem_type
        if assigned_type != declared_type:
            raise CompileError("Assigned value {} should have type {}, but is {}"
                               .format(expr, declared_type, assigned_type))
        self._update_nested_ident(ident, expr, index)

    def visitAssignIdent(self, ctx: xDroneParser.AssignIdentContext) -> None:
        identifier, expr = self.visit(ctx.ident()), self.visit(ctx.expr())
        ident = identifier.ident
        if identifier.ident in self.drones:
            raise CompileError("Identifier {} is a drone constant, cannot be assigned".format(ident))
        if ident not in self._get_latest_symbol_table():
            raise CompileError("Identifier {} has not been declared".format(ident))
        assigned_type = expr.type
        declared_type = self._get_latest_symbol_table().get_expression(ident).type
        if assigned_type != declared_type:
            raise CompileError("Identifier {} has been declared as {}, but assigned as {}"
                               .format(ident, declared_type, assigned_type))
        self._get_latest_symbol_table().update(ident, expr.value)

    def visitDel(self, ctx: xDroneParser.DelContext) -> None:
        identifier = self.visit(ctx.ident())
        ident = identifier.ident
        if identifier.ident in self.drones:
            raise CompileError("Identifier {} is a drone constant, cannot be deleted".format(ident))
        if ident not in self._get_latest_symbol_table():
            raise CompileError("Identifier {} has not been declared".format(ident))
        self._get_latest_symbol_table().delete(ident)

    def visitInsert(self, ctx: xDroneParser.InsertContext) -> None:
        list = self.visit(ctx.expr(0))
        if not isinstance(list.type, ListType):
            raise CompileError("Expression {} should have type list, but is {}".format(list, list.type))
        if ctx.AT():
            index = self.visit(ctx.expr(1))
            value = self.visit(ctx.expr(2))
        else:
            index = Expression(Type.int(), len(list.value))
            value = self.visit(ctx.expr(1))
        if index.type != Type.int():
            raise CompileError("Expression {} should have type int, but is {}".format(index, index.type))
        if index.value > len(list.value) or index.value < 0:
            raise CompileError("List {} has length {}, but has been inserted at out-of-range index {}"
                               .format(list, len(list.value), index.value))
        if not isinstance(list.type, EmptyList) and value.type != list.type.elem_type:
            raise CompileError("List {} has been declared as {}, but inserted with element type {}"
                               .format(list, list.type, value.type))
        self._insert_nested_ident(list.ident, value, index.value)

    def visitRemove(self, ctx: xDroneParser.RemoveContext) -> None:
        list = self.visit(ctx.expr(0))
        if not isinstance(list.type, ListType):
            raise CompileError("Expression {} should have type list, but is {}".format(list, list.type))
        if ctx.AT():
            index = self.visit(ctx.expr(1))
        else:
            index = Expression(Type.int(), len(list.value) - 1)
        if index.type != Type.int():
            raise CompileError("Expression {} should have type int, but is {}".format(index, index.type))
        if index.value >= len(list.value) or index.value < 0:
            raise CompileError("List {} has length {}, but has been removed at out-of-range index {}"
                               .format(list, len(list.value), index.value))
        self._remove_nested_ident(list.ident, index.value)

    def visitProcedureCall(self, ctx: xDroneParser.ProcedureCallContext) -> None:
        call = self.visit(ctx.call())
        if call is not None:
            raise CompileError("Procedure call should not return any expression, but {} is returned".format(call))
        return call

    def _visit_commands_with_scope(self, commands_ctx):
        # keep updates on existing variables, discard new variables
        prev_idents = self._get_latest_symbol_table().idents()
        self.visit(commands_ctx)
        self._get_latest_symbol_table().keep_idents(prev_idents)

    def visitIf(self, ctx: xDroneParser.IfContext) -> None:
        expr = self.visit(ctx.expr())
        if expr.type != Type.boolean():
            raise CompileError("Expression {} should have type boolean, but is {}".format(expr, expr.type))
        if expr.value:
            # scope - keep updates on existing variables, discard new variables
            self._visit_commands_with_scope(ctx.commands(0))
        else:
            if ctx.ELSE():
                # scope - keep updates on existing variables, discard new variables
                self._visit_commands_with_scope(ctx.commands(1))

    def visitWhile(self, ctx: xDroneParser.WhileContext) -> None:
        expr = self.visit(ctx.expr())
        if expr.type != Type.boolean():
            raise CompileError("Expression {} should have type boolean, but is {}".format(expr, expr.type))
        while expr.value:
            # scope - keep updates on existing variables, discard new variables
            self._visit_commands_with_scope(ctx.commands())
            expr = self.visit(ctx.expr())

    def visitFor(self, ctx: xDroneParser.ForContext) -> None:
        identifier, expr1, expr2 = self.visit(ctx.ident()), self.visit(ctx.expr(0)), self.visit(ctx.expr(1))
        ident = identifier.ident
        if ident not in self._get_latest_symbol_table() and ident not in self.drones:
            raise CompileError("Identifier {} has not been declared".format(ident))
        declared_type = self._get_latest_symbol_table().get_expression(ident).type
        if declared_type != Type.int():
            raise CompileError("Identifier {} has been declared as {}, but assigned as {}"
                               .format(ident, declared_type, Type.int()))
        if expr1.type != Type.int():
            raise CompileError("Expression {} should have type int, but is {}".format(expr1, expr1.type))
        if expr2.type != Type.int():
            raise CompileError("Expression {} should have type int, but is {}".format(expr2, expr2.type))

        if ctx.STEP():
            expr3 = self.visit(ctx.expr(2))
            if expr3.type != Type.int():
                raise CompileError("Expression {} should have type int, but is {}".format(expr3, expr3.type))
            step = expr3.value
        else:
            step = 1

        for i in range(expr1.value, expr2.value + 1, step):
            self._get_latest_symbol_table().update(ident, i)
            # scope - keep updates on existing variables, discard new variables
            self._visit_commands_with_scope(ctx.commands())

    def visitRepeat(self, ctx: xDroneParser.RepeatContext) -> None:
        expr = self.visit(ctx.expr())
        if expr.type != Type.int():
            raise CompileError("Expression {} should have type int, but is {}".format(expr, expr.type))
        times = expr.value

        for _ in range(times):
            # scope - keep updates on existing variables, discard new variables
            self._visit_commands_with_scope(ctx.commands())

    def visitReturn(self, ctx: xDroneParser.ReturnContext) -> None:
        if len(self.returned) == 1:
            raise CompileError("Cannot return in the Main function")
        self.returned[-1] = True  # order important
        if ctx.expr():
            expr = self.visit(ctx.expr())
            self.returned_value[-1] = Expression(expr.type, expr.value, ident=None)

    def visitParallel(self, ctx: xDroneParser.ParallelContext) -> None:
        parallel_commands = ParallelDroneCommands()
        for commands in ctx.commands():
            self.commands.append([])

            # scope - discard updates on existing variables, discard new variables
            new_symbol_table = copy.deepcopy(self._get_latest_symbol_table())
            self.symbol_table.append(new_symbol_table)
            self.returned.append(False)
            self.returned_value.append(None)
            self.visit(commands)
            returned_value = self.returned_value.pop(-1)
            self.returned.pop(-1)
            self.symbol_table.pop(-1)
            if returned_value is not None:
                raise CompileError("Parallel branch should not return anything, but {} is returned"
                                   .format(returned_value))

            branch = self.commands.pop(-1)
            try:
                parallel_commands.add(branch)
            except RepeatDroneNameException as e:
                raise CompileError("Parallel branches should have exclusive drone names, "
                                   "but {} appeared in more than one branches"
                                   .format(e.repeated_names))

        self._get_latest_commands().append(parallel_commands)

    ######## ident ########

    def visitIdent(self, ctx: xDroneParser.IdentContext) -> Identifier:
        ident = ctx.IDENT().getText()
        # ident in symbol table will shadow drone constant
        if ident in self._get_latest_symbol_table():
            return Identifier(str(ident), self._get_latest_symbol_table().get_expression(ident))
        if ident in self.drones:
            return Identifier(str(ident), Expression(Type.drone(), self.drones[ident]))
        return Identifier(str(ident), None)

    ######## list_elem ########

    def visitListElem(self, ctx: xDroneParser.ListElemContext) -> ListElem:
        expr1, expr2 = self.visit(ctx.expr(0)), self.visit(ctx.expr(1))
        if not isinstance(expr1.type, ListType):
            raise CompileError("Expression {} should have type list, but is {}".format(expr1, expr1.type))
        if expr2.type != Type.int():
            raise CompileError("Expression {} should have type int, but is {}".format(expr2, expr2.type))
        if expr2.value >= len(expr1.value) or expr2.value < 0:
            raise CompileError("List {} has length {}, but has been assessed with out-of-range index {}"
                               .format(expr1, len(expr1.value), expr2.value))
        return ListElem(expr1.ident, expr1, expr2.value)

    ######## vector_elem ########

    def visitVectorX(self, ctx: xDroneParser.VectorXContext) -> VectorElem:
        expr = self.visit(ctx.expr())
        if expr.type != Type.vector():
            raise CompileError("Expression {} should have type vector, but is {}".format(expr, expr.type))
        return VectorElem(expr.ident, expr, 0)

    def visitVectorY(self, ctx: xDroneParser.VectorYContext) -> VectorElem:
        expr = self.visit(ctx.expr())
        if expr.type != Type.vector():
            raise CompileError("Expression {} should have type vector, but is {}".format(expr, expr.type))
        return VectorElem(expr.ident, expr, 1)

    def visitVectorZ(self, ctx: xDroneParser.VectorZContext) -> VectorElem:
        expr = self.visit(ctx.expr())
        if expr.type != Type.vector():
            raise CompileError("Expression {} should have type vector, but is {}".format(expr, expr.type))
        return VectorElem(expr.ident, expr, 2)

    ######## functions ########

    def visitFuncIdent(self, ctx: xDroneParser.FuncIdentContext):
        ident = ctx.IDENT().getText()
        return FunctionIdentifier(str(ident))

    def visitCall(self, ctx: xDroneParser.CallContext) -> Optional[Expression]:
        func_identifier = self.visit(ctx.funcIdent())
        ident = func_identifier.ident
        arg_list = self.visit(ctx.argList()) if ctx.argList() else []
        if ident not in self.function_table:
            raise CompileError("Function or procedure {} has not been defined".format(ident))
        function = self.function_table.get_function(ident)
        arg_types = [arg.type for arg in arg_list]
        param_types = [param.type for param in function.param_list]
        if arg_types != param_types:
            raise CompileError("Arguments when calling function or procedure {} should have types {}, but is {}"
                               .format(ident, [str(type) for type in param_types], [str(type) for type in arg_types]))
        new_symbol_table = SymbolTable()
        param_idents = [param.ident for param in function.param_list]
        for param_ident, expr in zip(param_idents, arg_list):
            new_symbol_table.store(param_ident, expr)

        self.symbol_table.append(new_symbol_table)
        self.returned.append(False)
        self.returned_value.append(None)
        self.visit(function.get_commands())
        returned_value = self.returned_value.pop(-1)
        self.returned.pop(-1)
        self.symbol_table.pop(-1)
        if function.return_type is None:
            if returned_value is not None:
                raise CompileError("Procedure {} should not return anything, but {} is returned"
                                   .format(ident, returned_value))
            return None
        else:
            if returned_value is None:
                raise CompileError("Function {} has returned type {}, but nothing is returned"
                                   .format(ident, function.return_type))
            if returned_value.type != function.return_type:
                raise CompileError("Function {} has returned type {}, but {} is returned"
                                   .format(ident, function.return_type, returned_value.type))
            return returned_value

    def visitArgList(self, ctx: xDroneParser.ArgListContext) -> List[Expression]:
        exprs = [self.visit(expr) for expr in ctx.expr()]
        return exprs

    def visitFunction(self, ctx: xDroneParser.FunctionContext) -> None:
        func_identifier, return_type = self.visit(ctx.funcIdent()), self.visit(ctx.type_())
        ident = func_identifier.ident
        if ident in self.function_table:
            raise CompileError("Function or procedure {} already defined".format(ident))
        param_list = self.visit(ctx.paramList()) if ctx.paramList() else []
        self.function_table.store(ident, Function(ident, param_list, return_type, ctx.commands()))

    def visitProcedure(self, ctx: xDroneParser.ProcedureContext) -> None:
        func_identifier = self.visit(ctx.funcIdent())
        ident = func_identifier.ident
        if ident in self.function_table:
            raise CompileError("Function or procedure {} already defined".format(ident))
        param_list = self.visit(ctx.paramList()) if ctx.paramList() else []
        self.function_table.store(ident, Function(ident, param_list, None, ctx.commands()))

    def visitParamList(self, ctx: xDroneParser.ParamListContext) -> List[Parameter]:
        types = [self.visit(type) for type in ctx.type_()]
        idents = [self.visit(ident).ident for ident in ctx.ident()]
        if len(idents) != len(set(idents)):
            raise CompileError("Parameter names are duplicated in {}".format(idents))
        parameters = []
        for type, ident in zip(types, idents):
            parameters.append(Parameter(ident, type))
        return parameters

    ######## type ########

    def visitIntType(self, ctx: xDroneParser.IntTypeContext) -> Type:
        return Type.int()

    def visitDecimalType(self, ctx: xDroneParser.DecimalTypeContext) -> Type:
        return Type.decimal()

    def visitStringType(self, ctx: xDroneParser.StringTypeContext) -> Type:
        return Type.string()

    def visitBooleanType(self, ctx: xDroneParser.BooleanTypeContext) -> Type:
        return Type.boolean()

    def visitVectorType(self, ctx: xDroneParser.VectorTypeContext) -> Type:
        return Type.vector()

    def visitDroneType(self, ctx: xDroneParser.DroneTypeContext) -> Type:
        return Type.drone()

    def visitListType(self, ctx: xDroneParser.ListTypeContext) -> Type:
        elem_type = self.visit(ctx.type_())
        return Type.list_of(elem_type)

    ######## expr ########

    def visitIntExpr(self, ctx: xDroneParser.IntExprContext) -> Expression:
        signed_int = ctx.INT().getText()
        return Expression(Type.int(), int(signed_int))

    def visitDecimalExpr(self, ctx: xDroneParser.DecimalExprContext) -> Expression:
        signed_float = ctx.FLOAT().getText()
        return Expression(Type.decimal(), float(signed_float))

    def visitStringExpr(self, ctx: xDroneParser.StringExprContext) -> Expression:
        escaped_string = ctx.ESCAPED_STRING().getText()
        quotation_removed = str(escaped_string)[1:-1]
        unescaped = bytes(quotation_removed, "utf-8").decode("unicode_escape")
        return Expression(Type.string(), unescaped)

    def visitTrueExpr(self, ctx: xDroneParser.TrueExprContext) -> Expression:
        return Expression(Type.boolean(), True)

    def visitFalseExpr(self, ctx: xDroneParser.FalseExprContext) -> Expression:
        return Expression(Type.boolean(), False)

    def visitIdentExpr(self, ctx: xDroneParser.IdentExprContext) -> Expression:
        identifier = self.visit(ctx.ident())
        ident = identifier.ident
        if ident not in self._get_latest_symbol_table() and ident not in self.drones:
            # identifier.expression is None iff child.ident not in latest symbol table nor in drones constants
            raise CompileError("Identifier {} has not been declared".format(ident))
        return identifier.to_expression()

    def visitListElemExpr(self, ctx: xDroneParser.ListElemExprContext) -> Expression:
        expr1, expr2 = self.visit(ctx.expr(0)), self.visit(ctx.expr(1))
        if not isinstance(expr1.type, ListType):
            raise CompileError("Expression {} should have type list, but is {}".format(expr1, expr1.type))
        if expr2.type != Type.int():
            raise CompileError("Expression {} should have type int, but is {}".format(expr2, expr2.type))
        if expr2.value >= len(expr1.value) or expr2.value < 0:
            raise CompileError("List {} has length {}, but has been assessed with out-of-range index {}"
                               .format(expr1, len(expr1.value), expr2.value))
        return ListElem(expr1.ident, expr1, expr2.value).to_expression()

    def visitVectorXExpr(self, ctx: xDroneParser.VectorXExprContext) -> Expression:
        expr = self.visit(ctx.expr())
        if expr.type != Type.vector():
            raise CompileError("Expression {} should have type vector, but is {}".format(expr, expr.type))
        return VectorElem(expr.ident, expr, 0).to_expression()

    def visitVectorYExpr(self, ctx: xDroneParser.VectorYExprContext) -> Expression:
        expr = self.visit(ctx.expr())
        if expr.type != Type.vector():
            raise CompileError("Expression {} should have type vector, but is {}".format(expr, expr.type))
        return VectorElem(expr.ident, expr, 1).to_expression()

    def visitVectorZExpr(self, ctx: xDroneParser.VectorZExprContext) -> Expression:
        expr = self.visit(ctx.expr())
        if expr.type != Type.vector():
            raise CompileError("Expression {} should have type vector, but is {}".format(expr, expr.type))
        return VectorElem(expr.ident, expr, 2).to_expression()

    def visitList(self, ctx: xDroneParser.ListContext) -> Expression:
        exprs = [self.visit(expr) for expr in ctx.expr()]
        if len(exprs) == 0:
            return Expression(Type.empty_list(), [])
        if not all(e.type == exprs[0].type for e in exprs):
            raise CompileError("Elements in list {} should have the same type".format([str(e) for e in exprs]))
        return Expression(Type.list_of(exprs[0].type), [e.value for e in exprs])

    def visitVector(self, ctx: xDroneParser.VectorContext) -> Expression:
        expr1, expr2, expr3 = self.visit(ctx.expr(0)), self.visit(ctx.expr(1)), self.visit(ctx.expr(2))
        for expr in [expr1, expr2, expr3]:
            if expr.type != Type.int() and expr.type != Type.decimal():
                raise CompileError("Expression {} should have type int or decimal, but is {}".format(expr, expr.type))
        return Expression(Type.vector(), [float(expr1.value), float(expr2.value), float(expr3.value)])

    def visitFunctionCall(self, ctx: xDroneParser.FunctionCallContext) -> Expression:
        call = self.visit(ctx.call())
        if call is None:
            raise CompileError("Function call should return an expression, but nothing is returned")
        return call

    def visitSize(self, ctx: xDroneParser.SizeContext) -> Expression:
        expr = self.visit(ctx.expr())
        if not isinstance(expr.type, ListType):
            raise CompileError("Expression {} should have type list, but is {}".format(expr, expr.type))
        return Expression(Type.int(), len(expr.value))

    def visitParentheses(self, ctx: xDroneParser.ParenthesesContext) -> Expression:
        expr = self.visit(ctx.expr())
        return expr

    def visitPositNegate(self, ctx: xDroneParser.PositNegateContext) -> Expression:
        expr = self.visit(ctx.expr())
        if expr.type == Type.int() or expr.type == Type.decimal():
            if ctx.PLUS():
                result_value = +expr.value
            else:  # MINUS
                result_value = -expr.value
        elif expr.type == Type.vector():
            if ctx.PLUS():
                result_value = [+e for e in expr.value]
            else:  # MINUS
                result_value = [-e for e in expr.value]
        else:
            raise CompileError(
                "Expression {} should have type int, decimal or vector, but is {}".format(expr, expr.type))
        return Expression(expr.type, result_value)

    def visitNot(self, ctx: xDroneParser.NotContext) -> Expression:
        expr = self.visit(ctx.expr())
        if expr.type != Type.boolean():
            raise CompileError("Expression {} should have type boolean, but is {}".format(expr, expr.type))
        return Expression(Type.boolean(), not expr.value)

    def _is_int_or_decimal(self, type: Type):
        return type == Type.int() or type == Type.decimal()

    def _get_int_decimal_result_type(self, type1: Type, type2: Type):
        assert self._is_int_or_decimal(type1)
        assert self._is_int_or_decimal(type2)
        if type1 == Type.decimal() or type2 == Type.decimal():
            return Type.decimal(), float
        return Type.int(), int

    def visitMultiDivide(self, ctx: xDroneParser.MultiDivideContext) -> Expression:
        expr1, expr2 = self.visit(ctx.expr(0)), self.visit(ctx.expr(1))
        if self._is_int_or_decimal(expr1.type) and self._is_int_or_decimal(expr2.type):
            result_type, func = self._get_int_decimal_result_type(expr1.type, expr2.type)
            if ctx.MULTI():
                result_value = func(expr1.value * expr2.value)
            else:  # DIV
                if expr2.value == 0:
                    raise CompileError("Division by zero")
                result_value = func(expr1.value / expr2.value)
        elif self._is_int_or_decimal(expr1.type) and expr2.type == Type.vector():
            result_type = Type.vector()
            if ctx.MULTI():
                result_value = [expr1.value * e for e in expr2.value]
            else:  # DIV
                raise CompileError("Expression {} and {} have wrong types to perform multiplication or division"
                                   .format(expr1, expr2))
        elif expr1.type == Type.vector() and self._is_int_or_decimal(expr2.type):
            result_type = Type.vector()
            if ctx.MULTI():
                result_value = [e * expr2.value for e in expr1.value]
            else:  # DIV
                result_value = [e / expr2.value for e in expr1.value]
        else:
            raise CompileError("Expression {} and {} have wrong types to perform multiplication or division"
                               .format(expr1, expr2))
        return Expression(result_type, result_value)

    def visitPlusMinus(self, ctx: xDroneParser.PlusMinusContext) -> Expression:
        expr1, expr2 = self.visit(ctx.expr(0)), self.visit(ctx.expr(1))
        if self._is_int_or_decimal(expr1.type) and self._is_int_or_decimal(expr2.type):
            result_type, func = self._get_int_decimal_result_type(expr1.type, expr2.type)
            if ctx.PLUS():
                result_value = func(expr1.value + expr2.value)
            else:  # MINUS
                result_value = func(expr1.value - expr2.value)
        elif expr1.type == Type.vector() and expr2.type == Type.vector():
            result_type = Type.vector()
            if ctx.PLUS():
                result_value = [e1 + e2 for e1, e2 in zip(expr1.value, expr2.value)]
            else:  # MINUS
                result_value = [e1 - e2 for e1, e2 in zip(expr1.value, expr2.value)]
        else:
            raise CompileError("Expression {} and {} have wrong types to perform addition or subtraction"
                               .format(expr1, expr2))
        return Expression(result_type, result_value)

    def visitConcat(self, ctx: xDroneParser.ConcatContext) -> Expression:
        expr1, expr2 = self.visit(ctx.expr(0)), self.visit(ctx.expr(1))
        if expr1.type != Type.string():
            raise CompileError("Expression {} should have type string, but is {}".format(expr1, expr1.type))
        if expr2.type != Type.string():
            raise CompileError("Expression {} should have type string, but is {}".format(expr2, expr2.type))
        return Expression(Type.string(), expr1.value + expr2.value)

    def visitCompare(self, ctx: xDroneParser.CompareContext) -> Expression:
        expr1, expr2 = self.visit(ctx.expr(0)), self.visit(ctx.expr(1))
        if expr1.type != Type.int() and expr1.type != Type.decimal():
            raise CompileError("Expression {} should have type int or decimal, but is {}".format(expr1, expr1.type))
        if expr2.type != Type.int() and expr2.type != Type.decimal():
            raise CompileError("Expression {} should have type int or decimal, but is {}".format(expr2, expr2.type))
        if ctx.GREATER():
            result_value = expr1.value > expr2.value
        elif ctx.GREATER_EQ():
            result_value = expr1.value >= expr2.value
        elif ctx.LESS():
            result_value = expr1.value < expr2.value
        else:  # LESS_EQ
            result_value = expr1.value <= expr2.value
        return Expression(Type.boolean(), result_value)

    def visitEquality(self, ctx: xDroneParser.EqualityContext) -> Expression:
        expr1, expr2 = self.visit(ctx.expr(0)), self.visit(ctx.expr(1))
        if expr1.type != expr2.type:
            raise CompileError("Expressions {} and {} should have the same type".format(expr1, expr2))
        if ctx.EQ():
            result_value = expr1.value == expr2.value
        else:  # NOT_EQ
            result_value = expr1.value != expr2.value
        return Expression(Type.boolean(), result_value)

    def visitAnd(self, ctx: xDroneParser.AndContext) -> Expression:
        expr1, expr2 = self.visit(ctx.expr(0)), self.visit(ctx.expr(1))
        if expr1.type != Type.boolean():
            raise CompileError("Expression {} should have type boolean, but is {}".format(expr1, expr1.type))
        if expr2.type != Type.boolean():
            raise CompileError("Expression {} should have type boolean, but is {}".format(expr2, expr2.type))
        return Expression(Type.boolean(), expr1.value and expr2.value)

    def visitOr(self, ctx: xDroneParser.OrContext) -> Expression:
        expr1, expr2 = self.visit(ctx.expr(0)), self.visit(ctx.expr(1))
        if expr1.type != Type.boolean():
            raise CompileError("Expression {} should have type boolean, but is {}".format(expr1, expr1.type))
        if expr2.type != Type.boolean():
            raise CompileError("Expression {} should have type boolean, but is {}".format(expr2, expr2.type))
        return Expression(Type.boolean(), expr1.value or expr2.value)
