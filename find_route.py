import sys

#a function that takes in the data read from a file and store it into a list
def fill_list(list, data):
    for line in data:
        if line == "END OF INPUT\n":
            break
        line_array = line.strip("\n").split(" ")
        line_array[2] = int(line_array[2])
        list.append(line_array)

#A function that behaves the exact same as fill_list, but used to fill a hueristic list instead
def fill_hueristic(hueristic, data):
    for line in data:
        if line == "END OF INPUT\n":
            break
        line_array = line.strip("\n").split(" ")
        line_array[1] = int(line_array[1])
        hueristic.append(line_array)
        
#This function takes in a node and returns a list of all routes the node can go, the weight of each path, the destination,
#and the original location.  It also avoids returning paths to blacklisted locations(to avoid going back to expanded nodes)
def loc_search(list, location,  blacklist):
    #The list that will be returned and the line_num variable.  Not going to lie, I forgot what it's for and am too scared to
    #remove it
    paths = []
    line_num = 0
    
    #A for-each loop that will iterate through each member of the list
    for arr in list:
        #Checks if either member 0 or member 1 of arr(these would be the cities in the file), and fills the list with the data we want
        #Does not add a path if the connected city is blacklisted
        if arr[0] == location and arr[1] not in blacklist:
            des = [arr[2], line_num, arr[1], location]
            paths.append(des)
        elif arr[1] == location and arr[0] not in blacklist:
            des = [arr[2], line_num, arr[0], location]
            paths.append(des)
            
    #This is a back-up in case all paths are blacklist(If a node has only one path, the code could get returned a NULL for paths, which broke the code)
    #Does the exact same thing as the last loop, but adds blacklisted items
    if len(paths) == 0:
        for arr in list:
            if arr[0] == location:
                des = [arr[2], line_num, arr[1], location]
                paths.append(des)
            elif arr[1] == location:
                des = [arr[2], line_num, arr[0], location]
                paths.append(des)
        
        #Still can't remember what this was for        
        line_num+=1
        
    return paths

#These are some global variables that will be used in the search function
#Could use recursion instead, but this is simpler
sorted_paths = []
route = []
expanded = 0

#The uniform search function
def uniform_search(list, loc, destination, popped, distance):
    #Connecting the global variables
    global sorted_paths
    global expanded
    global pop_num
    global route
    global check_num
    
    i = 0
    check_num+=1
    #Iterator that will be used throughout the function
    i = 0
    
    #We use recursion, so if the location is the destination, we know we've found the path.  Thus we return
    if loc == destination:
        global expanded
        pop_num+=1
        check_num-=1
        
        route.append(loc)
        
        expanded = len(popped)
        return int(distance)
    
    #Get the available paths that exist from the location, while blacklisted the already expanded nodes
    paths = loc_search(list, loc, popped) 
        
    #We count this number to help us get nodes generated
    if paths[0][2] not in popped:
        pop_num+=len(paths)
        
    #In order to make sure the algorithm uses the least expensive path we push the paths with the current distance added
    #We use a for-each look to keep sorted_paths from having 3 dimensions
    #Also because we add to a global variable it remember all paths that can be taken at all times
    for p in paths:
        p[0] += distance
        sorted_paths.append(p)
    
    #If a node has not been expanded, we add it to the list
    if loc not in popped:
        popped.append(loc)
    
    #We sort the collection of all paths
    sorted_paths = sorted(sorted_paths)
    
    #We need to iterate sorted_paths becuase paths are never removed(Though now that I think about it, that would be a good idea)
    #So if we keep using the shortest path we will go down the same path over and over and over again
    #This will also check if all paths we've seen lead to an expanded node and if that is true it will call 
    while sorted_paths[i][2] in popped:
        i+=1
        if i == len(sorted_paths):
            print("No path Exist")
            expanded = len(popped)
            check_num-=1
            return "infinity"
        
    #Begins recursion by storing it into a variable, so we can return later.
    #update loc and distance for next loop
    answer = uniform_search(list, sorted_paths[i][2], destination, popped, sorted_paths[i][0])
    
    #Returns instantly if there is no route
    if answer == "infinity":
        return answer
    
    #Stores route by checking for a path with a destination of the point of the route we're in
    if route[len(route)-1] == sorted_paths[i][2]:
        route.append(sorted_paths[i][0])
        route.append(sorted_paths[i][3])
        
    return answer
    
#A function that will find and return the heuristic value of any given point
def find_h_val(dest, hueristics):
    for h in hueristics:
        if h[0] == dest:
            return h[1]
    
