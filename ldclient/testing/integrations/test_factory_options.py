from unittest.mock import patch

import pytest

from ldclient.integrations import DynamoDB, Redis


@pytest.fixture(params=[
    pytest.param((DynamoDB.new_feature_store, ('table',), 'dynamodb_opts', 'ldclient.integrations._DynamoDBFeatureStoreCore'), id='dynamodb-feature-store'),
    pytest.param((DynamoDB.new_big_segment_store, ('table',), 'dynamodb_opts', 'ldclient.integrations._DynamoDBBigSegmentStore'), id='dynamodb-big-segment-store'),
    pytest.param((DynamoDB.async_feature_store, ('table',), 'dynamodb_opts', 'ldclient.impl.integrations.dynamodb.async_dynamodb_feature_store._AsyncDynamoDBFeatureStoreCore'), id='async-dynamodb-feature-store'),
    pytest.param((Redis.new_feature_store, (), 'redis_opts', 'ldclient.integrations._RedisFeatureStoreCore'), id='redis-feature-store'),
    pytest.param((Redis.new_big_segment_store, (), 'redis_opts', 'ldclient.integrations._RedisBigSegmentStore'), id='redis-big-segment-store'),
    pytest.param((Redis.async_feature_store, (), 'redis_opts', 'ldclient.impl.integrations.redis.async_redis_feature_store._AsyncRedisFeatureStoreCore'), id='async-redis-feature-store'),
    pytest.param((Redis.async_big_segment_store, (), 'redis_opts', 'ldclient.impl.integrations.redis.async_redis_big_segment_store._AsyncRedisBigSegmentStore'), id='async-redis-big-segment-store'),
])
def store_factory(request):
    factory, args, options_name, constructor_path = request.param
    with patch(constructor_path) as constructor:
        yield factory, args, options_name, constructor


@pytest.mark.parametrize('explicit_none', [False, True], ids=['omitted', 'none'])
def test_factory_creates_fresh_options(store_factory, explicit_none):
    factory, args, options_name, constructor = store_factory
    kwargs = {options_name: None} if explicit_none else {}

    factory(*args, **kwargs)
    first_options = constructor.call_args.args[2]
    assert first_options == {}
    first_options['endpoint_url'] = 'http://first-store'

    factory(*args, **kwargs)
    second_options = constructor.call_args.args[2]
    assert second_options == {}
    assert second_options is not first_options


@pytest.mark.parametrize('options', [{}, {'socket_timeout': 5}], ids=['empty', 'nonempty'])
def test_factory_preserves_supplied_options(store_factory, options):
    factory, args, options_name, constructor = store_factory

    factory(*args, **{options_name: options})

    assert constructor.call_args.args[2] is options
