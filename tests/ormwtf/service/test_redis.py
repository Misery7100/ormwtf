import unittest

from ormwtf.service.redis import RedisBase, RedisConfig, RedisCredentials

# ----------------------- #

credentials = RedisCredentials(
    host="localhost",
    port=6479,
)

# ----------------------- #


class TestRedisBase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        class Base1(RedisBase):
            config = RedisConfig(
                credentials=credentials,
                collection="base1_redis",
            )

        class Base2(RedisBase):
            config = RedisConfig(
                credentials=credentials,
                collection="base2_redis",
                database=2,
            )

        cls.base1 = Base1
        cls.base2 = Base2

    # ....................... #

    @classmethod
    def tearDownClass(cls):
        with cls.base1._client() as client:
            client.flushdb()

        with cls.base2._client() as client:
            client.flushdb()

    # ....................... #

    def test_subclass(self):
        self.assertTrue(
            issubclass(self.base1, RedisBase),
            "Base1 should be a subclass of RedisBase",
        )

        self.assertTrue(
            issubclass(self.base2, RedisBase),
            "Base2 should be a subclass of RedisBase",
        )

    # ....................... #

    def test_registry(self):
        reg1 = RedisBase._registry.get(self.base1.config.database).get(
            self.base1.config.collection
        )
        reg2 = RedisBase._registry.get(self.base2.config.database).get(
            self.base2.config.collection
        )

        self.assertTrue(
            reg1 is self.base1,
            "Registry item should be Base1",
        )
        self.assertTrue(
            reg2 is self.base2,
            "Registry item should be Base2",
        )

    # ....................... #

    def test_find_save(self):
        case1 = self.base1()
        case2 = self.base2(id=case1.id)

        self.assertNotEqual(case1, case2, "Instances should be different")

        self.assertIsNone(
            self.base1.find(case1.id, bypass=True),
            "Should return None",
        )

        case1.save()

        self.assertIsNotNone(
            self.base1.find(case1.id, bypass=True),
            "Should return an instance",
        )

        self.assertIsNone(
            self.base2.find(case2.id, bypass=True),
            "Should return None",
        )

        case2.save()

        self.assertIsNotNone(
            self.base2.find(case2.id, bypass=True),
            "Should return an instance",
        )


# ----------------------- #


class TestRedisBaseAsync(unittest.IsolatedAsyncioTestCase):
    @classmethod
    def setUpClass(cls):
        class Base1(RedisBase):
            config = RedisConfig(
                credentials=credentials,
                collection="base1_redis_async",
            )

        class Base2(RedisBase):
            config = RedisConfig(
                credentials=credentials,
                collection="base2_redis_async",
                database=2,
            )

        cls.base1 = Base1
        cls.base2 = Base2

    # ....................... #

    @classmethod
    def tearDownClass(cls):
        with cls.base1._client() as client:
            client.flushdb()

        with cls.base2._client() as client:
            client.flushdb()

    # ....................... #

    async def test_afind_asave(self):
        case1 = self.base1()
        case2 = self.base2(id=case1.id)

        self.assertNotEqual(case1, case2, "Instances should be different")

        self.assertIsNone(
            await self.base1.afind(case1.id, bypass=True),
            "Should return None",
        )

        case1.save()

        self.assertIsNotNone(
            await self.base1.afind(case1.id, bypass=True),
            "Should return an instance",
        )

        self.assertIsNone(
            await self.base2.afind(case2.id, bypass=True),
            "Should return None",
        )

        case2.save()

        self.assertIsNotNone(
            await self.base2.afind(case2.id, bypass=True),
            "Should return an instance",
        )


# ----------------------- #

if __name__ == "__main__":
    unittest.main()
