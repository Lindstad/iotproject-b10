import batteri

batteri = batteri.Batteri()

print("Adc-Value: ", batteri.getADCValue())

print("Batterispænding:",batteri.Battery_voltage())

print("Batteriprocent:",batteri.Battery_procent())
