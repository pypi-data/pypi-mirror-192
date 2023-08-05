from typing import List
from typing import Optional
from typing import Union

from tecton.declarative.base import BaseFeatureDefinition
from tecton.declarative.base import FeatureReference
from tecton.declarative.logging_config import LoggingConfig
from tecton_core.feature_definition_wrapper import FrameworkVersion
from tecton_core.id_helper import IdHelper
from tecton_proto.args import feature_service_pb2
from tecton_proto.args.basic_info_pb2 import BasicInfo
from tecton_proto.args.feature_service_pb2 import FeatureServiceArgs


def build_feature_service_args(
    *,
    basic_info: BasicInfo,
    prevent_destroy: bool,
    online_serving_enabled: bool,
    features: List[Union[FeatureReference, BaseFeatureDefinition]],
    logging: Optional[LoggingConfig],
) -> FeatureServiceArgs:
    if features:
        feature_packages = [_feature_to_feature_service_feature_package(feature) for feature in features]
    else:
        feature_packages = None

    return FeatureServiceArgs(
        feature_service_id=IdHelper.from_string(IdHelper.generate_string_id()),
        info=basic_info,
        prevent_destroy=prevent_destroy,
        online_serving_enabled=online_serving_enabled,
        feature_packages=feature_packages,
        version=FrameworkVersion.FWV5.value,
        logging=logging._to_proto() if logging is not None else None,
    )


def _feature_to_feature_service_feature_package(
    feature: Union[FeatureReference, BaseFeatureDefinition],
) -> feature_service_pb2.FeatureServiceFeaturePackage:
    if not isinstance(feature, (FeatureReference, BaseFeatureDefinition)):
        raise TypeError(
            f"Object in FeatureService.features with an invalid type: {type(feature)}. Should be of type FeatureReference or BaseFeatureDefinition."
        )

    if isinstance(feature, BaseFeatureDefinition):
        # Get a default FeatureReference.
        feature = FeatureReference(feature_definition=feature)

    if feature.override_join_keys:
        override_join_keys = [
            feature_service_pb2.ColumnPair(feature_column=fv_key, spine_column=spine_key)
            for fv_key, spine_key in sorted(feature.override_join_keys.items())
        ]
    else:
        override_join_keys = None

    return feature_service_pb2.FeatureServiceFeaturePackage(
        feature_package_id=feature.id,
        namespace=feature.namespace,
        override_join_keys=override_join_keys,
        features=feature.features if feature.features else None,
    )
