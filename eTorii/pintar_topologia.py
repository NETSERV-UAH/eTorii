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
#! /usr/bin/python
import os
import cairo
import math

def paint_net(nodearray, name):
	#variables para pintar
	radio = int(40);
	lado = int(30);
	diff_elem = int(300);
	margen = int(75);
	width = int(600); #VALOR MINIMO
	heigth = int(300); #VALOR MINIMO
	#numero de niveles
	levels = num_levels(nodearray);
	#calculamos la altura
	h = int(2 * int(margen) + int((2 * int(radio) + diff_elem) * int(levels - 1)) ) #tam necesario
	if h > int(heigth):
		heigth = int(h); #altura del documento
	print "heigth: ", str(heigth)
	#numero maximo de nodos
	max_nodes = num_max_nodes(nodearray);
	w = int(2 * int(margen) + (2 * int(radio) + diff_elem) * int(max_nodes - 1)) #tam necesario
	if w > int(width):
		width = int(w); #anchura necesaria minima
	print "width: ", str(width)
	#indicamos el lienzo
	surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, width,heigth)
	ctx = cairo.Context(surface)
	
	ctx.set_source_rgb(1,1,1)
	ctx.set_operator(cairo.OPERATOR_SOURCE)
	ctx.paint()
	
	paint_links(ctx, radio, nodearray, diff_elem, margen, max_nodes);
	paint_nodes(ctx, radio, nodearray, diff_elem, margen, max_nodes);
	#paint_host(ctx, 200,200, lado);
	
	
	surface.write_to_png( str(name.split('.')[0]) + '_Topology.png')

def printNetworkByNodes(M):
		lista = sorted(M.keys())
		for x in lista:
				print x, M[x].keys()
	
def paint_nodes(cr, radio, nodearray, diff_elem, margen, max_nodes):
	lista = sorted(nodearray.keys())
	x_ant = y_ant = y = x = 0
	#metemos texto
	cr.select_font_face("Serif", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD)
	cr.set_font_size(26)
	for node in lista:
		if not node.startswith('h'):
			nodos_level = num_nodos_level(nodearray, int(node.split('s')[0]))
			x, y = calculo_pos(node, diff_elem, margen, nodos_level, max_nodes, radio)
			x_node = int(x - len(node)*8)
			y_node = int(y + 8)
			cr.set_line_width(2)
			cr.set_source_rgb(0.0, 0.0, 0.0)
			cr.arc(x, y, radio, 0, 2*math.pi) #es un arco completo
			cr.set_source_rgb(0.3, 0.4, 0.2)
			cr.fill()
			cr.set_source_rgb(1, 1, 1)
			cr.move_to(x_node, y_node)
			cr.show_text(node)
    
			cr.stroke()
	return;
	
def calculo_pos(node, diff_elem, margen, nodos_level, max_nodes, radio):
	if nodos_level < max_nodes:
		mult = int(max_nodes) - int(nodos_level)
		centrar = int((mult * (diff_elem + 2 * radio))/2)
	else:
		centrar = 0
	y = int((int(node.split('s')[0]) * (diff_elem + (2 * radio))) + int(margen))
	x = int((int(node.split('s')[1]) * (diff_elem + (2 * radio))) + int(margen)) + int(centrar)
		
	return x, y
	
def paint_links(cr, radio, nodearray, diff_elem, margen, max_nodes):
	lista_src = sorted(nodearray.keys())
	color = [[0,0,0],[0.2,0.23,0.9],[0.9,0.1,0.1],[0.1,0.5,0.1],[0.75,0.65,0.1]]
	i = 0
	for src in lista_src:
		if not src.startswith('h'):			
			lista_dst = nodearray[src].keys()
			nodos_level = num_nodos_level(nodearray, int(src.split('s')[0]))
			x_src, y_src = calculo_pos(src, diff_elem, margen, nodos_level, max_nodes, radio)
			for dst in lista_dst:
				if not dst.startswith('h'):
					#if (int(src.split('s')[0]) > int(dst.split('s')[0])):
					nodos_level = num_nodos_level(nodearray, int(dst.split('s')[0]))
					x_dst, y_dst = calculo_pos(dst, diff_elem, margen, nodos_level, max_nodes, radio)
					cr.set_line_width(4)
					cr.set_source_rgb(float(color[i][0]), float(color[i][1]), float(color[i][2]))
					cr.move_to(x_src, y_src) #src line
					cr.line_to(x_dst, y_dst) #dst line
					cr.stroke()
			i = i + 1
			if i > 4:
				i = 0;
	return;
	
def paint_host(cr, x, y, lado):
	cr.set_line_width(4)
	cr.set_source_rgb(0.7, 0.2, 0.0)
	cr.rectangle((x-lado/2),(y-lado/2), lado, lado) # coordenadas punto superior izquierda x-lado/2, y-lado/2
	cr.stroke()
	return;
	
#devuelve el numero de niveles de la arquitectura
def num_levels(nodearray):
	max = 0;
	for node in nodearray:
		if not node.startswith('h'):
			nivel = int(node.split('s')[0]) #nos quedamos con el numero que sale de partir el nodo
			if nivel > max:
				max = nivel;
	max = max + 1
	print "numero de niveles: ", max
	return max;
	
#Numero maximo de nodos
def num_max_nodes(nodearray):
	max = 0
	for node in nodearray:
		if not node.startswith('h'):
			num = int(node.split('s')[1])
			if num > int(max):
				max = int(num)
	
	max = max + 1
	print "El numero de nodos es ", str(max)
	return max;

#Devuelve el numero de nodos en un nivel
def num_nodos_level(nodearray, level):
	max = 0
	for node in nodearray:
		if (node.startswith(str(level))):
			num = int(node.split('s')[1])
			if num > int(max):
				max = int(num);
	return max + 1; 

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
			#print 'nodo1', nodo1, 'nodo2', nodo2
		elif len(claves) > 8 and claves[8] == 'E_RT':
			foundEdge = True
			nodo1 = str(claves[1])
			nodo2 = str(claves[2])
			#vacia los dict aux1 y aux 2
		if foundEdge:
			for x in aux1.keys():
					del aux1[x]
			for x in aux2.keys():
					del aux2[x]

			#si ya existe la clave 'nodo' se copia su contenido a aux, y se borra
			if In.has_key(nodo1):
					for x in In[nodo1].keys():
							aux1[x] = In[nodo1][x]
			In[nodo1] = {}
			if In.has_key(nodo2):
					for x in In[nodo2].keys():
							aux2[x] = In[nodo2][x]
			In[nodo2] = {}
			#print In
			#print 'aux1', aux1
			#print 'aux2', aux2
			# se incluyen en aux los nuevos edges
			aux1[nodo2] = 1000
			aux2[nodo1] = 1000
			# se copian los aux a I,  
			for x in aux1.keys():
					In[nodo1][x] = aux1[x]
			for x in aux2.keys():
					In[nodo2][x] = aux2[x]
			#print In

	f.close()

	return In	
		
# BEGIN
filepath = raw_input('Nombre del subdirectorio de topologias: ')
print

path = os.getcwd() + '/' + filepath
filenames = os.listdir(path)

for name in filenames:
	#print filenames
	filename = path + '/' + name
	print
	print '==============================================================='
	print 'Archivo de topologia: ', name
	print
	# Desde el fichero de entrada lee la topologia de enlaces
	I = readNetFromFile(filename)
	paint_net(I, name)
	# A dictionary of elements: {node:{neighbornode:ETport}}
