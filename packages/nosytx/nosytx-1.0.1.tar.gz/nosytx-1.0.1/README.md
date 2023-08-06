## Usage

```python

from nosytx import NoSytx
import asyncio

nosytx = NoSytx('token') #get token from https://nosytx.eu

print(asyncio.run(nosytx.api('endpoint'))) #get endpoint from https://nosytx.eu/api, for example: hi or angry

```