import subprocess

from findersel import settings


def get_selected_files(*, sort=False):
    cmd = f'{settings.APPLESCRIPT_LAUNCHER} {settings.APPLESCRIPT_PATH}'
    try:
        output = (
            subprocess.check_output(cmd, shell=True, stderr=subprocess.STDOUT)
            .decode('utf-8')
            .splitlines()
        )
        if sort:
            output = sorted(output)
    except subprocess.CalledProcessError:
        output = []
    yield from output
