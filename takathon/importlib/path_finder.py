from importlib.abc import MetaPathFinder, InspectLoader
from importlib.util import spec_from_loader

from takathon.importlib.path_name_resolver import get_path
from takathon.importlib.splitter import get_code


class TestModuleLoader(InspectLoader):
    def __init__(self, module, path, *args, **kwargs):
        self.module = module
        self.filename = path
        super().__init__(*args, **kwargs)

    def get_source(self, fullname):
        return self.module

    def get_filename(self, fullname):
        return self.filename


class TestModuleFinder(MetaPathFinder):
    def __init__(self, modules=None, *args, **kwargs):
        self.modules = modules or {}
        super().__init__(*args, **kwargs)

    def find_spec(self, fullname, path, target=None):
        mod_path, is_package = get_path(fullname)

        module = (self.modules.get(mod_path) or
                  get_code(open(mod_path).read())
                  )

        return spec_from_loader(fullname,
                                TestModuleLoader(module, mod_path),
                                is_package=is_package)
