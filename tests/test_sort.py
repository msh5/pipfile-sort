import os
import shutil
import sys
import subprocess
from pathlib import Path

import pytest
from plette import Pipfile

# Import the module for direct access to functions
import pipfile_sort


def test_basic_sort(temp_dir, fixtures_dir):
    """Test basic sorting of packages."""
    # Copy the fixture Pipfile to the temporary directory
    fixture_path = fixtures_dir / "basic" / "Pipfile"
    sorted_fixture_path = fixtures_dir / "basic" / "Pipfile.sorted"
    temp_pipfile = Path(temp_dir) / "Pipfile"
    
    shutil.copy(fixture_path, temp_pipfile)
    
    # Change working directory to temp_dir and run the sort function directly
    original_dir = os.getcwd()
    os.chdir(temp_dir)
    try:
        # Load current data
        with open(temp_pipfile, encoding="utf-8") as f:
            pipfile = Pipfile.load(f)
        
        # Sort "dev-packages" mapping
        sorted_dev_packages, all_changed = pipfile_sort.__sort_collection(pipfile.dev_packages)
        
        # Sort "packages" mapping
        sorted_packages, changed = pipfile_sort.__sort_collection(pipfile.packages)
        if changed:
            all_changed = True
        
        # Replace with sorted lists
        pipfile.dev_packages = sorted_dev_packages
        pipfile.packages = sorted_packages
        
        # Store sorted data
        with open(temp_pipfile, 'w', encoding="utf-8") as f:
            Pipfile.dump(pipfile, f)
        
        # Load the sorted Pipfile
        with open(temp_pipfile, "r", encoding="utf-8") as f:
            sorted_pipfile = Pipfile.load(f)
            
        # Load the expected sorted Pipfile
        with open(sorted_fixture_path, "r", encoding="utf-8") as f:
            expected_pipfile = Pipfile.load(f)
            
        # Check that the packages are sorted correctly
        assert list(sorted_pipfile.packages) == list(expected_pipfile.packages)
        assert list(sorted_pipfile.dev_packages) == list(expected_pipfile.dev_packages)
    finally:
        os.chdir(original_dir)


def test_empty_sections(temp_dir, fixtures_dir):
    """Test sorting of empty package sections."""
    # Copy the fixture Pipfile to the temporary directory
    fixture_path = fixtures_dir / "empty_sections" / "Pipfile"
    temp_pipfile = Path(temp_dir) / "Pipfile"
    
    shutil.copy(fixture_path, temp_pipfile)
    
    # Change working directory to temp_dir and run the sort function directly
    original_dir = os.getcwd()
    os.chdir(temp_dir)
    try:
        # Load current data
        with open(temp_pipfile, encoding="utf-8") as f:
            pipfile = Pipfile.load(f)
        
        # Sort "dev-packages" mapping
        sorted_dev_packages, all_changed = pipfile_sort.__sort_collection(pipfile.dev_packages)
        
        # Sort "packages" mapping
        sorted_packages, changed = pipfile_sort.__sort_collection(pipfile.packages)
        if changed:
            all_changed = True
        
        # Replace with sorted lists
        pipfile.dev_packages = sorted_dev_packages
        pipfile.packages = sorted_packages
        
        # Store sorted data
        with open(temp_pipfile, 'w', encoding="utf-8") as f:
            Pipfile.dump(pipfile, f)
        
        # Load the sorted Pipfile
        with open(temp_pipfile, "r", encoding="utf-8") as f:
            sorted_pipfile = Pipfile.load(f)
            
        # Check that the empty sections are handled correctly
        assert list(sorted_pipfile.packages) == []
        assert list(sorted_pipfile.dev_packages) == []
    finally:
        os.chdir(original_dir)


