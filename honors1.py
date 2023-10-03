##################################################################
##
#
#                       Honor Project Part 1
#
#       Import Modules
#       Open_file Function
#       Read_file Function
#       Fill_missing_values Function
#       
#       Algorithm
#           Call open_file function to get file pointers to neccisary files
#           Skip the header lines in the given csv file
#           Get dictionary of data from calling read_file function
#           Filter the dictionary to fit restrictions
#           Skip header of civil_twilight.txt
#           Turn data of civil_twilight into a dictionary
#           Check each key/value pair in data_dict 
#               If the time of the dictionary entry is not between dawn and dusk for that day
#                   Add that dictionary entry to a list of other entries that don't meet the daylight requirments
#           Go though list of faulty dictionary entries and delete them from the dictionary
#           Print header in csv file
#           Format each dictionary entry and print the formatted entry in the csv file
#           Count each line printed in the csv file
#           Display total data points in csv file in console
#
#           Loops through the data points in the created csv file
#               Checks if the current runway is safe based on data point conditions
#               Checks if the proposed runway is safe based on data point conditions
#               If either is safe, it adds the data point to the corresponding runways' dictionary and set
#
#           Creates a set of all the similar data points between the current and proposed runway
#           Displays all the data points to the corresponding runway file based on if the data point is safe 
#           Displays counts of the current, proposed, and combined runways safe data points
#
##
##################################################################



# import csv module
import csv
from operator import itemgetter
import math

# Variable for data points
count = 0


def open_file():
    '''
    Inputs: None
    Actions: Opens three files, clears daylight_weather.csv each time the program is run
    Returns: File pointers to the opened files
    '''
    # Open files
    file = open("TEW_2021_Observations.csv",'r')
    daylight_file = open("daylight_weather.csv",'w')
    daytime_file = open("civil_twilight.txt",'r')
    current_runway_file = open("current_runway_safe.csv",'w')
    proposed_runway_file = open("proposed_runway_safe.csv",'w')
    test_file = open("testFile.csv",'w')
    
    # Clears file
    test_file.truncate()
    daylight_file.truncate()
    current_runway_file.truncate()
    proposed_runway_file.truncate()
    
    return file, daylight_file, daytime_file,current_runway_file,proposed_runway_file, test_file


def read_file(fp):
    '''
    Takes: A file pointer
    Actions: Goes line by line through the file and assigns the date/time as a key 
            and the conditions as the value in a dictionary; Checks for repeats in lines and takes first occurence 
    Returns: A dictionary of data from file pointer
    '''
    temp_dict = {}  # Empty dictionary
    reader = csv.reader(file)  # Reads the file

    previous_key = ''  # Empty string
    
    # For each line in the read file
    for line in reader:
        
        date = line[0]  # Gets the date of the line
        time = line[1]  # Gets the time of the line
        
        # Creates a tuple fo the date and time
        current_key = (date,time)  
        
        key = line[0].split('/') # Splits the date into a list
        
        # Removes unneccisary data
        line.pop(3)
        line.pop(3)
        line.pop(7)
        line.pop(7)
        line.pop()
        
        value = line[2:8] # Gets the rest of the line exculding the date
        
        # If the current key is not the precious key
        if current_key != previous_key:        
            # If the month portion of the date is numerical and is between March and November
            if key[0].isdigit() and ( 3 <= int(key[0]) <= 11):
                # If the month number is a single digit
                if int(key[0]) < 10:
                    # Put a zero infront of it
                    key[0] = '0' + str(key[0])
                
                #If the day number is a single digit
                if int(key[1]) < 10:
                    # Put a zero infront of it
                    key[1] = '0' + str(key[1])
                
                # Sets year to last two digits (2021) --> (21)
                key[2] = key[2][-2:]
                
                # Joins line with slashs between the month, day, and year
                line[0] = key[0] + '/' + key[1] + '/' + key[2]
                
                # Adds the line to a dicionary with the date and time as the key and the rest of the line as the value
                temp_dict[line[0],time] = value
                
                date = line[0]  # Sets date to updated date
                
            # Assigns current key to the previous key
            previous_key = current_key
    
    # Returns the filled dictionary
    return temp_dict



