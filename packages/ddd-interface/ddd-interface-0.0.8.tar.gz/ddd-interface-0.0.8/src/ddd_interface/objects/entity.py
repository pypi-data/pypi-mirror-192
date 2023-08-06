import datetime
from typing import List, Optional, Dict, Tuple, Union
from ..domain.entity import Entity
from .value_obj import (
    UDict,
    UInt,
    UStr
)



class DatapipeServerInfo(Entity):
    def __init__(
        self,
        id: UStr,
        secret: UStr,
        endpoint: UStr,
        **kwargs
    ) -> None:
        all_args=locals()
        del all_args['self']
        del all_args['__class__']
        del all_args['kwargs']
        super().__init__(**all_args)
        self.id = id
        self.secret = secret
        self.endpoint = endpoint



class DatapipeDataInfo(Entity):
    def __init__(
        self,
        bucket: UStr,
        remote_path: UStr,
        local_path: UStr,
        timeout: UInt = 3,
        **kwargs
    ) -> None:
        all_args=locals()
        del all_args['self']
        del all_args['__class__']
        del all_args['kwargs']
        super().__init__(**all_args)
        self.bucket = bucket
        self.remote_path = remote_path
        self.local_path = local_path
        self.timeout = timeout



class ClusterConfigData(Entity):
    def __init__(
        self,
        data_server: DatapipeServerInfo,
        data: List[DatapipeDataInfo],
        **kwargs
    ) -> None:
        all_args=locals()
        del all_args['self']
        del all_args['__class__']
        del all_args['kwargs']
        super().__init__(**all_args)
        self.data_server = data_server
        self.data = data



class ClusterConfig(Entity):
    def __init__(
        self,
        cluster_name: UStr,
        region_id: UStr,
        config_data: Optional[ClusterConfigData] = None,
        entry_point: Optional[List[UStr]] = None,
        timeout: UInt = 20,
        **kwargs
    ) -> None:
        all_args=locals()
        del all_args['self']
        del all_args['__class__']
        del all_args['kwargs']
        super().__init__(**all_args)
        self.cluster_name = cluster_name
        self.region_id = region_id
        self.config_data = config_data
        self.entry_point = entry_point
        self.timeout = timeout



class BootstrapInfo(Entity):
    def __init__(
        self,
        cluster_config: ClusterConfig,
        template: UStr = 'normal',
        platform: UStr = 'aliyun',
        patch_setting: Optional[UDict] = None,
        **kwargs
    ) -> None:
        all_args=locals()
        del all_args['self']
        del all_args['__class__']
        del all_args['kwargs']
        super().__init__(**all_args)
        self.cluster_config = cluster_config
        self.template = template
        self.platform = platform
        self.patch_setting = patch_setting



class RandomTemplateVariables(Entity):
    def __init__(
        self,
        variables: List[UStr],
        lengths: Optional[List[UInt]] = None,
        **kwargs
    ) -> None:
        all_args=locals()
        del all_args['self']
        del all_args['__class__']
        del all_args['kwargs']
        super().__init__(**all_args)
        self.variables = variables
        self.lengths = lengths



class FileTemplateVariables(Entity):
    def __init__(
        self,
        variables: Optional[List[UStr]],
        path: UStr,
        **kwargs
    ) -> None:
        all_args=locals()
        del all_args['self']
        del all_args['__class__']
        del all_args['kwargs']
        super().__init__(**all_args)
        self.variables = variables
        self.path = path



class FilesTemplateVariables(Entity):
    def __init__(
        self,
        variables: List[UStr],
        paths: List[UStr],
        **kwargs
    ) -> None:
        all_args=locals()
        del all_args['self']
        del all_args['__class__']
        del all_args['kwargs']
        super().__init__(**all_args)
        self.variables = variables
        self.paths = paths



class APIGatewayRequest(Entity):
    def __init__(
        self,
        service_name: UStr,
        ip: Optional[UStr] = None,
        port: Optional[UInt] = None,
        route: Optional[UStr] = None,
        action: Optional[UStr] = None,
        auth: Optional[UDict] = None,
        method: UStr,
        data: Optional[UDict] = None,
        **kwargs
    ) -> None:
        all_args=locals()
        del all_args['self']
        del all_args['__class__']
        del all_args['kwargs']
        super().__init__(**all_args)
        self.service_name = service_name
        self.ip = ip
        self.port = port
        self.route = route
        self.action = action
        self.auth = auth
        self.method = method
        self.data = data



class APIGatewayBlacklistItem(Entity):
    def __init__(
        self,
        ip: UStr,
        creation_time: UStr,
        limit_time: UInt,
        limit_reason: UStr,
        **kwargs
    ) -> None:
        all_args=locals()
        del all_args['self']
        del all_args['__class__']
        del all_args['kwargs']
        super().__init__(**all_args)
        self.ip = ip
        self.creation_time = creation_time
        self.limit_time = limit_time
        self.limit_reason = limit_reason