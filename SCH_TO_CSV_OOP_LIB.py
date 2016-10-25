import re
import os

def listInList(smal, big) :
	T = True
	for a in smal :
		if a not in big :
			#print(smal)
			#print(big)
			return False
	return True

class Component(object):
	def __init__(self):
		self.SchematicName = ""
		self.PartType = ""
		self.Reference = ""
		self.Value = ""
		self.Footprint = ""
		self.Datasheet = ""
		self.unit = ""
		self.timestamp =""
		self.fields = []
	def print(self):
		print("Schematic : {}".format(self.SchematicName))
		print("PartType  : {}".format(self.PartType))
		print("Reference : {}".format(self.Reference))
		print("Value     : {}".format(self.Value))
		print("Footprint : {}".format(self.Footprint))
		print("Datasheet : {}".format(self.Datasheet))
		print("unit      : {}".format(self.unit))
		print("timestamp : {}".format(self.timestamp))
		for field in self.fields :
			print("{: <9} : {}".format(field['key'],field['value']))
	def getSchematicName(self) :
		return self.SchematicName
	def setSchematicName(self, v) :
		self.SchematicName = v
	def getPartType(self) :
		return self.PartType
	def setPartType(self, v) :
		self.PartType = v
	def getReference(self) :
		return self.Reference
	def setReference(self, v) :
		self.Reference = v
	def getValue(self) :
		return self.Value
	def setValue(self, v) :
		self.Value = v
	def getFootprint(self) :
		return self.Footprint
	def setFootprint(self, v) :
		self.Footprint = v
	def getDatasheet(self) :
		return self.Datasheet
	def setDatasheet(self, v) :
		self.Datasheet = v
	def getUnit(self) :
		return self.unit
	def setUnit(self, v) :
		self.unit = v
	def getTimestamp(self) :
		return self.timestamp
	def setTimestamp(self, v) :
		self.timestamp = v
	def getField(self, k):
		for field in self.fields :
			if field['key'] == k :
				return field['value']
		return ""
	def setField(self, k, v):
		self.fields.append({'key': k, 'value': v})
	def getFieldNames(self):
		keys = []
		for field in self.fields :
			keys.append(field['key'])
		return keys
	def isset(self):
		if self.SchematicName != "" and self.PartType != "" and self.Reference != "" and self.unit != "" and self.timestamp != "" :
			return True
		return False

def getCleanLine(line_to_be_cleaned):
	#function to create a clean string to generate new entries
	positions = []
	for r in range(len(line_to_be_cleaned)):
				
		if line_to_be_cleaned[r] == "\"":
			positions.append(r)
	if(len(positions) > 2):
		#this line has been contaminated
		line_to_be_returned = line_to_be_cleaned[:positions[0]+1] + line_to_be_cleaned[positions[1]:positions[2]+1] + line_to_be_cleaned[positions[3]:]
	else :
		#this line was clean
		line_to_be_returned = line_to_be_cleaned
	if "0000" in line_to_be_returned:
		i = 0
		for i in range (len(line_to_be_returned)-4):

			if line_to_be_returned[i:i+4] == "0000":
				break
		
		line_to_be_returned = line_to_be_returned[:i] + "0001" + line_to_be_returned[i+4 - len(line_to_be_returned):]
	return line_to_be_returned

