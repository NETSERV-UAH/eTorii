#!/usr/bin/python
'''
Copyright 2015 gistnetserv-uah

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

   http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
'''
import os
from collections import namedtuple, OrderedDict

def readNetFromFile(fn):
	"""
	Creates the network dictionary of nodes and vertices from a given readNetFromFile
	"""
		
	In = {}
	aux1 = {}
	aux2 = {}

	f = open(fn, 'r')

	for line in f:
		foundEdge = False
		claves = line.split()
		if len(claves) > 3 and claves[1] == 'duplex-link':
			foundEdge = True
			nodo1 = str(claves[2].strip('$ns()'))
			nodo2 = str(claves[3].strip('$ns()'))
		elif len(claves) > 8 and claves[8] == 'E_RT':
			foundEdge = True
			nodo1 = str(claves[1])
			nodo2 = str(claves[2])
		if foundEdge:
			for x in aux1.keys():
					del aux1[x]
			for x in aux2.keys():
					del aux2[x]
			if In.has_key(nodo1):
					for x in In[nodo1].keys():
							aux1[x] = In[nodo1][x]
			In[nodo1] = {}
			if In.has_key(nodo2):
					for x in In[nodo2].keys():
							aux2[x] = In[nodo2][x]
			In[nodo2] = {}
			aux1[nodo2] = 1000
			aux2[nodo1] = 1000
			for x in aux1.keys():
					In[nodo1][x] = aux1[x]
			for x in aux2.keys():
					In[nodo2][x] = aux2[x]
	f.close()

	return In

def printNetworkByNodes(M):
		lista = sorted(M.keys())
		for x in lista:
				print x, M[x]

def assignEToriiIDs(net):
	# select core nodes
	coreNodeList = []
	for node in net:
		if node.startswith('0'):
			coreNodeList.append(node)
	coreNodeList.sort()
	pendingCoreNodeList = list(coreNodeList)

	for node in net.keys():
		if node not in coreNodeList:
			idx = 1
			ETnet[node] = {}
			for neighbor in net[node].keys():
				ETnet[node][neighbor] = str(idx)
				idx = idx + 1 
	i = 1 # ETorii addresses starts by '1'
	for node in coreNodeList:
		addr = str(i) + '.'
		ETnet[node] = {}
		EToriiAddress[node] = []
		EToriiAddress[node].append(addr)
		i += 1
	pendingSetAddressMessages = OrderedDict()
	addrRecord = namedtuple('msg', 'dest src addr')


	pkt = 0;
	num_pkt = 0; #numero de paquetes en la red
	for coreNode in coreNodeList:
		assignPortsToCoreNeighbors(coreNode, net)
		for neighbor in net[coreNode].keys():
			ETaddress = ETnet[coreNode][neighbor] + '.'
			setMsgInfo = addrRecord(neighbor, coreNode, ETaddress)
			pendingSetAddressMessages[neighbor + '+' + ETaddress] = setMsgInfo

		while len(pendingSetAddressMessages):
			node = processSetAddressMessage(pendingSetAddressMessages)
			if not node.startswith('h'):
				num_pkt = num_pkt + 1
			pkt = pkt + 1 
	printOrderedTop(EToriiAddress)
	print "Total Packet = ", num_pkt

def assignPortsToCoreNeighbors(core, net):

	maxPortInUse = 0
	for neighbor in ETnet[core]:
		port = int(ETnet[core][neighbor].split('.')[1])
		if port > maxPortInUse:
			maxPortInUse = port

	for neighbor in net[core]:
		if not ETnet[core].has_key(neighbor):
			ETnet[core][neighbor]= EToriiAddress[core][0] + str(maxPortInUse + 1)
			maxPortInUse += 1

def printOrderedTop(top):
	# top is a dict of node:addressList
	nodeList = top.keys()
	nodeList.sort()
	print nodeList  
	for node in nodeList:
		print node,'>>', top[node]

def processSetAddressMessage(msgList):

	# This is a simple dispatcher
	# gets msg from list and delegates processing

	key, val = msgList.popitem(False)     # gets oldest msg
	node = val.dest
	msgSourceNode = val.src
	addr = val.addr

	if node.startswith('0'):
		processAddressInCoreNode(msgList, node, msgSourceNode, addr)
	elif node.startswith('h'):
		processAddressInHost(node, msgSourceNode, addr)
	else:
		processAddressInMiddleNode(msgList, node, msgSourceNode, addr)
	return node;

