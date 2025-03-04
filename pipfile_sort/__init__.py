import sys
from click import command
from click import option
from click import version_option
from plette import Pipfile
from plette.pipfiles import PackageCollection

APP_VERSION = "0.2.2"
PIPFILE_FILENAME = "./Pipfile"
PIPFILE_ENCODING = "utf-8"


@command()
@version_option(version=APP_VERSION)
@option(
    "--exit-code",
    is_flag=True,
    help="Modify exit code behavior. Without flag: returns 0 if no changes needed, "
    "1 if changes were made. With flag: returns 0 if no changes needed, "
    "2 if changes were made (useful for CI/CD).",
)
def main(exit_code):
    # Sort the Pipfile and get whether changes were made
    _, all_changed = sort_pipfile(PIPFILE_FILENAME, PIPFILE_ENCODING)

    # Exit code handling based on changes and flags
    if exit_code and all_changed:
        sys.exit(2)
    elif all_changed:
        sys.exit(1)
    else:
        sys.exit(0)


def sort_pipfile(pipfile_path, encoding=PIPFILE_ENCODING):
    """
    Sort a Pipfile and return the sorted Pipfile and whether changes were made.

    Args:
        pipfile_path: Path to the Pipfile to sort.
        encoding: Encoding of the Pipfile.

    Returns:
        A tuple containing:
        - The sorted Pipfile object.
        - A boolean indicating whether changes were made.
    """
    # Load current data
    with open(pipfile_path, encoding=encoding) as f:
        pipfile = Pipfile.load(f)

    # Sort "dev-packages" mapping
    sorted_dev_packages, all_changed = sort_collection(pipfile.dev_packages)

    # Sort "packages" mapping
    sorted_packages, changed = sort_collection(pipfile.packages)
    if changed:
        all_changed = True

    # Replace with sorted lists
    pipfile.dev_packages = sorted_dev_packages
    pipfile.packages = sorted_packages

    # Store sorted data
    with open(pipfile_path, "w", encoding=encoding) as f:
        Pipfile.dump(pipfile, f)

    return pipfile, all_changed


def sort_collection(org_collection):
    """
    Sort a package collection alphabetically.

    Args:
        org_collection: The original package collection to sort.

    Returns:
        A tuple containing:
        - The sorted package collection.
        - A boolean indicating whether changes were made.
    """
    org_packages = list(org_collection)
    sorted_packages = sorted(org_packages)

    # Create a new PackageCollection with sorted packages
    # Note: Using _data is necessary to access the internal data structure
    sorted_collection = PackageCollection(
        {
            # pylint: disable=protected-access
            p: org_collection[p]._data
            for p in sorted_packages
        }
    )

    return sorted_collection, org_packages != sorted_packages