def fill_missing_values(temp_dict):
    '''
    Takes: A dictionary
    Actions: Fills missing values, then filters the dictionary based on restrictions, then fills the rest of the missing values
    Returns: Filtered dictionary
    '''
    
    # Values: Temp, Ceiling, Visibility
    a_list = ['0','0','0']
    # Values: Wind Speed, Direction, Peak Wind
    b_list = ['0','0','0']
    # Possible indicators of missing values
    m_list = ['m', 'M']
            
    # For each value in dictionary
    for value in temp_dict.values():
        # For each index of the value
        for index, i in enumerate(value):
            # If the index is 0
            if (index == 0):
                # If value is in m_list
                if (i in m_list):
                    # Set the value to the stored value with a * to signify the value was filled
                    value[index] = a_list[0] + '*'
                else:
                    # Make the current value the stored value for filling missing values
                    a_list[0] = value[index]
                    
            # If the index is 4
            elif (index == 4):
                # If value is in m_list
                if (i in m_list):
                    # Set the value to the previous value with a * to signify the value was filled
                    value[index] = a_list[1] + '*'
                else:
                    # Make the current value the stored value for filling missing values
                    a_list[1] = value[index]
                    
            # If the index is 5
            elif (index == 5):
                # If value is in m_list
                if (i in m_list):
                    # Set the value to the previous value with a * to signify the value was filled
                    value[index] = a_list[2] + '*'
                else:
                    # Make the current value the stored value for filling missing values
                    a_list[2] = value[index]    
    
        
        
    filtered_dict = {}  # Enpty dictionary
    
    # For each key/value pair in given dictionary
    for key, num in temp_dict.items():
        # If data does not meet the flying requirments
        if ((int(num[0].strip('*')) < 35) or (int(num[4].strip('*')) < 2000) or (int(num[5].strip('*')) < 5)):
            # Set the entry to empty value
            data_dict[key] = ''
        # If the data meets the requirments
        else:
            # Put the entry in to filtered ductionary
            filtered_dict[key] = num
            
        
    # Repeat of last filling section
    # For each value in filtered dictionary
    for value in filtered_dict.values():
        # For each index in value
        for index, i in enumerate(value):
            # If the index is 0
            if (index == 1):
                # If value is in m_list
                if (i in m_list):
                    # Set the value to the stored value with a * to signify the value was filled
                    value[index] = b_list[0] + '*'
                else:
                    # Make the current value the stored value for filling missing values
                    b_list[0] = value[index]
            
            # If the index is 0
            elif (index == 2):
                # If value is in m_list
                if (i in m_list):
                    # Set the value to the stored value with a * to signify the value was filled
                    value[index] = b_list[1] + '*'
                else:
                    # Make the current value the stored value for filling missing values
                    b_list[1] = value[index]

            # If the index is 0
            elif (index == 3):
                # If value is in m_list
                if (i in m_list):
                    # Set the value to the stored value with a * to signify the value was filled
                    value[index] = b_list[2] + '*'
                else:
                    # Make the current value the stored value for filling missing values
                    b_list[2] = value[index]
    
    # Return the filtered dictionary
    return filtered_dict



#####################################################################
#                      Start of main program
#####################################################################



# Gets file pointers by calling open_file function
file, daylight_file, daytime_file, current_runway_file, proposed_runway_file, test_file = open_file()

# Skip the header lines of the obervations file
for i in range(6):
    next(file,None)

# Create a dictionary from the observations file
data_dict = read_file(file)

# Fill and filter dictionary by calling fill_missing_values function
data_dict = fill_missing_values(data_dict)
    
# Skips the header lines of the daylight file
for i in range(9):
    next(daytime_file,None)    
    

