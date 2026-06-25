from django.urls import include, path

def path_from(url_include, name: str = None):
    """
    Build a root path from include("package.urls"), reading:
    - BASE_URL
    - urlpatterns
    """
    if not isinstance(url_include, tuple) or len(url_include) != 3:
        raise TypeError("path_from expects include('package.urls').")

    urlconf_module, app_name, namespace = url_include
    base_url = getattr(urlconf_module, "BASE_URL", None)
    url_patterns = getattr(urlconf_module, "urlpatterns", None)

    if not isinstance(base_url, str):
        module_name = getattr(urlconf_module, "__name__", str(urlconf_module))
        raise AttributeError(f"{module_name} must define BASE_URL as a string.")
    if url_patterns is None:
        module_name = getattr(urlconf_module, "__name__", str(urlconf_module))
        raise AttributeError(f"{module_name} must define urlpatterns.")

    route = base_url.lstrip("/")
    if app_name:
        included = include((url_patterns, app_name), namespace=namespace)
    else:
        included = include(url_patterns)

    return path(route, included, name=name)