import re
from nose.plugins.plugintest import munge_nose_output_for_doctest as _cleanup

ds_warn = re.compile(r'^WARNING:.+Could not .+ datastore.+$\n', re.MULTILINE)

client = None

def cleanup(out):
    out = _cleanup(out)
    out = remove_ds_warns(out)
    return out


def remove_ds_warns(out):
    out = ds_warn.sub('', out)
    return out
