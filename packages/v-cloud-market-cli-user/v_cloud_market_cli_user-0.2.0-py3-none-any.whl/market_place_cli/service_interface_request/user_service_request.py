from rich.console import Console
from rich.prompt import IntPrompt

from market_place_cli.utils.regex import is_image_name, is_valid_path
from market_place_cli.utils.string_utils import get_unit_num
class UserServiceRequest:

    def __init__(self, console: Console):
        self.console = console

    def get_user_service_id(self) -> str:
        msg = '[bright_green]Please enter the user service id: '
        return self.console.input(msg)

    def get_api_func(self, apis) -> (bool, str):
        api_types = ['normal', 'secret']
        while True:
            is_secret = False
            self.console.print('Please Choose API Type: ')
            msg = '[purple]1[/] -- Normal API Request\n' + \
                '[purple]2[/] -- Secret API Request\n'
            self.console.print(msg)
            choice = self._get_int_num('[bright_green]Please choose a number: ')
            if choice < 1 or choice > 2:
                continue
            is_secret = choice == 2
            while True:
                keys = list(apis[api_types[choice-1]].keys())
                api_func_msg = ''
                for index in range(len(keys)):
                    api_func_msg += f'[purple]{index+1}[/]' + ' -- ' + keys[index] + '\n'
                self.console.print(api_func_msg)
                api_func_choice = self._get_int_num('[bright_green]Please choose an API function: ')
                while api_func_choice < 1 or api_func_choice > len(keys):
                    self.console.print('[bright_red]!! Invalid Index Number !!\n')
                    api_func_choice = self._get_int_num('[bright_green]Please choose an API function: ')
                return is_secret, keys[api_func_choice-1]

    def _get_int_num(self, msg):
        try:
            choice = int(self.console.input(msg))
            return choice
        except ValueError:
            self.console.print('[bright_red]The input you entered in invalid.')
            return 0

    def get_image_info(self, check_image_func: callable) -> str:
        img_name_tag = None
        msg = '[bright_green]Please enter the image name on Docker Hub: '
        while img_name_tag is None:
            value = self.console.input(msg)
            colon_index = value.rfind(":")
            if colon_index < 0:
                value += ":latest"
            if not is_image_name(value):
                msg = '[bright_red]Please enter a valid image name: '
                continue
            if not check_image_func(value):
                msg = '[bright_red]Please enter a publicly accessible image on Docker Hub: '
                continue
            img_name_tag = value
        return img_name_tag

    def get_ports(self, service_options: dict, provider_host: str, check_port_func: callable) -> list:
        resource_unit = service_options.get("resourceUnit", None)
        port_specification = service_options.get("portSpecification", None)
        region = service_options.get("region", None)
        if resource_unit is None or port_specification is None or region is None:
            self.console.print('[bright_red]Invalid service options.')
            return
        # get num of container-host ports pair
        try:
            host_port_num = get_unit_num(resource_unit)
        except ValueError:
                self.console.print('[bright_red]Invalid resource unit.')
        occupation_num = -1
        while occupation_num < 0 or occupation_num > host_port_num:
            try:
                occupation_num = int(self.console.input(f'[bright_green]{host_port_num} host port(s) available. Please input the number of host port(s) you want: '))
            except ValueError:
                self.console.print(f'[bright_red]Invalid input, please input number from 0 to {host_port_num}.')

        port_configs = []
        self.console.print(f'{occupation_num} port(s) will be set by user')
        for x in range(occupation_num):
            self.console.print(f'Container or host port {x + 1}:')
            container_port = self.get_container_port(port_configs)
            port_config = {
                "containerPort": container_port
            }
            if port_specification == "User Specified Service Port":
                host_port = self.get_host_port(region, provider_host, port_configs, check_port_func)
                port_config["hostPort"] = host_port
            protocol = self.get_port_protocol()
            if protocol:
                port_config["protocol"] = protocol
            port_configs.append(port_config)
        return port_configs

    def get_envs(self):
        env_list = []
        env_num = 0
        while True:
            result = self.console.input("Please input the number of env params you want(optional): ").strip()
            if result == '':
                break
            if not result.isdigit():
                self.console.print('[bright_red]Invalid input, please input number. ')
                continue
            env_num = int(result)
            break
        if env_num > 0:
            for i in range(env_num):
                name = ''
                value = ''
                while True:
                    try:
                        name = self.console.input(f"Please enter the name for env {i+1}(not empty and no space included): ").strip(" ")
                        if name and " " not in name:
                            while True:
                                value = self.console.input(f"Please enter the value for {name}(not empty): ").strip(" ")
                                if value:
                                    break
                            break
                    except Exception as e:
                        print('e')
                env = {
                    "name": name,
                    "value": value
                }
                env_list.append(env)
        return env_list

    def get_port_protocol(self) -> str:
        protocol_list = ['TCP', 'UDP']
        protocol = ''
        while protocol not in protocol_list:
            protocol = self.console.input('Please enter the protocol of the port (TCP or UDP, default TCP): ').strip().upper()
            if protocol in protocol_list or protocol == '':
                return protocol
            self.console.print('[bright_red]Invalid protocol.')

    def get_container_port(self, ports_configs: list) -> int:
        value = 0
        while value <= 0 or value > 65535:
            try:
                value = int(self.console.input('Please enter the container port: '))
                # check repetition
                for config in ports_configs:
                    if config["containerPort"] == value:
                        self.console.print('[bright_red]Container port cannot be repetitive! Please use another port.')
                        value = 0
            except ValueError:
                self.console.print('[bright_red]Invalid port number.')
                value = 0
        return value

    def get_host_port(self, region: str, provider_host: str, ports_configs: list, check_port_func: callable) -> int:
        value = 0
        msg = '[bright_green]Please input host port: '
        is_valid = False
        while not is_valid:
            try:
                value = int(self.console.input(msg))
                is_valid = value <= 0 or value > 65535
                if is_valid:
                    msg = '[bright_red]Please use a valid port number within the range of 1 - 65535: '
                    continue
                is_duplcated = False
                for config in ports_configs:
                    is_duplcated = (config["hostPort"] == value)
                if is_duplcated:
                    self.console.print('[bright_red]Host port cannot be repetitive! Please use another port.')
                    continue
                resp = check_port_func([value], region, provider_host)
                status = resp.get("status", None)
                is_valid = status is None or status == "NotOccupied"
                if not is_valid:
                    msg = '[bright_red]The inputted port has been occupied. Please change the port number: '
            except ValueError as e:
                print(e)
                msg = '[bright_red]Please enter a valid integer: '
                value = 0
        return value

    def get_mount_path(self) -> str:
        msg = "[bright_green]Please enter the directory to mount the data: "
        mount_path = self.console.input(msg)
        while not is_valid_path(mount_path):
            mount_path = self.console.input("[bright_red]Mount path is invalid: ")
        return mount_path
