"""
.. include:: ../docs/documentation.md
"""


import argparse
import atexit
import os
import queue
import subprocess
import sys
import warnings
from typing import Callable, Dict, List, Union

from winotify.audio import Sound
from winotify.config import TEMP_DIR, TOAST_SCRIPT_TEMPLATE
from winotify._communication import Listener, Sender
from winotify._registry import Registry, format_name


__version__ = "1.1.0"
__all__ = ("Notifier", "Notification", "Registry", "Sound")


def _run_ps(*, file='', command=''):
    startup_info = subprocess.STARTUPINFO()
    startup_info.dwFlags |= subprocess.STARTF_USESHOWWINDOW

    cmd = ["powershell.exe", "-ExecutionPolicy", "Bypass"]

    # We can't have both, but we need either
    if bool(file) == bool(command):
        raise ValueError

    if file:
        cmd.extend(["-file", file])
    elif command:
        cmd.extend(['-Command', command])

    with subprocess.Popen(
        cmd,
        # stdin, stdout, and stderr have to be defined here, because windows tries to duplicate these if not null
        stdin=subprocess.DEVNULL,
        stdout=subprocess.DEVNULL,  # set to null because we don't need the output :)
        stderr=subprocess.DEVNULL,
        startupinfo=startup_info
    ):
        pass


class Notification:
    """
    Creates a new notification
    """

    def __init__(self,
                 app_id: str,
                 title: str,
                 msg: str = "",
                 icon: str = "",
                 duration: str = 'short',
                 launch: str = ''):
        """
        Construct a new notification

        Args:
            app_id: your app name, make it readable to your user. It can contain spaces, however special characters
                    (eg. é) are not supported.
            title: The heading of the toast.
            msg: The content/message of the toast.
            icon: An optional path to an image to display on the left of the title & message.
                  Make sure the path is absolute.
            duration: How long the toast should show up for (short/long), default is short.
            launch: The url or callback to launch (invoked when the user clicks the notification)

        Notes:
            If you want to pass a callback to `launch` parameter,
            please use `create_notification` from `Notifier` object

        Raises:
            ValueError: If the duration specified is not short or long
        """

        self.app_id = app_id
        self.title = title
        self.msg = msg
        self.icon = icon
        self.duration = duration
        self.launch = launch
        self.audio: str = Sound.Silent
        self.tag = self.title
        self.group = self.app_id
        self.actions: List[str] = []
        if duration not in ("short", "long"):
            raise ValueError("Duration is not 'short' or 'long'")

    @property
    def script(self):
        """
        Auto-formats the Toast script
        """
        return TOAST_SCRIPT_TEMPLATE.format(
            launch=self.launch,
            duration=self.duration,
            icon=self.icon,
            title=self.title,
            msg=self.msg,
            actions='\n'.join(self.actions),
            audio=self.audio if self.audio != Sound.Silent else '<audio silent="true" />',
            tag=self.tag,
            group=self.group,
            app_id=self.app_id
        )

    def set_audio(self, sound: str, loop: bool):
        """
        Set the audio for the notification

        Args:
            sound: The audio to play when the notification is showing. Choose one from `winotify.audio` module,
                   (eg. audio.Sound.Default). The default for all notification is silent.
            loop: If True, the audio will play indefinitely until user clicks or dismisses the notification.

        """

        self.audio = f'<audio src="{sound}" loop="{str(loop).lower()}" />'

    def add_actions(self, label: str, launch: Union[str, Callable] = ""):
        """
        Add buttons to the notification. Each notification can have 5 buttons max.

        Args:
            label: The label of the button
            launch: The url to launch when clicking the button, 'file:///' protocol is allowed. Or a registered
                    callback function

        Returns: None

        Notes:
            Register a callback function using `Notifier.register_callback()` decorator before passing it here

        Raises:
              ValueError: If the callback function is not registered
        """

        if callable(launch):
            if hasattr(launch, 'url'):
                url = launch.url  # type: ignore
            else:
                raise ValueError(f"{launch} is not registered")
        else:
            url = launch

        xml = '<action activationType="protocol" content="{label}" arguments="{link}" />'
        if len(self.actions) < 5:
            self.actions.append(xml.format(label=label, link=url))

    def build(self):
        """
        This method is deprecated, call `Notification.show()` directly instead.

        Warnings:
            DeprecationWarning

        """
        warnings.warn("build method is deprecated, call show directly instead", DeprecationWarning)
        return self

    def show(self):
        """
        Show the toast
        """
        self.actions = '\n'.join(self.actions)

        if self.launch:
            self.launch = f'activationType="protocol" launch="{self.launch}"'

        _run_ps(command=self.script)


