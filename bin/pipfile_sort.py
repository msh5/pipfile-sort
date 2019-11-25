import plette

PIPFILE_FILENAME = './Pipfile'
PIPFILE_ENCODING = 'utf-8'

if __name__ == '__main__':
    # Load current data.
    with open(PIPFILE_FILENAME, encoding=PIPFILE_ENCODING) as f:
        pipfile = plette.Pipfile.load(f)

    # Sort "dev-packages" mapping.
    pipfile.dev_packages = plette.pipfiles.PackageCollection({
        s: pipfile.dev_packages[s]._data for s in sorted([
            p for p in pipfile.dev_packages
        ])
    })

    # Sort "packages" mapping.
    pipfile.packages = plette.pipfiles.PackageCollection({
        s: pipfile.packages[s]._data for s in sorted([
            p for p in pipfile.packages
        ])
    })

    # Store sorted data.
    with open(PIPFILE_FILENAME, 'w', encoding=PIPFILE_ENCODING) as f:
        plette.Pipfile.dump(pipfile, f)