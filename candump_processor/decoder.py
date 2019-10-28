
import json 
import codecs
from collections import OrderedDict 


class decoder():
    
    def __init__(self, definitions):
        #json definitions file
        self.map = json.load(open(definitions,'r'))

    def update_map(self, msg_id, msg_payload):
        if msg_id in self.map.keys():
            for j in self.map[str(msg_id)]:
                result = self._update_value(msg_payload, j["func"], **j["kwargs"])
                if result != "skip":
                    j['result'] = result

    def _update_value(self, payload, func, **kwargs):

        if func == "bit_is_set":
            return self._bit_is_set(payload, **kwargs)

        if func == "byte_by_val":
            return self._byte_by_val(payload, **kwargs)

        if func == "byte_is_equal":
            return self._byte_is_equal(payload, **kwargs)

        if func == "byte_minus_val":
            return self._byte_minus_val(payload, **kwargs)

        if func == "byte_value":
            return self._byte_value(payload, **kwargs)

        if func == "lidar_distance":
            return self._lidar_distance(payload, **kwargs)

        if func == "steer_angle":
            return self._steer_angle(payload, **kwargs)

        if func == "wheel_speed":
            return self._wheel_speed(payload, **kwargs)

        if func == "word_by_val":
            return self._word_by_val(payload, **kwargs)

        if func == "special_ids_40a":
            return self._special_ids_40a(payload, **kwargs)


    def _bit_is_set(self, payload, **kwargs):
        return payload[kwargs["byte_position"]] >> kwargs["offset"] & 1

    def _byte_by_val(self, payload, **kwargs):
        return payload[kwargs["byte_position"]]/kwargs["val"]

    def _byte_is_equal(self, payload, **kwargs):
        return 1 if payload[kwargs["byte_position"]] == kwargs["val"] else 0

    def _byte_minus_val(self, payload, **kwargs):
        return payload[kwargs["byte_position"]] - kwargs["val"]

    def _byte_value(self, payload, **kwargs):
        return payload[kwargs["byte_position"]]

    def _lidar_distance(self, payload, **kwargs):
        return (payload[kwargs["byte_position"]]/2.54)/10 if payload[kwargs["byte_position"]] < 0x7F else 0

    def _steer_angle(self, payload, **kwargs):
        return (payload[kwargs["hi_byte"]] * 256 + payload[kwargs["lo_byte"]]) * 0.1 - 1600

    def _wheel_speed(self, payload, **kwargs):
        return ((payload[kwargs["hi_byte"]] * 256 + payload[kwargs["lo_byte"]]) -10000)/100

    def _word_by_val(self, payload, **kwargs):
        return (payload[kwargs["hi_byte"]] * 256 + payload[kwargs["lo_byte"]]) / kwargs["val"]

    def _special_ids_40a(self, payload, **kwargs):
        if payload[0] == kwargs["idx1"] and payload[1] == kwargs["idx2"] and kwargs["sub"] == "odo":
            return payload[kwargs["p1"]] * 256 * 256 + payload[kwargs["p2"]] * 256 + payload[kwargs["p3"]]

        if payload[0] == kwargs["idx1"] and payload[1] == kwargs["idx2"] and kwargs["sub"] == "outtemp":
            return payload[kwargs["p1"]] - 40

        if payload[0] == kwargs["idx1"] and payload[1] == kwargs["idx2"] and kwargs["sub"] == "vin1":
            return payload[2:8].decode()

        if payload[0] == kwargs["idx1"] and payload[1] == kwargs["idx2"] and kwargs["sub"] == "vin2":
            return payload[2:8].decode()

        if payload[0] == kwargs["idx1"] and payload[1] == kwargs["idx2"] and kwargs["sub"] == "vin3":
            return  payload[2:7].decode()

        return "skip"

    def output(self):
        return self.map
