fdg

TECHNICAL MANUAL

# **CEM500**



![image_19](pdf_images\page1_19.jpeg)


HORIBA   A DVANCED   T ECHNOLOGY   F RANCE   
100B   ALLÉE DE   S T   E XUPÉRY   –   38330   M ONTBONNOT   S T   M ARTIN   –   F RANCE   

T EL   :   +33   4   76   41   86   39   –   F AX   :   +33   4   76   41   92   27
M AIL   :   SALES . HATFR @ HORIBA . COM   -W EB   :   WWW . HORIBA . COM   


---

CEM500 – Technical Manual   
HAT France

####### **Safety warning and liability**


![image_39](pdf_images\page2_39.jpeg)

![image_40](pdf_images\page2_40.jpeg)

![image_41](pdf_images\page2_41.jpeg)

![image_42](pdf_images\page2_42.png)


Chemicals used as reagent or used as cleaning solution or used to prepare calibration solutions

might be toxic, corrosive or irritant. Refer to the material safety data sheets (MSDS) for each

chemical. Wear protection glass and gloves.


The documentation and/or Product are provided on an “as is” basis

only

and

may

contain

deficiencies

or

inadequacies.

The

Documentation and/or Product are provided without warranty of any

kind, express or implied.

The manufacturer or its suppliers shall, regardless of any legal theory

upon which the claim is based, not be liable for any consequential,

incidental, direct, indirect, punitive or other damages whatsoever

(including, without limitation, damages for loss of business profits,

business interruption, loss of business information or data, or other

pecuniary loss) arising out the use of or inability to use the

Documentation and/or Product, even if the manufacturer or its

suppliers has been advised of the possibility of such damages.

![image_43](pdf_images\page2_43.jpeg)


![image_44](pdf_images\page2_44.png)

This equipment meets the requirements of all relevant European

safety directives. The equipment carries the CE mark.


Release C
Page   2   sur   40   


---

CEM500 – Technical Manual   
HAT France

To prevent electric shock:   

![image_47](pdf_images\page3_47.jpeg)

- Unplug the power cord before any servicing, wiring or

any operation inside the instrument.

- Connect this instrument only at a properly grounded


power socket.

- Keep the screws well tight.

![image_48](pdf_images\page3_48.png)

**This instrument must be earthed!**

In order to prevent any electric shock, verify that the power socket

used for this instrument has an earth connection in accordance

with regulations.

The security provided by this product is only assured for the

intended use.

Maintenance can only be performed by qualified personnel.

![image_50](pdf_images\page3_50.png)

![image_51](pdf_images\page3_51.png)

Do not dispose of this product as household waste. Use an

approved organization that collects and/or recycles waste electrical

and electronic equipment.


Release C
Page   3   sur   40   


---

CEM500 – Technical Manual   
HAT France

**CONTENTS**

**1.**

######### **Maintenance Schedule............................................................................... 6**

**2.**

######### **Procedures ................................................................................................. 7**

######### **2.1.**

######### **Maintenance Procedures for the Gas Circuit ................................ 7**

2.1.1. How to Change the Internal Membrane Pump .................................. 7

2.1.2. How to Check the Solenoid Valve ....................................................10

2.1.3. How to Check / Recalibrate the Pressure Sensor ............................11

2.1.4. How to Check / Calibrate the Flow Rate ...........................................13

######### **2.2.**

######### **Maintenance Procedures for Optics and Flow Cell .....................14**

2.2.1. How to Set the Signal Intensity .........................................................14

2.2.2. How to Clean the Quartz Disks of The Flow Cell ..............................15

2.2.3. How to Change the Xenon Block Lamp ............................................17

2.2.4. Calibration of Spectrograph ..............................................................18

######### **2.3.**

######### **How to Add / Remove a Gas ..........................................................20**

2.3.1. How to Add a Gas ............................................................................20

2.3.2. How to Remove a Gas .....................................................................20

######### **2.4.**

######### **Memory Re-initialization ................................................................21**

######### **2.5.**

######### **USB ..................................................................................................22**

2.5.1. How to Take Screenshots ................................................................22

2.5.2. How to Update the Software .............................................................22

######### **2.6.**

######### **Boards Synoptics ...........................................................................23**

2.6.1. DSP500 ............................................................................................23

2.6.2. XENON500 .......................................................................................29

2.6.3. OUT-4-20-500 ..................................................................................30

2.6.4. IN-4-20-500 ......................................................................................31

2.6.5. RELAY500 ........................................................................................32

