from pymodbus.client.sync import ModbusTcpClient

client = ModbusTcpClient('10.0.0.57', port=9093)
client.connect()
print(client)
rr = client.read_holding_registers(0, 92, unit=1)
if rr is None:
	client.close()
	print("Failed to connect")
	exit(1)

print("Connected")

voltageScalingFactor = (float(rr.registers[0]) + (float(rr.registers[1]) / 100))
amperageScalingFactor = (float(rr.registers[2]) + (float(rr.registers[3]) / 100))

# Voltage Related Statistics
batteryVoltage = float(rr.registers[24]) * voltageScalingFactor * 2**(-15)
print("Battery Voltage: %.2f" % batteryVoltage)
batterySenseVoltage = float(rr.registers[26]) * voltageScalingFactor * 2**(-15)
print("Battery Sense Voltage: %.2f" % batterySenseVoltage)
batteryVoltageSlow = float(rr.registers[38]) * voltageScalingFactor * 2**(-15)
print("Battery Voltage (Slow): %.2f" % batteryVoltageSlow)
batteryDailyMinimumVoltage = float(rr.registers[64]) * voltageScalingFactor * 2**(-15)
print("Battery Daily Minimum Voltage: %.2f" % batteryDailyMinimumVoltage)
batteryDailyMaximumVoltage = float(rr.registers[65]) * voltageScalingFactor * 2**(-15)
print("Battery Daily Maximum Voltage: %.2f" % batteryDailyMaximumVoltage)
targetRegulationVoltage = float(rr.registers[51]) * voltageScalingFactor * 2**(-15)
print("Target Regulation Voltage: %.2f" % targetRegulationVoltage)
arrayVoltage = float(rr.registers[27]) * voltageScalingFactor * 2**(-15)
print("Array Voltage: %.2f" % arrayVoltage)

# Current Related Statistics
arrayChargeCurrent = float(rr.registers[29]) * amperageScalingFactor * 2**(-15)
print("Array Charge Current: %.2f" % arrayChargeCurrent)
batteryChargeCurrent = float(rr.registers[28]) * amperageScalingFactor * 2**(-15)
print("Battery Charge Current: %.2f" % batteryChargeCurrent)
batteryChargeCurrentSlow = float(rr.registers[39]) * amperageScalingFactor * 2**(-15)
print("Battery Charge Current (slow): %.2f" % batteryChargeCurrentSlow)

# Wattage Related Statistics
inputPower = float(rr.registers[59]) * voltageScalingFactor * amperageScalingFactor * 2**(-17)
print("Array Input Power: %.2f" % inputPower)
outputPower = float(rr.registers[58]) * voltageScalingFactor * amperageScalingFactor * 2**(-17)
print("Controller Output Power: %.2f" % outputPower)

# Temperature Statistics
heatsinkTemperature = rr.registers[35]
print("Heatsink Temperature: %(c)d %(f).1f" % {"c": heatsinkTemperature, "f": 9.0/5.0 * heatsinkTemperature + 32})
batteryTemperature = rr.registers[36]
print("Battery Temperature: %(c)d %(f).1f" % {"c": batteryTemperature, "f": 9.0/5.0 * batteryTemperature + 32})

# Misc Statistics
chargeStates = ["START", "NIGHT_CHECK", "DISCONNECT", "NIGHT", "FAULT", "MPPT", "ABSORPTION", "FLOAT", "EQUALIZE",
				"SLAVE"]
chargeState = rr.registers[50]
print("Charge State %(chargeState)d - %(stateName)s" % {"chargeState": chargeState, "stateName": chargeStates[chargeState]})
secondsInAbsorptionDaily = rr.registers[77]
print("Seconds in Absorption: %(seconds)d (%(minutes).1f minutes)" % {"seconds": secondsInAbsorptionDaily, "minutes": float(secondsInAbsorptionDaily) / 60})
secondsInFloatDaily = rr.registers[79]
print("Seconds in Float: %d" % secondsInFloatDaily)
secondsInEqualizationDaily = rr.registers[78]
print("Seconds in Equalization: %d" % secondsInEqualizationDaily)



client.close()
