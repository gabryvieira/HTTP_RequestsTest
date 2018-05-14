import numpy as np
from requests import get

#####   WINDOWS  ###########################################################
# def get_Stopped_services_Windows():
#     for s in c.Win32_Service():
#         try:
#             if s.State == 'Stopped':
#                 print(s.Caption, s.State)
#         except Exception: # deal the exception
#                 print("Errno 0 Error")

def get_DefaultGateway_Windows():
    import wmi
    c = wmi.WMI()
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
    from pyroute2 import IPRoute
    ip = IPRoute()
    defRoutes = ip.get_default_routes()
    try:
        defRoutes = np.asarray(defRoutes).item(0) # converter em array unico e depois em string
        defRoutes = defRoutes['attrs'] # obter os values da key "attrs" onde se encontra o default gateway
    except IndexError:
        print("ERROR: NO INTERNET CONNECTION!")
        exit()

    # transforma num dicionario para facil iteracao
    defRoutes = dict(defRoutes)
    default_gateway = defRoutes["RTA_GATEWAY"]
    #print(default_gateway)
    return default_gateway


def default_gateway_macOSX():
    import netifaces
    gateways = netifaces.gateways()
    default_gateway = gateways['default'][netifaces.AF_INET][0]
    return default_gateway


def getExternalIPAddress():
    ip_addr = get('https://ipapi.co/ip/')
    return ip_addr.text






