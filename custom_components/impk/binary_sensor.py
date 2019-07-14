import requests
import urllib3
from requests.auth import HTTPDigestAuth

import voluptuous as vol

from homeassistant.components.binary_sensor import PLATFORM_SCHEMA, ENTITY_ID_FORMAT
from homeassistant.const import CONF_MONITORED_CONDITIONS, CONF_NAME
import homeassistant.helpers.config_validation as cv
from homeassistant.components.binary_sensor import BinarySensorDevice
from homeassistant.helpers.entity import async_generate_entity_id

CONF_NEWS = 'news'

DEFAULT_NAME = 'iMPK'

SENSOR_TYPES = {
    CONF_NEWS: ['getNews', 'm', 'Informacje']
}

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend({
    vol.Required(CONF_NAME, default=DEFAULT_NAME): cv.string,
    vol.Required(CONF_MONITORED_CONDITIONS, default=[]):
        vol.All(cv.ensure_list, [vol.In(SENSOR_TYPES)])
})


def setup_platform(hass, config, add_entities, discovery_info=None):
    name = config.get(CONF_NAME)
    dev = []
    for monitored_condition in config[CONF_MONITORED_CONDITIONS]:
        uid = '{}_{}'.format(name, monitored_condition)
        entity_id = async_generate_entity_id(ENTITY_ID_FORMAT, uid, hass=hass)
        dev.append(IMPKSensor(entity_id, name, monitored_condition))
    add_entities(dev, True)


class IMPKSensor(BinarySensorDevice):
    def __init__(self, entity_id, name, sensor_type):
        self.entity_id = entity_id
        self._name = name
        self._sensor_type = sensor_type
        self._news_list = []
        self._function = SENSOR_TYPES[sensor_type][0]
        self._parameter_name = SENSOR_TYPES[sensor_type][1]
        self._sensor_name = SENSOR_TYPES[sensor_type][2]

    @property
    def name(self):
        return '{} - {}'.format(self._name, self._sensor_name)

    @property
    def device_state_attributes(self):
        attr = dict()
        if self._news_list is not None:
            attr['list'] = self._news_list
            attr['html'] = self.get_html()
        return attr

    @property
    def is_on(self):
        return len(self._news_list) > 0

    def update(self):
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
        address = 'https://62.233.178.84:8088/mobile?function={}'.format(self._function)
        response = requests.get(address, auth=HTTPDigestAuth('android-mpk', 'g5crehAfUCh4Wust'), verify=False)
        if response.status_code == 200 and response.content.__len__() > 0:
            news = response.json()
            self._news_list = []
            for n in news:
                self._news_list.append(n[self._parameter_name])

    def get_html(self):
        html = '<table width="100%" border=1 style="border: 1px black solid; border-collapse: collapse;">\n'
        for n in self._news_list:
            html = html + '<tr><td style="padding: 4px">{}</td>'.format(n)
        if len(self._news_list) == 0:
            html = html + '<tr><td style="text-align: center; padding: 4px">Brak powiadomień</td>'
        html = html + '</table>'
        return html

