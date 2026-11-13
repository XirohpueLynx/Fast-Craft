#Author: XirohpueLynx
import os
from pathlib import Path
'''
filename=input("FileName.json: ")
filex=open(filename,"r")
block["wtype"]=input("Wood type: ") #oak
block["lcode"]=input("Code: ") #log
block["ldata"]=input("Data: ") #0
'''
filename=["birch_boat_from_log.json","birch_button_from_log.json","birch_door_from_log.json",
          "birch_fence_from_log.json","birch_fence_gate_from_log.json","birch_pressure_plate_from_log.json",
          "birch_stairs_from_log.json","birch_trapdoor_from_log.json","birch_wooden_slab_from_log.json",
          "sign_birch_from_log.json","bowl_from_log.json","stick_from_log.json","chest_from_log.json",
          "crafting_table_from_log.json","ladder_from_log.json"] #list of all the files
bdict=[ #Different block data dictionary
    {"wtype":"oak","lcode":"log","ldata":"0","pdata":"0"},
    {"wtype":"spruce","lcode":"log","ldata":"1","pdata":"1"},
    #{"wtype":"birch","lcode":"log","ldata":"2","pdata":"2"},
    {"wtype":"jungle","lcode":"log","ldata":"3","pdata":"3"},
    {"wtype":"acacia","lcode":"log2","ldata":"0","pdata":"4"},
    {"wtype":"dark_oak","lcode":"log2","ldata":"1","pdata":"5"},
    {"wtype":"crimson","lcode":"crimson_stem","ldata":"-1","pdata":"-1"},
    {"wtype":"warped","lcode":"warped_stem","ldata":"-1","pdata":"-1"},
    {"wtype":"oak","lcode":"stripped_oak_log","ldata":"-1","pdata":"0"},
    {"wtype":"spruce","lcode":"stripped_spruce_log","ldata":"-1","pdata":"1"},
    {"wtype":"birch","lcode":"stripped_birch_log","ldata":"-1","pdata":"2"},
    {"wtype":"jungle","lcode":"stripped_jungle_log","ldata":"-1","pdata":"3"},
    {"wtype":"acacia","lcode":"stripped_acacia_log","ldata":"-1","pdata":"4"},
    {"wtype":"dark_oak","lcode":"stripped_dark_oak_log","ldata":"-1","pdata":"5"},
    {"wtype":"crimson","lcode":"stripped_crimson_stem","ldata":"-1","pdata":"-1"},
    {"wtype":"warped","lcode":"stripped_warped_stem","ldata":"-1","pdata":"-1"},
    {"wtype":"oak","lcode":"wood","ldata":"0","pdata":"0"},
    {"wtype":"spruce","lcode":"wood","ldata":"1","pdata":"1"},
    {"wtype":"birch","lcode":"wood","ldata":"2","pdata":"2"},
    {"wtype":"jungle","lcode":"wood","ldata":"3","pdata":"3"},
    {"wtype":"acacia","lcode":"wood","ldata":"4","pdata":"4"},
    {"wtype":"dark_oak","lcode":"wood","ldata":"5","pdata":"5"},
    {"wtype":"crimson","lcode":"crimson_hyphae","ldata":"-1","pdata":"-1"},
    {"wtype":"warped","lcode":"warped_hyphae","ldata":"-1","pdata":"-1"},
    {"wtype":"oak","lcode":"wood","ldata":"8","pdata":"0"},
    {"wtype":"spruce","lcode":"wood","ldata":"9","pdata":"1"},
    {"wtype":"birch","lcode":"wood","ldata":"10","pdata":"2"},
    {"wtype":"jungle","lcode":"wood","ldata":"11","pdata":"3"},
    {"wtype":"acacia","lcode":"wood","ldata":"12","pdata":"4"},
    {"wtype":"dark_oak","lcode":"wood","ldata":"13","pdata":"5"},
    {"wtype":"crimson","lcode":"stripped_crimson_hyphae","ldata":"-1","pdata":"-1"},
    {"wtype":"warped","lcode":"stripped_warped_hyphae","ldata":"-1","pdata":"-1"}
    ]

lines=[] #store file's lines
index=0 #index for lines
bindex=0 #index for bdict
justPlank = None #if previous line was planks
justLog = None #if previous line was logs
justItem = None #if previous line was item (used only if not logs when changing data)
justResult = None
fileBName = None
noName = None
acacia = None