daytime_dict = {}  # Empty dictionary
reader = csv.reader(daytime_file)  # Uses csv reader

# For each line in reader
for line in reader:
    # For each value in line
    for i in (line):
        # Variables
        start = 0
        end = 0
        i = i.split()  # Turns value into a list
        day = i[0]
        
        # Try filling the time for a fay to '' if the month does not contain that day
        try:
            # If day is the 29th or 30th
            if int(day) == 29 or int(day) == 30:
    
                i.insert(3,'')
                i.insert(4,'')
            
            if int(day) == 31:
                index = 3
                for j in range(3):
                    i.insert(index,'')
                    i.insert(index+1,'')
                    index += 4
                
                i.insert(17,'')
                i.insert(18,'')
                i.insert(21,'')
                i.insert(22,'')
            
            
            temp_list = []  # Creates empty list
            # For each index in i
            for index, num in enumerate(i):
                if index != 0:
                    # If the index is the second time
                    if index % 2 != 0:
                        # Create a tuple of the dawn/dusk time and append it to the list
                        temp_tup = (num, i[index+1])
                        temp_list.append(temp_tup)    
            
            # Fills the daylight dictionary with the day as the key and the list of dawn/dusk times as the value
            daytime_dict[int(i[0])] = []
            daytime_dict[int(i[0])] = temp_list
            
        # If error occurs, continue to next line
        except ValueError:
            pass
        

  

time = ''  # Empty string
del_list = []  # Empty list for deleting dictionary entries

time_list = [] # Empty list for time
# For each key in dictionary
for data_key in data_dict.keys():
    # Split the date within the key into a list 
    date = data_key[0].split('/')
    # Get the month from the split date
    month = int(date[0])
    # Get the day from the split date
    day = int(date[1])
    # Get the time from the key
    time = data_key[1]
    # Makes a copy of the time without the colon
    temp_time = time.replace(':','')
    # Makes a copy of the time as a list
    time = time.split(':')
    # Gets the hour from the time list
    hour = time[0]
    # Gets the minute from the time list
    minute = time[1]
    
    # Gets the sunrise time from daylight dictionary
    dawn = (daytime_dict[day][month-1][0])
    '''
    dawn_hour = dawn[:2]
    dawn_min = dawn[3:]
    '''
    # Gets the suset time from daylight dictionary
    dusk = (daytime_dict[day][month-1][1])
    '''
    dusk_hour = dusk[:2]
    dusk_min = dusk[3:]
    
    

    
    hour = int(hour)
    minute = int(minute)
    dawn_hour = int(dawn_hour)
    dawn_min = int(dawn_min)
    dusk_hour = int(dusk_hour)
    dusk_min = int(dusk_min)
    '''
    
    # If time is outside sunrise and sunset
    if int(dawn) >= int(temp_time) or int(dusk) <= int(temp_time):
        # Add dictionary key to list to be deleted
        del_list.append(data_key)
    
# For each key listed in del_list
for i in del_list:
    # Delete that key from dictionary
    del data_dict[i]

# For each key in dictionary
for key in data_dict:
    # Get rid of the colon in the time
    time = key[1]
    time = time.replace(':','')

# Prints header
print('JEWETT FLD AP (MI),54822,,Lat: 42.5658,Lon: -84.4331,Elev: 922 ft,,,', file = daylight_file)
print('Date,Hr,Min,Temp (F),Wind Spd (mph),Wind Direction (deg),Peak Wind Gust(mph),Low Cloud Ht (ft),Visibility (mi)', file = daylight_file)