def processAddressInCoreNode(msgList, core, src, addr):

	coreSrc = addr[0] # solo me coje el primer digito del prefijo
	newPort = int(addr.split('.')[1])

	if coreSrc < EToriiAddress[core][0][0]: # lower core
		if len(ETnet[core]) == 0:
			ETnet[core][src] = EToriiAddress[core][0] + str(newPort)

		elif not ETnet[core].has_key(src):
			foundPort = False
			for i in ETnet[core].keys():
				iPort = int(ETnet[core][i].split('.')[1])
				foundPort = iPort == newPort
				if foundPort: break
			
			if foundPort:  	# we need to create a new self of core
				i = 1
				newId = EToriiAddress[core][0].split('.')[0] + str(i) + '.'
				while newId in EToriiAddress[core]:
					i = i + 1
					newId = EToriiAddress[core][0].split('.')[0] + str(i) + '.'
				EToriiAddress[core].append(newId)
				ETnet[core][src] = newId + str(newPort)
			else:			# port not found no need to creare a new self
				ETnet[core][src] = EToriiAddress[core][0] + str(newPort)

		else:
			oldPort = int(ETnet[core][src].split('.')[1])
			if newPort < oldPort:
				
				foundPort = False
				for i in ETnet[core].keys():
					iPort = int(ETnet[core][i].split('.')[1])
					foundPort = iPort == newPort
					if foundPort: break
				
				if foundPort:  	# we need to create a new self of core
					i = 1
					newId = EToriiAddress[core][0].split('.')[0] + str(i) + '.'
					while newId in EToriiAddress[core]:
						i = i + 1
						newId = EToriiAddress[core][0].split('.')[0] + str(i) + '.'
					EToriiAddress[core].append(newId)
					ETnet[core][src] = newId + str(newPort)
				else:			# port not found no need to creare a new self
					ETnet[core][src] = EToriiAddress[core][0] + str(newPort)

	elif (coreSrc == EToriiAddress[core][0][0]): 	#same core
		aux1 = int(ETnet[core][src].split('.')[0])
		aux2 = int(coreSrc)
		if  aux1 == aux2:
			newSelf = coreSrc + ETnet[core][src].split('.')[1] + '.'
			if (newSelf not in EToriiAddress[core]) and (len(EToriiAddress[core]) < len(ETnet[core])):
				EToriiAddress[core].append(newSelf)

			oldPort = int(ETnet[core][src].split('.')[1])

			if newPort < oldPort:
				ETnet[core][src] = newSelf + str(newPort)
				ETaddress = newSelf + str(newPort) + '.' 
				setMsgInfo = addrRecord(src, core, ETaddress)
				msgList[src + '+' + ETaddress] = setMsgInfo
		else:
			oldPort = int(ETnet[core][src].split('.')[1])

			if newPort < oldPort:
				ETnet[core][src] = ETnet[core][src].split('.')[0] + '.' + str(newPort)
				ETaddress = ETnet[core][src] + '.' 
				setMsgInfo = addrRecord(src, core, ETaddress)
				msgList[src + '+' + ETaddress] = setMsgInfo

def processNewSuffix(node, addr, src):
	"""
	check if forzed port number is already in use to change it
	"""
	oldPort = int(ETnet[node][src])
	aux = addr.split('.')
	newPort = int(aux[len(aux)-3])
	if newPort != oldPort:
		maxPort = 0
		for item in ETnet[node].keys():
			if int(ETnet[node][item]) > maxPort:
				maxPort = int(ETnet[node][item])
		for item in ETnet[node].keys():
			if int(ETnet[node][item]) == newPort:
				ETnet[node][item] = str(maxPort + 1)
		ETnet[node][src] = str(newPort)

def processAddressInHost(node, src, addr):

	shorterAddress, lowerAddress, lowerSuffix, equalLengthAddress, equalSuffix, diff_core, pos_newaddr = compareOldAndNewAddresses(addr, node)
	
	if shorterAddress or (lowerAddress and equalLengthAddress):
		# 1. Discard previous address/es, accept new primary address
		if diff_core:
			EToriiAddress[node] = []
			EToriiAddress[node].append(addr)
		else:
			#buscamos la posicion a sustituir
			EToriiAddress[node].pop(pos_newaddr)
			EToriiAddress[node].insert(pos_newaddr,addr)

	elif equalLengthAddress and (equalSuffix and diff_core):
		# 1. accept new secondary address
		EToriiAddress[node].append(addr)
	
	elif equalLengthAddress and not equalSuffix and not diff_core:
		# 1. If equelLengthAddress and equalcore and !equelSuffix
		#buscamos la posicion a sustituir
			EToriiAddress[node].pop(pos_newaddr)
			EToriiAddress[node].insert(pos_newaddr,addr)


