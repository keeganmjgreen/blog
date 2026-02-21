# IoT Integration of a Hydroponic Farm

```{figure} img/cover.jpg
:width: 100%


What's that behind the hydroponic farm? Another farm, of course.
```

After helping set up a small hydroponic farm, I recognized a need to be able to remotely monitor it during a later planned trip, and that this might be achieved by integrating it with the Internet of Things (IoT). I developed requirements subject to the constraints of what was possible, what was needed, and how I needed to achieve it for the additional purposes of learning and further developing my electrical engineering skills. I finished the first phase of the project in time to remotely monitor and control the farm across Canada.

The hydroponic farm consists of a long length of piping that functions as a continuous planter under grow lights. Aerated, nutrient-rich water is circulated through this piping from a reservoir, which is maintained at a specific temperature.

If the water pump and aerator are the heart and lungs of the farm, then the IoT integration of the farm serve as its eyes and brain. With IoT integration, the farm becomes one "device" connected to the internet.

```{figure} img/diagram.png
:width: 100%


The IoT integration allows for automatic data collection, cloud storage, and potential integration with available weather data. The IoT dashboard and Python-based interface enable remote monitoring, control, diagnostics, and programming.
```

The farm's IoT integration enables the farm conditions to be remotely monitored (using its IoT dashboard) and the farm inputs to be remotely controlled (using its Python interface). The *farm conditions* include the solute concentration of its water, the air temperature and relative humidity, the water temperature, and the illuminance at the upper and lower levels of plants. The *farm inputs* are the controlled lighting, water heating, water aeration, and water pumping.

```{figure} img/brain_in_a_box_integrated.jpg
:width: 100%


This is the box safekeeping&mdash;among other components&mdash;a WiFi-enabled single-board computer, a microcontroller, a small display for system checks, and an air temperature / relative humidity sensor. In addition, it holds a relay module, which handles the controlled inputs to the farm.
```

## Walkthrough of the IoT-Integrated Farm

```{figure} img/lux_sensor_w_camera_in_background.jpg
:width: 100%

One of two ambient light sensors, which measure illuminance in units of lux.
```

Virtually all smartphones have calibrated ambient light sensors. The one shown is positioned at plant height at the center of the farm's upper level underneath the farm lights, whereas the second one resides on the lower level. The sensors' hollow, transparent domes refract light onto their visible photosensitive chips. The cable assemblies between the ambient light sensors and the microcontroller board are long enough for the sensors to be repositioned to the farthest corners of the farm, such that the illuminance may be mapped across the upper and lower levels of plants.

```{figure} img/camera_w_lux_sensor_in_foreground.jpg
:width: 100%

The camera, which is trained on the farm's upper level.
```

This arrangement offers better lighting both for the plants and for the purposes of image capture, particularly to estimate plant growth using computer vision. The camera is also used for automatic detection of any problems or other occurrences, such as something getting bumped or falling over.

The blurry, horizontal black bars appearing in the image&mdash;and in those captured by the camera shown, for that matter&mdash;are due to the camera rapidly scanning its individual photosensors row-by-row, all while the lighting smoothly pulses on and off as a consequence of the lighting technology. This includes both the farm's fluorescent lights and the room's LED-array light fixture while they are turned on. If the lighting pulsed at a higher frequency, the black bars would be more narrow, whereas if the lighting pulsed at a sufficiently low frequency, the black bars would occupy entire images (ceasing to appear as bars at all).

```{figure} img/top_level_of_plants.jpg
:width: 100%

An approximation of what the camera sees.
```

From the true viewpoint of the camera, the middle two channels of the farm's lower level are more visible. Note that the lower level does, in fact, have four channels.

```{figure} img/two_levels_of_channels.jpg
:width: 100%

Aerated, nutrient-rich water is supplied to the channels that make up the upper level of the farm, followed by those making up the lower level. The channels carry water to be absorbed by the growth media of individual plants.
```

```{figure} img/water_tank.jpg
:width: 100%

The 40-liter water reservoir.
```

