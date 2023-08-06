import asyncio
import unittest
from datetime import datetime, timezone

from fastiot.core.broker_connection import NatsBrokerConnection
from fastiot.core.time import get_time_now
from fastiot.db.influxdb_helper_fn import get_new_async_influx_client_from_env
from fastiot.env.env import env_influxdb
from fastiot.msg.hist import HistObjectReq, HistObjectResp
from fastiot.msg.thing import Thing
from fastiot.testlib import populate_test_env
from fastiot_core_services.time_series.env import time_series_env
from fastiot_core_services.time_series.time_series_service import TimeSeriesService

THING = Thing(machine='SomeMachine', name="RequestSensor", value=42, timestamp=get_time_now(),
              measurement_id="1")


class TestTimeSeries(unittest.IsolatedAsyncioTestCase):

    async def asyncSetUp(self):
        populate_test_env()
        self.client = await get_new_async_influx_client_from_env()
        await self.delete_data()
        self.broker_connection = await NatsBrokerConnection.connect()
        await self._start_service()

    async def asyncTearDown(self):
        self.service_task.cancel()
        await self.client.close()

    async def _start_service(self):
        service = TimeSeriesService(broker_connection=self.broker_connection)
        self.service_task = asyncio.create_task(service.run())
        await asyncio.sleep(0.005)

    async def insert_data(self):
        for i in range(5):
            thing_msg = Thing(machine='test_machine', name=f'sensor_{i}',
                              value=1, unit=f"{i}", timestamp=f"2019-07-25T21:48:0{i}Z")

            await self.broker_connection.publish(Thing.get_subject(thing_msg.name), thing_msg)
            await asyncio.sleep(0.01)

    async def delete_data(self):
        await self.client.delete_api().delete(stop="2024-01-01T00:00:00Z", start="1970-01-01T00:00:00Z",
                                              bucket=env_influxdb.bucket, predicate='machine="test_machine"',
                                              org=env_influxdb.organisation)

    async def test_storage(self):
        await self.insert_data()
        await asyncio.sleep(0.5)     # Making sure the data is stored in the db
        query = \
            f'from(bucket: "{env_influxdb.bucket}") ' \
            '|> range(start: 2019-07-25T21:47:00Z)' \
            '|> group(columns: ["time"])' \
            '|> sort(columns: ["_time"])' \
            '|> filter(fn: (r) => r["machine"] == "test_machine")'
        tables = await self.client.query_api().query(query, org=env_influxdb.organisation)
        i = 0
        for table in tables:
            for row in table:
                self.assertEqual(f'sensor_{i}', row.get_measurement())
                i = i + 1
        self.assertEqual(5, i)
        await self.delete_data()
        await self.client.close()

    async def test_reply_standard(self):
        for i in range(5):
            data = [{"measurement":
                         f'sensor_{i}',
                     "tags":
                         {"machine": 'test_machine',
                          "unit": f"{i}"},
                     "fields":
                         {"value": f"{i}"},
                     "time": get_time_now()
                     }]
            await self.client.write_api().write(bucket=env_influxdb.bucket, org=env_influxdb.organisation, record=data,
                                                precision='ms')

        await asyncio.sleep(0.05)  # Making sure the data is stored in the db
        subject = HistObjectReq.get_reply_subject(name="things")
        reply: HistObjectResp = await self.broker_connection.request(subject=subject,
                                                                     msg=HistObjectReq(machine="test_machine",
                                                                                       timeout=10))

        for i in range(5):
            self.assertEqual(f'sensor_{i}'
                             , reply.values[i].get("sensor"))
            self.assertEqual(f'{i}'
                             , reply.values[i].get("unit"))
        await self.delete_data()
        await self.client.close()

    async def test_reply_start_end(self):
        for i in range(5):

            data = [{"measurement": f'sensor_{i}',
                     "tags": {"machine": 'test_machine',
                              "unit": "m"},
                     "fields": {"value": 1},
                     "time": f"2019-07-25T21:48:0{i}Z"
                     }]
            await self.client.write_api().write(bucket=env_influxdb.bucket, org=env_influxdb.organisation, record=data,
                                                precision='ms')

        await asyncio.sleep(0.05)  # Making sure the data is stored in the db
        subject = HistObjectReq.get_reply_subject(name="things")
        reply: HistObjectResp = await self.broker_connection.request(subject=subject,
                                                                     msg=HistObjectReq(machine="test_machine",
                                                                                       dt_start='2019-07-25T21:47:00Z',
                                                                                       dt_end='2019-07-25T21:48:04Z',
                                                                                       timeout=10))
        for i in range(4):
            self.assertEqual({"machine": 'test_machine',
                              "sensor": f'sensor_{i}',
                              "value": 1,
                              "unit": "m",
                              "timestamp": datetime(2019, 7,25,21,48,i, tzinfo=timezone.utc),
                              },
                             reply.values[i])
        with self.assertRaises(IndexError):
            reply.values[4]
        await self.delete_data()
        await self.client.close()

    async def test_error_code_1(self):
        subject = HistObjectReq.get_reply_subject(name=time_series_env.request_subject)
        reply: HistObjectResp = await self.broker_connection.request(subject=subject,
                                                                     msg=HistObjectReq(machine="test_machine",
                                                                                       timeout=10))
        self.assertEqual(1, reply.error_code)
        await self.client.close()


if __name__ == '__main__':
    unittest.main()
