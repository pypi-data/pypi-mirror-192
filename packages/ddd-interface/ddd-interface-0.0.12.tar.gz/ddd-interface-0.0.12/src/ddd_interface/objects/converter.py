from typing import List, Optional, Dict, Tuple, Union
from ..infrastructure.converter import Converter
from .entity import (
    APIGatewayBlacklistItem,
    APIGatewayRequest,
    BootstrapInfo,
    ClusterConfig,
    ClusterConfigData,
    Condition,
    DatapipeDataInfo,
    DatapipeServerInfo,
    FileTemplateVariables,
    FilesTemplateVariables,
    RandomTemplateVariables,
    TaskRequest
)
from .do import (
    APIGatewayBlacklistItemDO,
    APIGatewayRequestDO,
    BootstrapInfoDO,
    ClusterConfigDO,
    ClusterConfigDataDO,
    ConditionDO,
    DatapipeDataInfoDO,
    DatapipeServerInfoDO,
    FileTemplateVariablesDO,
    FilesTemplateVariablesDO,
    RandomTemplateVariablesDO,
    TaskRequestDO
)
from .value_obj import (
    UDict,
    UInt,
    UStr
)



class ConditionConverter(Converter):
    def to_entity(self, do: ConditionDO):
        return Condition(
            min_cpu_num = None if do.min_cpu_num is None else UInt(do.min_cpu_num),
            max_cpu_num = None if do.max_cpu_num is None else UInt(do.max_cpu_num),
            min_memory_size = None if do.min_memory_size is None else UInt(do.min_memory_size),
            max_memory_size = None if do.max_memory_size is None else UInt(do.max_memory_size),
            min_gpu_num = None if do.min_gpu_num is None else UInt(do.min_gpu_num),
            max_gpu_num = None if do.max_gpu_num is None else UInt(do.max_gpu_num),
            min_gpu_memory_size = None if do.min_gpu_memory_size is None else UInt(do.min_gpu_memory_size),
            max_gpu_memory_size = None if do.max_gpu_memory_size is None else UInt(do.max_gpu_memory_size)
        )
    def to_do(self, x:Condition):
        return ConditionDO(
            min_cpu_num = None if x.min_cpu_num is None else x.min_cpu_num.get_value(),
            max_cpu_num = None if x.max_cpu_num is None else x.max_cpu_num.get_value(),
            min_memory_size = None if x.min_memory_size is None else x.min_memory_size.get_value(),
            max_memory_size = None if x.max_memory_size is None else x.max_memory_size.get_value(),
            min_gpu_num = None if x.min_gpu_num is None else x.min_gpu_num.get_value(),
            max_gpu_num = None if x.max_gpu_num is None else x.max_gpu_num.get_value(),
            min_gpu_memory_size = None if x.min_gpu_memory_size is None else x.min_gpu_memory_size.get_value(),
            max_gpu_memory_size = None if x.max_gpu_memory_size is None else x.max_gpu_memory_size.get_value()
        )
condition_converter=ConditionConverter()



class DatapipeServerInfoConverter(Converter):
    def to_entity(self, do: DatapipeServerInfoDO):
        return DatapipeServerInfo(
            id = UStr(do.id),
            secret = UStr(do.secret),
            endpoint = UStr(do.endpoint)
        )
    def to_do(self, x:DatapipeServerInfo):
        return DatapipeServerInfoDO(
            id = x.id.get_value(),
            secret = x.secret.get_value(),
            endpoint = x.endpoint.get_value()
        )
datapipe_server_info_converter=DatapipeServerInfoConverter()



class DatapipeDataInfoConverter(Converter):
    def to_entity(self, do: DatapipeDataInfoDO):
        return DatapipeDataInfo(
            bucket = UStr(do.bucket),
            remote_path = UStr(do.remote_path),
            local_path = UStr(do.local_path),
            timeout = UInt(do.timeout)
        )
    def to_do(self, x:DatapipeDataInfo):
        return DatapipeDataInfoDO(
            bucket = x.bucket.get_value(),
            remote_path = x.remote_path.get_value(),
            local_path = x.local_path.get_value(),
            timeout = x.timeout.get_value()
        )
datapipe_data_info_converter=DatapipeDataInfoConverter()



