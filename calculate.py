import math
import csv

filename = 'bulletData.csv'

def get_range(vel, ang):
    return (math.pow(vel, 2) * math.sin(2 * math.radians(ang))) / 9.81 

def get_vel(distance, ang):
    return math.sqrt((distance * 9.81) / math.sin(2 * math.radians(ang)))

def get_max_height(vel, ang):
    return (math.pow(vel, 2) * math.pow(math.sin(math.radians(ang)), 2)) / (9.81 * 2) 

def get_saved_vel(filename):
    data = {}
    with open(filename) as csvfile:
        reader = csv.DictReader(csvfile, delimiter=',')
        for row in reader:
            data[row['weight']] = row['vel']
    return data

def get_saved_data(filename):
    data = {}
    with open(filename) as csvfile:
        reader = csv.DictReader(csvfile, delimiter=',')
        for row in reader:
            data[int(row['weight'])] = [float(row['vel']),float(row['times'])]
        
    return data

def clear_data(filename):
    fieldnames = ['weight', 'vel', 'times']
    with open(filename, 'w') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()  

def write_data(filename, data):
    fieldnames = ['weight', 'vel', 'times']
    with open(filename, 'w') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()   
        for row in data:
            writer.writerow({'weight' : row, 'vel' : data[row][0], 'times': data[row][1]})

    
def train(filename):
    weight = int(raw_input('Enter amount of bbs: '))
    angle = float(raw_input('Enter angle: '))
    distance = float(raw_input('Enter Distance flown: '))
    vel = get_vel(float(distance), float(angle))
    filedata = get_saved_data(filename)
    if weight in filedata:
        oldvel = filedata[weight][0]
        times = filedata[weight][1]
        newvel = (oldvel * times + float(vel)) / (times + 1)
        filedata[weight] = [newvel, times + 1]
    else:
        filedata[weight] = [vel, 1]
    write_data(filename, filedata)

def get_bullet_angle(distance, filename):
    data = get_saved_vel(filename)
    closest = None
    for bullet in data:
        for ang in range(30, 80):
            angle = float(ang)
            vel = float(data[bullet])
            if closest == None:
                closest = [bullet, angle, get_range(vel,angle)]
            elif abs(get_range(vel, angle) - distance) < abs(closest[2] - distance):
                closest = [bullet, angle, get_range(vel, angle)]
    return closest

def menu(filename):
    while True:
        print ("1. Train Data")
        print ("2. Test Data")
        print ("3. Exit")
        userinput = int(raw_input('Make selection: '))
        if userinput == 1:
            while True:
                print ("1. Clear Data")
                print ("2. New Data")
                print ("3. Read Data")        
                print ("4. Back")        
                userinput = int(raw_input('Make selection: '))
                if userinput == 1:
                    clear_data(filename)
                elif userinput == 2:
                    train(filename)
                elif userinput == 3:
                    print (get_saved_data(filename))
                else:
                    break
        elif userinput == 2:
            while True:
                userinput = float(raw_input('How far to shoot?(0 to exit): '))
                suggestion = get_bullet_angle(userinput, filename)
                if userinput == 0.0:
                    break
                else:
                    print ('Shoot a bullet with %s bbs at angle %s to go a distance of %s' % (suggestion[0], suggestion[1], suggestion[2]))
        else:
            exit(0)
print(get_bullet_angle(6, 'bulletData.csv'))
menu(filename)
