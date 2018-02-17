import socket
import errno
from socket import error as socket_error
import get_Default_Gateway as dfg
import check_devicePlatform as dpt

requests = []
requests = []
fname = "../requests.txt"
with open(fname) as f:
	content = f.readlines()
requests = [x.strip() for x in content]
# # Request 0
# requests.append("GET http://www.emaze.net/test.html HTTP/1.0\nHost:\n")
#
# # Request 1
# requests.append("GET http://www.emaze.net/test.html HTTP/1.0\n\n")
#
# # Request 2
# requests.append("GET http://www.emaze.net/ HTTP/1.0\nHost:\n")
#
# # Request 3
# requests.append("GET http://www.emaze.net/ HTTP/1.0\n\n")
#
# # Request 4
# requests.append("GET / HTTP/1.0\nHost:\n")
#
# # Request 5
# requests.append("GET / HTTP/1.0\n\n")

def main():
    ip = check_device_platform()
    print("Default Gateway: ", ip)
    #print("IPv4 Address: ", address)
    print("\n")
    printAvailableRequests()
    print("\n")
    print("1 - Perform all requests")
    print("2 - Perform some requests")

    selectedRequests = []
    selectedFinalReq = []
    option = input("Option --> ")

    try:
        option = int(option)
        if option < 1 or option > 2:
            print("Please, select option 1 or 2!")
            exit()
        elif option == 2:  # selected request
            printAvailableRequests()
            print("Choose one or more requests to perform:")
            reqOpt = input("Requests --> ")

            try: # for a single request
                reqOpt = int(reqOpt)
                if reqOpt < 0 or reqOpt > (len(requests) - 1):
                    print("Wrong request number!")
                    exit()
                else:  # fazer para apenas um pedido
                    selectedRequests.append(requests[reqOpt])
                    ports = ChoosePorts()
                    PerformAllRequests(ports, selectedRequests, ip)

            # more than one request
            except ValueError:
                reqOpt = str(reqOpt)
                #selectedRequests.append(reqOpt)
                selectedRequests = [int(x) for x in reqOpt.split(',')]  # list comprehension
                for a in range(len(requests)):
                    for i in range(len(selectedRequests)):
                        if a == selectedRequests[i]:
                            selectedFinalReq.append(requests[a])
                ports = ChoosePorts()
                PerformAllRequests(ports, selectedFinalReq, ip)

        else:  # to all requests
            ports = ChoosePorts()
            PerformAllRequests(ports, requests, ip)

    except ValueError:
        print("ERROR: Only integer options are acceptable!")
        exit()


def check_device_platform():
    plat_dev, plat_release = dpt.get_devicePlatform()
    ip_def = ""
    if plat_dev == "Windows":
        print("Running script on Windows ", plat_release)
        ip_def = dfg.get_DefaultGateway_Windows()
    elif plat_dev == "Linux":
        print("Running script on Linux ", plat_release)
        ip_def = dfg.default_gateway_linux()
    return ip_def


def printAvailableRequests():
    print("---------List of available request------------")
    for i in requests:
        print("{} - {}".format(requests.index(i), repr(i)))


# PORTS
def ChoosePorts():
    ports = []
    port = input("Port: ")
    try:
        port = int(port)    # one number is recognize as INT type
        ports.append(port)
    except ValueError:
        port = str(port)
        ports = [int(x) for x in port.split(',')] # list comprehension
        print(len(ports))
    return ports


# request = requests[requestID].encode('utf-8')
def PerformAllRequests(ports, requests, ip):
    for request in range(len(requests)):
        request = requests[request].encode('utf-8')
        for a in range(len(ports)):
            print("\n")
            print("Trying {}:{}".format(ip, int(ports[a])))
            print("{}".format(request))

            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            try:  # catching the exception
                s.connect((ip, int(ports[a])))
                s.send(request)
            except Exception:  # deal the exception
                print("Errno 10061: CONNECTION REFUSED!")
            s.close()

    print("Finished")


if __name__ == '__main__':
    main()