class SCH_FILE(object):
	def __init__(self):
		self.contents = ""
		self.numb_of_comps = 0
		self.subcircuits_names = []
		self.number_of_subcircuits = 0
		self.components = []
		self.subcircuits = []
		self.SchematicName = ""
		self.path = ""
	def setPath(self, path):
		self.path = path
	def getPath(self):
		return self.path
	def setSchematicName(self, x):
		self.SchematicName = x
	def getSchematicName(self):
		return self.SchematicName
	def SetContents(self,content):
		#load the contents of the .sch file
		self.contents = content
	def SwapComponents(self, i, j):
		self.components[i] , self.components[j] = self.components[j] , self.components[i]
	def number_of_components(self , x):
		self.numb_of_comps = x
	def get_number_of_components(self):
		return self.numb_of_comps
	def getComponents(self):
		return self.components
	def getLastComponent(self):
		last_position = len(self.getComponents())-1
		return self.components[last_position]
	def append_subcircuit(self, subcircuit_instance):
		self.subcircuits.append(subcircuit_instance)
	def appendComponent(self,component):
		self.components.append(component)
		self.numb_of_comps = self.numb_of_comps + 1
	def printprops(self):
		#print(self.contents)
		print(self.numb_of_comps)
		#print(self.components)
		#print(self.components[0].GetAnnotation())
		print(self.subcircuits_names)
		print(self.number_of_subcircuits)
		print(self.SchematicName)
	def getOdederdFieldsList(self) :
		alist = []
		before = {}
		for comp in self.components :
			kel = comp.getFieldNames()
			for a in kel :
				if not a in alist :
					alist.append(a)
					before[a]=[]
					f = False
					for b in kel :
						if b == a :
							f = True
						elif not f :
							before[a].append(b)
				else :
					f = False
					for b in kel :
						if b == a :
							f = True
						elif not f :
							if b not in before[a] :
								before[a].append(b)
		
		orderd_list = []
		last_list =""
		while not listInList(alist, orderd_list) :
			for a in alist :
				# print("test a {}".format(a))
				if not (a in orderd_list) :
					# print("a not in {}".format(orderd_list))
					if listInList(before[a], orderd_list) :
						orderd_list.append(a)
			# print("loop--------------------------------------------------------------------------------------------")
			# print(orderd_list)
			# print(last_list)
			
			# if notting changed force changed:
			# this is a fallback against blocking
			if orderd_list[len(orderd_list)-1] == last_list :
				# print("meme????????????????????")
				a_size = 1000
				for a in alist :
					if a not in orderd_list :
						if len(before[a]) < a_size :
							a_size = len(before[a])
				for a in alist :
					if a not in orderd_list :
						if len(before[a]) == a_size :
							orderd_list.append(a)
							break;
			last_list = orderd_list[len(orderd_list)-1]
		# print(orderd_list)
		return orderd_list
		
	def ParseSubCircuits(self):
		content = self.contents
		ListOfSubSchematics = []
		SchemaFileName = re.compile("^F1\s\"(?P<filename>[^\"]+)\"")
		Sheet = re.compile("^\$Sheet")
		EndSheet = re.compile("^\$EndSheet")
		for count in range(len(content)):
			if Sheet.match(content[count]) :
				while not EndSheet.match(content[count]) :
					FileName = SchemaFileName.search(content[count])
					if FileName :
						ListOfSubSchematics.append(FileName.group("filename"))
						print(FileName.group("filename")) # DEBUG
						break # quit loop
					count += 1
						#test_var = 0
						#for p in range(len(content[count+subcounter])):
						#	if content[count+subcounter][p] == "\"":
						#		if test_var == 0:
						#			startOfString = p+1
						#			test_var = 1
						#			#print(p)
						#		else:
						#			endOfString = p
						#			break
						#if startOfString != 0:			
						#	ListOfSubSchematics.append(content[count+subcounter][startOfString:endOfString])
		self.subcircuits_names = ListOfSubSchematics
		self.number_of_subcircuits = len(ListOfSubSchematics)
	def ParseComponents(self):
		if self.subcircuits_names == []:
			self.ParseSubCircuits()
		content = self.contents
		
		compStart = re.compile("^\$Comp")
		compEnd = re.compile("^\$EndComp")
		compL = re.compile("^L\s+(?P<name>[^\s]+)\s+(?P<reference>[^\s]+)")
		virtual = re.compile("^L\s+[^\s]+\s+#[^\s]+")
		compU = re.compile("^U\s+(?P<unit>[^\s]+)\s+[^\s]+\s+(?P<time_stamp>[^\s]+)")
		Field = re.compile(r"""^F\s
							(?P<field_number>[0-9]+)\s+		# field number
							\"(?P<field_value>[^\"]+)\"\s+	# field text
							[HV]\s+							# orientation = H (horizontal) or V (vertical).
							-?[0-9]+\s+-?[0-9]+\s+				# position X and Y
							[0-9]+\s+						# dimension (default = 50)
							[01]+\s+						# Flags: visibility = 0 (visible) or 1 (invisible)
							[LRCBT]\s*[LRCBT]\s*			# hjustify vjustify = L R C B or T
							[IN]+\s*						# Style: Italic = I or N ( since January 2009)
							[BN]+\s*						# Style Bold = B or N ( since January 2009)
							(\"(?P<field_name>[^\"]+)\")?	# Name of the field (delimited by double quotes) (only if it is not the default name)
						""", re.VERBOSE)
		
		for count in range(len(content)):
			if compStart.match(content[count]):
				count += 1
				if not virtual.match(content[count]) :
					Comp = Component()
					Comp.setSchematicName(self.getSchematicName())
					
					while not compEnd.match(content[count]) :
						L = compL.search(content[count])
						U = compU.search(content[count])
						F = Field.search(content[count])
						if L :
							Comp.setPartType(L.group("name"))
							Comp.setReference(L.group("reference"))
						if U :
							Comp.setTimestamp(U.group("time_stamp"))
							Comp.setUnit(U.group("unit"))
							
						if F :
							if F.group("field_number") == "0" :
								# • reference = 0.
								pass
							elif F.group("field_number") == "1" :
								# • value = 1.
								Comp.setValue(F.group("field_value"))
							elif F.group("field_number") == "2" :
								# • Pcb FootPrint = 2.
								Comp.setFootprint(F.group("field_value"))
							elif F.group("field_number") == "3" :
								# • User doc link = 3.
								Comp.setDatasheet(F.group("field_value"))
							else :
								Comp.setField(F.group("field_name"),F.group("field_value"))
						count = count + 1
						if count >= len(content) :
							break
					# END while
					# Comp.print()
					self.components.append(Comp)
					self.number_of_components(self.get_number_of_components() + 1)
				# END not Virtual
		
		
		for subcircuitcounter in range(len(self.subcircuits_names)):
			for p in range (len(self.path),1,-1):
				if self.path[p-1] == "/":
					break
			to_open = self.path[:p] + self.subcircuits_names[subcircuitcounter]
			print("Trying to open: {}".format(to_open))
			try:
				f = open(to_open)
			except IOError:
				print("Fail opening!")
				return "error"
			else:
				self.append_subcircuit(SCH_FILE())
				self.get_subcircuit(subcircuitcounter).setPath(to_open)
				self.get_subcircuit(subcircuitcounter).SetContents(f.readlines())
				f.close()
				self.get_subcircuit(subcircuitcounter).setSchematicName(self.subcircuits_names[subcircuitcounter])
				self.get_subcircuit(subcircuitcounter).ParseComponents()			
				self.AppendComponents(self.get_subcircuit(subcircuitcounter).getComponents())

	def get_subcircuit(self, x):
		return self.subcircuits[x]
	
	def AppendComponents(self, componentList):
		for item in range(len(componentList)):
			self.components.append(componentList[item])
			self.numb_of_comps = self.get_number_of_components() + 1
	def SaveBOMInCSV(self,savepath):
		if not '.csv' in savepath:
			savepath = savepath + '.csv'
		try:
			f = open(savepath, 'w')
		except IOError:
			if savepath:	
				return "error"
		else:
			f.write("\"SchematicName\"")
			f.write(",")
			f.write("\"PartType\"")
			f.write(",")
			f.write("\"timestamp\"")
			f.write(",")
			f.write("\"Reference\"")
			f.write(",")
			f.write("\"unit\"")
			f.write(",")
			f.write("\"Value\"")
			f.write(",")
			f.write("\"Footprint\"")
			f.write(",")
			f.write("\"Datasheet\"")
			
			fields = self.getOdederdFieldsList()
			for field in fields :
				f.write(",\""+field+"\"")
			f.write("\n")
			
			for item in self.components :
				f.write("\""+item.getSchematicName()+"\",")
				f.write("\""+item.getPartType()+"\",")
				f.write("\""+item.getTimestamp()+"\",")
				f.write("\""+item.getReference()+"\",")
				f.write("\""+item.getUnit()+"\",")
				f.write("\""+item.getValue()+"\",")
				f.write("\""+item.getFootprint()+"\",")
				f.write("\""+item.getDatasheet()+"\"")
				for field in fields :
					f.write(",\""+item.getField(field)+"\"")
				f.write("\n")
			f.close
	
	def getSubCircuitName(self):
		return self.subcircuits_names
	def getSubCircuits(self):
		return self.subcircuits
	
	def ModifyNewSCHFile(self, oldSCHFile, CSV_FILE, savepath, matchByTimestamp = True, matchByReference = False, matchBySchematicName = False):
		if not matchByReference and not matchByTimestamp :
			return "error" 
		compStart = re.compile("^\$Comp")
		compEnd = re.compile("^\$EndComp")
		compL = re.compile("^L\s+(?P<name>[^\s]+)\s+(?P<virtual>#?)(?P<reference>[^\s]+)")
		# virtual = re.compile("^L\s+[^\s]+\s+#[^\s]+")
		compU = re.compile("^U\s+(?P<unit>[^\s]+)\s+(?P<mm>[^\s]+)\s+(?P<time_stamp>[^\s]+)")
		compP = re.compile("^P\s+(?P<x>-?[0-9]+)\s+(?P<y>-?[0-9]+)")
		Field = re.compile(r"""^F\s
							(?P<field_number>[0-9]+)\s+		# field number
							\"(?P<field_value>[^\"]*)\"\s+	# field text
							(?P<field_layout>				# group all the layout
							[HV]\s+							# orientation = H (horizontal) or V (vertical).
							-?[0-9]+\s+-?[0-9]+\s+			# position X and Y
							[0-9]+\s+						# dimension (default = 50? in my case 60?)
							[01]+\s+						# Flags: visibility = 0 (visible) or 1 (invisible)
							[LRCBT]\s*[LRCBT]\s*			# hjustify vjustify = L R C B or T
							[IN]+\s*						# Style: Italic = I or N ( since January 2009)
							[BN]+)							# Style Bold = B or N ( since January 2009)
							\s*							# End group all the layout
							(\"(?P<field_name>[^\"]+)\")?	# Name of the field (delimited by double quotes) (only if it is not the default name)
						""", re.VERBOSE)
		compO = re.compile("^\s+-?[01]\s+-?[01]\s+-?[01]\s+-?[01]\s*")
		Standard_Layout = "H {x} {y} 50  0001 C CNN"
		content = self.contents
		count = 0
		len_cont = len(content)
		while count < len_cont :
			if compStart.match(content[count]):
				# print(count)
				compStarCount = count
				mL = compL.match(content[compStarCount+1])
				mU = compU.match(content[compStarCount+2])
				mP = compP.match(content[compStarCount+3])
				
				if not mL or not mU or not mP :
					print("Error: Bad component!!!")
				else :
					# print(mL.group("reference"))
					if not mL.group("virtual") == "#" :
						name      = mL.group("name")
						reference = mL.group("reference")
						unit      = mU.group("unit")
						mm        = mU.group("mm")
						timestamp = mU.group("time_stamp")
						pos_x     = mP.group("x")
						pos_y     = mP.group("y")
						
						match = False
						
						for c in CSV_FILE.getComponents() :
							if ( 	(not matchBySchematicName or c.getSchematicName() == self.SchematicName) and
									(not matchByReference     or c.getReference()     == reference) and
									(not matchByTimestamp     or c.getTimestamp()     == timestamp) ) :
								match = c
								break
						
						if match :
							print("{} found in {} on {}".format(match.getReference(),self.SchematicName,compStarCount))
							# UPDATE start of component
							content[compStarCount+1] = "L {} {}\n".format(match.getPartType() , match.getReference())
							content[compStarCount+2] = "U {} {} {}\n".format(unit, mm, match.getTimestamp())
							# dont change pos
							
							FieldList = []
							#field list
							
							count = compStarCount+3
							FieldListLineStart = count+5
							while not compEnd.match(content[count]) :
								
								#O = compO.match(content[count])
								F = Field.match(content[count])
								if F :
									if F.group("field_number") == "0" :
										# • reference = 0.
										content[count] = "F 0 \"{}\" {}\n".format(match.getReference() , F.group("field_layout"))
									elif F.group("field_number") == "1" :
										# • value = 1.
										content[count] = "F 1 \"{}\" {}\n".format(match.getValue() , F.group("field_layout"))
									elif F.group("field_number") == "2" :
										# • Pcb FootPrint = 2.
										layout = Standard_Layout.format(x=pos_x,y=pos_y)
										# F.group("field_layout") hide the footprint
										content[count] = "F 2 \"{}\" {}\n".format(match.getFootprint() , layout)
									elif F.group("field_number") == "3" :
										# • User doc link = 3.
										content[count] = "F 3 \"{}\" {}\n".format(match.getDatasheet() , F.group("field_layout"))
										FieldListLineStart = count+1
									else :
										# keep layout if field exists
										FieldList.append({"field_layout":F.group("field_layout"),"field_name":F.group("field_name")})
								count+=1
							# remove al existing fields
							for a in range( len(FieldList)) :
								content.pop(FieldListLineStart)
								len_cont -= 1
								count -= 1
							newFields = match.getFieldNames()
							fn = 4
							for key in newFields :
								layout = Standard_Layout.format(x=pos_x,y=pos_y)
								for existingField in FieldList :
									if existingField["field_name"] == key :
										layout = existingField["field_layout"]
								# print(key)
								# print(match.getField(key))
								content.insert(FieldListLineStart,"F {} \"{}\" {} \"{}\"\n".format(fn, match.getField(key), layout, key))
								len_cont += 1
								count+=1
								fn+=1
								FieldListLineStart += 1
						else :
							print("{} {} not found in cvs".format(reference, timestamp))
				#if not virtual.match(content[count]) :
					# Comp = Component()
					# Comp.setSchematicName(self.getSchematicName())
					# $Comp
					# L name reference
					# U N mm time_stamp
					# P posx posy
					# List of fields
					# 	1 posx posy (redundant: not used)
					# 	A B C B ( orientation matrix with A, B, C, D = - 1, 0 or 1)
			count+=1
		# print("EOF count = {}".format(count))
		if os.path.isfile(savepath) :
			os.rename(savepath, savepath+".bak")
		
		try:
			f = open(savepath, 'w+')
		except IOError:
			return "error"
		else:			
			for i in range (len(content)):
				f.write(content[i])
			f.close
		
		for i in range(len(self.subcircuits)):
			for p in range (len(savepath),1,-1):
				if savepath[p-1] == "/":
					break
			new_savepath = savepath[:p] + self.subcircuits_names[i]
			
			# print("new_savepath")
			self.subcircuits[i].ModifyNewSCHFile(0, CSV_FILE, new_savepath)
			#mainFile.ModifyNewSCHFile(0, openCSVFile,savePath):
	def ModifyNewSCHFileOld(self, oldSCHFile, CSV_FILE, savepath):
		#this will break if the order is not FarnellLink; MouserLink; DigiKeyLink
		print(str(CSV_FILE.getNumberOfComponents()))
		print(str(self.get_number_of_components()))
		#print("BPJTESTSR1")
		#print(self.SchematicName)
		#print("BPJTESTSR2")
		if CSV_FILE.getNumberOfComponents() and self.get_number_of_components():
			for i in range (CSV_FILE.getNumberOfComponents()):
				for p in range (self.get_number_of_components()):
					if CSV_FILE.getComponents()[i].getAnnotation() == self.getComponents()[p].GetAnnotation() and self.SchematicName ==  CSV_FILE.getComponents()[i].getSchematic(): 
						toAddFarnellLink = " "
						toAddMouserLink = " "
						toAddDigikeyLink = " "
						if len(CSV_FILE.getComponents()[i].getFarnellLink()) > 1:

							toAddFarnellLink = CSV_FILE.getComponents()[i].getFarnellLink()

						if len(CSV_FILE.getComponents()[i].getMouserLink())>1:
							toAddMouserLink = CSV_FILE.getComponents()[i].getMouserLink()

						if len(CSV_FILE.getComponents()[i].getDigiKeyLink())>1:
							toAddDigikeyLink = CSV_FILE.getComponents()[i].getDigiKeyLink()

						self.getComponents()[p].addNewInfo(toAddFarnellLink,toAddMouserLink,toAddDigikeyLink)

						q = 0

						while self.contents[q+self.getComponents()[p].getStartLine()][0] != "F":

							q = q + 1
						while self.contents[q+self.getComponents()[p].getStartLine()][0] == "F":

							q = q + 1

						q= q -1
						if "FarnellLink" in self.contents[q+self.getComponents()[p].getStartLine()]:
							positions = []
						
							for r in range(len(self.contents[q+self.getComponents()[p].getStartLine()])):
								
								if self.contents[q+self.getComponents()[p].getStartLine()][r] == "\"":
									positions.append(r)
							
									
							self.contents[q+self.getComponents()[p].getStartLine()] = self.contents[q+self.getComponents()[p].getStartLine()][:positions[-4]+1]+self.getComponents()[p].GetFarnellLink() + self.contents[q+self.getComponents()[p].getStartLine()][positions[-3]:]
							
							#place both DigiKeyLink and  MouserLink on same line:
							FarnellLine = self.contents[q+self.getComponents()[p].getStartLine()]
							bufferstring = getCleanLine(self.contents[q-1+self.getComponents()[p].getStartLine()])
							self.contents[q+self.getComponents()[p].getStartLine()] = FarnellLine +  bufferstring[:2] + str(int(bufferstring[2])+2)+ bufferstring[3:5]+ self.getComponents()[p].getMouserLink() + bufferstring[5:-1] + " \"MouserLink\"" + "\n"
							FarnellLine = self.contents[q+self.getComponents()[p].getStartLine()]
							self.contents[q+self.getComponents()[p].getStartLine()] = FarnellLine +  bufferstring[:2] + str(int(bufferstring[2])+3)+ bufferstring[3:5]+ self.getComponents()[p].getDigiKeyLink() + bufferstring[5:-1] + " \"DigiKeyLink\"" + "\n"
							
							#print("HOIHOIHOIHOI")
						elif "MouserLink" in self.contents[q+self.getComponents()[p].getStartLine()]:	
							#PLACE FarnellLink before, DigiKey After
							if "FarnellLink" in self.contents[q-1 + self.getComponents()[p].getStartLine()]: #is FarnellLink in Previous Line
								positions = []
						
								for r in range(len(self.contents[q-1 + self.getComponents()[p].getStartLine()])):
								
									if self.contents[q-1+self.getComponents()[p].getStartLine()][r] == "\"":
										positions.append(r)
																
								self.contents[q-1+self.getComponents()[p].getStartLine()] = self.contents[q-1+self.getComponents()[p].getStartLine()][:positions[-4]+1]+self.getComponents()[p].GetFarnellLink() + self.contents[q-1+self.getComponents()[p].getStartLine()][positions[-3]:]
							#Reparse MouserString
							
							positions = []
						
							for r in range(len(self.contents[q+self.getComponents()[p].getStartLine()])):
								
								if self.contents[q+self.getComponents()[p].getStartLine()][r] == "\"":
									positions.append(r)
							
									
							self.contents[q+self.getComponents()[p].getStartLine()] = self.contents[q+self.getComponents()[p].getStartLine()][:positions[-4]+1]+self.getComponents()[p].getMouserLink() + self.contents[q+self.getComponents()[p].getStartLine()][positions[-3]:]
							
							# add DigiKeyLink onto MouserLink Line
							if "FarnellLink" in self.contents[q-1 + self.getComponents()[p].getStartLine()]:
								bufferstring = getCleanLine(self.contents[q-2+self.getComponents()[p].getStartLine()])
							else:
								bufferstring = getCleanLine(self.contents[q-1+self.getComponents()[p].getStartLine()])
								# PUT FarnellLink in place:
								q = q -1
								bufferstring = self.contents[q+self.getComponents()[p].getStartLine()]
								self.contents[q+self.getComponents()[p].getStartLine()] = self.contents[q+self.getComponents()[p].getStartLine()] +  bufferstring[:2] + str(int(bufferstring[2])+1)+ bufferstring[3:5]+ self.getComponents()[p].GetFarnellLink() + bufferstring[5:-1] + " \"FarnellLink\"" + "\n"
								q = q + 1
								
							MouserLine = self.contents[q+self.getComponents()[p].getStartLine()]
							self.contents[q+self.getComponents()[p].getStartLine()] = MouserLine +  bufferstring[:2] + str(int(bufferstring[2])+1)+ bufferstring[3:5]+ self.getComponents()[p].getDigiKeyLink() + bufferstring[5:-1] + " \"DigiKeyLink\"" + "\n"
						
						
						elif "DigiKeyLink" in self.contents[q+self.getComponents()[p].getStartLine()]:
							orignalBufferLine = ""
							if "FarnellLink" in self.contents[q-2 + self.getComponents()[p].getStartLine()]: #is FarnellLink in the line before previous Line
								orignalBufferLine = getCleanLine(self.contents[q-3 + self.getComponents()[p].getStartLine()])
								positions = []
						
								for r in range(len(self.contents[q-2 + self.getComponents()[p].getStartLine()])):
									if self.contents[q-2+self.getComponents()[p].getStartLine()][r] == "\"":
										positions.append(r)
																
								self.contents[q-2+self.getComponents()[p].getStartLine()] = self.contents[q-2+self.getComponents()[p].getStartLine()][:positions[-4]+1]+self.getComponents()[p].GetFarnellLink() + self.contents[q-2+self.getComponents()[p].getStartLine()][positions[-3]:]
								
								if "MouserLink" in self.contents[q - 1 + self.getComponents()[p].getStartLine()]:
									positions = []
						
									for r in range(len(self.contents[q-1 + self.getComponents()[p].getStartLine()])):
										if self.contents[q-1+self.getComponents()[p].getStartLine()][r] == "\"":
											positions.append(r)
																
									self.contents[q-1+self.getComponents()[p].getStartLine()] = self.contents[q-1+self.getComponents()[p].getStartLine()][:positions[-4]+1]+self.getComponents()[p].getMouserLink() + self.contents[q-1+self.getComponents()[p].getStartLine()][positions[-3]:]
									#controleer
								if "DigiKeyLink" in self.contents[q + self.getComponents()[p].getStartLine()]:
									positions = []
						
									for r in range(len(self.contents[q + self.getComponents()[p].getStartLine()])):
										if self.contents[q+self.getComponents()[p].getStartLine()][r] == "\"":
											positions.append(r)
																
									self.contents[q+self.getComponents()[p].getStartLine()] = self.contents[q+self.getComponents()[p].getStartLine()][:positions[-4]+1]+self.getComponents()[p].getDigiKeyLink() + self.contents[q+self.getComponents()[p].getStartLine()][positions[-3]:]
								
								
								
							elif "FarnellLink" in self.contents[q-1 + self.getComponents()[p].getStartLine()]: #is FarnellLink in Previous Line
								orignalBufferLine = getCleanLine(self.contents[q-2 + self.getComponents()[p].getStartLine()])
								positions = []
						
								for r in range(len(self.contents[q-1 + self.getComponents()[p].getStartLine()])):
									if self.contents[q-1+self.getComponents()[p].getStartLine()][r] == "\"":
										positions.append(r)
																
								self.contents[q-1+self.getComponents()[p].getStartLine()] = self.contents[q-1+self.getComponents()[p].getStartLine()][:positions[-4]+1]+self.getComponents()[p].GetFarnellLink() + self.contents[q-1+self.getComponents()[p].getStartLine()][positions[-3]:]
								#add MouserLink to Previous line
								FarnellLine = self.contents[q-1+self.getComponents()[p].getStartLine()]
								
								self.contents[q+self.getComponents()[p].getStartLine()] = FarnellLine +  orignalBufferLine[:2] + str(int(orignalBufferLine[2])+2)+ orignalBufferLine[3:5]+ self.getComponents()[p].getMouserLink() + orignalBufferLine[5:-1] + " \"MouserLink\"" + "\n"
								
								#Missing DigiKeyLink Operation
								positions = []
						
								for r in range(len(self.contents[q + self.getComponents()[p].getStartLine()])):
									if self.contents[q+self.getComponents()[p].getStartLine()][r] == "\"":
										positions.append(r)
										
								#print(self.contents[q+self.getComponents()[p].getStartLine()][:positions[-4]+1])
								
								self.contents[q+self.getComponents()[p].getStartLine()] = self.contents[q+self.getComponents()[p].getStartLine()][:positions[-4]+1]+self.getComponents()[p].GetFarnellLink() + self.contents[q-1+self.getComponents()[p].getStartLine()][positions[-3]:]
							elif "MouserLink" in self.contents[q-1 + self.getComponents()[p].getStartLine()]:
								#mouserlink in previous line
								bufferstring = getCleanLine(self.contents[q - 2 + self.getComponents()[p].getStartLine()])
								self.contents[q-1 + self.getComponents()[p].getStartLine()] = self.contents[q-1 + self.getComponents()[p].getStartLine()] + bufferstring[:2] + str(int(bufferstring[2])+1)+ bufferstring[3:5]+ self.getComponents()[p].GetFarnellLink() + bufferstring[5:-1] + " \"FarnellLink\"" + "\n"
								
								positions = []
						
								for r in range(len(self.contents[q - 1 + self.getComponents()[p].getStartLine()])):
									if self.contents[q-1+self.getComponents()[p].getStartLine()][r] == "\"":
										positions.append(r)
								self.contents[q -1 +self.getComponents()[p].getStartLine()] = self.contents[q -1 +self.getComponents()[p].getStartLine()][:2] + str(int(bufferstring[2])+2) + self.contents[q -1 +self.getComponents()[p].getStartLine()][3:positions[-4]+1]+self.getComponents()[p].getDigiKeyLink() + self.contents[q - 1 +self.getComponents()[p].getStartLine()][positions[-3]:]
								#print(self.contents[q -1 +self.getComponents()[p].getStartLine()])
								positions = []
						
								for r in range(len(self.contents[q + self.getComponents()[p].getStartLine()])):
									if self.contents[q+self.getComponents()[p].getStartLine()][r] == "\"":
										positions.append(r)
								self.contents[q +self.getComponents()[p].getStartLine()] = self.contents[q +self.getComponents()[p].getStartLine()][:2] + str(int(bufferstring[2])+3) + self.contents[q +self.getComponents()[p].getStartLine()][3:positions[-4]+1]+self.getComponents()[p].getDigiKeyLink() + self.contents[q +self.getComponents()[p].getStartLine()][positions[-3]:]
								
							else:
								#No Links other than DigiKeyLink found
								positions = []
						
								for r in range(len(self.contents[q + self.getComponents()[p].getStartLine()])):
									if self.contents[q+self.getComponents()[p].getStartLine()][r] == "\"":
										positions.append(r)
								
								#print(positions)
								#print(self.contents[q+self.getComponents()[p].getStartLine()])
								bufferstring = getCleanLine(self.contents[q - 1 +self.getComponents()[p].getStartLine()]) #could be wrong if value exist in last line
								self.contents[q+self.getComponents()[p].getStartLine()] = self.contents[q +self.getComponents()[p].getStartLine()][:2] + str(int(bufferstring[2])+3) + self.contents[q+self.getComponents()[p].getStartLine()][3:positions[-4]+1]+self.getComponents()[p].getDigiKeyLink() + self.contents[q+self.getComponents()[p].getStartLine()][positions[-3]:]
								
								
								#bufferstring = getCleanLine(self.contents[q - 1 +self.getComponents()[p].getStartLine()]) #could be wrong if value exist in last line
								self.contents[q-1+self.getComponents()[p].getStartLine()] = self.contents[q-1+self.getComponents()[p].getStartLine()] +  bufferstring[:2] + str(int(bufferstring[2])+1)+ bufferstring[3:5]+ self.getComponents()[p].GetFarnellLink() + bufferstring[5:-1] + " \"FarnellLink\"" + "\n"
								FarnellLine = self.contents[q -1 +self.getComponents()[p].getStartLine()]
								self.contents[q -1 +self.getComponents()[p].getStartLine()] = FarnellLine +  bufferstring[:2] + str(int(bufferstring[2])+2)+ bufferstring[3:5]+ self.getComponents()[p].getMouserLink() + bufferstring[5:-1] + " \"MouserLink\"" + "\n"
						else:
						#No links have been found
							bufferstring = getCleanLine(self.contents[q+self.getComponents()[p].getStartLine()])
														
							self.contents[q+self.getComponents()[p].getStartLine()] = self.contents[q+self.getComponents()[p].getStartLine()] +  bufferstring[:2] + str(int(bufferstring[2])+1)+ bufferstring[3:5]+ self.getComponents()[p].GetFarnellLink() + bufferstring[5:-1] + " \"FarnellLink\"" + "\n"
							FarnellLine = self.contents[q+self.getComponents()[p].getStartLine()]
							self.contents[q+self.getComponents()[p].getStartLine()] = FarnellLine +  bufferstring[:2] + str(int(bufferstring[2])+2)+ bufferstring[3:5]+ self.getComponents()[p].getMouserLink() + bufferstring[5:-1] + " \"MouserLink\"" + "\n"
							MouserLine = self.contents[q+self.getComponents()[p].getStartLine()]
							self.contents[q+self.getComponents()[p].getStartLine()] = MouserLine +  bufferstring[:2] + str(int(bufferstring[2])+3)+ bufferstring[3:5]+ self.getComponents()[p].getDigiKeyLink() + bufferstring[5:-1] + " \"DigiKeyLink\"" + "\n"
				
			try:
				f = open(savepath, 'w')
			except IOError:
				return "error"
			else:			
				for i in range (len(self.contents)):
					f.write(self.contents[i])
				f.close
				
			for i in range(len(self.subcircuits)):
				for p in range (len(savepath)):
					if savepath[-p] == "/":
						break #find first forwardslash to add other file name
				
				new_savepath = savepath[:-p+1]+self.subcircuits_names[i]
				print("new_savepath")
				self.subcircuits[i].ModifyNewSCHFile(0, CSV_FILE, new_savepath)
				#mainFile.ModifyNewSCHFile(0, openCSVFile,savePath):
	def deleteContents(self):
		for p in range (len(self.subcircuits)):
			# first delete subcircuits
			self.subcircuits[0].deleteContents()
		
		for i in range (len(self.components)):
			del self.components[0]
		self.contents = ""
		self.numb_of_comps = 0
		self.subcircuits_names = []
		self.number_of_subcircuits = 0
		self.components = []
		self.subcircuits = []
		self.SchematicName = ""
		self.path = ""
		
