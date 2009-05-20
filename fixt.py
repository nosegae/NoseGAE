import re
from nose.plugins.plugintest import munge_nose_output_for_doctest as _cleanup

remove_info = re.compile(
    r'^(root: )?INFO: Attempting to remove file at .+datastore.*$\n', re.MULTILINE)
ds_warn = re.compile(r'^(root: )?WARNING:.+Could not .+ datastore.+$\n', re.MULTILINE)
pil_warn = re.compile(r'(root: )?WARNING:.*PIL$\n', re.MULTILINE)
nose_capt_start = re.compile(
    r'^-------------------- >> begin captured logging << --------------------$\n', re.MULTILINE)
nose_capt_end = re.compile(
    r'^--------------------- >> end captured logging << ---------------------$\n', re.MULTILINE)

client = None

def cleanup(out):
    out = _cleanup(out)
    out = remove_warns(out)
    return out


def remove_warns(out):
    orig_out = out
    out = remove_info.sub('', out)
    out = ds_warn.sub('', out)
    out = pil_warn.sub('', out)
    if out != orig_out:
        # lazily replace nose's stdout capture,
        # in the case of log output.
        # fixme: probably a better way?
        out = nose_capt_start.sub('', out)
        out = nose_capt_end.sub('', out)
    return out
