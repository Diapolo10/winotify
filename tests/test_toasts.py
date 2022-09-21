import unittest
from pathlib import Path

from winotify import Notification
from winotify.audio import Sound


class MyTestCase(unittest.TestCase):
    def test_toast(self):
        toast = Notification(app_id="winotify test",
                             title="Winotify Test Toast",
                             msg="New Notification!")

        toast.show()
        print(toast.script)

    def test_toast_with_icon(self):
        toast = Notification(app_id="winotify test",
                             title="Winotify Test Toast With Icon",
                             msg="New Notification!",
                             icon=Path(__file__).parent / "icon.png")

        toast.show()
        print(toast.script)

    def test_toast_with_sound(self):
        toast = Notification(app_id="winotify test",
                             title="Winotify Test Toast",
                             msg="New Notification!")
        toast.set_audio(Sound.SMS, loop=False)

        toast.show()
        print(toast.script)

    def test_toast_illegal_char(self):
        toast = Notification(app_id="winotify test",
                             title="This is illegal >>",
                             msg="< [YEAH] >")

        toast.show()
        print(toast.script)

    def test_toast_non_english(self):
        toast = Notification(app_id="winotify test",
                             title="السلام عليكم",
                             msg="Peace be upon you!")

        toast.show()
        print(toast.script)

    def test_toast_with_action(self):
        toast = Notification(app_id="winotify test",
                             title="Winotify Test Toast",
                             msg="New Notification with actions!")
        toast.add_actions("go to github", "https://github.com/versa-syahptr/winotify")

        toast.show()
        print(toast.script)


if __name__ == '__main__':
    unittest.main()