######### **2.7.**

######### **Modbus Addresses ........................................................................33**

**3.**

######### **Troubleshooting ........................................................................................36**

######### **3.1.**

######### **General Troubleshooting ...............................................................36**

Release C
Page   4   sur   40   


---

CEM500 – Technical Manual   
HAT France

######### **3.2.**

######### **Measurements troubleshooting ....................................................37**

######### **3.3.**

######### **Measuring Errors for Parameters ..................................................38**

**4.**

######### **General Specifications..............................................................................39**

Release C
Page   5   sur   40   


---

CEM500 – Technical Manual   
HAT France

###### **1.** ##### **Maintenance Schedule**

The maintenance of the CEM500 analyser is limited to the replacement of spare parts such as the

lamp block after one year if used in continuous mode, and to the replacement of the membrane of the

sampling pump (optional).

The maintenance schedule of spare-parts is detailed in **Table 1** .

**Table 1.** Maintenance schedule

**Spare part**

**Reference**

**Frequency of replacement**

Xenon lamp block

E-XEN-G-1

Given for 10 9 flashes

(3 years of lifetime in continuous mode)

Internal membrane pump with

heated head

MKIT-SPL- G-1

Every year

In rare cases, there might be exceptional maintenance, depending on the use of the analyser (refer
to   Table 2 ).

**Table 2.** Exceptional maintenance

**Spare part**

**Reference**

**Frequency of replacement**

Lens (diameter 12 mm) with one

O-ring

O-LENS-1

3 to 10 years depending on the use

Disk (diameter 12 mm) with three

O-rings

O-DISK-G

3 to 10 years depending on the use


Release C
Page   6   sur   40   


---

CEM500 – Technical Manual   
HAT France

###### **2.** ##### **Procedures**

######## **2.1. Maintenance Procedures for the Gas Circuit**

######### **2.1.1. How to Change the Internal Membrane Pump**

The sampling pump is optional.

The head of the pump is heated with the rest of the gas circuit and has a flow rate of about 6 L/min.

If the pump runs continuously, the membrane must be changed once per year.

**Procedure to check the head of peristaltic sampling pump**

To check if the head of the peristaltic sampling pump needs to be changed, proceed as follows:

a. Put the analyser in stopped mode in the Timing screen shown below:

![image_128](pdf_images\page7_128.jpeg)

b. Disconnect any outlet tubing from the analyser.

c. Connect the outlet to a flow meter (0 - 10 L/min, preferentially a ball model) to the zero inlet of

the analyser. Leave the inlet of the flow meter free on ambient air.

d. On the Factory screen, go to the “Outputs 24 VDC” and press on OFF below the “Sampling

pump”, as shown on the following screenshot.   

Release C
Page   7   sur   40   


---

CEM500 – Technical Manual   
HAT France

![image_130](pdf_images\page8_130.jpeg)

A strong noise must be heard when the pump is running. If not, check the electrical connections of

the pump.

The flow meter must indicate a flow rate of about 6 L/min. If lower than 4 L/min, change the membrane

of the pump.

**Procedure to change the internal membrane of peristaltic sampling pump**

The following figure shows the different elements of the peristaltic sampling pump and their assembly

order:

![image_131](pdf_images\page8_131.jpeg)

To change the membrane of the peristaltic sampling pump, the following tools and materials are

required:

Release C
Page   8   sur   40   


---

CEM500 – Technical Manual   
HAT France

•

Fork wrench or socket wrench 5.5mm

•

Pin-wrench for two-hole nuts, pin diameter 4mm

•

Holding tool

•

Heat-resistant thread adhesive

To change the membrane of the peristaltic sampling pump, proceed as follows:

a. **Preparatory step**

Disconnect the pump from the power supply. Check that the pump is electrically dead and

secure this.

b. **Removing pump head**

•

Mark the position of the carrier (1), intermediate plate (3), and head plate (4) relative to each

other by a drawing line (M) with a felt-tip marker. This is to ensure that the parts will be

reassembled in the correct position at a later stage.

•

Release the nuts (6) and remove them together with the disk springs (5).

 The disk spring are fitted in order to maintain the tension of the wave diaphragm right across

the temperature range of the pump.

•

Remove head plate (4).

•

Remove o’ring (10) from head plate (4).

•

Remove the valve plate (11) and the intermediate plate (3).

c. **Changing diaphragm**

•

Release the retainer plate (7) by turning it anti-clockwise with a pin wrench or a wrench for

