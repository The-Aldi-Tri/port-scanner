import common_ports
import socket
import re

def get_open_ports(target, port_range, verbose = False):
  ip = ""
  open_ports = []
  
  try:
    # Get ip address by hostname
    ip = socket.gethostbyname(target)
    
    # Will scan ports between port_range
    for port in range(port_range[0], port_range[1]+1):
      # Create a new socket using the given address family and socket type
      s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

      # Set the default timeout in seconds (float)
      socket.setdefaulttimeout(1)

      # Returns an error indicator
      result = s.connect_ex((ip,port))

      # If no error found, save the open port
      if result == 0:
        open_ports.append(port)

      # Close a socket file descriptor.
      s.close()

  except KeyboardInterrupt:
    return "\n Exiting Program !!!!"
  except socket.gaierror:
    # Return error if target contain only aplphabet (invalid hostname)
    if re.search('[a-zA-Z]', target):
      return "Error: Invalid hostname"
    return "Error: Invalid IP address"
  except socket.error:
    return "Error: Invalid IP address"

  if verbose:
    hostname = ""
    try:
      # Get hostname by ip address
      hostname = socket.gethostbyaddr(ip)[0]
    except socket.herror:
      hostname = ""

    if(hostname == ""):
      header = "Open ports for {IP}\nPORT     SERVICE\n".format(IP=ip)
    else:
      header = "Open ports for {URL} ({IP})\nPORT     SERVICE\n".format(URL=hostname, IP=ip)
      
    body = ""
    for port in open_ports:
      service = common_ports.ports_and_services[port]
      body += str(port) + " "*(9-len(str(port))) + service
      if open_ports[len(open_ports)-1] != port:
        body += "\n"
      
    return(header+body)
  else:
    return(open_ports)

  