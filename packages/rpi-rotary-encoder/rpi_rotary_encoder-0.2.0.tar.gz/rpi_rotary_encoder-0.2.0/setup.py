# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['rotary_encoder']

package_data = \
{'': ['*']}

install_requires = \
['rotary-encoder-gpio-core>=0.1.0,<0.2.0']

setup_kwargs = {
    'name': 'rpi-rotary-encoder',
    'version': '0.2.0',
    'description': 'A rotary encoder library for the raspberry pi that "just works"',
    'long_description': '# Rotary Encoder\n\nA rotary encoder package for the Raspberry pi that "just works".\n\nTested with a [KY-040 Rotary Encoder](https://www.rcscomponents.kiev.ua/datasheets/ky-040-datasheet.pdf) on a Raspberry pi 3 B+\n\n## Installation\n\nInstall via pip:\n```\npip install rpi-rotary-encoder\n```\n\n## Example\n\n```python\nimport rotary_encoder\n\n\ncounter = 0\n\ndef increment():\n    global counter\n    counter += 1\n    print(counter)\n\n\ndef decrement():\n    global counter\n    counter -= 1\n    print(counter)\n\n\ndef press():\n    print("PRESS")\n\n\ndef release():\n    print("RELEASE")\n\n\nwith rotary_encoder.connect(\n    clk_pin=20,                           # required\n    dt_pin=21,                            # required\n    sw_pin=26,                            # optional\n    on_clockwise_turn=increment,          # optional\n    on_counter_clockwise_turn=decrement,  # optional\n    on_button_down=press,                 # optional\n    on_button_up=release,                 # optional\n):\n    input("press enter to quit\\n")\n```\n\n\n## Advanced Usage\n\nWhen calling `connect` you can pass in an optional `callback_handling` argument. This controls how the callbacks are executed. The options are:\n\n- `CallbackHandling.GLOBAL_WORKER_THREAD`: The default. Callbacks are called in a global worker thread. This means all callbacks across all rotary encoders are called in the same thread. This ensures that all callbacks are executed sequentially. This is the least likely to cause problems with race conditions.\n- `CallbackHandling.LOCAL_WORKER_THREAD`: Similar to the above, except that each individual rotary encoders callbacks are executed on a different thread. This means that sequential execution of the callbacks of one encoder is still guaranteed, but not across several encoders. The responsiveness of the individual encoders may be slightly improved.\n- `CallbackHandling.SPAWN_THREAD`: Spawn a new thread for every callback. The execution of your callbacks is no longer sequential, and you will have to make sure that your callbacks are thread safe.\n- `CallbackHandling.GPIO_INTERUPT_THREAD`:  Not recommended. Similar in behavior to `CallbackHandling.SPAWN_THREAD` except that the threads are spawned by the underlying C extension library.\n\n## Similar Projects:\n\nThe [pigpio-encoder](https://pypi.org/project/pigpio-encoder/) is a similar library based on pigpio.\n',
    'author': 'Momo Eissenhauer',
    'author_email': 'momo.eissenhauer@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
