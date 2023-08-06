from typing import List, Optional, Dict, Tuple, Union
from ..application.assembler import Assembler
from .entity import (
    APIGatewayBlacklistItem,
    APIGatewayRequest,
    BootstrapInfo,
    ClusterConfig,
    ClusterConfigData,
    DatapipeDataInfo,
    DatapipeServerInfo,
    FileTemplateVariables,
    FilesTemplateVariables,
    RandomTemplateVariables
)
from .dto import (
    APIGatewayBlacklistItemDTO,
    APIGatewayRequestDTO,
    BootstrapInfoDTO,
    ClusterConfigDTO,
    ClusterConfigDataDTO,
    DatapipeDataInfoDTO,
    DatapipeServerInfoDTO,
    FileTemplateVariablesDTO,
    FilesTemplateVariablesDTO,
    RandomTemplateVariablesDTO
)
from .value_obj import (
    UDict,
    UInt,
    UStr
)



class DatapipeServerInfoAssembler(Assembler):
    def to_entity(self, dto: DatapipeServerInfoDTO):
        return DatapipeServerInfo(
            id = UStr(dto.id),
            secret = UStr(dto.secret),
            endpoint = UStr(dto.endpoint)
        )
    def to_dto(self, x:DatapipeServerInfo):
        return DatapipeServerInfoDTO(
            id = x.id.get_value(),
            secret = x.secret.get_value(),
            endpoint = x.endpoint.get_value()
        )
datapipe_server_info_assembler=DatapipeServerInfoAssembler()



class DatapipeDataInfoAssembler(Assembler):
    def to_entity(self, dto: DatapipeDataInfoDTO):
        return DatapipeDataInfo(
            bucket = UStr(dto.bucket),
            remote_path = UStr(dto.remote_path),
            local_path = UStr(dto.local_path),
            timeout = UInt(dto.timeout)
        )
    def to_dto(self, x:DatapipeDataInfo):
        return DatapipeDataInfoDTO(
            bucket = x.bucket.get_value(),
            remote_path = x.remote_path.get_value(),
            local_path = x.local_path.get_value(),
            timeout = x.timeout.get_value()
        )
datapipe_data_info_assembler=DatapipeDataInfoAssembler()



class ClusterConfigDataAssembler(Assembler):
    def to_entity(self, dto: ClusterConfigDataDTO):
        return ClusterConfigData(
            data_server = datapipe_server_info_assembler.to_entity(dto.data_server),
            data = [datapipe_data_info_assembler.to_entity(m) for m in dto.data]
        )
    def to_dto(self, x:ClusterConfigData):
        return ClusterConfigDataDTO(
            data_server = datapipe_server_info_assembler.to_do(x.data_server),
            data = [datapipe_data_info_assembler.to_do(m) for m in x.data]
        )
cluster_config_data_assembler=ClusterConfigDataAssembler()



class ClusterConfigAssembler(Assembler):
    def to_entity(self, dto: ClusterConfigDTO):
        return ClusterConfig(
            cluster_name = UStr(dto.cluster_name),
            region_id = UStr(dto.region_id),
            config_data = None if dto.config_data is None else cluster_config_data_assembler.to_entity(dto.config_data),
            entry_point = None if dto.entry_point is None else [UStr(m) for m in dto.entry_point],
            timeout = UInt(dto.timeout)
        )
    def to_dto(self, x:ClusterConfig):
        return ClusterConfigDTO(
            cluster_name = x.cluster_name.get_value(),
            region_id = x.region_id.get_value(),
            config_data = None if x.config_data is None else cluster_config_data_assembler.to_do(x.config_data),
            entry_point = None if x.entry_point is None else [m.get_value() for m in x.entry_point],
            timeout = x.timeout.get_value()
        )
cluster_config_assembler=ClusterConfigAssembler()



