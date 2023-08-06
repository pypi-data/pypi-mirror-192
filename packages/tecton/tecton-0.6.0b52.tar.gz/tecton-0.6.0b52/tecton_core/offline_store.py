import enum
from datetime import timedelta
from typing import Union

import attrs
import pendulum

from tecton_core import time_utils
from tecton_core.feature_definition_wrapper import FeatureDefinitionWrapper as FeatureDefinition

TIME_PARTITION = "time_partition"
ANCHOR_TIME = "_anchor_time"
SECONDS_TO_NANOSECONDS = 1000 * 1000 * 1000


class PartitionType(str, enum.Enum):
    DATE_STR = "DateString"
    EPOCH = "Epoch"


@attrs.frozen
class TimestampFormats:
    spark_format: str
    python_format: str


@attrs.frozen
class OfflineStorePartitionParams:
    partition_by: str
    partition_type: PartitionType
    partition_interval: pendulum.duration


def get_offline_store_partition_params(feature_definition: FeatureDefinition) -> OfflineStorePartitionParams:
    # Examples of how our offline store is partitioned
    ### BWAFV on Delta
    # Partition Column: time_partition
    # Materialized Columns: _anchor_time, [join_keys], [feature_columns]

    ### Continuous SWAFV on Parquet
    # Partition Column: time_partition
    # Materialized Columns: timestamp, _anchor_time, [join_keys], [feature_columns]
    # Note: Very weird that we have a timestamp parquet column here - redundant with _anchor_time

    ### BWAFV on Parquet
    # Partition Column: _anchor_time
    # Materialized Columns: _anchor_time, [join_keys], [feature_columns]
    # !! In this case we need to drop the partition column from the top level columns

    ### BFV on Parquet
    # Partition Column: _anchor_time
    # Materialized Columns: ts, [join_keys], [feature_columns]

    offline_store_config = feature_definition.offline_store_config
    store_type = offline_store_config.WhichOneof("store_type")
    if store_type == "delta":
        partition_by = TIME_PARTITION
        partition_type = PartitionType.DATE_STR
        partition_interval = pendulum.duration(
            seconds=offline_store_config.delta.time_partition_size.ToTimedelta().total_seconds()
        )
    elif store_type == "parquet":
        partition_by = ANCHOR_TIME
        partition_type = PartitionType.EPOCH
        partition_interval = pendulum.duration(
            seconds=feature_definition.batch_materialization_schedule.total_seconds()
        )
        if feature_definition.is_continuous:
            partition_by = TIME_PARTITION
    else:
        raise Exception("Unexpected offline store config")
    return OfflineStorePartitionParams(partition_by, partition_type, partition_interval)


def timestamp_to_partition_date_str(timestamp: pendulum.DateTime, partition_params: OfflineStorePartitionParams) -> str:
    partition_interval_timedelta = partition_params.partition_interval.as_timedelta()
    aligned_time = time_utils.align_time_downwards(timestamp, partition_interval_timedelta)
    partition_format = _timestamp_formats(partition_interval_timedelta).python_format
    return aligned_time.strftime(partition_format)


def timestamp_to_partition_epoch(
    timestamp: pendulum.DateTime,
    partition_params: OfflineStorePartitionParams,
    is_continuous: bool,
    feature_store_format_version: int,
) -> int:
    if is_continuous:
        aligned_time = timestamp
    else:
        aligned_time = time_utils.align_time_downwards(timestamp, partition_params.partition_interval.as_timedelta())
    return time_utils.convert_timestamp_for_version(aligned_time, feature_store_format_version)


def window_size_seconds(window: Union[timedelta, pendulum.Duration]):
    if isinstance(window, pendulum.Duration):
        window = window.as_timedelta()
    if window % timedelta(seconds=1) != timedelta(0):
        raise AssertionError(f"partition_size is not a round number of seconds: {window}")
    return int(window.total_seconds())


def _timestamp_formats(partition_size: timedelta):
    if partition_size % timedelta(days=1) == timedelta(0):
        return TimestampFormats(spark_format="yyyy-MM-dd", python_format="%Y-%m-%d")
    else:
        return TimestampFormats(spark_format="yyyy-MM-dd-HH:mm:ss", python_format="%Y-%m-%d-%H:%M:%S")
