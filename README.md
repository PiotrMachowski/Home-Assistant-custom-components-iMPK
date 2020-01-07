# iMPK sensor

[![hacs_badge](https://img.shields.io/badge/HACS-Default-orange.svg)](https://github.com/custom-components/hacs)
[![buymeacoffee_badge](https://img.shields.io/badge/Donate-buymeacoffe-ff813f?style=flat)](https://www.buymeacoffee.com/PiotrMachowski)

This sensor uses unofficial API retrieved by decompilation of [*iMPK*](https://play.google.com/store/apps/details?id=pl.wasko.android.mpk) application to provide a list of news available in original app.

## Configuration options

| Key | Type | Required | Default | Description |
| --- | --- | --- | --- | --- |
| `name` | `string` | `False` | `iMPK` | Name of sensor |
| `monitored_conditions` | `list` | `True` | - | List of conditions to monitor |

### Possible monitored conditions

| Key | Description |
| --- | --- | 
| `news` | List of news available in application |

## Example usage

```
binary_sensor:
  - platform: impk
    monitored_conditions:
      - news
```

## Installation

Download [*binary_sensor.py*](https://github.com/PiotrMachowski/Home-Assistant-custom-components-iMPK/raw/master/custom_components/impk/binary_sensor.py) and [*manifest.json*](https://github.com/PiotrMachowski/Home-Assistant-custom-components-iMPK/raw/master/custom_components/impk/manifest.json) to `config/custom_components/impk` directory:
```bash
mkdir -p custom_components/impk
cd custom_components/impk
wget https://github.com/PiotrMachowski/Home-Assistant-custom-components-iMPK/raw/master/custom_components/impk/binary_sensor.py
wget https://github.com/PiotrMachowski/Home-Assistant-custom-components-iMPK/raw/master/custom_components/impk/manifest.json
```

## Hints

* This binary sensor provides `html` attribute which can be used in [*HTML card*](https://github.com/PiotrMachowski/Home-Assistant-Lovelace-HTML-card) or [*HTML Template card*](https://github.com/PiotrMachowski/Home-Assistant-Lovelace-HTML-Template-card):
  * HTML card:
    ```yaml
    - type: custom:html-card
      title: 'iMPK'
      content: |
        <big><center>News</center></big>
        [[ binary_sensor.impk_news.attributes.html ]]
    ```
  * HTML Template card:
    ```yaml
    - type: custom:html-template-card
      title: 'iMPK'
      ignore_line_breaks: true
      content: |
        <big><center>News</center></big>
        {{ state_attr('binary_sensor.impk_news','html') }}
    ```
* This integration is available in [*HACS*](https://github.com/custom-components/hacs/).

<a href="https://www.buymeacoffee.com/PiotrMachowski" target="_blank"><img src="https://bmc-cdn.nyc3.digitaloceanspaces.com/BMC-button-images/custom_images/orange_img.png" alt="Buy Me A Coffee" style="height: auto !important;width: auto !important;" ></a>