Water is supplied by the reservoir through the clear plastic tubing, and returning water drains back into the reservoir through its lid's opening. A water pump is submerged and mounted on the bottom of the reservoir, with its intake in front of two air stones to maximize their effect. The air stones are small, porous rock cylinders in which air supply lines are embedded. The air stones diffuse air into the water at their porous surfaces, much like how gas diffusion layers ("GDLs") diffuse the reactants in a fuel cell. Next in line is the water heater, which is also mounted on the bottom of the reservoir. It has an integrated thermostat, with a thermometer to provide temperature feedback to what is most likely a bang-bang control system for the heating element: if the temperature has been allowed to fall below the setpoint (with a threshold), it turns on; if the temperature has exceeded the setpoint (with a threshold), it turns off. The setpoint is adjustable using a built-in dial, which was set to its maximum to override the internal thermostat&mdash;within its upper limit&mdash;using IoT-integrated temperature control, to which temperature feedback is provided via temperature probe.

As is shown, the power cables of the pump and heater, the blue air hoses from the aerator, and the wires for the total dissolved solids (TDS) and temperature probes are all routed through the lid's opening.

```{figure} img/water_aerator_w_meters.jpg
:width: 100%

The water aerator (alongside manual pH and TDS meters), with its blue air supply lines leading to the adjacent water reservoir.
```

The dial of the aerator is set to its maximum knowing that the level of aeration may be adjusted using slow pulse-width modulation (PWM). The aerator is plugged into the system relay module&mdash;along with the pump, heater, and farm lights, for that matter.

```{figure} img/brain_in_a_box.jpg
:width: 100%

From a partially complete stage of the project: The box for holding the single-board computer, the microcontroller, the small display, necessary wiring, and the sensors and actuators.
```

The actuators are the electromechanical relays in the relay module at the top, which is finally mounted on the box. The relay module board is itself mounted in its own plastic case. The relays inside control the four black AC sockets for the light, water heater, water aerator, and water pump. When their corresponding relays are actuated, these controlled farm inputs draw power from the shared 10-A AC power cable shown. As such, the relay module assembly also functions as a grounded, four-outlet power strip, and the wiring safely has twice the current rating required per outlet. Electrical connections are insulated using waterproof butt connectors.

```{figure} img/relay_module_integrated.jpg
:width: 100%

The relay module assembly mounted on the box.
```

The black, white, and green wires correspond to hot, neutral, and ground AC power terminals, respectively.

```{figure} img/main_board.jpg
:width: 100%

The Arduino Uno microcontroller board and the LCD module contained within the box.
```

The LCD screen is used for system checks; it is on by default but is not displaying anything here.

```{figure} img/brain_in_a_box_closeup.jpg
:width: 100%

Inside the box.
```

Shown above is the breadboard on which components are mounted, such as the air temperature and relative humidity sensor, and where relatively compact electrical connections are made, such as those with the ambient light sensors (top). All components share the same DC power, be it through USB or the 5-V and ground rails of the Arduino Uno and Raspberry Pi. DC power is supplied by an AC adapter, but altogether the breadboard has one of two DC connectors (with 5-V and 3.3-V voltage regulators) that is designed for alternate use.

```{figure} img/relay_module_1.jpg
:width: 100%

The relay module by itself, and its wiring and AC sockets.
```

```{figure} img/relay_module_2.jpg
:width: 100%

The other side of the relay module, showing its built-in PCB.
```

## Connection Schematic of the IoT Integration

Toward the left side of the schematic below are the peripheral sensors for monitoring the farm conditions (total dissolved solids `TDS_water`, temperatures `T_water` and `T_air`, relative humidity `RH_air`, upper illuminance `Ev_upper` and lower illuminance `Ev_lower`). On the bottom right are the controls for the farm inputs. At the center is the microcontroller, LCD module, and single-board computer, all on the back of the breadboard on which most of the outlying electrical connections are made.

```{figure} img/Connection Schematic.png
:width: 100%

Connection schematic.
```

Components such as PCBs, from the single-board computer to those of the ambient light sensors, and all other sensors such as the water probes, are indicated by rectangles in bold.

Power supply lines and analog or digital signal-carrying lines between components are indicated by single lines. Buses (USB and I²C) and other cables between components are indicated by multiple lines running in parallel.

5-V voltage sources (to component inputs labeled `VCC` and `VDD`) and grounds other than that of the neutral&ndash;hot&ndash;ground AC power supply naturally correspond to the `5V` and `GND` pins of the microcontroller. The adjacent Vin pin should not be used in our case where 5 V is supplied by the single-board computer, even though the microcontroller runs at 5 V, because its onboard voltage regulator (tied to `Vin`) needs at least 6&ndash;7 V to operate.

Connections are depicted approximately to match where they are physically made with components.

Schematic elements drawn in light gray were either planned but not fully implemented (such as standalone relays that are built into the relay module) or implemented but unused (such as the standalone relay driver).