retainer plate. While doing so, hold the connecting rod extension (9) in place with holding

tool.

Take care to ensure that the washer (12) does not slip under the diaphragm support (8).

•

Remove wave diaphragm (2).

•

Check that all parts are free from dirt and clean them if necessary.

•

Slide a new wave diaphragm (2) onto the threaded bolt of the retainer plate (7).

 The wave diaphragm assembly consists of two equivalent parts placed on top of one

another; the top and bottom are identical.

•

Apply a small amount of heat-resistant thread adhesive to the thread of the retainer plate (7).

•

Screw the retainer plate (7) with wave diaphragm (2) into the connecting rod extension (9);

to tighten the retainer plate, use the wrench for retainer plate/the pin wrench to turn it

clockwise (torque: 4.6Nm). While doing so, hold the connecting rod extension (9) in place

with the holding tool; and hold the wave diaphragms so that they do not twist.

d. **Changing valve plate and sealing ring**

•

Check that intermediate plate and head plate are clean. If damages, distortion, or corrosion

are evident on these parts they should be replaced.

•

Place the intermediate plate (3) on the carrier (1) in the position indicated by the felt tip pen

mark (M).

•

Lay the new valve plate (11) onto the intermediate plate (3).

 Regarding the placement of the vale plate: The notch on outer edge of the valve plate must

be at the left rear, when looking at the pump from the motor.
•   
Fit the new o’ring (10) in the head plate (4).
e.   Refitting pump head

Release C
Page   9   sur   40   


---

CEM500 – Technical Manual   
HAT France

•

Place the head plate (4) on the intermediate plate (3) in the positions indicated by the felt-tip

pen marking.

•

Place disk spring (5).

•

Put the nuts (6) in place and tighten them diagonally, until each of them lies level on the top

spring washer; realign the pump head. From when you start applying pressure on the disk

springs, tighten the nuts through an angle of 340°. That is equivalent to a torque of 80Ncm.

f. **Final step**

•

Reconnect the pump to the electricity supply.

######### **2.1.2. How to Check the Solenoid Valve**

The main element of the gas circuit is the 3-way solenoid valve represented below that selects the

zero air (deactivated) or the sample (activated) to the measuring flow cell.

In stopped mode, the solenoid valve stays deactivated to the zero air.

If the gas circuit has not reached the temperature setting point (with a tolerance of 10 °C), the solenoid

valve stays on the zero-air inlet to prevent humid and dirty sample to enter in the cold flow cell that

may produce condensation and deposits.

To check the solenoid valve, proceed as follows:

a. Disconnect the sample line.

b. Put the analyser in stopped mode in the Timing screen.

![image_144](pdf_images\page10_144.jpeg)

c. Connect a flow meter (preferentially ball model) on an air cylinder or small air pump to get a

flow rate of about 2 L/min.
d. Connect the outlet of the flow meter to the zero inlet and check that the flow rate stays roughly

unchanged around 2 L/min.

e. On the Factory screen, go to the “Outputs 24 VDC” and press on OFF below the “EV sample”,

as shown below.

A strong sound "click" must be heard just when pressing on the OFF key. If not, check the solenoid

valve connection on the DSP500 board.

The flow meter must immediately go down to a null flow. A small flow rate remaining may indicate a

Release C
Page   10   sur   40   


---

CEM500 – Technical Manual   
HAT France

leakage on the zero circuit or inside the solenoid valve.

f. Now connect the flow meter outlet to the sample inlet and check that the flow rate goes up

again to roughly 2 L/min (go back to the previous screen if expired).

![image_146](pdf_images\page11_146.jpeg)

A strong sound "click" must be heard again just when pressing on the ON key.

The flow meter must immediately go down to a null flow. A small flow rate remaining may indicate a

leakage on the inlet circuit or inside the solenoid valve.

######### **2.1.3. How to Check / Recalibrate the Pressure Sensor**

The pressure probe is used for two reasons:

•

To automatically compensate the gas pressure (above or under the atmospheric pressure) as

the measurement is directly affected by over / under pressure.

•

To give a flow rate indication. This flow rate must be calibrated according to the outlet circuit

if a good accuracy is needed, but this will not affect the measurements.

If the sampling pump is placed before the flow cell (recommended configuration), the pressure during

measurements is always above the atmospheric pressure. With an outlet going to the atmospheric

pressure (recommended) the over pressure generally stays below 5 to 10 mbar, generating a very

small pressure compensation.

Release C
Page   11   sur   40   


---

