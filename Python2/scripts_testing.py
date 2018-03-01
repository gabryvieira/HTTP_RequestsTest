import socket
import errno
from socket import error as socket_error
import get_Default_Gateway as dfg
import check_devicePlatform as dpt

requests = []
fname = "../requests.txt"
with open(fname) as f:
	content = f.readlines()
requests = [x.strip() for x in content]

# Request 0
# requests.append("GET http://www.emaze.net/test.html HTTP/1.0\nHost:\n")

def main():
	ip = check_device_platform()
	print('')
	print("IP address to perform the requests:")
	print "1 - Use default gateway", ip
	print("2 - Another IP address")
	ipOption = input("Option --> ") #input for int on python2
	if isinstance(ipOption, int):
		if ipOption < 1 or ipOption > 2:
			print("Please, select option 1 or 2!")
			exit()

		elif ipOption == 1:
			print("Default Gateway: ", ip)

		else:
			destIP = raw_input("IP Address: ") # raw_input for string on python2
			ip = destIP
	else:
		print("ERROR: Only integer options are acceptable!")
		exit()

	print ip
	print("\n")
	printAvailableRequests()
	print("\n")
	print("1 - Perform all requests")
	print("2 - Perform some requests")

	selectedRequests = []
	selectedFinalReq = []
	option = input("Option --> ")
	if isinstance(option, int):
		if option < 1 or option > 2:
			print("Please, select option 1 or 2!")
			exit()
		elif option == 2: # selected request
			printAvailableRequests()
			print("Choose one or more requests to perform:")
			reqOpt = input("Requests --> ")
			if isinstance(reqOpt, int): # fazer para um pedido
				if reqOpt < 0 or reqOpt > (len(requests) - 1):
					print("Wrong request number!")
					exit()
				else: # fazer para apenas um pedido		
					selectedRequests.append(requests[reqOpt])
					ports = ChoosePorts()
					PerformAllRequests(ports, selectedRequests, ip)

			else: # sacar mais que um pedido 
				selectedRequests.append(reqOpt)
				selectedRequests = [x for xs in selectedRequests for x in xs] # converte string para array
				for a in xrange(len(requests)):
					for i in xrange(len(selectedRequests)):
						if a == selectedRequests[i]:
							selectedFinalReq.append(requests[a])
				ports = ChoosePorts()
				PerformAllRequests(ports, selectedFinalReq, ip)

		else: # fazer pra todos os pedidos
			ports = ChoosePorts()
			PerformAllRequests(ports, requests, ip)


				
def check_device_platform():
	plat_dev, plat_release = dpt.get_devicePlatform()
	print plat_dev
	print plat_release
	ip_def =""
	ipv4_addr =""
	if plat_dev.lower() == "windows":  #lower for case sensitive string
		print "Running script on Windows ",plat_release
		ip_def = dfg.get_DefaultGateway_Windows()
	elif plat_dev.lower() == "linux":
		print "Running script on Linux ", plat_release
		ip_def = dfg.default_gateway_linux()
	elif plat_dev.lower() == "darwin": #mac os x
		print "Running script on Mac OS X ", plat_release
		ip_def = dfg.default_gateway_macOSX()
	return ip_def



def printAvailableRequests():
	print("---------List of available request------------")
	for i in requests:
		print("{} - {}".format(requests.index(i), repr(i)))

#PORTS
def ChoosePorts():
	ports = []
	port = input("Port: ") 
	if isinstance(port, int): #one number is recognize as INT type
		ports.append(port)
		print(ports)
	else:
		ports.append(port)
		ports = [x for xs in ports for x in xs] # iterate over the string
		print(ports)
	return ports

#request = requests[requestID].encode('utf-8')
def PerformAllRequests(ports, requests, ip):
	for request in xrange(len(requests)):
		#print(requests[request])

		request = requests[request].encode('utf-8')
		for a in xrange(len(ports)):
			print("\n")
			print("Trying {}:{}".format(ip, int(ports[a])))
			print("{}".format(request))

			s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			try: #catching the exception
				s.connect((ip, int(ports[a])))
				s.send(request)
			except Exception: # deal the exception
				print("Errno 10061: CONNECTION REFUSED!")			
			s.close()

	print("Finished")


if __name__ == '__main__':
	main()
