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

## Hints

This binary sensor provides `html` attribute which can be used in [*HTML card*](https://github.com/PiotrMachowski/Home-Assistant-Lovelace-HTML-card) or [*HTML Template card*](https://github.com/PiotrMachowski/Home-Assistant-Lovelace-HTML-Template-card):
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