CEM500 – Technical Manual   
HAT France

To check or recalibrate the pressure probe, proceed as follows:

a. Disconnect any tubing from the back of the analyser.

b. Put the analyser in stopped mode in the Timing screen.

![image_148](pdf_images\page12_148.jpeg)

c. On the Process screen, press anywhere highlighted by the red. This opens a new screen for

temperature, pressure and flow rate.

![image_149](pdf_images\page12_149.jpeg)

d. Press on the zero key. The relative pressure must go down to zero hPa.
e. Connect a pressure meter (range 0 - 1 bar) on the gas outlet.
f. Connect an air cylinder on the zero inlet and adjust the regulator to 0.5 bar (note: a small

membrane pump can be used instead of the air cylinder).

g. Read the pressure on the pressure meter and compare it to the displayed relative pressure.

h. In case of minor difference, the pressure factor can be readjusted to get the right value.

i.

In case of no response or incoherent response, the pressure sensor must be changed.

Release C
Page   12   sur   40   


---

CEM500 – Technical Manual   
HAT France

######### **2.1.4. How to Check / Calibrate the Flow Rate**

To check and / or calibrate the flow rate, proceed as follows:

a. Keep the analyser is stopped mode as explained before and make sure that the pressure

reading is zero (inlets out outlet free).
b.   I nsert a mass flow meter or ball flow meter (range 0 - 10 L/min) between an air cylinder and

the zero inlet.

c. Adjust the regulator of the air cylinder to get a flow rate of about 1 L/min.

d. On the Process screen, press anywhere highlighted by the red. This opens a new screen for

temperature, pressure and flow rate.

![image_151](pdf_images\page13_151.jpeg)

e. Adjust the flow factor proportionally to get the same flow rate reading than the flow meter.

Release C
Page   13   sur   40   


---

CEM500 – Technical Manual   
HAT France

######## **2.2. Maintenance Procedures for Optics and Flow Cell**

######### **2.2.1. How to Set the Signal Intensity**

The intensity of the signal can be monitored and changed. To do so, proceed as follows:

a. Put the analyser in stopped mode in the Timing screen.

![image_153](pdf_images\page14_153.jpeg)

b. Go to the Check screen and select the signal button. This button displays the lamp spectrum

obtained after the last measuring cycle, as shown below:

![image_154](pdf_images\page14_154.jpeg)

Release C
Page   14   sur   40   


---

CEM500 – Technical Manual   
HAT France

c. The intensity of the signal can be modified by playing on the screw of the lamp block, as shown

below. First, untight the M4 nut. Then untight the screw as much as possible.

![image_156](pdf_images\page15_156.jpeg)

Screw M4 x 12

![image_157](pdf_images\page15_157.png)

![image_159](pdf_images\page15_159.png)

Nut M4

d. Once untighted, press PLAY on the screen displaying the lamp spectrum.

e. By tightening the screw, you can follow the evolution of the intensity of the signal on the screen.

f. The signal requirements depending on the wavelengths are:

•   
the more intense peak at 229 nm (aligned on the red reference line) should be between
1400 and 1600 mV.   
•   
The peak at 200 nm should have a signal of about 200 mV.
g. Once the signal is meeting the previous requirements, tight the M4 nut while making sure the

M4 x 12 screw does not move. The lamp is now well aligned and will not move.
h. Go back to the lamp screen and adjust for number of flashes to get a signal of about 200 mV

at 200 nm.
The lamp alignment is necessary after a change of lamp.

######### **2.2.2. How to Clean the Quartz Disks of The Flow Cell**

The two quartz windows of the flow cell may have to be cleaned in case of abnormal operation like

insufficient heating, abnormal level of dust or particles in the sample gas.

They may have to be replaced after a long operating time (over years of continuous operation) in case

the transparency has decreased due to UV irradiation.

To clean the flow cell windows, proceed as follows:

a. Make sure the power cord is disconnected.

b. Unscrew the four knurled knob maintaining the cover of the heated compartment and remove

the cover.

c. If necessary, wait for the heated parts to cool down to ambient temperature to avoid any

burning during manipulations.

d. Unscrew the three fitting nuts of the flow cell to remove the tubing as shown in the following

figure:

Release C
Page   15   sur   40   


---

CEM500 – Technical Manual   
HAT France

![image_162](pdf_images\page16_162.jpeg)


e. Unscrew the four M4x25 screws of the flow cell as shown below:

![image_164](pdf_images\page16_164.jpeg)