class BootstrapInfoAssembler(Assembler):
    def to_entity(self, dto: BootstrapInfoDTO):
        return BootstrapInfo(
            cluster_config = cluster_config_assembler.to_entity(dto.cluster_config),
            template = UStr(dto.template),
            platform = UStr(dto.platform),
            patch_setting = None if dto.patch_setting is None else UDict(dto.patch_setting)
        )
    def to_dto(self, x:BootstrapInfo):
        return BootstrapInfoDTO(
            cluster_config = cluster_config_assembler.to_do(x.cluster_config),
            template = x.template.get_value(),
            platform = x.platform.get_value(),
            patch_setting = None if x.patch_setting is None else x.patch_setting.get_value()
        )
bootstrap_info_assembler=BootstrapInfoAssembler()



class RandomTemplateVariablesAssembler(Assembler):
    def to_entity(self, dto: RandomTemplateVariablesDTO):
        return RandomTemplateVariables(
            variables = [UStr(m) for m in dto.variables],
            lengths = None if dto.lengths is None else [UInt(m) for m in dto.lengths]
        )
    def to_dto(self, x:RandomTemplateVariables):
        return RandomTemplateVariablesDTO(
            variables = [m.get_value() for m in x.variables],
            lengths = None if x.lengths is None else [m.get_value() for m in x.lengths]
        )
random_template_variables_assembler=RandomTemplateVariablesAssembler()



class FileTemplateVariablesAssembler(Assembler):
    def to_entity(self, dto: FileTemplateVariablesDTO):
        return FileTemplateVariables(
            variables = None if dto.variables is None else [UStr(m) for m in dto.variables],
            path = UStr(dto.path)
        )
    def to_dto(self, x:FileTemplateVariables):
        return FileTemplateVariablesDTO(
            variables = None if x.variables is None else [m.get_value() for m in x.variables],
            path = x.path.get_value()
        )
file_template_variables_assembler=FileTemplateVariablesAssembler()



class FilesTemplateVariablesAssembler(Assembler):
    def to_entity(self, dto: FilesTemplateVariablesDTO):
        return FilesTemplateVariables(
            variables = [UStr(m) for m in dto.variables],
            paths = [UStr(m) for m in dto.paths]
        )
    def to_dto(self, x:FilesTemplateVariables):
        return FilesTemplateVariablesDTO(
            variables = [m.get_value() for m in x.variables],
            paths = [m.get_value() for m in x.paths]
        )
files_template_variables_assembler=FilesTemplateVariablesAssembler()



class APIGatewayRequestAssembler(Assembler):
    def to_entity(self, dto: APIGatewayRequestDTO):
        return APIGatewayRequest(
            service_name = UStr(dto.service_name),
            ip = None if dto.ip is None else UStr(dto.ip),
            port = None if dto.port is None else UInt(dto.port),
            route = None if dto.route is None else UStr(dto.route),
            action = None if dto.action is None else UStr(dto.action),
            auth = None if dto.auth is None else UDict(dto.auth),
            method = UStr(dto.method),
            data = None if dto.data is None else UDict(dto.data)
        )
    def to_dto(self, x:APIGatewayRequest):
        return APIGatewayRequestDTO(
            service_name = x.service_name.get_value(),
            ip = None if x.ip is None else x.ip.get_value(),
            port = None if x.port is None else x.port.get_value(),
            route = None if x.route is None else x.route.get_value(),
            action = None if x.action is None else x.action.get_value(),
            auth = None if x.auth is None else x.auth.get_value(),
            method = x.method.get_value(),
            data = None if x.data is None else x.data.get_value()
        )
api_gateway_request_assembler=APIGatewayRequestAssembler()



class APIGatewayBlacklistItemAssembler(Assembler):
    def to_entity(self, dto: APIGatewayBlacklistItemDTO):
        return APIGatewayBlacklistItem(
            ip = UStr(dto.ip),
            creation_time = UStr(dto.creation_time),
            limit_time = UInt(dto.limit_time),
            limit_reason = UStr(dto.limit_reason)
        )
    def to_dto(self, x:APIGatewayBlacklistItem):
        return APIGatewayBlacklistItemDTO(
            ip = x.ip.get_value(),
            creation_time = x.creation_time.get_value(),
            limit_time = x.limit_time.get_value(),
            limit_reason = x.limit_reason.get_value()
        )
api_gateway_blacklist_item_assembler=APIGatewayBlacklistItemAssembler()