for block in bdict:
    #make folders
    if block["lcode"] == "log2": #don't allow log2 folder, call it log
        filePath = Path(block["wtype"])/"log"
    elif block["lcode"] == "wood" and int(block["ldata"]) >= 8:
        filePath = Path(block["wtype"])/"stripped_wood"
    else:
        filePath = Path(block["wtype"])/block["lcode"].replace(block["wtype"]+"_","")
    if not os.path.isdir(filePath): #Check for folder
        os.makedirs(filePath)
    
    for file in filename:
        if "bowl" in file or "chest" in file or "crafting" in file or "ladder" in file or "stick" in file:
            if block["lcode"] == "log" or block["lcode"] == "log2":
                continue
            fileBName = "log"
            noName = True
        else:
            fileBName = "birch"
            noName = False
        if "boat" in file and (block["wtype"] == "crimson" or block["wtype"] == "warped"):
            continue
        index=0 #reset variables
        lines=[]
        filex=open(file,"r")
        
        newfilename=file.replace("birch",block["wtype"]) #fix block name in file name

        #fix block type in file name
        if block["lcode"] == "log" or block["lcode"] == "log2":
            newfilename = newfilename.replace("log",(block["wtype"]+"_")*noName+"log")
            #if "stripped" in block["lcode"]:
                #newfilename=newfilename.replace("log","stripped_log")
        elif block["lcode"] == "wood":
            if int(block["ldata"]) < 8:
                newfilename=newfilename.replace("log",(block["wtype"]+"_")*noName+"wood")
            else:
                newfilename=newfilename.replace("log","stripped_"+(block["wtype"]+"_")*noName+"wood")
        #elif "hyphae" in block["lcode"]:
            #if "stripped" in block["lcode"]:
                #newfilename=newfilename.replace("log","stripped_"+(block["wtype"]+"_")*noName+"hyphae")
            #else:
                #newfilename=newfilename.replace("log",(block["wtype"]+"_")*noName+"hyphae")
        #elif "stem" in block["lcode"]:
            #if "stripped" in block["lcode"]:
                #newfilename=newfilename.replace("log","stripped_"+(block["wtype"]+"_")*noName+"stem")
            #else:
                #newfilename=newfilename.replace("log",(block["wtype"]+"_")*noName+"stem")
        elif int(block["pdata"]) < 0: #if new wood (works bc they are named in code, no need ID)
            newfilename=newfilename.replace("log",block["lcode"].replace(block["wtype"]+"_",(block["wtype"]+"_")*noName)).replace("wooden_","")
        else:
            newfilename=newfilename.replace("log","stripped_"+(block["wtype"]+"_")*noName+"log")

        print(newfilename) #signify new file started
        #if block["wtype"]=="acacia" and block["lcode"]=="wood" and block["ldata"]=="12" and block["pdata"]=="4" and "bowl" in file:
            #acacia = True
        #else:
            #acacia = False

        for line in filex:
            lines.append(str(line))

            #if acacia and "A\":" in line:
                #print("acacia bowl")
            
            if "identifier" in line: #replace identifier file name with actual file name
                lines[index]=lines[index].replace(file[:-5],newfilename[:-5])
                #print(lines[index])
                justPlank = False
                justLog = False

            else:
                #fix for oak to become "wooden" items bc of old naming in mc
                if block["wtype"] == "oak":
                    if "group" in line: #make sure groups isn't changed
                        pass
                    elif "button" in line or "_door" in line or "pressure_plate" in line: #change appropriate item names to wooden
                        lines[index]=line.replace(fileBName,"wooden")
                    elif "sign" in line or "fence_gate" in line or "trapdoor" in line: #change appropriate item names to without wooden
                        lines[index]=line.replace("birch_","")
                        
                if fileBName in lines[index]: #fix wood type name
                    if block["wtype"] == "oak" and block["lcode"] == fileBName:
                        pass
                    elif block["wtype"] == "oak" and "stairs" in line:
                        lines[index] = lines[index].replace(fileBName,block["wtype"])
                    else:
                        if fileBName == "log":
                            lines[index] = lines[index].replace(fileBName,block["lcode"])[:-1]+",\n"
                            if int(block["pdata"]) >= 0: #not new wood
                                if block["lcode"] == "wood":
                                    lines.append("                \"data\": "+block["ldata"]+"\n")
                                else:
                                    lines.append("                \"data\": "+block["pdata"]+"\n")
                                index += 1
                            else:
                                lines[index]=lines[index].replace(",","")
                        else:
                            lines[index] = line.replace(fileBName,block["wtype"])
                    justPlank = False
                    justLog = False
                    
                elif "log" in line: #fix code name for the wood type
                    lines[index]=line.replace("log",block["lcode"])
                    justPlank = False
                    justLog = True
                    
                elif "planks" in line:
                    if "stem" in block["lcode"] or "hyphae" in block["lcode"]: #if nether wood
                        lines[index]=line.replace("planks",block["wtype"]+"_planks") #add the crimson/warped on to the plank code name
                    justPlank = True
                    justLog = False
                    
                elif "\"data\": 2" in lines[index]: #fix data (the coding id of the block)
                    if block["pdata"] == "-1": #if doesn't have a plank data ie. new wood (-ve used to signify no data needed), delete line, rewind index
                        del lines[index]
                        index -= 1
                        lines[index]=lines[index][:-2]+"\n" #remove the comma (also removes the return (/new line)), so add back on
                    elif justPlank: #if the data is for planks
                        lines[index]=line.replace("2",block["pdata"])
                    elif justLog and block["ldata"] == "-1": #if data for new wood
                        del lines[index]
                        lines[index-1]=lines[index-1][:-2]+"\n" #remove the comma (also removes the return (/new line)), so add back
                        index -= 1
                    elif justLog: #all other woods
                        lines[index]=line.replace("2",block["ldata"])
                    elif justItem: #not log, but result item
                        
                        lines[index]=line.replace("2",block["pdata"])
                    justPlank = False
                    justLog = False
                    
                elif "count" in line and "," not in lines[index-1]:
                    lines[index-1] = lines[index-1][:-1]+",\n"
                    
                else:
                    justPlank = False
                    justLog = False
                    
                justItem = False
                if "item" in line:
                    justItem = True
                    if ("minecraft:") in line and ("bowl" in file or "chest" in file or "crafting" in file or "ladder" in file or "stick" in file) and not justResult:
                          lines[index]=lines[index].replace("minecraft:","")
                    elif int(block["pdata"]) < 0: #look 4 new wood
                        if "wooden" in line:
                            lines[index]=lines[index].replace("wooden",block["wtype"])
                        elif "slab" in line or "fence" in line and not "fence_gate" in line:
                            lines[index]=lines[index].replace("fence",block["wtype"]+"_fence").replace("slab",block["wtype"]+"_slab")
                        
                justResult = False
                if "result" in line:
                    justResult = True
            index += 1
        
        index=0
        filex.close()

        filey=open(filePath/newfilename,"w")
        for item in lines:
            filey.write(lines[index])
            index += 1
        filey.close()
        
        lines=[]
        index=0

    bindex+=1
    
    print("done")
