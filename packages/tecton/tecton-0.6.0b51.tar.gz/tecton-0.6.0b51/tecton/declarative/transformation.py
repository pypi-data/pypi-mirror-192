from typing import Optional
from typing import Set
from typing import Union

import attrs
from google.protobuf.empty_pb2 import Empty

from tecton._internals import errors
from tecton.declarative.base import BaseTransformation
from tecton_core.materialization_context import UnboundMaterializationContext
from tecton_proto.args import pipeline_pb2

SPARK_SQL_MODE = "spark_sql"
PYSPARK_MODE = "pyspark"
SNOWFLAKE_SQL_MODE = "snowflake_sql"
SNOWPARK_MODE = "snowpark"
ATHENA_MODE = "athena"
PANDAS_MODE = "pandas"
PYTHON_MODE = "python"


class Constant:
    ALLOWED_TYPES = [str, int, float, bool, type(None)]

    def __init__(self, value: Optional[Union[str, int, float, bool]]):
        self.value = value
        self.value_type = type(value)

        if self.value_type not in self.ALLOWED_TYPES:
            raise errors.InvalidConstantType(value, self.ALLOWED_TYPES)

    def __repr__(self):
        return f"Constant(value={self.value}, type={self.value_type})"


def const(value: Optional[Union[str, int, float, bool]]) -> Constant:
    """
    Wraps a const and returns a ``Constant`` object that can be used inside pipeline functions.

    :param value: The constant value that needs to be wrapped and used in the pipeline function.
    :return: A Constant object.
    """
    return Constant(value)


@attrs.define
class PipelineNodeWrapper:
    """A dataclass used to build feature view pipelines.

    Attributes:
        node_proto: The Pipeline node proto that this wrapper represents.
        transformations: The set of Transformation objects included by this node or its dependencies.
    """

    node_proto: pipeline_pb2.PipelineNode
    transformations: Set[BaseTransformation] = attrs.field(factory=set)

    @classmethod
    def create_from_arg(
        cls, arg: Union["PipelineNodeWrapper", Constant, UnboundMaterializationContext], transformation_name: str
    ) -> "PipelineNodeWrapper":
        if isinstance(arg, PipelineNodeWrapper):
            return arg
        elif isinstance(arg, Constant):
            constant_node = pipeline_pb2.ConstantNode()
            if arg.value is None:
                constant_node.null_const.CopyFrom(Empty())
            elif arg.value_type == str:
                constant_node.string_const = arg.value
            elif arg.value_type == int:
                constant_node.int_const = repr(arg.value)
            elif arg.value_type == float:
                constant_node.float_const = repr(arg.value)
            elif arg.value_type == bool:
                constant_node.bool_const = arg.value
            return PipelineNodeWrapper(node_proto=pipeline_pb2.PipelineNode(constant_node=constant_node))
        elif isinstance(arg, UnboundMaterializationContext):
            node = pipeline_pb2.PipelineNode(materialization_context_node=pipeline_pb2.MaterializationContextNode())
            return PipelineNodeWrapper(node_proto=node)
        else:
            raise errors.InvalidTransformInvocation(transformation_name, arg)

    def add_transformation_input(
        self, input: "PipelineNodeWrapper", arg_index: Optional[int] = None, arg_name: Optional[str] = None
    ):
        assert self.node_proto.HasField(
            "transformation_node"
        ), "add_transformation_input should only be used with Transformation Nodes."
        assert (arg_index is None) != (arg_name is None), "Exactly one of arg_index or arg_name should be set."
        input_proto = pipeline_pb2.Input(
            arg_index=arg_index,
            arg_name=arg_name,
            node=input.node_proto,
        )
        self.node_proto.transformation_node.inputs.append(input_proto)
        self.transformations.update(input.transformations)
