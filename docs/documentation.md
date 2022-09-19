# What is winotify?

`winotify` is a python library and a command-line application for creating
Windows 10 toast notifications.

## Features

* Notification stays in the action center
* Clickable notification with 5 additional buttons
* Use a function as a callback when clicking the notification

## Installation

Install `winotify` using pip

```sh
pip install winotify
```

## Examples

### A simple notification with icon

```python
from winotify import Notification

toast = Notification(
    app_id="example app",
    title="Winotify Test Toast",
    msg="New Notification!",
    icon=r"C:\path\to\icon.png"
)

toast.show()
```

## Notification with buttons

```python
from winotify import Notification, audio

toast = Notification(...)
toast.add_actions(
    label="open github",
    launch="https://github.com/versa-syahptr/winotify/"
)
```

## Notification with notification sound

```python
from winotify import Notification, audio

toast = Notification(...)
toast.set_audio(audio.Mail, loop=False)
```

All supported audio can be found in the `audio` module.

## Notification with callback feature

This is an advanced feature of `winotify`. Please follow this guide carefully.

* Declare your app id, default interpreter, and script path globally

    ```python
    import winotify

    r = winotify.Registry("app_id", winotify.PY_EXE, r"c:\abs\path\to\script.py")
    notifier = winotify.Notifier(r)
    ```

* Register a function to use as a callback using the
  `Notifier.register_callback` decorator

    ```python
    @Notifier.register_callback
    def say_hello():
        print("hello")
    ```

* Create a new `Notification` using `Notifier.create_notification`, then pass
  the registered function to the `launch`-parameter,

    ```python
    toast = notifier.create_notification(
        title="a notification", 
        msg='a notification test with callback',
        launch=say_hello
    )

    # or pass it to Notification.add_actions

    toast.add_actions(
        label="say hello in console",
        launch=say_hello
    )
    ```

* Start the notifier thread

    ```python
    if __name__ == '__main__':
        notifier.start()
    ```

## Usage as a command-line application

```batch
winotify.exe ^
-id myApp ^
-t "A Title" ^
-m "A message" ^
-i "c:\path\to\icon.png" ^
--audio default ^
--open-url "http://google.com" ^
--action "open github" ^
--action_url "http://github.com"         
```

> Use `winotify-nc.exe` instead of `winotify.exe` to hide the console window.
