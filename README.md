# iMPK sensor

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

## Instalation

Download [*binary_sensor.py*](https://github.com/PiotrMachowski/Home-Assistant-custom-components-iMPK/raw/master/binary_sensor.py) and [*manifest.json*](https://github.com/PiotrMachowski/Home-Assistant-custom-components-iMPK/raw/master/manifest.json) to `config/custom_compoments/impk` directory:
```bash
mkdir -p custom_compoments/impk
cd custom_compoments/impk
wget https://github.com/PiotrMachowski/Home-Assistant-custom-components-iMPK/raw/master/binary_sensor.py
wget https://github.com/PiotrMachowski/Home-Assistant-custom-components-iMPK/raw/master/manifest.json
```

## Hints

This binary sensor provide `html` attribute which can be used in [*Lovelace HTML card*](https://github.com/PiotrMachowski/Home-Assistant-Lovelace-HTML-card):
```yaml
- type: custom:html-card
  title: 'iMPK'
  data:
    - html: '<big><center>News</center></big>'
    - entity_id: binary_sensor.impk_news
      attribute: html
```