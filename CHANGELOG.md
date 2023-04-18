
# Changelog

## [0.0.1] - 2023-04-01

- Initial release

## [0.0.2] - 2023-04-01

- Replaced how the `FAUNA_SECRET` is loaded

## [0.0.3] - 2023-04-02

- Added `aiohtpp-sse`
- Added `aiohttp-jinja2`
- Added README.md

## [0.0.4] - 2023-04-03

- Removed `aiohttp-jinja2`
- Added app module with response decorators and custom `web.Application` class

## [0.0.6] - 2023-04-09

- Fixed some bugs on `AioClient` prompting for a new token

## [0.0.7] - 2023-04-09

- Fixed `render_template` bugs leading to not parsing the template into the response body

## [0.0.9] - 2023-04-10

- Added `oneOf` constraint for `AioModel` to avoid excesive use of enums, Union and if statements.

## [0.0.10] - 2023-04-10

- Added `asgi` module with the `aioasgi` middleware function in order to support ASGI based servers like `uvicorn` and `hypercorn`

## [0.0.12] - 2023-04-10

## [0.0.13] - 2023-04-17

- Added `Api` class with automatic documentation generation and inference of the request and response models from the function signature.
