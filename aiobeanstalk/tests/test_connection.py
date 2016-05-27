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

    async def async_test_use(self):
        using = await self.conn.using()
        self.assertEqual("default", using)

        await self.conn.use("sometube")
        using = await self.conn.using()
        self.assertEqual("sometube", using)

    def test_use(self):
        self.loop.run_until_complete(self.async_test_use())

    async def async_test_watch(self):
        watching = await self.conn.watching()
        self.assertEqual(["default"], watching)

        tube = str(uuid.uuid4())
        count = await self.conn.watch(tube)
        self.assertEqual(2, count)

        watching = await self.conn.watching()
        self.assertEqual(["default", tube], watching)

    def test_watch(self):
        self.loop.run_until_complete(self.async_test_watch())