def processAddressInMiddleNode(msgList, node, src, addr):

	shorterAddress, lowerAddress, lowerSuffix, equalLengthAddress, equalSuffix, diff_core, pos_newaddr = compareOldAndNewAddresses(addr, node)

	if shorterAddress or (lowerAddress and equalLengthAddress):
		# acceptNewPrimaryAddr(addr, node, 'primary')
			# 1. 
			# 2. Discard previous address/es, accept new primary address
			# 3. Forward address to neighbors
		if pos_newaddr == 0:
			EToriiAddress[node] = []
			EToriiAddress[node].append(addr)
			if (len(addr.split('.'))-1) > (int(node[0]) + 1):
				processNewSuffix(node, addr, src) 
		else:
			EToriiAddress[node].pop(pos_newaddr)
			EToriiAddress[node].insert(pos_newaddr,addr)
			#deberiamos propagar el nuevo
		
		for item in ETnet[node].keys():
			if item != src:
				ETaddress = EToriiAddress[node][pos_newaddr] + ETnet[node][item] + '.'
				setMsgInfo = addrRecord(item, node, ETaddress)
				msgList[item + '+' + ETaddress] = setMsgInfo

	elif equalLengthAddress:
		if equalSuffix or diff_core:
		# acceptSecondaryAddr(addr, node, 'secondary')
			# 0. Check if the Suffix is the same, if not we put the same and send up
			# 1. accept new secondary address
			# 2. forward address to neighbors			

			EToriiAddress[node].append(addr)
			for item in ETnet[node].keys():
				if item != src:
					ETaddress = addr + ETnet[node][item] + '.' 
					setMsgInfo = addrRecord(item, node, ETaddress)
					msgList[item + '+' + ETaddress] = setMsgInfo

		else:
			#si no son iguales los sufijos descartamos paquete pero asignamos nuevo puerto al switch
			# 1 Buscamos puerto de entrada
			# 2 Asingamos el Swicth a ese puerto en nuestra entrada
			# 2.1 Buscamos si existe otro switch con ese puerto
			# 2.2 Asignamos el nuevo switch al puerto
			# 3 Descartamos el reenvio
			port_in = 0;
			if (int(EToriiAddress[node][0].split('.')[0]) >= int(addr.split('.')[0])) and (len(EToriiAddress[node][0].split('.')) == len(addr.split('.'))):
				if int(ETnet[node][src]) > int(addr.split('.')[int(len(addr.split('.'))/2)]) or (int(addr.split('.')[0]) == 1):
					port_in = addr.split('.')[int(len(addr.split('.'))/2)]
			if port_in != 0:
				for switch, port in ETnet[node].iteritems():
					if port == port_in and src != switch:
						port_up = puerto_max(ETnet[node])
						ETnet[node][switch] = str(port_up)
						if switch[0] == 'h':
							#si tenemos host debajo debemos notificarles el cambio de ide de puerto
							for host in EToriiAddress[node]:
								ETaddress = host + ETnet[node][switch] + '.'
								setMsgInfo = addrRecord(switch, node, ETaddress)
								msgList[switch + '+' + ETaddress] = setMsgInfo
					ETnet[node][src] = port_in #asignamos ese valor
			
	elif lowerSuffix: # or equalSuffix:
		# acceptNewSuffix(addr, node, 'suffix')
			# 1. process suffix to update port numbers if necessary
			# 2. forward address to 'upper' neighbors
		if (int(EToriiAddress[node][0].split('.')[0]) >= int(addr.split('.')[0])) and (len(addr.split('.')) - len(EToriiAddress[node][0].split('.')) <= 2 ):
			processNewSuffix(node, addr, src)
		for item in ETnet[node].keys():
			if item != src and item[0] < node[0]:
				ETaddress = addr + ETnet[node][item] + '.' 
				setMsgInfo = addrRecord(item, node, ETaddress)
				msgList[item + '+' + ETaddress] = setMsgInfo
		#si tenemos host debajo debemos notificarles el cambio de ide de puerto
		for item in ETnet[node].keys():
			if item != src and item[0] == 'h':
				for host in EToriiAddress[node]:
					ETaddress = host + ETnet[node][item] + '.'
					setMsgInfo = addrRecord(item, node, ETaddress)
					msgList[item + '+' + ETaddress] = setMsgInfo
		
