from morph.core.ModuleCapability import ModuleCapability

class Module:
    def __init__(self, module_name: str, description: str, capabilities: list[ModuleCapability]):
        self.module_name = module_name
        self.description = description
        self.capabilities = capabilities
    
    # There needs to be a way to check if the module's capability can be satisfied by another module
    def can_satisfy(self, capability: str) -> bool:
        return False

