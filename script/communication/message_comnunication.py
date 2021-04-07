from domain.communication.Message import Message
from domain.game.Stage import Stage
from domain.game.Topic import Topic
from infra.communication.station.ZmqReqRepConnector import ZmqReqRepConnector

if __name__ == "__main__":
    zmq_connector = ZmqReqRepConnector("tcp://10.248.74.150:5556")

    message = zmq_connector.receive_object()

    if message.get_topic() == Topic.START_CYCLE:
        print(message.get_payload())

    zmq_connector.send_object(Message(Topic.STAGE_COMPLETED, Stage.STAGE_COMPLETED))