The USB connection between the single-board computer and microcontroller eliminates the need to use the UART and microcontroller reset connections, along with the rudimentary logic-level shifter for the former, at the cost of additional wiring. The USB connection also makes the `5V` and `GND` connections between the computer and microcontroller unnecessary. However, unlike the UART connections, there is no need to disconnect them.

## Overview of the IoT Integration

The farm conditions (total dissolved solids `TDS_water`, temperatures `T_water` and `T_air`, relative humidity `RH_air`, upper illuminance `Ev_upper` and lower illuminance `Ev_lower`) are all made to be constantly available to the microcontroller. Recall that the water temperature sensor and ambient light sensors provide direct feedback for the water heater and farm lights. The microcontroller and single-board computer communicate via UART, emulated by USB in our case. The microcontroller regularly transmits the farm conditions&mdash;along with the commanded farm inputs&mdash;to the computer within a fraction of a second upon actuating those inputs; the microcontroller is programmed to wait until receiving the frequent farm input commands issued by the computer, before actuating those inputs and reading any of the sensor data. This synchronizes the microcontroller and computer to a common update interval that has demonstrated to be long enough for the computer to reliably run its computer vision tasks&mdash;the relatively computationally expensive bottleneck&mdash;before the deadline of the next update.

Meanwhile, the commands received by the microcontroller serve to function as a heartbeat from the computer. This is a safety feature. If, for whatever reason, the commands fail or are delayed, the updating of the farm inputs will time out and they will be turned off until commands resume. Because the computer is not directly in charge of any actuators, there is no need for it to be programmed to constantly check the status of an overseeing device; it is the overseeing device.

```{figure} img/System Level Block Diagram.png
:width: 100%

System level block diagram.
```

The microcontroller runs, waits to receive commands, and transmits as soon as it receives power. The program was debugged and further tested using a serial monitor on a computer (and `minicom` on the single-board computer).

The single-board computer runs a Python module, which performs many ongoing tasks:

- Transmits commands for the controlled farm inputs.