class ClusterConfigDataConverter(Converter):
    def to_entity(self, do: ClusterConfigDataDO):
        return ClusterConfigData(
            data_server = datapipe_server_info_converter.to_entity(do.data_server),
            data = [datapipe_data_info_converter.to_entity(m) for m in do.data]
        )
    def to_do(self, x:ClusterConfigData):
        return ClusterConfigDataDO(
            data_server = datapipe_server_info_converter.to_do(x.data_server),
            data = [datapipe_data_info_converter.to_do(m) for m in x.data]
        )
cluster_config_data_converter=ClusterConfigDataConverter()



class ClusterConfigConverter(Converter):
    def to_entity(self, do: ClusterConfigDO):
        return ClusterConfig(
            cluster_name = UStr(do.cluster_name),
            region_id = UStr(do.region_id),
            config_data = None if do.config_data is None else cluster_config_data_converter.to_entity(do.config_data),
            entry_point = None if do.entry_point is None else [UStr(m) for m in do.entry_point],
            timeout = UInt(do.timeout)
        )
    def to_do(self, x:ClusterConfig):
        return ClusterConfigDO(
            cluster_name = x.cluster_name.get_value(),
            region_id = x.region_id.get_value(),
            config_data = None if x.config_data is None else cluster_config_data_converter.to_do(x.config_data),
            entry_point = None if x.entry_point is None else [m.get_value() for m in x.entry_point],
            timeout = x.timeout.get_value()
        )
cluster_config_converter=ClusterConfigConverter()



class BootstrapInfoConverter(Converter):
    def to_entity(self, do: BootstrapInfoDO):
        return BootstrapInfo(
            cluster_config = cluster_config_converter.to_entity(do.cluster_config),
            template = UStr(do.template),
            platform = UStr(do.platform),
            patch_setting = None if do.patch_setting is None else UDict(do.patch_setting)
        )
    def to_do(self, x:BootstrapInfo):
        return BootstrapInfoDO(
            cluster_config = cluster_config_converter.to_do(x.cluster_config),
            template = x.template.get_value(),
            platform = x.platform.get_value(),
            patch_setting = None if x.patch_setting is None else x.patch_setting.get_value()
        )
bootstrap_info_converter=BootstrapInfoConverter()



class RandomTemplateVariablesConverter(Converter):
    def to_entity(self, do: RandomTemplateVariablesDO):
        return RandomTemplateVariables(
            variables = [UStr(m) for m in do.variables],
            lengths = None if do.lengths is None else [UInt(m) for m in do.lengths]
        )
    def to_do(self, x:RandomTemplateVariables):
        return RandomTemplateVariablesDO(
            variables = [m.get_value() for m in x.variables],
            lengths = None if x.lengths is None else [m.get_value() for m in x.lengths]
        )
random_template_variables_converter=RandomTemplateVariablesConverter()



class FileTemplateVariablesConverter(Converter):
    def to_entity(self, do: FileTemplateVariablesDO):
        return FileTemplateVariables(
            variables = None if do.variables is None else [UStr(m) for m in do.variables],
            path = UStr(do.path)
        )
    def to_do(self, x:FileTemplateVariables):
        return FileTemplateVariablesDO(
            variables = None if x.variables is None else [m.get_value() for m in x.variables],
            path = x.path.get_value()
        )
file_template_variables_converter=FileTemplateVariablesConverter()



class FilesTemplateVariablesConverter(Converter):
    def to_entity(self, do: FilesTemplateVariablesDO):
        return FilesTemplateVariables(
            variables = [UStr(m) for m in do.variables],
            paths = [UStr(m) for m in do.paths]
        )
    def to_do(self, x:FilesTemplateVariables):
        return FilesTemplateVariablesDO(
            variables = [m.get_value() for m in x.variables],
            paths = [m.get_value() for m in x.paths]
        )
files_template_variables_converter=FilesTemplateVariablesConverter()



