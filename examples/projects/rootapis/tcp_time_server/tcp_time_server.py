
from NetCatKS.Components import ComponentsRegistration
from NetCatKS.NetCAT import DefaultFactory, IDefaultService

components = ComponentsRegistration().init()

application = IDefaultService(
    DefaultFactory(config=components.config.get_tcp())
).start()