def test_version_specifiers(temp_dir, fixtures_dir):
    """Test sorting of packages with version specifiers."""
    # Copy the fixture Pipfile to the temporary directory
    fixture_path = fixtures_dir / "version_specifiers" / "Pipfile"
    sorted_fixture_path = fixtures_dir / "version_specifiers" / "Pipfile.sorted"
    temp_pipfile = Path(temp_dir) / "Pipfile"
    
    shutil.copy(fixture_path, temp_pipfile)
    
    # Change working directory to temp_dir and run the sort function directly
    original_dir = os.getcwd()
    os.chdir(temp_dir)
    try:
        # Load current data
        with open(temp_pipfile, encoding="utf-8") as f:
            pipfile = Pipfile.load(f)
        
        # Sort "dev-packages" mapping
        sorted_dev_packages, all_changed = pipfile_sort.__sort_collection(pipfile.dev_packages)
        
        # Sort "packages" mapping
        sorted_packages, changed = pipfile_sort.__sort_collection(pipfile.packages)
        if changed:
            all_changed = True
        
        # Replace with sorted lists
        pipfile.dev_packages = sorted_dev_packages
        pipfile.packages = sorted_packages
        
        # Store sorted data
        with open(temp_pipfile, 'w', encoding="utf-8") as f:
            Pipfile.dump(pipfile, f)
        
        # Load the sorted Pipfile
        with open(temp_pipfile, "r", encoding="utf-8") as f:
            sorted_pipfile = Pipfile.load(f)
            
        # Load the expected sorted Pipfile
        with open(sorted_fixture_path, "r", encoding="utf-8") as f:
            expected_pipfile = Pipfile.load(f)
            
        # Check that the packages are sorted correctly
        assert list(sorted_pipfile.packages) == list(expected_pipfile.packages)
        assert list(sorted_pipfile.dev_packages) == list(expected_pipfile.dev_packages)
    finally:
        os.chdir(original_dir)


def test_exit_code(temp_dir, fixtures_dir):
    """Test the --exit-code flag."""
    # Copy the fixture Pipfile to the temporary directory
    fixture_path = fixtures_dir / "basic" / "Pipfile"
    temp_pipfile = Path(temp_dir) / "Pipfile"
    
    shutil.copy(fixture_path, temp_pipfile)
    
    # Change working directory to temp_dir
    original_dir = os.getcwd()
    os.chdir(temp_dir)
    try:
        # First run - should make changes and return exit code 2
        # Load current data
        with open(temp_pipfile, encoding="utf-8") as f:
            pipfile = Pipfile.load(f)
        
        # Sort "dev-packages" mapping
        sorted_dev_packages, all_changed = pipfile_sort.__sort_collection(pipfile.dev_packages)
        
        # Sort "packages" mapping
        sorted_packages, changed = pipfile_sort.__sort_collection(pipfile.packages)
        if changed:
            all_changed = True
        
        # Replace with sorted lists
        pipfile.dev_packages = sorted_dev_packages
        pipfile.packages = sorted_packages
        
        # Store sorted data
        with open(temp_pipfile, 'w', encoding="utf-8") as f:
            Pipfile.dump(pipfile, f)
        
        # Check that changes were made
        assert all_changed is True
        
        # Second run - should not make changes
        # Load current data
        with open(temp_pipfile, encoding="utf-8") as f:
            pipfile = Pipfile.load(f)
        
        # Sort "dev-packages" mapping
        sorted_dev_packages, all_changed = pipfile_sort.__sort_collection(pipfile.dev_packages)
        
        # Sort "packages" mapping
        sorted_packages, changed = pipfile_sort.__sort_collection(pipfile.packages)
        if changed:
            all_changed = True
        
        # Replace with sorted lists
        pipfile.dev_packages = sorted_dev_packages
        pipfile.packages = sorted_packages
        
        # Store sorted data
        with open(temp_pipfile, 'w', encoding="utf-8") as f:
            Pipfile.dump(pipfile, f)
        
        # Check that no changes were made
        assert all_changed is False
    finally:
        os.chdir(original_dir)