insert = ''  # Empty string
# For key, valye pair in dictionary
for key, value in data_dict.items():
    # Formats the hour and minute of the time to not have leading zeros
    if len(key[1]) == 4:
        hour = key[1][0]
        minute = key[1][2:]
    else:
        hour = key[1][0:2]
        minute = key[1][3:]
        
    if minute[0] == '0':
        minute = minute[1:]        
    
    
    # Two data entries were out of order so this if/elif statment switches them around
    if key[1] == '18:35' and key[0] == '06/25/21':
        temp_tup = (key[0], hour, minute ,value[0], value[1], value[2], value[3], value[4], value[5])
        temp_list = list(temp_tup)
        data_str = ','.join(temp_list)
        data_str = data_str + ','
        insert = data_str[:]
    
    elif key[1] == '18:32' and key[0] == '06/25/21':
        temp_tup = (key[0], hour, minute ,value[0], value[1], value[2], value[3], value[4], value[5])
        temp_list = list(temp_tup)
        data_str = ','.join(temp_list)
        data_str = data_str + ','
        print(data_str,file= daylight_file)
        print(insert,file= daylight_file)

    
    
    else:
        # Formats the data entry and prints it in the csv file
        temp_tup = (key[0], hour, minute ,value[0], value[1], value[2], value[3], value[4], value[5])
        temp_list = list(temp_tup)
        data_str = ','.join(temp_list)
        data_str = data_str + ','
        print(data_str,file= daylight_file)
        
    
    # Add to count that tracks the number of lines in csv file
    count += 1  
  

#count = count 
# Prints count to console
print(f'Total feasible data points: {count}')





###############################################################################
#
#                       Part 2
#
###############################################################################


# inintalizes counts for data points
current_count = 0
proposed_count = 0

# Creates empty dictionaries for data points
current_dict = {}
proposed_dict = {}

# Creates empty sets for data points
current_set = set()
proposed_set = set()

# Prints header
print('JEWETT FLD AP (MI),54822,,Lat: 42.5658,Lon: -84.4331,Elev: 922 ft,,,', file = current_runway_file)
print('Date,Hr,Min,Temp (F),Wind Spd (mph),Wind Direction (deg),Peak Wind Gust(mph),Low Cloud Ht (ft),Visibility (mi)', file = current_runway_file)

# Prints header
print('JEWETT FLD AP (MI),54822,,Lat: 42.5658,Lon: -84.4331,Elev: 922 ft,,,', file = proposed_runway_file)
print('Date,Hr,Min,Temp (F),Wind Spd (mph),Wind Direction (deg),Peak Wind Gust(mph),Low Cloud Ht (ft),Visibility (mi)', file = proposed_runway_file)

# For each key/value pair in data dictionary
for key, value in data_dict.items():
    # Define speed and angle of wind, and peack wind gust 
    wind_speed = int(value[1].strip('*')) / 1.15  # converts speed from mph to knots
    wind_angle = int(value[2].strip('*'))
    wind_gusts = int(value[3].strip('*')) / 1.15 # converts peak gust from mph to knots
    
    # Find test angle for current runway
    if 10 <= wind_angle <= 190:
        test_angle = abs(100 - wind_angle)
    
    elif 190 < wind_angle <= 360 or 0 <= wind_angle < 10:
        test_angle = abs(280 - wind_angle)
    # Converts angle to radians
    test_angle = math.radians(test_angle)
    
    
    # Find test angle for proposed runway
    if 100 <= wind_angle <= 280:
        proposed_test_angle = abs(190 - wind_angle)
    elif 280 < wind_angle <= 360 or 0 <= wind_angle < 100:
        proposed_test_angle = abs(10 - wind_angle)
    # Converts angle to radians
    proposed_test_angle = math.radians(proposed_test_angle)
    
    # Gets the crosswind componets for the current and proposed runways
    proposed_crosswind = abs(wind_speed * math.sin(proposed_test_angle))
    current_crosswind = abs(wind_speed * math.sin(test_angle))
        
    # wind speed is greater than 20
    if wind_gusts > 20:
        # Ignore data point
        pass
    # If wind is above 5 knots
    elif wind_speed > 5:
        # Get the cross winds
        # Determain if current runway from angle 1 is safe
        if ((5 <= current_crosswind <= 8) and wind_gusts <= 12):
            
            # Add the data point to dictionary and set
            current_set.add(key)
            current_dict[key] = value

            
        elif (8 <= current_crosswind <= 12) and wind_gusts <= 15:
            
            # Add the data point to dictionary and set
            current_set.add(key)
            current_dict[key] = value

            
        elif (12 <= current_crosswind < 15) and wind_gusts <= 20:
            
            # Add the data point to dictionary and set
            current_set.add(key)
            current_dict[key] = value


        # If the proposed runway's crosswind is valid
        if (5 <= proposed_crosswind <= 8) and wind_gusts <= 12:
            
            # Add the data point to dictionary and set
            proposed_set.add(key)
            proposed_dict[key] = value
    
        elif (8 <= proposed_crosswind <= 12) and wind_gusts <= 15:
            
            # Add the data point to dictionary and set
            proposed_set.add(key)
            proposed_dict[key] = value
            
        elif (12 <= proposed_crosswind < 15) and wind_gusts <= 20:
            
            # Add the data point to dictionary and set
            proposed_set.add(key)
            proposed_dict[key] = value
            
            
            
            
            
            
            
    
    # If wind is 5 knots or below
    else:
        # Add the data point to both dictionaries and sets
        current_set.add(key)
        proposed_set.add(key)
        current_dict[key] = value
        proposed_dict[key] = value
        
