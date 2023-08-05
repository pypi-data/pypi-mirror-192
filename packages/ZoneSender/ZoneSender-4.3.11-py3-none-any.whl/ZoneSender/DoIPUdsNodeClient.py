import grpc
from . import ZoneSenderData
from .Protos import UdsOnDoIP_TP_pb2, UdsOnDoIP_TP_pb2_grpc


class DoIPUdsNodeClient(object):
    def __init__(self):
        self._udsStub = UdsOnDoIP_TP_pb2_grpc.UdsOnDoIP_TPStub(
            channel=grpc.insecure_channel(
                target=f'{ZoneSenderData.DOIP_UDS_NODE_IP}:{ZoneSenderData.DOIP_UDS_NODE_PORT}',
                options=ZoneSenderData.GRPC_OPTIONS
            )
        )

    def generate_key(self, seed: list, algorithm_number=0x4F):
        try:
            res_ = self._udsStub.generate_key(UdsOnDoIP_TP_pb2.request_para(
                seed_value=seed,
                algorithm_number=algorithm_number,
            ))
            print(f'seed:{seed}, algorithm_number:{algorithm_number}')
            return res_.key_value
        except Exception as e:
            print(e)
            return [0x00, 0x00, 0x00, 0x00]