f. Unscrew the four screws maintaining the extensions on each side of the flow cell as shown

below:

![image_165](pdf_images\page16_165.jpeg)

g. The disks can be cleaned with a soft tissue imbibed of alcohol. If they remain dirty, you can

soak them (and the absorption flow cell) in a 5% sulfuric acid H 2 SO 4   solution for about 30
minutes. Then take them out and dry them with a soft tissue. If the disks are not totally clear

Release C
Page   16   sur   40   


---

CEM500 – Technical Manual   
HAT France

after cleaning, replacing them is recommended. It is also recommended to change the O-rings

if the geometry is affected. Only use O-rings provided by the manufacturer.

Once all elements are clean and dry, assemble the flow cell as indicated in the previous picture:

a. Be careful to dry the O-ring before putting them back.

b. Place the absorption flow cell back in the CEM500 enclosure using four M4x25 screws.

c. Check the signal.

######### **2.2.3. How to Change the Xenon Block Lamp**

As for the quartz windows of the flow cell, the quartz lens can be damaged by the UV irradiation after

a long time of exposure (over three years of continuous operation).

To clean or replace the lens from the lamp block, proceed as follows:

a. Turn off the analyser.

b. Unscrew the four screws of the lamp block as shown below and disconnect the lamp

connector.

![image_168](pdf_images\page17_168.jpeg)

c. Unscrew the four screws maintaining the lens as shown below:

![image_170](pdf_images\page17_170.jpeg)

d. The lens can be cleaned with a soft tissue imbibed of alcohol. If the lens is not totally clear

after cleaning, it must be replaced.

e. Reassemble following the reversed order and check the light level (refer to section 2.2.1).

Release C
Page   17   sur   40   


---

CEM500 – Technical Manual   
HAT France

######### **2.2.4. Calibration of Spectrograph**

![image_154](pdf_images\page18_154.jpeg)

Never neither try to open the spectrograph nor to clean the grating. The grating will be

immediately destroyed by the contact to any tissue, even very soft.

The spectrograph might need to be recalibrated in case of replacement or software update.

To calibrate the spectrograph, proceed as follows:

a. Cycle some air several times to make sure the gas circuit and flow cell are cleaned.

b. Go on the Check screen:

![image_173](pdf_images\page18_173.jpeg)

c. Select the signal button. This button displays the lamp spectrum obtained after the last

measuring cycle, as shown below:

![image_174](pdf_images\page18_174.png)

Release C
Page   18   sur   40   


---

CEM500 – Technical Manual   
HAT France

d. On the Check screen, refer to the two wavelength bands used for the absorbance calculation

defined as “Peak wavelength” and “Ref wavelength”. Check that the signal are not saturated

(around 2000 mV). If yes, an error will occur during the measurements.

The values can be read by moving the cursor with the vertical arrows. If necessary, use the

horizontal arrows to displace the graph or press on the graph to zoom it. The Y scale is

automatic but may be override by the small arrows placed above the Y axis.

e. Press on “CALIBRATION” on the left side of the screen. The four main peaks will automatically

match the four red lines.

f. If not, you can manually calibrate the spectrograph by unticking “Auto calibration” and

adjusting the “Lambda start” wavelength.

Release C
Page   19   sur   40   


---

CEM500 – Technical Manual   
HAT France

######## **2.3. How to Add / Remove a Gas**

######### **2.3.1. How to Add a Gas**

The CEM500 analyser is made for one gas, including gas declaration, linearity, compensations

(offsets and gains) and an output 4-20 mA module.

Any additional gas requires an extra cost to include complete calibration and output 4-20 mA.

In case you need to declare a new parameter, proceed as follows:

a. In the Factory screen, select <NEW> on the frame called “List of parameters”.

![image_177](pdf_images\page20_177.jpeg)

b. Select the parameter you want in the list and click on the green arrow.

c. Enter the password to be able to add the gas.

d. The following stream is about MULTIPLEXING and the number of streams, if any.

e. The last screen is about the positions of 4-20 mA output modules.

The parameter is now added to the list on the frame called “List of parameters”.

######### **2.3.2. How to Remove a Gas**

In case you need to remove a parameter, proceed as follows:

a. On the Factory screen, click on the parameter you wish to delete on the frame called “List of

parameters”.

b. A window will appear, to confirm the erasing of the parameter. Click on the green arrow.

The parameter will be deleted from the list on the frame called “List of parameters”.

Release C
Page   20   sur   40   


---

CEM500 – Technical Manual   
HAT France

