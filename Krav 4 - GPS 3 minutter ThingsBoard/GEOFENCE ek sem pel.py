import math
# forklaring https://study.com/skill/learn/determining-if-a-point-lies-inside-outside-or-on-a-circle-given-the-center-point-a-radius-explanation.html

# koordinat 1
lat_1 = 55.694331
lon_1 = 12.548807

# koordinat 2
lat_2 = 55.693950
lon_2 = 12.548942

R = 0.0003 # radius (3 meter) max GPS precision

def is_in_fence(lat_1, lon_1, lat_2, lon_2): 
        a = lat_1 - lat_2
        b = lon_1 - lon_2
        # absolutte tal for at håndtere -graderne
        #(syd for ekvator og den vestlige halvkugle)
        a = abs(a) # giver absolutte tal (uden fortegn +-)
        b = abs(b) # giver absolutte tal (uden fortegn +-)
        # udregn afstanden fra punkt
        c = math.sqrt((b**2) + (a**2))
        print(c)   
        if c >= R:
            print("Outside fence")
            return False
        if c < R:
            print("Inside fence")
            return True

is_in_fence(lat_1, lon_1, lat_2, lon_2)