- Receives farm data (which includes both the farm conditions and the current state of the controlled farm inputs), parses it, places it in a data table, and writes it to a data log file that is read into the IoT dashboard via [InfluxDB](https://www.influxdata.com/)&mdash;a time series database. Entries in both the data table and log are timestamped. An alternative for the data log is using the InfluxDB Python API.

- Checks local sunrise and sunset times (at a given latitude and longitude coordinates) and schedules the farm lights to match these or specified artificial sun times. This eliminates the need for a bulky and noisy electromechanical timer.

- Implements control for the water heater based on the current temperature and a specified setpoint.

- Runs the duty cycles of the water aerator and pump to regulate the level of aeration and the rate at which dissolved nutrients are provided to the plants. This also eliminates the need for an electromechanical timer for the water aerator in particular.

- Captures images from the camera, saves them at a specified interval (for example, every minute on the minute), and runs computer vision tasks to estimate a *scene change detection metric* and a *plant growth metric*. These are also recorded in the previously mentioned data table and log file.

The above itemized tasks are performed in the background by dedicated Python functions, which run in parallel as the targets of multithreading (more accurately, just "threading").

Because the pins of the single-board computer were only used for serial communication with and providing power to the microcontroller&mdash;functions which are redundant with a USB connection thereto&mdash;the Python module was debugged and tested on a full computer taking the place of the single-board computer.

### Metrics

The scene change detection metric ("SCDM") is used for the automatic detection of any visible problems or other occurrences. It is a measure of image-to-image differences and compares each image to the previous one taken. Relatively fast events cause it to spike temporarily. These include the camera being moved slightly, the farm lights being toggled, the room lights being toggled, someone moving within the frame, or something getting knocked over. The SCDM is practically unreactive to slow events, such as sunrise and sunset, the visible rise and fall of the water level in the channels with pump duty cycling, and the plants growing, wilting, or perking up.

Meanwhile, the plant growth metric ("PGM") is intended to reflect the amount of visible plant material. An established method for doing this is finding the visible area of leaves. (This method is used, for instance, by the Living Lab at Vancouver's Simon Fraser University.) However, between the blurry, horizontal black bars mentioned previously, the low camera resolution, and the particularly visible image noise, the borders of the leaves cannot be discerned here for this purpose. An alternative is measuring the amount of green in the images, which are represented by points in three-dimensional RGB color space. This may be done using multiple methods.

One such method is using a mathematical function developed by trial-and-error that maps a point in the color space to a PGM value ideally between $0$ and $1$. The more rigorous method is calculating the Euclidean distance from the color point to $\{r, g, b\} = \{255, 0, 255\}$. To bind the PGM to the range $[0, 1]$, this distance is then normalized with respect to the Euclidean distance measured along the diagonal spanning opposite corners of the cubic color space. (At this point, see the table that follows.) It is important to note that the color point $\{255, 0, 255\}$ is pure magenta.

Why magenta? Because it is the polar opposite of green in the color space. This is why commercial and scientific hydroponic and similar farms often have magenta grow lights (and presumably not just magenta-tinted ones); energy is not wasted on frequencies of the electromagnetic spectrum that are not put toward synthesizing fructose sugar. Plants are green because chlorophyll absorbs every color for this purpose&mdash;at least those in the visible spectrum&mdash;except for green, which is reflected back into our eyes. When green leaves are seen under pure magenta lights, they should appear black&mdash;for pure green materials, they may as well be in darkness. Last time I checked, however, plants are not made of [vantablack](https://en.wikipedia.org/wiki/Vantablack#/media/File:Vantablack_01.JPG). A leaf is merely dim under magenta lights because even if the latter were pure magenta and the only lighting present, the former is never pure green (and not even close in our overall lighting-camera setup).

This is one reason why the aforementioned methods of computing a PGM are not theoretically accurate&mdash;at least not entirely so&mdash;even for it being a dimensionless metric. For instance, the non-magenta-based formulae in the table that follows achieves an imperfect PGM of $0.9$ for a dark shade of pure green. Another reason for the lack of theoretical accuracy is the opposite: anything making up the scene that surrounds the foliage has a green color component that cannot be ignored and might make it register as being green overall. For instance, although the magenta-based formula (which was implemented and in use) achieves a $0.9/1$ PGM for dark green, it returns an unfortunately large value of $0.8$ for black just for also being distant from magenta.

In any case, a PGM value for a shade of green foliage that is typically seen by the camera ought to be re-scaled up to $1$ and a PGM value for, say, black ought to be re-scaled down to $0$ in the magenta-based formula.

```{figure} img/PGM_Formula_Tests.png
:width: 100%

Comparison of plant growth metric formulae.
```

## The Python-Based Command-Line Interface

```{figure} img/Python_API_Screenshot_Framed.png
:width: 100%

Python-based command-line interface.
```

The command-line interface for the farm IoT integration uses the Python language shell running on the single-board computer, which is accessed through SSH from a computer on the same WiFi network (wireless LAN).

`iot_farm` is the Python module from which objects such as `water_heater` and `data_frame` are imported for use. Here, `water_heater` is an instance of the `ControlledFarmInput` class defined in the module. 10 seconds is the update interval mentioned above.

The user can evaluate Python expressions, set the states of the farm inputs, check the *commanded* states of the farm inputs, and query and work with the farm data. Manually set states of the farm inputs are enacted until their dedicated Python functions toggle them again&mdash;except for the water temperature control function, the only one that is not time-based.

## The IoT Dashboard

The Python module writes the farm data to a log file, which a piece of software called [Telegraf](https://www.influxdata.com/time-series-platform/telegraf/) reads to feed the data into an InfluxDB instance &mdash;a distributed time series database &mdash;in accordance with a specified configuration file. A locally hosted [Grafana dashboard](https://grafana.com/grafana/) pulls the data, for the purpose of visualization in an interactive web app.

```{figure} img/SBC Level Block Diagram.png
:width: 100%

IoT data flow.
```

This is the startup sequence: The Python module, the InfluxDB service, the Telegraf process, the Telegraf service, and, finally, the Grafana service. These run concurrently.

The Grafana dashboard, as seen on another device on the network, is shown below for a relatively short test run (~12 hours total) in which the sensors and actuators are not connected within the farm and the camera is disconnected.

```{figure} img/Hydroponic Farm IoT Integration - Grafana - Framed.png
:width: 100%

Grafana dashboard.
```

## Another Design Iteration Using a WiFi-Enabled ESP32 Microcontroller

```{figure} img/iteration_2/overview.jpg
:width: 100%

Overview.
```

```{figure} img/iteration_2/interconnections.jpg
:width: 100%

Interconnections.
```

```{figure} img/iteration_2/arduino_iot_cloud_dashboard.webp
:width: 100%

Arduino Cloud IoT dashboard.
```