######## **2.4. Memory Re-initialization**

This procedure erases all the configuration (channel, parameters, general settings…). It may be

exceptionally used in case of board replacement. The configuration must then be-reintroduced either

manually or from a configuration file saved on a USB key.

To do a memory re-initialization, you must be logged as administrator by using the password 7895.

Then, proceed as follows:

a. In the Factory screen, select ERASE on the “Configuration” frame.

b. Note that you can select SAVE before doing the re-initialization. It will save the configuration

on a USB key. This configuration back-up includes: the gas channels with their linearity and

compensation tables (offsets and gains).

![image_179](pdf_images\page21_179.png)


Release C
Page   21   sur   40   


---

CEM500 – Technical Manual   
HAT France

######## **2.5. USB**

######### **2.5.1. How to Take Screenshots**

To take screenshots, proceed as follows:

a. Go on the Communication screen.

![image_181](pdf_images\page22_181.png)

b. Select ON at the top left of this screen.

From now on, a screenshot will be saved on your USB key when you insert it in the USB plug on the

CEM500 enclosure. This configuration will last for 1 hour. Then, do this procedure again to reactivate

the USB screen copy.

######### **2.5.2. How to Update the Software**

In case you need to update the software, proceed as follows:

a. On one hand, on the analyser: save the configuration (in the factory screen) on a USB key.

b. On the other hand, save the software file on this USB key.

c. Turn off the analyser.

d. Plug in the USB key on the analyser.

e. Turn on the analyser.

f. Choose the version of software you want to download and press on START.

g. Once the downloading is finished, remove the USB stick.

h. On the factory screen, you can load the configuration again. You can then start using the

analyser.

Release C
Page   22   sur   40   


---

######## **2.6. Boards Synoptics**

######### **2.6.1. DSP500**

![image_183](pdf_images\page23_183.png)


---

CEM500 – Technical Manual   
HAT France

![image_185](pdf_images\page24_185.png)


Release C
Page   24   sur   40   


---

CEM500 – Technical Manual   
HAT France

![image_187](pdf_images\page25_187.png)


Release C
Page   25   sur   40   


---

CEM500 – Technical Manual   
HAT France

![image_189](pdf_images\page26_189.png)


Release C
Page   26   sur   40   


---

CEM500 – Technical Manual   
HAT France

![image_191](pdf_images\page27_191.png)


Release C
Page   27   sur   40   


---

CEM500 – Technical Manual   
HAT France

![image_193](pdf_images\page28_193.png)


Release C
Page   28   sur   40   


---

CEM500 – Technical Manual   
HAT France

######### **2.6.2. XENON500**

![image_195](pdf_images\page29_195.png)

Release C
Page   29   sur   40   


---

CEM500 – Technical Manual   
HAT France

######### **2.6.3. OUT-4-20-500**

![image_197](pdf_images\page30_197.png)

Release C
Page   30   sur   40   


---

CEM500 – Technical Manual   
HAT France

######### **2.6.4. IN-4-20-500**

![image_199](pdf_images\page31_199.png)

Release C
Page   31   sur   40   


---

CEM500 – Technical Manual   
HAT France

######### **2.6.5. RELAY500**

![image_201](pdf_images\page32_201.png)

Release C
Page   32   sur   40   


---

######## **2.7. Modbus Addresses**

**Category**

**Address**

**in**

**Decimal**

**Type**

**Description**

**Unit**

**Comment**

ZERO

**512**

Table of 16x6 intergers

(year, month, day, hour,

min, sec)

Last zeroing date

For each channel

**96**

Table of 16xIEEE754 float

(32 bit)

Concentration of zero gas

ppm

For each channel

**352**

IEEE754 float (32 bit)

Optical signal at 250 nm on

last zero

mV

**128**

Table of 16xIEEE754 float

(32 bit)

Zero drift

ppm

For each channel

CALIBRATION

**640**

Table of 16x6 intergers

(year, month, day, hour,

min, sec)

Last calibration date

For each channel

**160**

Table of 16xIEEE754 float

(32 bit)

Concentration of standard

gas

ppm

For each channel

**192**

Table of 16xIEEE754 float

(32 bit)

Optical signal at 250 nm on

standard

mV

For each channel

**224**

Table of 16xIEEE754 float

(32 bit)

Difference (measurement

minus standard)

ppm

For each channel

MEASUREMENT

**768**

Table of 16x6 intergers

(year, month, day, hour,

min, sec)

Last measurement date

**64**

