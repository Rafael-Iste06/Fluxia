# fluxia_vm.py

from typing import Any, Dict, List, Tuple, Callable

class VMError(Exception):
    pass

class Frame:
    def __init__(self, code: List[Tuple], env: Dict[str, Any], ip: int = 0):
        self.code = code
        self.env = env
        self.ip = ip

class FluxiaVM:
    def __init__(self, functions: Dict[str, Tuple[List[str], List[Tuple]]], uses: List[str]):
        self.functions = functions
        self.uses = uses
        self.stack: List[Any] = []
        self.globals: Dict[str, Any] = {}
        self.builtins: Dict[str, Callable] = {}
        self.call_stack: List[Frame] = []
        self._setup_builtins()

    def _setup_builtins(self):
        self.builtins["print"] = self._builtin_print
        if "gui" in self.uses:
            try:
                from fluxia_gui import setup_gui_builtins
                setup_gui_builtins(self)
            except ImportError as e:
                print(e)

    def _builtin_print(self, *args):
        print(*args)

    def run(self):
        if "__main__" in self.functions:
            self.call_function("__main__", [])
        if "main" in self.functions:
            return self.call_function("main", [])
        return None

    def call_function(self, name: str, args: List[Any]):
        if name in self.builtins:
            return self.builtins[name](*args)

        if name not in self.functions:
            raise VMError(f"Undefined function {name}")
        params, code = self.functions[name]
        if len(args) != len(params):
            raise VMError(f"Function {name} expected {len(params)} args, got {len(args)}")

        env = dict(zip(params, args))
        frame = Frame(code, env)
        self.call_stack.append(frame)
        result = self.exec_frame()
        self.call_stack.pop()
        return result

    def exec_frame(self):
        frame = self.call_stack[-1]
        code = frame.code
        env = frame.env
        ip = frame.ip
        stack = self.stack

        while ip < len(code):
            instr = code[ip]
            ip += 1
            op = instr[0]

            if op == "PUSH_CONST":
                stack.append(instr[1])

            elif op == "LOAD_VAR":
                name = instr[1]
                if name in env:
                    stack.append(env[name])
                elif name in self.globals:
                    stack.append(self.globals[name])
                else:
                    raise VMError(f"Undefined variable {name}")

            elif op == "STORE_VAR":
                name = instr[1]
                value = stack.pop()
                if name in env:
                    env[name] = value
                else:
                    self.globals[name] = value

            elif op == "POP":
                if not stack:
                    raise VMError("Stack underflow on POP")
                stack.pop()

            elif op == "BINARY_ADD":
                b = stack.pop(); a = stack.pop()
                stack.append(a + b)
            elif op == "BINARY_SUB":
                b = stack.pop(); a = stack.pop()
                stack.append(a - b)
            elif op == "BINARY_MUL":
                b = stack.pop(); a = stack.pop()
                stack.append(a * b)
            elif op == "BINARY_DIV":
                b = stack.pop(); a = stack.pop()
                stack.append(a / b)

            elif op == "BINARY_GT":
                b = stack.pop(); a = stack.pop()
                stack.append(a > b)
            elif op == "BINARY_LT":
                b = stack.pop(); a = stack.pop()
                stack.append(a < b)
            elif op == "BINARY_GTE":
                b = stack.pop(); a = stack.pop()
                stack.append(a >= b)
            elif op == "BINARY_LTE":
                b = stack.pop(); a = stack.pop()
                stack.append(a <= b)
            elif op == "BINARY_EQ":
                b = stack.pop(); a = stack.pop()
                stack.append(a == b)
            elif op == "BINARY_NEQ":
                b = stack.pop(); a = stack.pop()
                stack.append(a != b)

            elif op == "JUMP_IF_FALSE":
                target = instr[1]
                cond = stack.pop()
                if not cond:
                    ip = target

            elif op == "JUMP":
                ip = instr[1]

            elif op == "CALL":
                fname = instr[1]
                argc = instr[2]
                args = [stack.pop() for _ in range(argc)]
                args.reverse()
                frame.ip = ip
                result = self.call_function(fname, args)
                frame = self.call_stack[-1]
                code = frame.code
                env = frame.env
                ip = frame.ip
                stack.append(result)

            elif op == "RETURN":
                result = stack.pop() if stack else None
                frame.ip = ip
                return result

            else:
                raise VMError(f"Unknown opcode {op}")

        frame.ip = ip
        return None
