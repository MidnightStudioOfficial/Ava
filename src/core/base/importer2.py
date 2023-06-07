import asyncio
import importlib

class Importer:
    def __init__(self, modules) -> None:
        self.modules = modules

    async def import_module2(self, package_name, pack):
        print(f"Importing {package_name}")
        return importlib.import_module(package_name, package=pack)

    async def import_all(self):
        tasks = []
        for n in self.modules:
            package_name = self.modules[n]["package_name"]
            pack = self.modules[n]["pack"]
            tasks.append(asyncio.ensure_future(self.import_module2(package_name, pack)))
        await asyncio.gather(*tasks)

# Example usage
modules = {
    "math": {"package_name": "math", "pack": None},
    "os": {"package_name": "os", "pack": None}
}
importer = Importer(modules)
asyncio.run(importer.import_all())