#more global variables
pop_num = 0
check_num = 0

def astar_search(list, loc, destination, popped, distance, heuristics):
    #Setting up global variables again
    global sorted_paths
    global pop_num
    global check_num
    
    i = 0
    check_num+=1
    
    #We use recursion, so if the location is the destination, we know we've found the path.  Thus we return
    if loc == destination:
        global expanded
        check_num-=2
        route.append(loc)
        expanded = len(popped)
        return distance
    
    #Get the available paths that exist from the location, while blacklisted the already expanded nodes
    paths = loc_search(list, loc, popped) 
    
    if paths[0][2] not in popped:
        pop_num+=len(paths)
    
    #Changes adds the current distance to the paths, but also inserts the heuristic value combined with distance at the beginning
    for p in paths:
        p[0] += distance
        p.insert(0, p[0] + find_h_val(p[2], heuristics))
        sorted_paths.append(p)
    
    if loc not in popped:
        popped.append(loc)
        
    #sorts paths based on the first value of every member
    sorted_paths = sorted(sorted_paths)
    
    #We need to iterate sorted_paths becuase paths are never removed(Though now that I think about it, that would be a good idea)
    #So if we keep using the shortest path we will go down the same path over and over and over again
    #This will also check if all paths we've seen lead to an expanded node and if that is true it will call 
    while sorted_paths[i][3] in popped:
        i+=1
        if i == len(sorted_paths):
            print("No path Exist")
            expanded = len(popped)
            check_num-=1
            return "infinity"
    
    #Begins recursion by storing it into a variable, so we can return later.
    #update loc and distance for next loop
    answer = astar_search(list, sorted_paths[i][3], destination, popped, sorted_paths[i][1], hueristics)
    
    #Returns instantly if there is nor route
    if answer == "infinity":
        return answer

    #Stores route by checking for a path with a destination of the point of the route we're in
    if route[len(route)-1] == sorted_paths[i][3]:
        route.append(sorted_paths[i][1])
        route.append(sorted_paths[i][4])
        
    return answer
   
#This was made just to act as a base for the other search types, it is not part of the assignment
def search(list, loc, destination, popped):
    i = 0
    
    if loc == destination:
        print("destination found.  Popped", popped, len(popped))
        return
    paths = loc_search(list, loc, popped)
    if loc not in popped:
        popped.append(loc)
    while i != len(paths)-1 and len(paths) > 1 and paths[i][1] in popped:
        i+=1

    search(list, paths[i][1], destination, popped)    

#Checks if both the start and end cities are valid and if neither are it returns false
def check_city(list, start, end):
    valid_start, valid_end = False, False
    
    i = 0
    
    for set in list:
        if start in set:
            valid_start = True
        if end in set:
            valid_end = True
        i+=1
        
    return valid_start and valid_end
 
#Function to print the route based off of a list
def print_route(route):
    i = len(route)-1
    temp = 0
    
    print("Route:")
    while i > 0:
        print(route[i], "to", route[i-2], ",", route[i-1]-temp, "km")
        temp = route[i-1]
        i-=2
     
#Initialise and assign data
data = open(sys.argv[1], "r")
origin = sys.argv[2]
destination = sys.argv[3]

#The ordering of a list changes if it is using a*, so we have a value for that
is_astar = 0

#Checks if there is enough command line arguments to be using a*
if len(sys.argv) > 4:
    is_astar = 1
    hueristic_data = open(sys.argv[4], "r")
    hueristics = []
    fill_hueristic(hueristics, hueristic_data)

#Initial Function variables
list = []
blacklist = []
fill_list(list, data)

#Makes sure both cities are valid and exits if they aren't
if check_city(list, origin, destination) == False:
    print("Invalid city detected: Exiting program")
    sys.exit()
paths = loc_search(list, origin, blacklist)

#Gets distance from seach functions
if len(sys.argv) > 4:
    distance = astar_search(list, origin, destination, blacklist, 0, hueristics)
else:
    distance = uniform_search(list, origin, destination, blacklist, 0)

#Prints required data
print("Nodes Popped: ", check_num + expanded)
print("Nodes Expanded: ", expanded)
print("Nodes Generated: ", pop_num + expanded)

if distance == "infinity":
    print("Distance: ", distance)
    print("Route:\nNone")
else:
    print("Distance: ", distance,"km")
    print_route(route)


data.close()
if len(sys.argv) > 4:
    hueristic_data.close()