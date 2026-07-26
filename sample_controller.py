from idf_parser import load_idf,save_idf,replace_cooling_setpoint

idf=load_idf("building.idf")
idf=replace_cooling_setpoint(idf,"24.0","23.0")
save_idf("building_modified.idf",idf)
print("Cooling setpoint updated.")
