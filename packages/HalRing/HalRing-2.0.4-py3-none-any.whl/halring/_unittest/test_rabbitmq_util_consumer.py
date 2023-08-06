# coding=utf-8
import unittest
import json
import os
import sys

nga_root = str(os.path.abspath(__file__).split("_unittest")[0])
sys.path.append(nga_root)

from halring.rabbitmq_lib.halring_rabbitmq import Consumer
from halring.rabbitmq_lib.halring_rabbitmq import MQClient
import time


class TestRabbitmqUtilConsumer(unittest.TestCase):

    def test_001_consumer(self):

        mqclient = MQClient(host="10.112.15.114", user="aqc001", password="L@rtern@9c", virtual_host="aqc")
        connection = mqclient.connect()
        queue = "1111"

        class MyConsumer(Consumer):
            def callback(self, channel, method, properties, body):
                message = body.decode()
                temp_message = json.loads(message)

                print(temp_message.get("publish_time"))
                print(temp_message.get("randomint"))
                # channel.basic_ack(delivery_tag=method.delivery_tag)
                t = time.strftime("%Y%m%d%H%M%S", time.localtime())
                txt_path = "D:\\Workspace\\timer_txt\\"
                txt_name = t + "_consumer.txt"
                with open(txt_path + txt_name, "w+") as f:
                    f.write("publish_time:" + temp_message.get("publish_time") + "\n")
                    f.write("consume_time:" + t + "\n")
                    f.close()

        consumer = MyConsumer(connection)
        consumer.start_consuming(queue)

    def test_002_consumer_pro(self):

        mqclient = MQClient(host="10.112.15.114", user="aqc001", password="L@rtern@9c", virtual_host="aqc")
        connection = mqclient.connect()
        queue = "1111"

        class MyConsumer(Consumer):
            '''定义计数器字典'''
            delivery_task_waiting_counter = {}

            def callback(self, channel, method, properties, body):
                message = body.decode()
                temp_message = json.loads(message)
                '''
                包含 任务批次总数的  MQ 结构
                {
                    "delivery_task_id": (int)id,
                    "MQ_total": (int)2,
                    "publish_time" : time_data,
                    "randomint": (int)
                    ""
                }
                '''

                print(temp_message.get("publish_time"))
                print(temp_message.get("randomint"))
                print(temp_message.get("MQ_total"))

                current_delivery_task_id = temp_message.get("delivery_task_id")
                current_delivery_mq_total = temp_message.get("delivery_task_id")
                if current_delivery_task_id not in self.delivery_task_waiting_counter.keys():
                    '''如果总数就是1就不要计数了'''
                    if current_delivery_mq_total == 1:
                        '''直接实例化应用'''
                        # TODO
                        pass
                    else:

                        '''未记过数且MQ>1的delivery_task开始计数'''
                        '''这个结构里还可以加点东西以备重复，先做个简单计数的例子'''
                        count_dict = {"total": current_delivery_mq_total, "count": 1}
                        self.delivery_task_waiting_counter[current_delivery_task_id] = count_dict

                else:
                    '''已经在计数中的delivery_task_id'''
                    '''取出count_dict'''
                    count_dict = self.delivery_task_waiting_counter.get(current_delivery_task_id)

                    current_count = count_dict.get("count") + 1
                    if current_count == count_dict.get("total"):
                        '''达到总数以后开始实例化应用'''
                        '''并把这个id从计数字典中pop掉'''
                        self.delivery_task_waiting_counter.pop(current_delivery_task_id)
                        # TODO
                        pass
                    else:
                        '''未达到总数继续计数'''
                        count_dict["count"] = current_count

        consumer = MyConsumer(connection)
        consumer.start_consuming(queue)


if __name__ == '__main__':
    a = TestRabbitmqUtilConsumer().test_001_consumer()
