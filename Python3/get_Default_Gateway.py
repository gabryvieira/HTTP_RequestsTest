import numpy as np
import wmi
from pyroute2 import IPRoute

#####   WINDOWS  ###########################################################


c = wmi.WMI()
def get_Stopped_services_Windows():
    for s in c.Win32_Service():
        try:
            if s.State == 'Stopped':
                print(s.Caption, s.State)
        except Exception: # deal the exception
                print("Errno 0 Error")


def get_DefaultGateway_Windows():
    def_gtw = ""
    ip_addr = ""
    wmi_sql = "select IPAddress,DefaultIPGateway from Win32_NetworkAdapterConfiguration where IPEnabled=True"
    wmi_out = c.query(wmi_sql)
    for dev in wmi_out:
        if dev.IPAddress != None or dev.DefaultIPGateway != None:
            ip_addr = dev.IPAddress[0]
            def_gtw = dev.DefaultIPGateway[0]
    return def_gtw

#################################################################################

################ LINUX ########################################

def default_gateway_linux():
    ip = IPRoute()
    defRoutes = ip.get_default_routes()
    try:
        defRoutes = np.asarray(defRoutes).item(0) # converter em array unico e depois em string
        print(defRoutes)
        defRoutes = defRoutes['attrs'] # obter os values da key "attrs" onde se encontra o default gateway
    except IndexError:
        print("ERROR: NO INTERNET CONNECTION!")
        exit() #finalizar script aqui!

    # transforma num dicionario para facil iteracao
    defRoutes = dict(defRoutes)
    default_gateway = defRoutes["RTA_GATEWAY"]
    print(default_gateway)
    return default_gateway









