import typing

# TODO: ADD A TON OF ERROR HANDLING
# Input = None
# No commas included


class UsageParser(object):
    @staticmethod
    def parse(*input: str) -> typing.List[typing.Mapping[str, typing.Any]]:
        return_list = []
        parsed_str = None
        for input_str in input:
            split_list = input_str.split(',')
            id = split_list[0]
            last_id_dig = id[-1]

            # extended
            if last_id_dig == '4':
                dmcc = split_list[1]
                mnc = split_list[2]
                bytes_used = split_list[3]
                cellid = split_list[4]
                parsed_str = UsageParser.convert_to_obj(id=id, bytes_used=bytes_used, dmcc=dmcc, mnc=mnc, cellid=cellid)
            
            # hex
            elif last_id_dig == '6':
                hex_str = split_list[1]
                converted_hex = UsageParser.convert_hex(hex_str)
                parsed_str = UsageParser.convert_to_obj(id=id,
                mnc = converted_hex['mnc'],
                bytes_used= converted_hex['bytes_used'],
                cellid = converted_hex['cellid'],
                ip= converted_hex['ip'])
            
            # basic
            else:
                bytes_used = split_list[1]
                parsed_str = UsageParser.convert_to_obj(id=id, bytes_used=bytes_used)

            return_list.append(parsed_str)
        return return_list

    @staticmethod
    def convert_to_obj(id: str, mnc: str = None, bytes_used: str = None, dmcc: str = None, cellid: str = None, ip: str = None):
        
        def convert_field__not_null(val, convert_func):
            if val:
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
    