# Intalizes a count for the combined data points
combined_count = 0

# Uses set intersection to get all the similar data points in both the current and proposed runways' sets
similar_set = current_set.intersection(proposed_set)

# For each data point in the similar set
for i in similar_set:
    # Add to the combined count
    combined_count += 1

# For each data point in the current runway's dictionary
for key,value in current_dict.items():
    
    # Formats the hour and minute of the time to not have leading zeros
    if len(key[1]) == 4:
        hour = key[1][0]
        minute = key[1][2:]
    else:
        hour = key[1][0:2]
        minute = key[1][3:]
        
    if minute[0] == '0':
        minute = minute[1:]        
    # Make a tuple of the data for display
    temp_tup = (key[0], hour, minute ,value[0], value[1], value[2], value[3], value[4], value[5])
    temp_list = list(temp_tup)
    data_str = ','.join(temp_list)
    # Adds either to the end of the display string if the data point in is both sets
    if key in similar_set:
        data_str = data_str + ',either'
    else:
        data_str = data_str + ','
    # Display the data point in the corresponding runway file
    print(data_str,file= current_runway_file)
        
    # Increase the current runway data point counter by 1
    current_count += 1
    
# For each data point in the proposed runway dictionary
for key,value in proposed_dict.items():
    # Formats the hour and minute of the time to not have leading zeros
    if len(key[1]) == 4:
        hour = key[1][0]
        minute = key[1][2:]
    else:
        hour = key[1][0:2]
        minute = key[1][3:]
        
    if minute[0] == '0':
        minute = minute[1:]        
    
    # Make a tuple of all the data for display
    temp_tup = (key[0], hour, minute ,value[0], value[1], value[2], value[3], value[4], value[5])
    temp_list = list(temp_tup)
    data_str = ','.join(temp_list)
    # Adds "either" to the end of the string if the data point is in either set
    if key in similar_set:
        data_str = data_str + ',either'
    else:
        data_str = data_str + ','
    # Display the data point in the corresponding runway file
    print(data_str,file= proposed_runway_file)
    # Increase the proposed data point counter by 1
    proposed_count += 1



# Display counts to console to confirm program runs correctly
print('Data points that are safe for the current runway: {}'.format(current_count))
print('Data points that are safe for the proposed runway: {}'.format(proposed_count))
print('Data points that are safe for both runways: {}'.format(combined_count))



        
    
# Closes all files
file.close()
daylight_file.close()
daytime_file.close()
current_runway_file.close()
proposed_runway_file.close()
test_file.close()