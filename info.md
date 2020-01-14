[![hacs_badge](https://img.shields.io/badge/HACS-Default-orange.svg)](https://github.com/custom-components/hacs)
[![buymeacoffee_badge](https://img.shields.io/badge/Donate-buymeacoffe-ff813f?style=flat)](https://www.buymeacoffee.com/PiotrMachowski)

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

## Example usage

```
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

<a href="https://www.buymeacoffee.com/PiotrMachowski" target="_blank"><img src="https://bmc-cdn.nyc3.digitaloceanspaces.com/BMC-button-images/custom_images/orange_img.png" alt="Buy Me A Coffee" style="height: auto !important;width: auto !important;" ></a>
