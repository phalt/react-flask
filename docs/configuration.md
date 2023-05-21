# 🔧 Configuration

Beckett is heavily convention-based, yet you can configure quite a bit of it based on what your project set up needs.

## Settings

All settings should be set as environment variables.

### `ENVIRONMENT`

**Default**: `development`

When this variable is set to `development` in order to enable the Beckett hot-reloader and auto generation features.

### `BECKETT_METAFILE_PATH`

**Defaut**: `{pwd}/metafile.json`

The file tracks the manifest of React pages registered in the app, and enables hot-reloading in development.
In production is provides a link between the Flask view function and the React page (because it will be generated with a hash that the Flask view function doesn't know about).

### `BECKETT_REACT_PAGE_TEMPLATE`

**Default**: `{pwd}/template/beckett_page.template`

This is the template used when generating new React pages.
