# Author: MetariumProject

# local libraries
from ...utils import ServiceAlreadyExistsError
from ..base import SubstrateBaseEncoder


class SubstrateTopicCreatorAsDataCustodian(SubstrateBaseEncoder):

    FUNCTION_CALL = "new_topic"

    def is_valid_data(self, data: dict = {}):
        assert "topic_id" in data and isinstance(data["topic_id"], int)# topic id
        assert "scribes" in data and isinstance(data["scribes"], list)# list of scribes authorized to the topic
        # return true
        return True
    
    def compose_call(self, data:dict={}):
        return self.metarium_node.compose_call(
            call_module=self.__class__.SUBSTRATE_EXTRINSIC,
            call_function=self.__class__.FUNCTION_CALL,
            call_params={
                'topic_id': str(data["topic_id"]),
                'scribes': data["scribes"]
            }
        )


class SubstrateTopicAccessSettingAddressModifierAsDataCustodian(SubstrateBaseEncoder):

    FUNCTION_CALL = "change_topic_access_setting_address"

    def is_valid_data(self, data: dict = {}):
        print(f"\n\n{data = }")
        assert "topic_id" in data and isinstance(data["topic_id"], int)# topic id
        assert "new_access_setting_address" in data and isinstance(data["new_access_setting_address"], str)# new access setting address
        # return true
        return True
    
    def compose_call(self, data:dict={}):
        return self.metarium_node.compose_call(
            call_module=self.__class__.SUBSTRATE_EXTRINSIC,
            call_function=self.__class__.FUNCTION_CALL,
            call_params={
                'topic_id': str(data["topic_id"]),
                'new_access_setting_address': data["new_access_setting_address"]
            }
        )