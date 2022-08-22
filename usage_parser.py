import typing
# TODO: add pydocs and more comments
class UsageParser(object):
    @staticmethod
    def parse(*input: str) -> typing.List[typing.Mapping[str, typing.Any]]:
        return_list = []
        parsed_str = None
        for input_str in input:
            split_list, id, last_id_dig = UsageParser.parse_input(input_str)

            # extended
            if last_id_dig == '4':
                parsed_str = UsageParser.parse_extended(split_list, id)
            
            # hex
            elif last_id_dig == '6':
                parsed_str = UsageParser.parse_hex(split_list, id)
            
            # basic
            elif last_id_dig is not None:
                parsed_str = UsageParser.parse_basic(split_list, id)

            if parsed_str is not None:
                return_list.append(parsed_str)
            else:
                print(f'Failed to parse input string {input_str}')
        return return_list

    @staticmethod
    def convert_to_obj(id: str, mnc: str = None, bytes_used: str = None, dmcc: str = None, cellid: str = None, ip: str = None):
        
        def convert_field__not_null(val, convert_func):
            if val:
                print(f'{val} via {convert_func}')
                return convert_func(val)

        return_obj = {
            'id': convert_field__not_null(id, int),
            'bytes_used': convert_field__not_null(bytes_used, int),
            'dmcc': dmcc,
            'mnc':  convert_field__not_null(mnc, int),
            'cellid': convert_field__not_null(cellid, int),
            'ip': ip
        }
        return return_obj

    @staticmethod
    def convert_hex(hex_str: str):
        ip = f'{int(hex_str[16:18], base=16)}.{int(hex_str[18:20], base=16)}.{int(hex_str[20:22], base=16)}.{int(hex_str[22:24], base=16)}'
        return_obj = {
            'mnc': int(hex_str[0:4], base=16),
            'bytes_used': int(hex_str[4:8], base=16),
            'cellid': int(hex_str[8:16], base=16),
            'ip':  ip
        }
        return return_obj
    
    @staticmethod
    def parse_extended(input_list: typing.List[str], id: str):
        dmcc = input_list[1]
        mnc = input_list[2]
        bytes_used = input_list[3]
        cellid = input_list[4]
        return UsageParser.convert_to_obj(id=id, bytes_used=bytes_used, dmcc=dmcc, mnc=mnc, cellid=cellid)


    @staticmethod
    def parse_basic(input_list: typing.List[str], id: str):
        bytes_used = input_list[1]
        return UsageParser.convert_to_obj(id=id, bytes_used=bytes_used)

    @staticmethod
    def parse_hex(input_list: typing.List[str], id: str):
        hex_str = input_list[1]
        converted_hex = UsageParser.convert_hex(hex_str)
        return UsageParser.convert_to_obj(id=id,
                mnc = converted_hex['mnc'],
                bytes_used= converted_hex['bytes_used'],
                cellid = converted_hex['cellid'],
                ip=converted_hex['ip'])

    @staticmethod
    def parse_input(input_str: str):
        if input_str:
            split_list = input_str.split(',')
            # Input needs to have at least 2 components
            if len(split_list) > 1:
                id = split_list[0]
                last_id_dig = id[-1]
                return split_list,id,last_id_dig
        return None,None,None