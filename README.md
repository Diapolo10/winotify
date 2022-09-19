# Winotify

A pure python module to show notification toast on Windows 10.

No dependencies, no requirements, all you need is PowerShell installed on your
machine (which every Windows computer does).

## Installation

Install winotify using `pip`

```sh
pip install winotify
```

## Features

* Notification stays in the action center
* Clickable notification with 5 additional buttons
* Use a function as a callback when clicking the notification

## Usage

### A simple notification with icon

```python
from winotify import Notification

toast = Notification(
    app_id="windows app",
    title="Winotify Test Toast",
    msg="New Notification!",
    icon=r"C:\path\to\icon.png"
)

toast.show()
```

**Result:**

![Example notification][notification_screenshot]

**The notification stays in the action centre!**

![Notification in the action centre][action_centre_screenshot]

> Note that the icon path must be **absolute**, otherwise
the notification will not show.

### Set the notification sound

All supported audio can be found in the `audio` module.

```python
from winotify import Notification, audio

toast = Notification(...)
toast.set_audio(audio.Mail, loop=False)
```

### Add action button

```python
from winotify import Notification

toast = Notification(...)
toast.add_actions(label="Button text", 
                  launch="https://github.com/versa-syahptr/winotify/")
```

> You can add up to 5 buttons each notification

## CLI

```batch
winotify ^
-id myApp ^
-t "A Title" ^
-m "A message" ^
-i "c:\path\to\icon.png" ^
--audio default ^
--open-url "http://google.com" ^
--action "open github" ^
--action_url "http://github.com"         
```

> Use `winotify-nc` instead of `winotify` to hide the console window.

## Contributing

Pull requests are welcome. For major changes, please open an issue first to
discuss what you would like to change.

Please make sure to update tests as appropriate.

## Licence

This project is licensed under the permissive[MIT][license] license.

[notification_screenshot]: ./docs/assets/winotify_ss1.png?raw=true
[action_centre_screenshot]: ./docs/assets/winotify_ss2.png?raw=true
[license]: ./LICENSE
