from dataclasses import dataclass

from smol_evm.context import ExecutionContext


@dataclass
class EVMException(Exception):
    context: ExecutionContext


@dataclass
class UnknownOpcode(Exception):
    opcode: int

    def __str__(self):
        return f"opcode={hex(self.opcode)}"


@dataclass
class InvalidCodeOffset(EVMException):
    offset: int

    def __str__(self):
        return f"offset={hex(self.offset)}, context={self.context}"


@dataclass
class InvalidJumpDestination(EVMException):
    target_pc: int

    def __str__(self):
        return f"target_pc={hex(self.target_pc)}, context={self.context}"
