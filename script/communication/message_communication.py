from domain.communication.Message import Message
from domain.game.Stage import Stage
from domain.game.Topic import Topic
from infra.communication.robot.ZmqReqRepConnector import ZmqReqRepConnector

if __name__ == "__main__":
    req_connector = ZmqReqRepConnector("tcp://*:5556")

    message = Message(Topic.START_CYCLE, Stage.START_CYCLE)

    input("Press enter to send message")
    req_connector.send_object(message)

    message = req_connector.receive_object()

    if message.get_payload() == Stage.STAGE_COMPLETED:
        print(message.get_payload())
