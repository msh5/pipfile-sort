from click import command
from click import option
import plette
import sys


PIPFILE_FILENAME = './Pipfile'
PIPFILE_ENCODING = 'utf-8'


@command()
@option('--exit-code', is_flag=True, help=
    'change to behavior of exit code. default behavior of return value, 0 is no differences, 1 is error exit. '
    'return 2 when add this option. 2 is exists differences.')
def main(exit_code):
    # Load current data.
    with open(PIPFILE_FILENAME, encoding=PIPFILE_ENCODING) as f:
        pipfile = plette.Pipfile.load(f)

    # Sort "dev-packages" mapping.
    sorted_dev_packages, all_changed = __sort_collection(pipfile.dev_packages)

    # Sort "packages" mapping.
    sorted_packages, changed = __sort_collection(pipfile.packages)
    if changed:
        all_changed = True

    # Replace with sorted lists
    pipfile.dev_packages = sorted_dev_packages
    pipfile.packages = sorted_packages

    # Store sorted data.
    with open(PIPFILE_FILENAME, 'w', encoding=PIPFILE_ENCODING) as f:
        plette.Pipfile.dump(pipfile, f)

    # When --exit-code option is valid and package collection has been changed, exit with 2.
    if exit_code and all_changed:
        sys.exit(2)


def __sort_collection(org_collection):
    org_packages = [p for p in org_collection]
    sorted_packages = sorted(org_packages)

    return (
        plette.pipfiles.PackageCollection({
            p: org_collection[p]._data for p in sorted_packages
        }),
        org_packages != sorted_packages,
    )

