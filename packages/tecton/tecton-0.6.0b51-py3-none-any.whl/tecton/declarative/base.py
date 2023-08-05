import abc
import datetime
from typing import Dict
from typing import List
from typing import Optional

import attrs

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


# TODO(jake): Use unified_utils.short_tecton_object_repr instead.
def _feature_definition_short_repr(fd: "BaseFeatureDefinition"):
    return f"{type(fd).__name__}('{fd.name}')"


# FeatureReference needs to be in base.py to avoid a circular dependency issue with BaseFeatureDefinition.
@attrs.define
class FeatureReference:
    """A reference to a Feature Definition used in Feature Service construction.

    By default, you can add all of the features in a Feature Definition (i.e. a Feature View or Feature Table) to a
    Feature Service by passing the Feature Definition into the ``features`` parameter of a Feature Service. However,
    if you want to specify a subset, you can use this class.

    You can use the double-bracket notation ``my_feature_view[[<features>]]`` as a short-hand for generating a
    FeatureReference from a Feature Defintion. This is the preferred way to select a subset of of the features
    contained in a Feature Definition. As an example:

    .. highlight:: python
    .. code-block:: python

       from tecton import FeatureService
       from feature_repo.features import my_feature_view_1, my_feature_view_2

       my_feature_service = FeatureService(
           name='my_feature_service',
           features=[
               # Add all features from my_feature_view_1 to this FeatureService
               my_feature_view_1,
               # Add a single feature from my_feature_view_2, 'my_feature'
               my_feature_view_2[['my_feature']]
           ]
       )

    :param feature_definition: The Feature View or Feature Table.
    :param namespace: A namespace used to prefix the features joined from this FeatureView. By default, namespace
        is set to the FeatureView name.
    :param features: The subset of features to select from the FeatureView. If empty, all features will be included.
    :param override_join_keys: A map from feature view join key to spine join key override.
    """

    feature_definition: "BaseFeatureDefinition" = attrs.field(
        on_setattr=attrs.setters.frozen, repr=_feature_definition_short_repr
    )
    namespace: str
    features: Optional[List[str]]
    override_join_keys: Optional[Dict[str, str]]

    def __init__(
        self,
        *,
        feature_definition: "BaseFeatureDefinition",
        namespace: Optional[str] = None,
        features: Optional[List[str]] = None,
        override_join_keys: Optional[Dict[str, str]] = None,
    ):
        namespace = namespace if namespace is not None else feature_definition.name
        return self.__attrs_init__(
            feature_definition=feature_definition,
            namespace=namespace,
            features=features,
            override_join_keys=override_join_keys,
        )

    @property
    def id(self) -> id_pb2.Id:
        return self.feature_definition._id

    def with_name(self, namespace: str) -> "FeatureReference":
        self.namespace = namespace
        return self

    def with_join_key_map(self, join_key_map: Dict[str, str]) -> "FeatureReference":
        self.override_join_keys = join_key_map.copy()
        return self


class BaseFeatureDefinition(Fco):
    """Base class for Feature Views and Feature Tables."""

    @property
    def name(self) -> str:
        """The name of this Feature Definition."""
        raise NotImplementedError

    def __getitem__(self, features: List[str]) -> FeatureReference:
        """
        Used to select a subset of features from a Feature View for use within a Feature Service.

        .. code-block:: python

            from tecton import FeatureService

            # `my_feature_view` is a feature view that contains three features: `my_feature_1/2/3`. The Feature Service
            # can be configured to include only two of those features like this:
            feature_service = FeatureService(
                name="feature_service",
                features=[
                    my_feature_view[["my_feature_1", "my_feature_2"]]
                ],
            )
        """
        if not isinstance(features, list):
            raise TypeError("The `features` field must be a list")

        return FeatureReference(feature_definition=self, features=features)

    def with_name(self, namespace: str) -> FeatureReference:
        """
        Used to rename a Feature View used in a Feature Service.

        .. code-block:: python

            from tecton import FeatureService

            # The feature view in this feature service will be named "new_named_feature_view" in training data dataframe
            # columns and other metadata.
            feature_service = FeatureService(
                name="feature_service",
                features=[
                    my_feature_view.with_name("new_named_feature_view")
                ],
            )

            # Here is a more sophisticated example. The join keys for this feature service will be "transaction_id",
            # "sender_id", and "recipient_id" and will contain three feature views named "transaction_features",
            # "sender_features", and "recipient_features".
            transaction_fraud_service = FeatureService(
                name="transaction_fraud_service",
                features=[
                    # Select a subset of features from a feature view.
                    transaction_features[["amount"]],

                    # Rename a feature view and/or rebind its join keys. In this example, we want user features for both the
                    # transaction sender and recipient, so include the feature view twice and bind it to two different feature
                    # service join keys.
                    user_features.with_name("sender_features").with_join_key_map({"user_id" : "sender_id"}),
                    user_features.with_name("recipient_features").with_join_key_map({"user_id" : "recipient_id"}),
                ],
            )
        """
        return FeatureReference(feature_definition=self, namespace=namespace)

    def with_join_key_map(self, join_key_map: Dict[str, str]) -> FeatureReference:
        """
        Used to rebind join keys for a Feature View used in a Feature Service. The keys in `join_key_map` should be the feature view join keys, and the values should be the feature service overrides.

        .. code-block:: python

            from tecton import FeatureService

            # The join key for this feature service will be "feature_service_user_id".
            feature_service = FeatureService(
                name="feature_service",
                features=[
                    my_feature_view.with_join_key_map({"user_id" : "feature_service_user_id"}),
                ],
            )

            # Here is a more sophisticated example. The join keys for this feature service will be "transaction_id",
            # "sender_id", and "recipient_id" and will contain three feature views named "transaction_features",
            # "sender_features", and "recipient_features".
            transaction_fraud_service = FeatureService(
                name="transaction_fraud_service",
                features=[
                    # Select a subset of features from a feature view.
                    transaction_features[["amount"]],

                    # Rename a feature view and/or rebind its join keys. In this example, we want user features for both the
                    # transaction sender and recipient, so include the feature view twice and bind it to two different feature
                    # service join keys.
                    user_features.with_name("sender_features").with_join_key_map({"user_id" : "sender_id"}),
                    user_features.with_name("recipient_features").with_join_key_map({"user_id" : "recipient_id"}),
                ],
            )
        """
        return FeatureReference(feature_definition=self, override_join_keys=join_key_map.copy())
