import requests
import urllib3
from datetime import datetime, timedelta
from requests.auth import HTTPDigestAuth

import voluptuous as vol

from homeassistant.components.sensor import PLATFORM_SCHEMA, ENTITY_ID_FORMAT
from homeassistant.const import CONF_ID, CONF_NAME
import homeassistant.helpers.config_validation as cv
from homeassistant.helpers.entity import Entity
from homeassistant.helpers.entity import async_generate_entity_id

CONF_STOPS = 'stops'
CONF_LINES = 'lines'
DEFAULT_NAME = 'iMPK'

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend({
    vol.Optional(CONF_NAME, default=DEFAULT_NAME): cv.string,
    vol.Required(CONF_STOPS): vol.All(cv.ensure_list, [
        vol.Schema({
            vol.Required(CONF_ID): cv.positive_int,
            vol.Optional(CONF_NAME): cv.string,
            vol.Optional(CONF_LINES, default=[]): cv.ensure_list
        })])
})


def setup_platform(hass, config, add_entities, discovery_info=None):
    name = config.get(CONF_NAME)
    stops = config.get(CONF_STOPS)
    available_stops = IMPKSensor.get_stops()
    dev = []
    for stop in stops:
        stop_id = str(stop.get(CONF_ID))
        lines = stop.get(CONF_LINES)
        real_stop_name = IMPKSensor.get_stop_name(stop_id, available_stops)
        if real_stop_name is None:
            raise Exception("Invalid stop id: {}".format(stop_id))
        stop_name = stop.get(CONF_NAME) or stop_id
        uid = '{}_{}'.format(name, stop_name)
        entity_id = async_generate_entity_id(ENTITY_ID_FORMAT, uid, hass=hass)
        dev.append(IMPKSensor(entity_id, name, stop_id, stop_name, real_stop_name, lines))
    add_entities(dev, True)


class IMPKSensor(Entity):
    def __init__(self, entity_id, name, stop_id, stop_name, real_stop_name, watched_lines):
        self.entity_id = entity_id
        self._name = name
        self._stop_id = stop_id
        self._watched_lines = watched_lines
        self._stop_name = stop_name
        self._real_stop_name = real_stop_name
        self._departures = []
        self._departures_number = 0
        self._departures_by_line = dict()

    @property
    def name(self):
        return '{} - {}'.format(self._name, self._stop_name)

    @property
    def state(self):
        if self._departures_number is not None and self._departures_number > 0:
            dep = self._departures[0]
            return IMPKSensor.departure_to_str(dep)
        return None

    @property
    def unit_of_measurement(self):
        return None

    @property
    def device_state_attributes(self):
        attr = dict()
        attr['stop_name'] = self._real_stop_name
        if self._departures is not None:
            attr['list'] = self._departures
            attr['html_timetable'] = self.get_html_timetable()
            attr['html_departures'] = self.get_html_departures()
            if self._departures_number > 0:
                dep = self._departures[0]
                attr['line'] = dep["line"]
                attr['direction'] = dep["direction"]
                attr['departure'] = dep["departure"]
                attr['time_to_departure'] = dep["time_to_departure"]
                attr['original_departure'] = dep["original_departure"]
                attr['delay'] = dep["delay"]
        return attr

    def update(self):
        now = datetime.now()
        departures = IMPKSensor.get_departures(self._stop_id)
        if departures is None:
            return
        positions = IMPKSensor.get_positions()
        courses = list(map(lambda d: d["c"], departures))
        delays = IMPKSensor.get_delays(courses, positions)
        print(positions)
        stops = IMPKSensor.get_stops()
        parsed_departures = []
        for departure_details in departures:
            line = departure_details["l"]
            time = departure_details["t"]
            course = departure_details["c"]
            if len(self._watched_lines) > 0 and line not in self._watched_lines:
                continue
            direction = IMPKSensor.get_stop_name(departure_details["d"], stops)
            delay = delays[course] if course in delays else 0
            original_departure = datetime.strptime(time, '%Y-%m-%d %H:%M:%S')
            departure = original_departure + timedelta(milliseconds=delay)
            time_to_departure = (departure - now).total_seconds() // 60
            parsed_departures.append(
                {
                    "line": line,
                    "direction": direction,
                    "departure": "{:02}:{:02}".format(departure.hour, departure.minute),
                    "original_departure": "{:02}:{:02}".format(original_departure.hour, original_departure.minute),
                    "time_to_departure": int(time_to_departure),
                    "delay": int(delay // 1000)
                })
        self._departures = parsed_departures
        self._departures_number = len(parsed_departures)
        self._departures_by_line = IMPKSensor.group_by_line(self._departures)

    def get_html_timetable(self):
        html = '<table width="100%" border=1 style="border: 1px black solid; border-collapse: collapse;">\n'
        lines = list(self._departures_by_line.keys())
        lines.sort()
        for line in lines:
            directions = list(self._departures_by_line[line].keys())
            directions.sort()
            for direction in directions:
                if len(direction) == 0:
                    continue
                html = html + '<tr><td style="text-align: center; padding: 4px"><big>{}, kier. {}</big></td>'.format(
                    line, direction)
                departures = ', '.join(map(lambda x: x["departure"], self._departures_by_line[line][direction]))
                html = html + '<td style="text-align: right; padding: 4px">{}</td></tr>\n'.format(departures)
        if len(lines) == 0:
            html = html + '<tr><td style="text-align: center; padding: 4px">Brak połączeń</td>'
        html = html + '</table>'
        return html

    def get_html_departures(self):
        html = '<table width="100%" border=1 style="border: 1px black solid; border-collapse: collapse;">\n'
        for departure in self._departures:
            html = html + '<tr><td style="text-align: center; padding: 4px">{}</td></tr>\n'.format(
                IMPKSensor.departure_to_str(departure))
        html = html + '</table>'
        return html

    @staticmethod
    def departure_to_str(dep):
        return '{}, kier. {}: {} ({}m)'.format(dep["line"], dep["direction"], dep["departure"],
                                              dep["time_to_departure"])

    @staticmethod
    def group_by_line(departures):
        departures_by_line = dict()
        for departure in departures:
            line = departure["line"]
            direction = departure["direction"]
            if line not in departures_by_line:
                departures_by_line[line] = dict()
            if direction not in departures_by_line[line]:
                departures_by_line[line][direction] = []
            departures_by_line[line][direction].append(departure)
        return departures_by_line

    @staticmethod
    def get_stop_name(stop_id, stops):
        found = list(filter(lambda stop: stop_id in map(lambda post: post["s"], stop['p']), stops))
        return found[0]["n"] if found else None

    @staticmethod
    def get_delays(courses, positions):
        delays = dict()
        # list(filter(lambda position: "course" in position and position["course"] in courses, positions))
        for position in positions:
            if len(delays) == len(courses):
                break
            if "course" not in position or position["course"] not in courses:
                continue
            course = position["course"]
            delay = position["delay"]
            delays[course] = int(delay)
        return delays

    @staticmethod
    def get_positions():
        return IMPKSensor.get_data("getPositions")

    @staticmethod
    def get_stops():
        return IMPKSensor.get_data("getPosts")

    @staticmethod
    def get_departures(stop_id):
        return IMPKSensor.get_data("getPostInfo&symbol={}".format(stop_id))

    @staticmethod
    def get_data(function):
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
        address = 'https://62.233.178.84:8088/mobile?function={}'.format(function)
        response = requests.get(address, auth=HTTPDigestAuth('android-mpk', 'g5crehAfUCh4Wust'), verify=False)
        if response.status_code == 200 and response.content.__len__() > 0:
            return response.json()
        return None
