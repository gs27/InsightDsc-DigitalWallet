#!/usr/bin/env python

import sys
import csv
import time
from pprint import pprint

class Antifraud(object):

	# Build graph based on batch transactions file
	def build_graph(self, batch_file):

		graph = dict()
		with open(batch_file,'rU') as f_batch_handle:
			f_batch = csv.reader(f_batch_handle)
			for line in f_batch:

				try:
					usr1 = int(line[1])
					usr2 = int(line[2])
				except:
					continue	#Invalid record, skipping it

				if usr1 not in graph:
					graph[usr1] = list()
					graph[usr1].append(usr2)
				else:
					#graph[usr1] = list(set(graph[usr1])) 
					graph[usr1].append(usr2)
		
				if usr2 not in graph:
					graph[usr2] = list()
					graph[usr2].append(usr1)
				else:
					#graph[usr2] = list(set(graph[usr2])) 
					graph[usr2].append(usr1)        
        
		f_batch_handle.close()
		self.graph = graph


	# Flatten nested lists
	def flatten_lists(self,lst):
		flatten = [entry for sublist in lst for entry in sublist]
		flatten = list(set(flatten)) # remove duplicates
		return flatten


	# find degree between 2 users, return 0 if no degree
	def find_degree(self, graph, usr1, usr2):
		
		if (usr1 not in self.graph) or (usr2 not in self.graph):
			degree = 0
			return degree

		dist1 = self.graph[usr2]
		#print usr1, usr2, dist1
		if usr1 in dist1:
			degree = 1
			return degree

		dist2 = self.flatten_lists([self.graph[key2] for key2 in dist1])
		#print usr1, usr2, dist2
		if (usr1 in dist2):
			degree = 2
			return degree

		dist3 = self.flatten_lists([self.graph[key3] for key3 in dist2])
		#print usr1, usr2, dist3
 		if (usr1 in dist3):
			degree = 3
			return degree

		dist4 = self.flatten_lists([self.graph[key4] for key4 in dist3])
		#print usr1, usr2, dist4
 		if (usr1 in dist4):
			degree = 4
			return degree


	def print_graph(self, graph):
		pprint(graph)
		
		
	def print_output(self,graph,stream_file,outfile_1,outfile_2,outfile_3):
		output1 = open(outfile_1,'w')
		output2 = open(outfile_2,'w')
		output3 = open(outfile_3,'w')	

		i = 0
		start_time = time.time()
		with open(stream_file,'rU') as f_stream_handle:
			f_stream = csv.reader(f_stream_handle)
			for line in f_stream:
				try:
					usr1 = int(line[1])
					usr2 = int(line[2])
					i += 1
				except:
					continue
	
				degree = self.find_degree(self.graph, usr1, usr2)
				if degree == 0:
					output1.write("unverified \n")
					output2.write("unverified \n")
					output3.write("unverified \n")
				elif degree == 1:
					output1.write("trusted \n")
					output2.write("trusted \n")
					output3.write("trusted \n")
				elif degree == 2:
					output1.write("unverified \n")
					output2.write("trusted \n")
					output3.write("trusted \n")
				elif degree == 3:
					output1.write("unverified \n")
					output2.write("unverified \n")
					output3.write("trusted \n")						
				elif degree == 4:
					output1.write("unverified \n")
					output2.write("unverified \n")
					output3.write("trusted \n")
				else:
					output1.write("unverified \n")
					output2.write("unverified \n")
					output3.write("unverified \n")			
	
		f_stream_handle.close()
		output1.close()                   
		output2.close()
		output3.close()
		
		elapsed_time = end_time - start_time
		print("Average time taken to identify degree per transaction is {0:.2e} s".format(elapsed_time/i))

if __name__ == '__main__':
	try:
		batch_file = sys.argv[1]
		stream_file = sys.argv[2]
		outfile_1 = sys.argv[3]
		outfile_2 = sys.argv[4]
		outfile_3 = sys.argv[5]
	except:
		print("Usage: batch_file_nm_with_path, stream_file_nm_with_path, output1_file_nm_with_path, output2_file_nm_with_path, output3_file_nm_with_path")
		batchFile = raw_input("Batch payment file: \n")
		streamFile = raw_input("Stream payment file: \n")
		outfile_1 = raw_input("Out file1: \n")
		outfile_2 = raw_input("Out file2: \n")
		outfile_3 = raw_input("Out file3: \n")
	
	digital_wallet = Antifraud() # Init the object
	
	start_time = time.time()
	digital_wallet.build_graph(batch_file) #buld graph
	end_time = time.time()
	
	elapsed_time = end_time - start_time
	print("Time taken to build graph is {0:.2e} s".format(elapsed_time))
	#digital_wallet.print_graph(digital_wallet.graph) #print graph
	
	digital_wallet.print_output(digital_wallet.graph,stream_file,outfile_1,outfile_2,outfile_3)
	
