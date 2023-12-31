import math

file = open("input.txt", "r")
#file = open("input_test.txt", "r")
#file = open("input_test_2.txt", "r")
data_raw = file.readlines()
file.close()
data = []
for line in data_raw:
    data.append(line.strip())

modules = {"button": {"type": "button", "destinations": ["broadcaster"]}}
conjunction_modules = []
for line in data:
    if line.startswith("broadcaster"):
        modules["broadcaster"] = {"type": "broadcaster", "destinations": line.strip().split(" -> ")[1].split(", ")}
    elif line.startswith("%"):
        module, destinations = line.strip()[1:].split(" -> ")
        modules[module] = {"type": "flip-flop", "state": "off", "destinations": destinations.split(", ")}
    elif line.startswith("&"):
        module, destinations = line.strip()[1:].split(" -> ")
        modules[module] = {"type": "conjunction", "destinations": destinations.split(", ")}
        conjunction_modules.append(module)

for conjunction_module in conjunction_modules:
    input_modules = {}
    for module in modules.keys():
        if conjunction_module in modules[module]["destinations"]:
            input_modules[module] = "low"
    modules[conjunction_module]["inputs"] = input_modules

#print(modules)

number_button_presses = 100000
high_pulse_count = 0
low_pulse_count = 0

"""
part 2:

When does rx receive a low pulse? rx only occurs in:

  &rs -> rx

and so conjunction module rs needs all input modules to have sent high pulses.

rs has four modules as inputs to it:

  bt, dl, fr, rv

which all need to be high.
"""
rs_inputs = {}
for input_module in modules["rs"]["inputs"]:
    # store a list of button presses needed before an input to rs was last
    # sending a high pulse
    rs_inputs[input_module] = set()

for button_press in range(1, number_button_presses+1):
    pulses = [("button", "low", "broadcaster")] # modules and what they are sending
    low_pulse_count += 1
    while pulses:
        module_out, pulse, module_in = pulses.pop(0)
        #print(f"{module_out} -{pulse}-> {module_in}")
        if module_in in modules.keys():
            if modules[module_in]["type"] == "broadcaster":
                # send the same pulse to the destinations
                for destination in modules[module_in]["destinations"]:
                    pulses.append((module_in, pulse, destination))
                    if pulse == "high":
                        high_pulse_count += 1
                    else:
                        low_pulse_count += 1
            elif modules[module_in]["type"] == "flip-flop":
                # ignores high; flips state on low and emits high when turned on, low
                # when turned off
                if pulse == "low":
                    if modules[module_in]["state"] == "off":
                        modules[module_in]["state"] = "on"
                        for destination in modules[module_in]["destinations"]:
                            pulses.append((module_in, "high", destination))
                            high_pulse_count += 1
                    elif modules[module_in]["state"] == "on":
                        modules[module_in]["state"] = "off"
                        for destination in modules[module_in]["destinations"]:
                            pulses.append((module_in, "low", destination))
                            low_pulse_count += 1
            elif modules[module_in]["type"] == "conjunction":
                # update the received pulse from the specific module
                modules[module_in]["inputs"][module_out] = pulse
                #### part 2 stuff ####
                if module_in == "rs" and "high" in modules[module_in]["inputs"].values():
                    for rs_input in rs_inputs.keys():
                        if modules[module_in]["inputs"][rs_input] == "high":
                            rs_inputs[rs_input].add(button_press)
                ######################
                # if all high, send low; else send high
                if "low" in modules[module_in]["inputs"].values(): # not all high
                    for destination in modules[module_in]["destinations"]:
                        pulses.append((module_in, "high", destination))
                        high_pulse_count += 1
                else: # all high
                    for destination in modules[module_in]["destinations"]:
                        pulses.append((module_in, "low", destination))
                        low_pulse_count += 1
    
    # part 1
    if button_press == 1000:
        #print("high_pulse_count", high_pulse_count)
        #print("low_pulse_count", low_pulse_count)
        print("part 1:", high_pulse_count*low_pulse_count)
    
    # part 2
    if min([len(x) for x in rs_inputs.values()]) > 1: # we've got at least two readings for each
        # check they're all increasing regularly i.e. cycles of "high" are
        # repeating consistently
        all_lcms_of_each_other = True
        min_button_press_nums = []
        for button_presses in rs_inputs.values():
            min_button_press_num = min(button_presses)
            if max([x % min_button_press_num for x in button_presses]) > 0:
                all_lcms_of_each_other = False
            else:
                min_button_press_nums.append(min_button_press_num)
        if all_lcms_of_each_other:
            print("part 2:", math.lcm(*min_button_press_nums))
            break

"""
bt: is high regularly, every 3739 button presses
dl: is high regularly, every 4001 button presses
fr: is high regularly, every 3943 button presses
rv: is high regularly, every 3821 button presses
"""