def puerto_max(d):
    #""" a) create a list of the dict's keys and values; 
    #    b) return the key with the max value"""  
	max_port = 0
	for switch, port in d.iteritems():
		if max_port < port:
			max_port = int(port);
	return max_port + 1 
	
def compareOldAndNewAddresses(newAddr, node):
	
	addrIsShorter = True
	addrIsLower = True
	addrIsEqualLength = False
	suffixIsLower = True
	suffixIsEqual = False
	diffcore = True
	pos = 0

	if EToriiAddress.has_key(node):
		#Debemos comprar direcciones del mismo nodo si es que existen
		oldAddr = ""
		pos = 0
		for i in range(0,len(EToriiAddress[node])):
			if not comparePreffixes(newAddr, EToriiAddress[node][i]):
				oldAddr = EToriiAddress[node][i]
				pos = i
				break;
		if oldAddr == "": #si no tenemos coincidencia en el core entonces cogemos la mas prioritaria
			oldAddr = EToriiAddress[node][0]
			pos = 0
		addrIsShorter = newAddr.count('.') < oldAddr.count('.')
		addrIsEqualLength = newAddr.count('.') == oldAddr.count('.')
		addrIsLower = addrIsShorter or (addrIsEqualLength and compareAddresses(newAddr, oldAddr))

		diffcore = comparePreffixes(newAddr, oldAddr)
		#Comparar Prefijo
		compSuffixes = compareSuffixes(newAddr, oldAddr)
		if compSuffixes == 'isLower': 
			suffixIsLower = True
			suffixIsEqual = False
		elif compSuffixes == 'isEqual': 
			suffixIsLower = False
			suffixIsEqual = True
		else:
			suffixIsLower = False
			suffixIsEqual = False
		
	return addrIsShorter, addrIsLower, suffixIsLower, addrIsEqualLength, suffixIsEqual, diffcore, pos

def compareAddresses(new, old):
	isLower = False
	
	newList = new.split('.')
	oldList = old.split('.')
	
	newPref = newList.pop(0)
	newList.pop()
	
	oldPref = oldList.pop(0)
	oldList.pop()
	
	if newPref[0] <= oldPref[0]: 
		
		n = min(len(newList),len(oldList))
		i = 0
		while i<n:
			if int(newList[i]) < int(oldList[i]): 
				isLower = True
				break
			elif int(newList[i]) > int(oldList[i]):
				break
			else: i = i + 1

	return isLower

def compareSuffixes(new, old):
	isLower = False
	isEqual = False

	newList = new.split('.')
	oldList = old.split('.')
	newList.pop(0)
	newList.pop()
	oldList.pop(0)
	oldList.pop()
	
	n = min(len(newList),len(oldList))
	
	i = 0
	while i<n:
		if int(newList[i]) < int(oldList[i]): 
			isLower = True
			isEqual = False
			break
		elif int(newList[i]) > int(oldList[i]):
			isLower = False
			isEqual = False
			break
		else: 
			isEqual = True
			i = i + 1

	if isLower: result = 'isLower'
	elif isEqual: result ='isEqual'
	else: result = 'isGreater'

	return result

def comparePreffixes(new, old):
	isdiff = False
	
	newList = new.split('.')
	oldList = old.split('.')
	
	Core_new = newList.pop(0)
	Core_old = oldList.pop(0)

	if int(Core_new) != int(Core_old):
		isdiff = True

	return isdiff

# GLOBAL DEFINITIONS
# key=srcNode+addressAssign; value=namedtuple(destNode, srcNode, addressAssigned)
addrRecord = namedtuple('msg', 'dest src addr')

# BEGIN
filepath = raw_input('Subdirectory name topologies: ')
print

path = os.getcwd() + '/' + filepath
filenames = os.listdir(path)

#print filenames


for name in filenames:
	filename = path + '/' + name
	print
	print '==============================================================='
	print 'Topology File: ', name
	print
	# Desde el fichero de entrada lee la topologia de enlaces
	I = readNetFromFile(filename)
	# A dictionary of elements: {node:{neighbornode:ETport}}
	ETnet = {}
	# A dictionary of elements: {node:list of ETaddresses}
	EToriiAddress = {}

	assignEToriiIDs(I)
