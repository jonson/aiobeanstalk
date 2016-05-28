import asyncio
import uuid
from unittest import TestCase

import os
from aiobeanstalk import connection


class TestBeanstalkConnection(TestCase):

    def setUp(self):
        super().setUp()
        self.loop = asyncio.get_event_loop()
        coro = connection.create_connection([os.getenv('BEANSTALK_HOST', 'beanstalk'), 11300], loop=self.loop)
        self.conn = self.loop.run_until_complete(coro)

    def tearDown(self):
        super().tearDown()
        try:
            if self.conn:
                self.conn.close()
                self.loop.run_until_complete(self.conn.wait_closed())
        finally:
            self.conn = None

    def test_use(self):

        async def test():
            using = await self.conn.using()
            self.assertEqual("default", using)

            await self.conn.use("sometube")
            using = await self.conn.using()
            self.assertEqual("sometube", using)

        self.loop.run_until_complete(test())

    def test_watch(self):

        async def test():
            watching = await self.conn.watching()
            self.assertEqual(["default"], watching)

            tube = str(uuid.uuid4())
            count = await self.conn.watch(tube)
            self.assertEqual(2, count)

            watching = await self.conn.watching()
            self.assertEqual(["default", tube], watching)

        self.loop.run_until_complete(test())

    def test_tubes(self):

        async def test():
            tubes = await self.conn.tubes()
            self.assertEqual(["default"], tubes)

        self.loop.run_until_complete(test())

    def test_stats_tube(self):

        async def test():
            stats = await self.conn.stats_tube("default")

            # just a quick sanity check
            self.assertEqual('default', stats['name'])

        self.loop.run_until_complete(test())
