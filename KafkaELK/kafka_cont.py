from confluent_kafka import Producer, Consumer
from elasticsearch import Elasticsearch, helpers
import json
import socket

class kafka_connect:
    def __init__(self, ip_port):
        self.ip_port = ip_port # xx.xxx.xxx.xxx:9092 xxx自己kafka的IP
    # 轉換msgKey或msgValue成為utf-8的字串
    def try_decode_utf8(self, data):
        if data:
            return data.decode('utf-8')
        else:
            return None
    # 當發生Re-balance時, 如果有partition被assign時被呼叫
    def print_assignment(self, consumer, partitions):
        result = '[{}]'.format(','.join([p.topic + '-' + str(p.partition) for p in partitions]))
        print('Setting newly assigned partitions:', result)
    # 當發生Re-balance時, 之前被assigned的partition會被移除
    def print_revoke(self, consumer, partitions):
        result = '[{}]'.format(','.join([p.topic + '-' + str(p.partition) for p in partitions]))
        print('Revoking previously assigned partitions: ' + result)
    def kafka_consumer(self):
        props = {
            'bootstrap.servers': self.ip_port,  # Kafka集群在那裡? (置換成要連接的Kafka集群)
            'group.id': 'goodgo',
            'auto.offset.reset': 'earliest',  # Offset從最前面開始
        }
        # 步驟2. 產生一個Kafka的Consumer的實例
        consumer = Consumer(props)
        # 步驟3. 指定想要訂閱訊息的topic名稱
        topicName = 'LongMoonTest'
        # 步驟4. 讓Consumer向Kafka集群訂閱指定的topic
        consumer.subscribe([topicName], on_assign=self.print_assignment, on_revoke=self.print_revoke)
        count = 0 # 紀錄筆數
        while True:
            records = consumer.consume(num_messages=500, timeout=1.0)  # 批次讀取
            if len(records) > 0:
                count += 1
                for record in records:
                    topic = record.topic()
                    partition = record.partition()
                    offset = record.offset()
                    # 取出msgKey與msgValue
                    msgKey = self.try_decode_utf8(record.key())
                    msgValue = self.try_decode_utf8(record.value())
                    print('%s-%d-%d : (%s , %s)' % (topic, partition, offset, msgKey, msgValue))
                    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                    s.connect(("8.8.8.8", 80))
                    ip_port = "http://"+s.getsockname()[0] + ":9200"
                    savedata_els(http_ip_port=ip_port,msgValue=msgValue)
                    s.close()

                # 秀出metadata與msgKey & msgValue訊息
def savedata_els(http_ip_port,msgValue):
    els_save_data = json.loads(msgValue)
    es = Elasticsearch(http_ip_port)
    actions = []
    action = {
        "_index": "meowjango",
        "_type": "meowjango",
    }
    action.update(els_save_data)
    actions.append(action)
    print(actions)
    helpers.bulk(es, actions)


if __name__ == '__main__':
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    ip_port = s.getsockname()[0] + ":9092"
    kafka = kafka_connect(ip_port=ip_port)
    s.close()

    while True:
        kafka.kafka_consumer()