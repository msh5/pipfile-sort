import sys
from collections import defaultdict

from click import command, option, version_option
from plette import Pipfile
from plette.pipfiles import PackageCollection

APP_VERSION = "0.4.1"
PIPFILE_FILENAME = "./Pipfile"
PIPFILE_ENCODING = "utf-8"


@command()
@version_option(version=APP_VERSION)
@option(
    "--exit-code",
    is_flag=True,
    help="""Change behaviour of exit code:
    - 0 is no differences
    - 1 is error exit
    - 2 is difference exists (added by this flag)
    """,
)
@option(
    "--case-sensitive",
    is_flag=True,
    help="If we want to sort with respect to case. If enabled, "
    "uppercase & lowercase will be grouped together respectively",
)
@option(
    "--no-group-types",
    is_flag=True,
    help="If we want to disable sorting according to datatype. If enabled, "
    "semgrep, git will be grouped together respectively.",
)
def main(exit_code, case_sensitive, no_group_types):
    # Load current data.
    with open(PIPFILE_FILENAME, encoding=PIPFILE_ENCODING) as f:
        pipfile = Pipfile.load(f)

    # Sort "dev-packages" mapping.
    sorted_dev_packages, all_changed = __sort_collection(
        pipfile.dev_packages,
        case_sensitive=case_sensitive,
        no_group_types=no_group_types,
    )

    # Sort "packages" mapping.
    sorted_packages, changed = __sort_collection(
        pipfile.packages,
        case_sensitive=case_sensitive,
        no_group_types=no_group_types,
    )
    if changed:
        all_changed = True

    # Replace with sorted lists
    pipfile.dev_packages = sorted_dev_packages
    pipfile.packages = sorted_packages

    # Store sorted data.
    with open(PIPFILE_FILENAME, "w", encoding=PIPFILE_ENCODING) as f:
        Pipfile.dump(pipfile, f)

    # When --exit-code option is valid and package collection has been changed,
    # exit with 2.
    if exit_code and all_changed:
        sys.exit(2)


def __sort_collection(
    org_collection: PackageCollection,
    case_sensitive=False,
    no_group_types=False,
):
    sorted_packages = []

    if not no_group_types:
        data_type_dict: defaultdict[list] = defaultdict(list)
        for p in org_collection:
            data_type_dict[type(org_collection[p]._data)].append(p)

        for v in data_type_dict.values():
            sorted_packages.extend(
                sorted(
                    v,
                    key=lambda i: i if case_sensitive else i.upper(),
                )
            )
    else:
        sorted_packages = sorted(
            [p for p in org_collection],
            key=lambda v: v if case_sensitive else v.upper(),
        )

    return (
        PackageCollection({p: org_collection[p]._data for p in sorted_packages}),
        [p for p in org_collection] != sorted_packages,
    )