Table of 16xIEEE754 float

(32 bit)

Optical signal at 250 nm on

measurement

mV

For each channel

**16**

Table of 16xIEEE754 float

(32 bit)

Measurement

ppm

For each channel

**48**

Table of 16xinteger (16

bit)

Error code

0=no error, refer to

operating manual


---

CEM500 – Technical Manual   
HAT France

**Category**

**Address**

**in**

**Decimal**

**Type**

**Description**

**Unit**

**Comment**

MAIN PARAMETERS

**256**

Table of 16xIEEE754 float

(32 bit)

Range

ppm

For each channel

**288**

Table of 16xIEEE754 float

(32 bit)

Calibration coefficient

For each channel

**320**

Table of 16xIEEE754 float

(32 bit)

Offset value

ppm

For each channel

OTHER PARAMETERS

**354**

IEEE754 float (32 bit)

Pressure (relative)

hPa

**356**

IEEE754 float (32 bit)

Temperature

°C

**352**

IEEE754 float (32 bit)

Optical signal at 250 nm on

last zero

mV

**896**

Integer (16 bits)

Automatic zero period

Minutes

**897**

Integer (16 bits)

Automatic

calibration

period

hours

STATUS
898
Integer (16 bits)
Measurement
Value = 1
898
Integer (16 bits)
Standby
Value = 2
898
Integer (16 bits)
Zeroing
Value = 3
898
Integer (16 bits)
Calibration
Value = 4
898
Integer (16 bits)
Full system calibration
Not applicable
898
Integer (16 bits)
Backflush
Value = 6
898
Integer (16 bits)
Maintenance
Value = 7
ALARMS
899
Integer (16 bits)
Analyser failure
Value = 1
899
Integer (16 bits)
Light failure
Value = 2
899
Integer (16 bits)
Range limit alarm
Value = 3
899
Integer (16 bits)
Minimum range alarm
Value = 4
899
Integer (16 bits)
Temperature failure
Value = 5
899
Integer (16 bits)
Pressure failure
Value = 6
REMOTE CONTROL
900
Integer (16 bits)
Start zero
Write 1, go back to

Release C
Page   34   sur   40   


---

CEM500 – Technical Manual   
HAT France

zero when finished

**901**

Integer (16 bits)

Start calibration

Write 1, go back to

zero when finished

**902**

Integer (16 bits)

Start measurement

Write 1, go back to

zero when finished

**903**

Integer (16 bits)

Stop measurements

Write 1, go back to

zero when finished

**904**

Integer (16 bits)

Start full system calibration

Not applicable

**905**

Integer (16 bits)

Startbackflush

Write 1, go back to

zero when finished

**906**

Table of 6xintergers (year,

month, day, hour, min,

sec)

Clock adjustment

Any engaged cycle

will be aborted

From Software V1.14

Release C
Page   35   sur   40   


---

###### **3.** ##### **Troubleshooting**

######## **3.1. General Troubleshooting**

![image_206](pdf_images\page36_206.jpeg)

**Disconnect the power cord before servicing!**

**Symptoms**

**Checking / Origin**

- Check the power socket

The screen remains totally black after

connecting the power cord.

- Check J1 connector (mains input, high voltage!)

**AND**

- Check J2 connector on the DSP500 (mains input

for the power supply, high voltage!)

The red LED D1 on the DSP500 board is
OFF.

- Check J3 connector (24V output from the power

supply)

- Failure on the power supply of the DSP500 board

The screen remains totally black after

connecting the power cord.

- Check the backlight connector of the screen J10.

**AND**

- Failure off the DSP500 board.

The red LED D1 on the DSP500 board is
ON.

The screen is lighted but nothing is

displayed.

- Check the screen connector J8 on the rear of the
DSP500 board

- Failure off the DSP500 board.



---

CEM500 – Technical Manual   
HAT France

######## **3.2. Measurements troubleshooting**

**Symptoms**

**Origin**

Frozen value
- Check the mode and select the continuous mode
- A zeroing cycle is in progress, wait for the end of the cycle (< 1 min)
- A automatic calibration cycle is in progress, wait the end of the cycle
(<1 min)

Value is too low

- Bad zeroing: check or redo the zero

- Bad calibration: check the instrument with a standard

- No flow rate: check the gas circulation

Value is too high

- Bad calibration: check the instrument with a standard.

- Internal temperature no stabilised, wait 4 hours after power on for full

accuracy

Unstable value

- Deposit or dirty on the optical parts (lens and/or windows), check the

