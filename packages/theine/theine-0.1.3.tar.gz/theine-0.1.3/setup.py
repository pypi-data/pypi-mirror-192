# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['theine', 'theine.adapters']

package_data = \
{'': ['*']}

install_requires = \
['theine-core>=0.1.6,<0.2.0', 'typing-extensions>=4.4.0,<5.0.0']

setup_kwargs = {
    'name': 'theine',
    'version': '0.1.3',
    'description': 'high performance in-memory cache',
    'long_description': '# Theine\nHigh performance in-memory cache inspired by [Caffeine](https://github.com/ben-manes/caffeine).\n\n- High performance [Rust core](https://github.com/Yiling-J/theine-core)\n- High hit ratio with [W-TinyLFU eviction policy](https://arxiv.org/pdf/1512.00727.pdf)\n- Expired data are removed automatically using [hierarchical timer wheel](http://www.cs.columbia.edu/~nahum/w6998/papers/ton97-timing-wheels.pdf)\n- Simple API\n- Django cache backend\n\n## Table of Contents\n\n- [Requirements](#requirements)\n- [Installation](#installation)\n- [API](#api)\n- [Decorator](#decorator)\n- [Django Cache Backend](#django-cache-backend)\n- [Benchmarks(WIP)](#benchmarks)\n  * [continuous benchmark](#continuous-benchmark)\n  * [10k requests zipf](#10k-requests-zipf)\n\n## Requirements\nPython 3.7+\n\n## Installation\n```\npip install theine\n```\n\n## API\n\n```Python\nfrom theine import Cache\nfrom datetime import timedelta\n\ncache = Cache("tlfu", 10000)\n# without default, return None on miss\nv = cache.get("key")\n\n# with default, return default on miss\nsentinel = object()\nv = cache.get("key", sentinel)\n\n# set with ttl\ncache.set("key", {"foo": "bar"}, timedelta(seconds=100))\n\n# delete from cache\ncache.delete("key")\n```\n\n## Decorator\nTheine support string keys only, so to use a decorator, a function to convert input signatures to string is necessary. **The recommended way is specifying the function explicitly**, this is approach 1, Theine also support generating key automatically, this is approach 2. I will list pros and cons below.\n\n**- explicit key function**\n\n```python\nfrom theine import Cache, Memoize\nfrom datetime import timedelta\n\n@Memoize(Cache("tlfu", 10000), timedelta(seconds=100))\ndef foo(a:int) -> int:\n    return a\n\n@foo.key\ndef _(a:int) -> str:\n    return f"a:{a}"\n\nfoo(1)\n\n# asyncio\n@Memoize(Cache("tlfu", 10000), timedelta(seconds=100))\nasync def foo_a(a:int) -> int:\n    return a\n\n@foo_a.key\ndef _(a:int) -> str:\n    return f"a:{a}"\n\nawait foo_a(1)\n\n```\n\n**Pros**\n- A decorator with both sync and async support, you can replace your lru_cache with Theine now.\n- Thundering herd protection(multithreading: set `lock=True` in `Memoize`, asyncio: always enabled).\n- Type checked. Mypy can check key function to make sure it has same input signature as original function and return a string.\n\n**Cons**\n- You have to use 2 functions.\n- Performance. Theine API: around 8ms/10k requests ->> decorator: around 12ms/10k requests.\n\n**- auto key function**\n\n```python\nfrom theine import Cache, Memoize\nfrom datetime import timedelta\n\n@Memoize(Cache("tlfu", 10000), timedelta(seconds=100), typed=True)\ndef foo(a:int) -> int:\n    return a\n\nfoo(1)\n\n# asyncio\n@Memoize(Cache("tlfu", 10000), timedelta(seconds=100), typed=True)\nasync def foo_a(a:int) -> int:\n    return a\n\nawait foo_a(1)\n\n```\n**Pros**\n- Same as explicit key version.\n- No extra key function.\n\n**Cons**\n- Worse performance: around 18ms/10k requests.\n- Auto removal of stale keys is disabled due to current implementation.\n- Unexpected memory usage. The auto key function use same methods as Python\'s lru_cache. Take a look [this issue](https://github.com/python/cpython/issues/88476) or [this one](https://github.com/python/cpython/issues/64058).\n\n\n## Django Cache Backend\n\n```Python\nCACHES = {\n    "default": {\n        "BACKEND": "theine.adapters.django.Cache",\n        "TIMEOUT": 300,\n        "OPTIONS": {"MAX_ENTRIES": 10000},\n    },\n}\n```\n\n## Benchmarks\n### continuous benchmark\nhttps://github.com/Yiling-J/cacheme-benchmark\n\n### 10k requests zipf\nCachetools: https://github.com/tkem/cachetools\n\nSource Code: https://github.com/Yiling-J/theine/blob/main/benchmarks/benchmark_test.py\n\n|       | Theine API | Theine(W-TinyLFU) Custom-Key Decorator | Theine(W-TinyLFU) Auto-Key Decorator | Cachetools(LFU) Decorator |\n|-------|------------|----------------------------------------|--------------------------------------|---------------------------|\n| Read  | 6.03 ms    | 10.75 ms                               | 12.75 ms                             | 17.10 ms                  |\n| Write | 23.22 ms   | 26.22 ms                               | 67.53 ms                             | 440.50 ms                 |\n\n',
    'author': 'Yiling-J',
    'author_email': 'njjyl723@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
