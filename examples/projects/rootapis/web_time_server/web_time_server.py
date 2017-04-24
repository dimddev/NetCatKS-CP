
from NetCatKS.Components import ComponentsRegistration
from NetCatKS.NetCAT import IDefaultWebService, DefaultWebFactory

components = ComponentsRegistration().init()

application = IDefaultWebService(
    DefaultWebFactory(config=components.config.get_web())
).start()
