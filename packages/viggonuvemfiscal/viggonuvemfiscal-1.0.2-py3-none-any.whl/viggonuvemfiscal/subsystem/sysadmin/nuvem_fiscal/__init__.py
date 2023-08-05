from viggocore.common import subsystem
from viggonuvemfiscal.subsystem.sysadmin.nuvem_fiscal \
  import resource, controller, router

subsystem = subsystem.Subsystem(resource=resource.NuvemFiscal,
                                controller=controller.Controller,
                                router=router.Router)
