import abc
import datetime
from typing import List

from tecton._internals.fco import Fco
from tecton_proto.args import feature_view_pb2
from tecton_proto.args import virtual_data_source_pb2
from tecton_proto.common import id_pb2


class BaseStreamConfig(abc.ABC):
    @abc.abstractmethod
    def _merge_stream_args(self, data_source_args: virtual_data_source_pb2.VirtualDataSourceArgs):
        pass


class BaseBatchConfig(abc.ABC):
    @property
    @abc.abstractmethod
    def data_delay(self) -> datetime.timedelta:
        pass

    @abc.abstractmethod
    def _merge_batch_args(self, data_source_args: virtual_data_source_pb2.VirtualDataSourceArgs):
        pass


class OutputStream(abc.ABC):
    @abc.abstractmethod
    def _to_proto() -> feature_view_pb2.OutputStream:
        pass


class BaseEntity(Fco):
    @property
    def name(self) -> str:
        """Name of this Entity."""
        raise NotImplementedError

    @property
    def join_keys(self) -> List[str]:
        """Join keys for this Entity."""
        raise NotImplementedError


class BaseTransformation(Fco):
    """Base class for unified and declarative transformations.

    Does not have any of its own methods - just used as a shared type.
    """

    @property
    # Override Fco._id() again so to pass some pyclean checks.
    def _id(self) -> id_pb2.Id:
        raise NotImplementedError


class BaseDataSource(Fco):
    @property
    def name(self) -> str:
        """The name of this Data Source."""
        raise NotImplementedError

    @property
    def data_delay(self) -> datetime.timedelta:
        raise NotImplementedError