class Notifier:
    """Handles the part of displaying the notifications"""

    def __init__(self, registry: Registry):
        """
        A `Notification` manager class.

        Args:
            registry: A `Registry` instance containing the `app_id`, default interpreter, and the script path.
        """
        self.app_id = registry.app_id
        self.icon = ""
        pidfile = TEMP_DIR / f'{self.app_id}.pid'

        # alias for callback_to_url()
        self.cb_url = self.callback_to_url

        if self._protocol_launched:
            # communicate to main process if it's alive
            self.func_to_call = sys.argv[1].split(':')[1]
            self._cb: Dict[str, Callable] = {}  # callbacks are stored here because we have no listener
            if os.path.isfile(pidfile):
                sender = Sender(self.app_id)
                sender.send(self.func_to_call)
                sys.exit()
        else:
            self.listener = Listener(self.app_id)
            with open(pidfile, 'w', encoding='utf-8') as file:
                file.write(str(os.getpid()))  # pid file
            atexit.register(os.unlink, pidfile)

    @property
    def callbacks(self):
        """
        Returns:
            A dictionary containing all registered callbacks, with each function's name as the key

        """
        if hasattr(self, 'listener'):
            return self.listener.callbacks
        return self._cb

    def set_icon(self, path: str):
        """
        Set icon globally for all notification
        Args:
            path: The absolute path of the icon

        Returns:
            None

        """
        self.icon = path

    def create_notification(self,
                            title: str,
                            msg: str = '',
                            icon: str = '',
                            duration: str = 'short',
                            launch: Union[str, Callable] = '') -> Notification:
        """

        See Also:
            `Notification`

        Notes:
            `launch` parameter can be a callback function here

        Returns:
            `Notification` object

        """
        if self.icon:
            icon = self.icon

        if callable(launch):
            url = self.callback_to_url(launch)
        else:
            url = launch

        notif = Notification(self.app_id, title, msg, icon, duration, url)
        return notif

    def start(self):
        """
        Start the listener thread. This method *must* be called first in the main function,
        Otherwise, all the callback function will never get called.

        Examples:
            ```python
            if __name__ == "__main__":
                notifier.start()
                ...
            ```
        """
        if self._protocol_launched:  # call the callback directly
            self.callbacks.get(self.func_to_call)()

        else:
            self.listener.callbacks.update(self.callbacks)
            self.listener.thread.start()

    def update(self):
        """
        check for available callback function in queue then call it
        this method *must* be called *every time* in loop.

        If all callback functions don't need to run in main thread, calling this functions is *optional*

        Examples:
            ```python
            # the main loop
            while True:
                notifier.update()
                ...
            ```
        """
        if self._protocol_launched:
            return

        listener_queue = self.listener.queue
        try:
            func = listener_queue.get_nowait()
            if callable(func):
                func()
            else:
                print(f"{func.__name__} ")
        except queue.Empty:
            pass

    @property
    def _protocol_launched(self) -> bool:
        """
        check whether the app is opened directly or via notification

        Returns:
            True, if opened from notification; False if opened directly
        """
        if len(sys.argv) <= 1:
            return False

        arg = sys.argv[1]
        return format_name(self.app_id) + ':' in arg and len(arg.split(':')) > 0

    def register_callback(self, function=None, *, run_in_main_thread=False):
        """
        A decorator to register a function to be used as a callback
        Args:
            func: the function to decorate
            run_in_main_thread: If True, the callback function will run in main thread

        Examples:
            ```python
            @notifier.register_callback
            def foo(): ...
            ```

        Returns:
            The registered function

        """
        def inner(func):
            if run_in_main_thread:
                func.rimt = run_in_main_thread
            self.callbacks[func.__name__] = func
            func.url = self.callback_to_url(func)
            return func

        if function is None:
            return inner

        return inner(function)

    def callback_to_url(self, func: Callable) -> str:
        """
        Translate the registered callback function `func` to url notation.

        Args:
            func: The registered callback function

        Returns:
             url-notation string eg. `my-app-id:foo`, where **my-app-id** is the app id
             and **foo** is the function name

        """
        url = ''
        if callable(func) and func.__name__ in self.callbacks:
            url = format_name(self.app_id) + ":" + func.__name__
        return url

    def clear(self):
        """
        Clear all notification created by `Notifier` from action center

        """
        cmd = (
            "[Windows.UI.Notifications.ToastNotificationManager,"
            " Windows.UI.Notifications, ContentType = WindowsRuntime] > $null\n"
            f"[Windows.UI.Notifications.ToastNotificationManager]::History.Clear('{self.app_id}')"
        )
        _run_ps(command=cmd)