class APIGatewayRequestConverter(Converter):
    def to_entity(self, do: APIGatewayRequestDO):
        return APIGatewayRequest(
            service_name = UStr(do.service_name),
            method = UStr(do.method),
            ip = None if do.ip is None else UStr(do.ip),
            port = None if do.port is None else UInt(do.port),
            route = None if do.route is None else UStr(do.route),
            action = None if do.action is None else UStr(do.action),
            auth = None if do.auth is None else UDict(do.auth),
            data = None if do.data is None else UDict(do.data)
        )
    def to_do(self, x:APIGatewayRequest):
        return APIGatewayRequestDO(
            service_name = x.service_name.get_value(),
            method = x.method.get_value(),
            ip = None if x.ip is None else x.ip.get_value(),
            port = None if x.port is None else x.port.get_value(),
            route = None if x.route is None else x.route.get_value(),
            action = None if x.action is None else x.action.get_value(),
            auth = None if x.auth is None else x.auth.get_value(),
            data = None if x.data is None else x.data.get_value()
        )
api_gateway_request_converter=APIGatewayRequestConverter()



class APIGatewayBlacklistItemConverter(Converter):
    def to_entity(self, do: APIGatewayBlacklistItemDO):
        return APIGatewayBlacklistItem(
            ip = UStr(do.ip),
            creation_time = UStr(do.creation_time),
            limit_time = UInt(do.limit_time),
            limit_reason = UStr(do.limit_reason)
        )
    def to_do(self, x:APIGatewayBlacklistItem):
        return APIGatewayBlacklistItemDO(
            ip = x.ip.get_value(),
            creation_time = x.creation_time.get_value(),
            limit_time = x.limit_time.get_value(),
            limit_reason = x.limit_reason.get_value()
        )
api_gateway_blacklist_item_converter=APIGatewayBlacklistItemConverter()



class TaskRequestConverter(Converter):
    def to_entity(self, do: TaskRequestDO):
        return TaskRequest(
            task_name = UStr(do.task_name),
            region_id = UStr(do.region_id),
            condition = condition_converter.to_entity(do.condition),
            git_url = None if do.git_url is None else UStr(do.git_url),
            git_branch = None if do.git_branch is None else UStr(do.git_branch),
            task_type = None if do.task_type is None else UStr(do.task_type),
            task_template = None if do.task_template is None else UStr(do.task_template),
            task_env = None if do.task_env is None else UStr(do.task_env),
            task_command = None if do.task_command is None else [UStr(m) for m in do.task_command],
            task_arg = None if do.task_arg is None else [UStr(m) for m in do.task_arg],
            task_working_dir = None if do.task_working_dir is None else UStr(do.task_working_dir),
            task_image = None if do.task_image is None else UStr(do.task_image),
            task_start_time = None if do.task_start_time is None else UStr(do.task_start_time),
            priority = UInt(do.priority),
            amount = UInt(do.amount),
            duration = None if do.duration is None else UInt(do.duration),
            disk_size = None if do.disk_size is None else UInt(do.disk_size),
            end_style = UStr(do.end_style),
            restart_policy = UStr(do.restart_policy),
            timeout = UInt(do.timeout),
            cluster_name = None if do.cluster_name is None else UStr(do.cluster_name)
        )
    def to_do(self, x:TaskRequest):
        return TaskRequestDO(
            task_name = x.task_name.get_value(),
            region_id = x.region_id.get_value(),
            condition = condition_converter.to_do(x.condition),
            git_url = None if x.git_url is None else x.git_url.get_value(),
            git_branch = None if x.git_branch is None else x.git_branch.get_value(),
            task_type = None if x.task_type is None else x.task_type.get_value(),
            task_template = None if x.task_template is None else x.task_template.get_value(),
            task_env = None if x.task_env is None else x.task_env.get_value(),
            task_command = None if x.task_command is None else [m.get_value() for m in x.task_command],
            task_arg = None if x.task_arg is None else [m.get_value() for m in x.task_arg],
            task_working_dir = None if x.task_working_dir is None else x.task_working_dir.get_value(),
            task_image = None if x.task_image is None else x.task_image.get_value(),
            task_start_time = None if x.task_start_time is None else x.task_start_time.get_value(),
            priority = x.priority.get_value(),
            amount = x.amount.get_value(),
            duration = None if x.duration is None else x.duration.get_value(),
            disk_size = None if x.disk_size is None else x.disk_size.get_value(),
            end_style = x.end_style.get_value(),
            restart_policy = x.restart_policy.get_value(),
            timeout = x.timeout.get_value(),
            cluster_name = None if x.cluster_name is None else x.cluster_name.get_value()
        )
task_request_converter=TaskRequestConverter()
