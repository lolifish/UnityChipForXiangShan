from toffee import Env
from ..agent import WayLookupAgent
from ..bundle import WayLookupBundle, bundle_dict

class WayLookupEnv(Env):
    def __init__(self, dut):
        super().__init__()
        self.dut = dut
        self.bundle = WayLookupBundle.from_dict(bundle_dict).bind(dut)
        self.agent = WayLookupAgent(self.bundle)
        self.bundle.set_all(0)