def main():
    """Runs the program"""
    audio_map = {key.lower(): value for key, value in Sound._asdict().items()}

    parser = argparse.ArgumentParser(
        prog="winotify[-nc]",
        description="Show notification toast on Windows 10. Use 'winotify-nc' for no console window."
    )
    parser.version = __version__
    parser.add_argument('-id',
                        '--app-id',
                        metavar="NAME",
                        default="windows app",
                        help="Your app name")
    parser.add_argument("-t",
                        "--title",
                        default="Winotify Test Toast",
                        help="the notification title")
    parser.add_argument("-m",
                        "--message",
                        default='New Notification!',
                        help="the notification's main messages")
    parser.add_argument("-i",
                        "--icon",
                        default='',
                        metavar="PATH",
                        help="the icon path for the notification (note: the path must be absolute)")
    parser.add_argument("--duration",
                        default="short",
                        choices=("short", "long"),
                        help="the duration of the notification should display (default: short)")
    parser.add_argument("--open-url",
                        default='',
                        metavar='URL',
                        help="the URL to open when user click the notification")
    parser.add_argument("--audio",
                        help="type of audio to play (default: silent)")
    parser.add_argument("--loop",
                        action="store_true",
                        help="whether to loop audio")
    parser.add_argument("--action",
                        metavar="LABEL",
                        action="append",
                        help="add button with LABEL as text, you can add up to 5 buttons")
    parser.add_argument("--action-url",
                        metavar="URL",
                        action="append",
                        required=("--action" in sys.argv),
                        help="an URL to launch when the button clicked")
    parser.add_argument("-v",
                        "--version",
                        action="version")

    args = parser.parse_args()

    toast = Notification(args.app_id,
                         args.title,
                         args.message,
                         args.icon,
                         args.duration,
                         args.open_url)

    if args.audio is not None:
        if args.audio not in audio_map.keys():
            sys.exit("Invalid audio " + args.audio)
        else:
            toast.set_audio(audio_map[args.audio], args.loop)

    actions = args.action
    action_urls = args.action_url
    if actions and action_urls:
        if len(actions) == len(action_urls):
            dik = dict(zip(actions, action_urls))
            for action, url in dik.items():
                toast.add_actions(action, url)
        else:
            parser.error("imbalance arguments, "
                         "the amount of action specified is not the same as the specified amount of action-url")

    toast.show()


if __name__ == '__main__':
    main()
