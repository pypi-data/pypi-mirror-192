# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['aiochannel']

package_data = \
{'': ['*']}

install_requires = \
['pylama>=8.4.1,<9.0.0']

setup_kwargs = {
    'name': 'aiochannel',
    'version': '1.2.0',
    'description': 'asyncio Channels (closable queues) inspired by golang',
    'long_description': '|Build Status|\n|Python Versions|\n\naiochannel - AsyncIO Channel\n============================\n\nChannel concept for asyncio.\n\n*requires* Python 3.6+\n\n`PyPI link <https://pypi.org/project/aiochannel>`__\n`GitHub link <https://github.com/tbug/aiochannel>`__\n\nInstall\n-------\n\n::\n\n   pip install aiochannel\n\nUsage\n-----\n\nBasics\n~~~~~~\n\n``Channel`` has a very similar API to ``asyncio.Queue``.\nThe key difference is that a channel is only considered\n"done" when it has been both closed and drained, so calling ``.join()``\non a channel will wait for it to be both closed and drained (Unlike\n``Queue`` which will return from ``.join()`` once the queue is empty).\n\n*NOTE* Closing a channel is permanent. You cannot open it again.\n\n.. code-block:: python\n       :name: test_simple\n\n       import asyncio\n       from aiochannel import Channel\n\n       # ...\n\n       async def main():\n           # A Channel takes a max queue size and an loop\n           # both optional. loop is not recommended as\n           # in asyncio is phasing out explicitly passed event-loop\n           my_channel: Channel[str] = Channel(100)\n\n           # You add items to the channel with\n           await my_channel.put("my item")\n           # Note that this can throw ChannelClosed if the channel\n           # is closed, during the attempt at adding the item\n           # to the channel. Also note that .put() will block until\n           # it can successfully add the item.\n\n\n           # Retrieving is done with\n           my_item = await my_channel.get()\n           # Note that this can also throw ChannelClosed if the\n           # channel is closed before or during retrival.\n           # .get() will block until an item can be retrieved.\n\n           # Note that this requires someone else to close and drain\n           # the channel.\n           # Lastly, you can close a channel with `my_channel.close()`\n           # In this example, the event-loop call this asynchronously\n           asyncio.get_event_loop().call_later(0.1, my_channel.close)\n\n           # You can wait for the channel to be closed and drained:\n           await my_channel.join()\n\n           # Every call to .put() after .close() will fail with\n           # a ChannelClosed.\n           # you can check if a channel is marked for closing with\n           if my_channel.closed():\n               print ("Channel is closed")\n\n       asyncio.run(main())\n\n\nLike the ``asyncio.Queue`` you can also call non-async get and put:\n\n\n.. code-block:: python\n\n\n       # non-async version of put\n       my_channel.put_nowait(item)\n       # This either returns None,\n       # or raises ChannelClosed or ChannelFull\n\n       # non-async version of get\n       my_channel.get_nowait()\n       # This either returns the next item from the channel\n       # or raises ChannelEmpty or ChannelClosed\n       # (Note that ChannelClosed emplies that the channel\n       # is empty, but also that is will never fill again)\n\nAs of ``0.2.0`` ``Channel`` also implements the async iterator protocol.\nYou can now use ``async for`` to iterate over the channel until it\ncloses, without having to deal with ``ChannelClosed`` exceptions.\n\n.. code-block:: python\n\n\n       # the channel might contain data here\n       async for item in channel:\n           print(item)\n       # the channel is closed and empty here\n\nwhich is functionally equivalent to\n\n.. code-block:: python\n\n\n       while True:\n           try:\n               data = yield from channel.get()\n           except ChannelClosed:\n               break\n\n           # process data here\n\nNoteworthy changes\n~~~~~~~~~~~~~~~~~~\n\n1.2.0\n^^^^^\n\nAdded typing support with generics. Now you can specify the type\nexplicitly, your IDE or mypy will follow this annotations.\n\n\n.. code-block:: python\n\n    from aiochannel import Channel\n\n    channel: Channel[str] = Channel(100)\n\n\nFixing issue #13 that could lead to "getters" waiting forever\nwhen a channel was closed with less items then pending getters.\n\n0.2.0\n^^^^^\n\n``Channel`` implements the async iterator protocol. You can use\n``async for`` to iterate over the channel until it closes, without\nhaving to deal with ``ChannelClosed`` exceptions.\n\nSee the ``async for`` example.\n\n.. _section-1:\n\n0.2.3\n^^^^^\n\n``Channel`` proxies it’s ``__iter__`` to the underlying queue\nimplementation’s ``__iter__`` (which by default is\n``collections.deque``), meaning that you are now able to iterate channel\nvalues (which also enables ``list(channel)``).\n\n.. _section-2:\n\n1.0.0\n^^^^^\n\nDropping 3.4’s ``@coroutine`` annotations. Everything is now defined\nwith ``async``.\n\n\n1.1.0\n^^^^^\n\nDropping Python 3.5 support.\n\n\n1.1.1\n^^^^^\n\nFixing an ``InvalidStateError`` when get or put futures were cancelled.\n\n\n.. |Build Status| image:: https://github.com/tbug/aiochannel/actions/workflows/test.yml/badge.svg\n   :target: https://github.com/tbug/aiochannel/actions/workflows/test.yml\n\n.. |Python Versions| image:: https://img.shields.io/pypi/pyversions/aiochannel.svg\n   :target: https://pypi.org/project/aiochannel/\n',
    'author': 'Henrik Tudborg',
    'author_email': 'henrik@tudb.org',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/tbug/aiochannel',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7.2,<4.0.0',
}


setup(**setup_kwargs)
