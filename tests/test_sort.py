import os
import shutil
from pathlib import Path
from contextlib import contextmanager

from plette import Pipfile

# Import the module for direct access to functions
import pipfile_sort


@contextmanager
def change_dir(path):
    """Context manager for changing the current working directory."""
    original_dir = os.getcwd()
    try:
        os.chdir(path)
        yield
    finally:
        os.chdir(original_dir)


def test_basic_sort(temp_dir, fixtures_dir):
    """Test basic sorting of packages."""
    run_sort_test(temp_dir, fixtures_dir, "basic")


def test_empty_sections(temp_dir, fixtures_dir):
    """Test sorting of empty package sections."""
    sorted_pipfile, _ = run_sort_test(
        temp_dir, fixtures_dir, "empty_sections", has_expected_file=False
    )
    
    # Check that the empty sections are handled correctly
    assert list(sorted_pipfile.packages) == []
    assert list(sorted_pipfile.dev_packages) == []


def test_version_specifiers(temp_dir, fixtures_dir):
    """Test sorting of packages with version specifiers."""
    run_sort_test(temp_dir, fixtures_dir, "version_specifiers")


def test_exit_code(temp_dir, fixtures_dir):
    """Test the --exit-code flag."""
    # Set up test files
    temp_pipfile = setup_test_pipfile(temp_dir, fixtures_dir, "basic")
    
    # Change directory and run the sort twice
    with change_dir(temp_dir):
        # First run - should make changes
        _, all_changed = pipfile_sort.sort_pipfile(temp_pipfile)
        
        # Check that changes were made
        assert all_changed is True
        
        # Second run - should not make changes
        _, all_changed = pipfile_sort.sort_pipfile(temp_pipfile)
        
        # Check that no changes were made
        assert all_changed is False


def setup_test_pipfile(temp_dir, fixtures_dir, fixture_subdir, fixture_name="Pipfile"):
    """Set up a test Pipfile in the temporary directory."""
    fixture_path = fixtures_dir / fixture_subdir / fixture_name
    temp_pipfile = Path(temp_dir) / "Pipfile"
    
    shutil.copy(fixture_path, temp_pipfile)
    return temp_pipfile


def sort_pipfile(pipfile_path):
    """Sort a Pipfile and return the sorted Pipfile and whether changes were made."""
    return pipfile_sort.sort_pipfile(pipfile_path)


def load_pipfile(pipfile_path):
    """Load a Pipfile from a path."""
    with open(pipfile_path, "r", encoding="utf-8") as f:
        return Pipfile.load(f)


def run_sort_test(temp_dir, fixtures_dir, fixture_subdir, has_expected_file=True):
    """Run a sort test with the given fixture subdirectory."""
    # Set up test files
    temp_pipfile = setup_test_pipfile(temp_dir, fixtures_dir, fixture_subdir)
    
    # Change directory and sort the Pipfile
    with change_dir(temp_dir):
        # Sort the Pipfile
        sorted_pipfile, all_changed = sort_pipfile(temp_pipfile)
        
        # If there's an expected file, compare with it
        if has_expected_file:
            sorted_fixture_path = fixtures_dir / fixture_subdir / "Pipfile.sorted"
            expected_pipfile = load_pipfile(sorted_fixture_path)
            
            # Check that the packages are sorted correctly
            assert list(sorted_pipfile.packages) == list(expected_pipfile.packages)
            assert list(sorted_pipfile.dev_packages) == list(
                expected_pipfile.dev_packages
            )
            
        return sorted_pipfile, all_changed
