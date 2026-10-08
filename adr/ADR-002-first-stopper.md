**Problem:** package metadata was not correctly recognized.

**Root cause:** project used PEP 621 [project] metadata without an appropriate build-system declaration / sufficiently recent build backend.

**Solution:** explicitly define the build backend in pyproject.toml.