light level at 200 nm, must be typically around 200 mV

- Interference from another gas: check the gas composition

- Bad calibration (too sensitive): check with a standard.


Release C
Page   37   sur   40   


---

CEM500 – Technical Manual   
HAT France

######## **3.3. Measuring Errors for Parameters**

**Error**

**Signification**

**Origin / Remediation**

**no**

1

Gas circuit temperature

too low (more that 10 °C

bellow the set point)

- Wait for temperature stabilisation after power on, minimum

10 min on 230V AC.

- Wong configuration: check the temperature setting screen.

- Failure on the heating system or temperature probe.

2
Detector fault   

- Check the spectrograph connection.

- Failure on the spectrograph board.

3

The light level is too

high on the range of

wavelengths used for

the considered gas

- Reduce the number of flashes in the lamp screen

- Failure on the CCD500 or SPECTRO500 board (replace)

4

The light level is too low

on

the

range

of

wavelengths used for

the considered gas

- Deposits inside the gas flow cell: clean the windows (or

mirrors for CEM500-L). Check also that the temperature

setting is correct, normally 190°C (or 240°C for CEM500-L)

- Deposits on the lens, clean the lens (in front of the lamp) with

alcohol

- Bad lamp alignment: check the alignment by adjusting the

screw on the rear of the lamp holder

- Failure on the xenon lamp circuit if no flashes are visible

during the measurement: check the connection of the

XENON500 board on the DSP500 board (the orange neon

lamp N1 on the XENON500 board must always be on, if not

replace the XENON500 board) and check the lamp connection

on the XENON500 board

5

Pressure fault

- Check the pressure probe connection

- Over pressure (>2 bar or > 2000 hPa)

- Pressure probe failure

6
Flow alarm
- Value is superior to upper limit value
- Value is lower than lower limit value   
- Check if alarm values are relevant
- Check if gas is still flowing in the gas circuit


Release C
Page   38   sur   40   


---

CEM500 – Technical Manual   
HAT France

###### **4.** ##### **General Specifications**

Sample temperature:

0 °C to 400 °C

Sample pressure:

0 to 2 bar (2000 hPa or 30 psi) absolute pressure

Outlet pressure:

Atmospheric pressure (recommended)

Sample contact materials:

Stainless steel, quartz, PTFE, FFKM

Zero inlet:

Air or nitrogen (air recommended)

Zero pressure:

Without pump: 10 to 50 hPa above the atmospheric pressure

With pump: atmospheric pressure

Zero temperature:

0 ºC to 400 ºC (ambient temperature recommended)

Sample Inlet/outlet:

Stainless steel fittings (Swagelok) for external diameter 6.4 mm (1/4”)

Display:

Colour TFT LCD, Size: 10.4”, resolution: 640 x 480 pixels LED backlight

with screen saver.

Resistive touch screen

Memory:

5000 records (up to 16 measurement channels) with date and time

Communication:

RS232 - MODBUS protocol

RS485 - MODBUS protocol

USB port:

For USB memory keys, any format (FAT16, FAT32)

Standard USB connector type A with IP68 protective cap

Recorded measurement downloads (compatible with Excel®)

Complete configuration backup/restore (proprietary format)

Screen copy in BMP format (compatible with Windows®)

Software

Extensions:

12 internal sockets for input modules (logical input, 4-20 mA input),

output modules (4-20 mA) or relays modules

Outputs:

Active 4-20 mA (optional), load 500 Ohm maxi, resolution 0.005 mA,

Individual galvanic isolation

Connection on removable screw terminals

Relays (optional):

Normally open (NO) and normally closed (NC) contacts

Contact rating: 5A @ 277VAC/30VDC resistive

Connection on removable screw terminals

Release C
Page   39   sur   40   


---

CEM500 – Technical Manual   
HAT France

Power supply:

110-264 VAC / maxi 900 W / 50-60Hz (250 VA after stabilization)

Operating limits:

0 to 40 °C

Safety standard:

IEC 61010-1, EN 61010-1

EMC standard:

EN61326/A1/A2/A3, IEC61000-3-2, IEC61000-3-3, IEC61000-4-2,

IEC61000-4-3,

IEC61000-4-4,

IEC61000-4-5,

IEC61000-4-6,

IEC61000-4-11

Enclosure:

IP65 / Nema 4X, stainless steel 316L with painting

Dimensions:

521 x 345 x 252.5 mm

Weight:

30 kg approx.

---------

Release C
Page   40   sur   40   


---