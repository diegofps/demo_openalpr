#!/usr/bin/python3

import pyinotify
import asyncio


def handle_read_callback(notifier):
    print('handle_read callback')
    notifier.loop.stop()


wm = pyinotify.WatchManager()
loop = asyncio.get_event_loop()
notifier = pyinotify.AsyncioNotifier(wm, loop,
                                     callback=handle_read_callback)
wm.add_watch('.', pyinotify.ALL_EVENTS)
loop.run_forever()
notifier.stop()

