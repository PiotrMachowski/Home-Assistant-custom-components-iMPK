[![HACS Default][hacs_shield]][hacs]
[![GitHub Latest Release][releases_shield]][latest_release]
[![GitHub All Releases][downloads_total_shield]][releases]
[![Buy me a coffee][buy_me_a_coffee_shield]][buy_me_a_coffee]
[![PayPal.Me][paypal_me_shield]][paypal_me]


[hacs_shield]: https://img.shields.io/static/v1.svg?label=HACS&message=Default&style=popout&color=green&labelColor=41bdf5&logo=HomeAssistantCommunityStore&logoColor=white
[hacs]: https://hacs.xyz/docs/default_repositories

[latest_release]: https://github.com/PiotrMachowski/Home-Assistant-custom-components-iMPK/releases/latest
[releases_shield]: https://img.shields.io/github/release/PiotrMachowski/Home-Assistant-custom-components-iMPK.svg?style=popout

[releases]: https://github.com/PiotrMachowski/Home-Assistant-custom-components-iMPK/releases
[downloads_total_shield]: https://img.shields.io/github/downloads/PiotrMachowski/Home-Assistant-custom-components-iMPK/total

[buy_me_a_coffee_shield]: https://img.shields.io/static/v1.svg?label=%20&message=Buy%20me%20a%20coffee&color=6f4e37&logo=buy%20me%20a%20coffee&logoColor=white
[buy_me_a_coffee]: https://www.buymeacoffee.com/PiotrMachowski

[paypal_me_shield]: https://img.shields.io/static/v1.svg?label=%20&message=PayPal.Me&logo=paypal
[paypal_me]: https://paypal.me/PiMachowski

# iMPK sensor

These sensors use unofficial API retrieved by decompilation of [*iMPK*](https://play.google.com/store/apps/details?id=pl.wasko.android.mpk) application.
Binary sensor provides a list of news available in the original app, sensor retrieves departures for desired stops.

## Configuration options

### Binary sensor

| Key | Type | Required | Default | Description |
| --- | --- | --- | --- | --- |
| `name` | `string` | `False` | `iMPK` | Name of sensor |
| `monitored_conditions` | `list` | `True` | - | List of conditions to monitor |

#### Possible monitored conditions

| Key | Description |
| --- | --- | 
| `news` | List of news available in application |

### Sensor

| Key | Type | Required | Default | Description |
| --- | --- | --- | --- | --- |
| `name` | `string` | `False` | `iMPK` | Name of sensor |
| `stops` | `list` | `True` | - | List of stop configurations |

#### Stop configuration

| Key | Type | Required | Default | Description |
| --- | --- | --- | --- | --- |
| `id` | `positive integer` | `True` | - | ID of a stop |
| `name` | `string` | `False` | id | Name of a stop |
| `lines` | `list` | `False` | all available | List of monitored lines. |
| `directions` | `list` | `False` | all available | List of monitored directions. |

## Example usage

```yaml
binary_sensor:
  - platform: impk
    monitored_conditions:
      - news
sensor:
  - platform: impk
    stops:
      - id: 120820
      - id: 124202
        lines:
          - "D"
          - "131"
      - id: 124202
        name: "REJA"
        directions:
          - "REJA"
```

## Installation

### Using [HACS](https://hacs.xyz/) (recommended)

This integration can be installed using HACS.
To do it search for `iMPK` in *Integrations* section.

### Manual

To install this integration manually you have to download [*impk.zip*](https://github.com/PiotrMachowski/Home-Assistant-custom-components-iMPK/releases/latest/download/impk.zip) and extract its contents to `config/custom_components/impk` directory:
```bash
mkdir -p custom_components/impk
cd custom_components/impk
wget https://github.com/PiotrMachowski/Home-Assistant-custom-components-iMPK/releases/latest/download/impk.zip
unzip impk.zip
rm impk.zip
```

## Hints

* These sensors provides attributes which can be used in [*HTML card*](https://github.com/PiotrMachowski/Home-Assistant-Lovelace-HTML-card) or [*HTML Template card*](https://github.com/PiotrMachowski/Home-Assistant-Lovelace-HTML-Template-card): `html`, `html_timetable`, `html_departures`
  * HTML card:
    ```yaml
    - type: custom:html-card
      title: 'iMPK'
      content: |
        <big><center>News</center></big>
        [[ binary_sensor.impk_news.attributes.html ]]
        <big><center>Timetable</center></big>
        [[ sensor.impk_120820.attributes.html_timetable ]]
        <big><center>Departures</center></big>
        [[ sensor.impk_124202.attributes.html_departures ]]
    ```
  * HTML Template card:
    ```yaml
    - type: custom:html-template-card
      title: 'iMPK'
      ignore_line_breaks: true
      content: |
        <big><center>News</center></big></br>
        {{ state_attr('binary_sensor.impk_news','html') }}
        </br><big><center>Timetable</center></big></br>
        {{ state_attr('sensor.impk_120820','html_timetable') }}
        </br><big><center>Departures</center></big></br>
        {{ state_attr('sensor.impk_124202','html_departures') }}
    ```
* This integration is available in [*HACS*](https://github.com/custom-components/hacs/).

<a href="https://www.buymeacoffee.com/PiotrMachowski" target="_blank"><img src="https://bmc-cdn.nyc3.digitaloceanspaces.com/BMC-button-images/custom_images/orange_img.png" alt="Buy Me A Coffee" style="height: auto !important;width: auto !important;" ></a>
<a href="https://paypal.me/PiMachowski" target="_blank"><img src="https://www.paypalobjects.com/webstatic/mktg/logo/pp_cc_mark_37x23.jpg" border="0" alt="PayPal Logo" style="height: auto !important;width: auto !important;"></a>
