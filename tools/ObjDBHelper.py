import os
import json

#----------------------------------------------------------------------------------
#
# This sets up the basic JSON file for an object.
#
#----------------------------------------------------------------------------------
def init_object(directory, internalName, className):
    data = {}
    data.update({"InternalName": internalName})
    data.update({"ClassName": className})
    data.update({"Name": internalName})
    data.update({"List": "ObjectList"})
    data.update({"Category": "unknown"})
    data.update({"Description": ""})
    data.update({"Properties": {}})
    data.update({"Models": []})
    data.update({"Links": []})
        
    outf = open(directory + "/" + internalName + ".json", "w")
    outf.write(json.dumps(data, indent=4))
    outf.close()

#----------------------------------------------------------------------------------
#
# This sets up the basic JSON file for each element in the given file of object
# names. The strings in the input file should be structured like this:
#  "UnitConfigName" ("ParameterConfigName")
#
#----------------------------------------------------------------------------------
def init_objects(filepath):
    with open(filepath) as f:
        objs = f.readlines()
    objs = [x.strip() for x in objs]
    
    directory = "/objects"
    if not os.path.isdir(directory):
        os.makedirs(directory)
    
    for obj in objs:
        splitName = obj.split(" (")
        
        unitConfigName = splitName[0]
        parameterConfigName = splitName[1][:-1]    # last character is ')'
        
        init_object(directory, unitConfigName, parameterConfigName)
    
#----------------------------------------------------------------------------------
#
# This will compile all single object files in the given directory into a huge list
# of objects.
#
#----------------------------------------------------------------------------------
def build_objects(dirpath, destpath):
    data = {
        "Objects": {},                   # contains every object structure
        "Categories": {}                 # categorizes every object alphabetically
        }
    
    objects = data["Objects"]
    categories = data["Categories"]
    
    # Populate and initialize categories
    with open(dirpath + "/_Categories.json", "r") as catsfile:
        cats = json.load(catsfile)
    cats = cats["Categories"]
    
    for catname, catdict in cats.items():
        print("-- Processing category " + catname + " ...")
        
        categories.update({catname: catdict})
        
        if not "Objects" in catdict:
            catdict.update({"Objects": []})
    
    # Now, add each object
    for objdir in os.listdir(dirpath):
        with open(dirpath + "/" + objdir, "r") as objfile:
            obj = json.load(objfile)
        
        if not "InternalName" in obj:    # make sure we load objects
            continue
        
        internalName = obj["InternalName"]
        category = obj["Category"]

        objects.update({internalName: obj})
        print("-- Processing object " + internalName + " ...")
        
        if category in categories:
            categories[category]["Objects"].append(internalName)
    
    # Sort category objects, just to be safe
    for catname, catdict in categories.items():
        catdict["Objects"].sort()
    
    # Finally, store all the data
    outf = open(destpath, "w")
    outf.write(json.dumps(data, indent=4))
    outf.close()
    
    print("-- Done")

def update_objects(dirpath):
    with open("_props.json", "r") as objfile:
        updatedprops = json.load(objfile)
    
    for objdir in os.listdir(dirpath):
        with open(dirpath + "/" + objdir, "r") as objfile:
            obj = json.load(objfile)
        
        if not "InternalName" in obj:    # make sure we load objects
            continue
        
        internalName = obj["InternalName"]
        
        if not internalName in updatedprops:
            continue
        
        obj.update({"Properties": updatedprops[internalName]})
        
        with open(dirpath + "/" + objdir, "w") as objfile:
            json.dump(obj, objfile, indent=4)

update_objects("C:/Users/Aurum/Documents/GitHub/KinopioDatabase/objects")