class CSV_FILE(object):
	def __init__(self):
			self.contents = []
			self.components = []
			self.number_of_components = 0
			self.startposition = 0
			self.endposition = 0
			self.FarnellLink = ""
			self.SchematicName = ""
			self.name = ""
			self.annotation = ""
			self.value = ""
	def setContents(self, to_be_inserted):
				self.contents = to_be_inserted
	def printContents(self):
				print(self.contents)
	def printLine(self, line):
			print(self.contents[line])
	def printComponents(self):
			for i in range (self.number_of_components):
				print(self.components[i].getFarnellLink())
	def getNumberOfComponents(self):
			return self.number_of_components
	def getComponents(self):
			return self.components
	def readCSVline(self,line) :
		commaSepLine = re.compile(r'\s*(\"?)\s*([^\"]*?)\s*\1\s*(,|$)')
		result = commaSepLine.findall(line)
		last = True
		items = []
		# bit more complex loop since the end char $ sometimes delivers double matches
		# regular code instad of regular expersion might be simpler :(
		for match in result :
			if match[2] == "," :
				if match[1] :
					items.append(match[1])
				else :
					items.append('')
			else :
				if last :
					last = False
					if match[1] :
						items.append(match[1])
					else :
						items.append('')
		return items
	
	def generateCSVComponents(self,headerItems):
		for i in range(1, len(self.contents)):
			comp = Component()
			compItems = self.readCSVline(self.contents[i])
			if len(compItems) != len(headerItems) :
				print(self.contents[i])
				return 'error'
			for e in range(0,len(headerItems)) :
				if headerItems[e] == "SchematicName" :
					comp.setSchematicName(compItems[e])
				elif headerItems[e] == "PartType" :
					comp.setPartType(compItems[e])
				elif headerItems[e] == "timestamp" :
					comp.setTimestamp(compItems[e])
				elif headerItems[e] == "Reference" :
					comp.setReference(compItems[e])
				elif headerItems[e] == "unit" :
					comp.setUnit(compItems[e])
				elif headerItems[e] == "Value" :
					comp.setValue(compItems[e])
				elif headerItems[e] == "Footprint" :
					#print(compItems[e])
					comp.setFootprint(compItems[e])
				elif headerItems[e] == "Datasheet" :
					comp.setDatasheet(compItems[e])
				else:
					if compItems[e] != '' and headerItems[e] != '' :
						comp.setField(headerItems[e],compItems[e])
			if comp.isset() :
				print("{} with timestamp {} in list".format(comp.getReference(),comp.getTimestamp()))
				self.components.append(comp)
				self.number_of_components += 1
	def deleteContents(self):
		for i in range (len(self.components)):
			del self.components[0]
		self.contents = []
		self.components = []
		self.number_of_components = 0
		self.startposition = 0
		self.endposition = 0
		self.FarnellLink = ""
		self.SchematicName = ""
		self.name = ""
		self.annotation = ""
		self.value = ""
		#break

