# Modules Hello World

REF: https://github.com/GoogleCloudPlatform/appengine-modules-helloworld-python

This is a sample application using the Google App Engine [Modules API][10].
It demonstrates how to create multiple modules serving different functions
as well as custom routing to different modules.

There are two main applications defined in [`helloworld.py`][4] and
[`printenv.py`][5]. The `helloworld` application is the one from the
[Getting Started][3] and is used for the default module. The other
two modules, one for a [`mobile-frontend`][7] and another for a
[`static-backend`][8], both use `printenv.py`. This module has a single
handler which prints all the WSGI and CGI environment variables
associated with the request as well as the output of all methods
offered by the Modules API.

In addition to these applications, there is custom routing defined
via [`dispatch.yaml`][6]. Requests to any module for the path
`/mobile` are served by the `mobile-frontend` module and similarly all
requests for the path `/work` are served by the `static-backend` module.

## Deploying

To deploy your each module for your application, run

```
$PATH_TO_SDK/appcfg.py update app.yaml mobile_frontend.yaml static_backend.yaml
```

using the [Google App Engine SDK][9] with version at least 1.8.2. To set-up the custom
routing, you'll also need to run

```
$PATH_TO_SDK/appcfg.py update_dispatch .
```

from directory containing the application.

## Products
- [App Engine][1]

## Language
- [Python][2]

[1]: https://developers.google.com/appengine
[2]: https://python.org
[3]: https://github.com/GoogleCloudPlatform/appengine-guestbook-python/tree/part1-helloworld
[4]: https://github.com/GoogleCloudPlatform/appengine-modules-helloworld-python/blob/master/helloworld.py
[5]: https://github.com/GoogleCloudPlatform/appengine-modules-helloworld-python/blob/master/printenv.py
[6]: https://github.com/GoogleCloudPlatform/appengine-modules-helloworld-python/blob/master/dispatch.yaml
[7]: https://github.com/GoogleCloudPlatform/appengine-modules-helloworld-python/blob/master/mobile_frontend.yaml
[8]: https://github.com/GoogleCloudPlatform/appengine-modules-helloworld-python/blob/master/static_backend.yaml
[9]: https://developers.google.com/appengine/downloads#Google_App_Engine_SDK_for_Python
[10]: https://developers.google.com/appengine/docs/python/modules
