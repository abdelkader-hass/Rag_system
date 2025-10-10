

TECHNICAL MANUAL

# **EL200**



![image_19](./vol/documents/imgs\page1_19.jpeg)


HORIBA|||A DVANCED|||T ECHNOLOGY|||F RANCE|||
100B|||ALLÉE DE|||S T|||E XUPÉRY|||–|||38330|||M ONTBONNOT|||S T|||M ARTIN|||–|||F RANCE|||

T EL|||:|||+33|||4|||76|||41|||86|||39|||–|||F AX|||:|||+33|||4|||76|||41|||92|||27
M AIL|||:|||SALES . HATFR @ HORIBA . COM|||-W EB|||:|||WWW . HORIBA . COM|||


---

EL200 – Technical Manual|||
HAT France

####### **Safety warning and liability**


![image_39](./vol/documents/imgs\page2_39.jpeg)

![image_40](./vol/documents/imgs\page2_40.jpeg)

![image_41](./vol/documents/imgs\page2_41.jpeg)

![image_42](./vol/documents/imgs\page2_42.jpeg)


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

![image_43](./vol/documents/imgs\page2_43.jpeg)


This equipment meets the requirements of all relevant European

safety directives. The equipment carries the CE mark.

The battery installed is also CE compliant.

![image_44](./vol/documents/imgs\page2_44.png)


Release F
Page|||2|||sur|||31|||


---

EL200 – Technical Manual|||
HAT France

To prevent electric shock:|||

![image_47](./vol/documents/imgs\page3_47.jpeg)

- Unplug the power cord before any servicing, wiring or

any operation inside the instrument.

- Connect this instrument only at a properly grounded


power socket.

- Keep the screws well tight.

![image_48](./vol/documents/imgs\page3_48.png)

**This instrument must be earthed!**

In order to prevent any electric shock, verify that the power socket

used for this instrument has an earth connection in accordance

with regulations.

The security provided by this product is only assured for the

intended use.

Maintenance can only be performed by qualified personnel.

![image_50](./vol/documents/imgs\page3_50.png)

![image_51](./vol/documents/imgs\page3_51.png)

Do not dispose of this product as household waste. Use an

approved organization that collects and/or recycles waste electrical

and electronic equipment.


Release F
Page|||3|||sur|||31|||


---

EL200 – Technical Manual|||
HAT France

**CONTENTS**

**1.**

######### **Maintenance ............................................................................................... 5**

**2.**

######### **Procedures ................................................................................................. 7**

######### **2.1.**

######### **Calibration ........................................................................................ 7**

2.1.1. Calibration Screen ............................................................................. 7

2.1.2. Calibration Procedure ........................................................................ 8

2.1.3. Linearization Curve ............................................................................ 8

2.1.4. Calibration Standards ........................................................................ 9

######### **2.2.**

######### **How to Connect a Probe ................................................................13**

2.2.1. Connections on the EL200 Electronic Board ....................................13

2.2.2. RS485 Probes ..................................................................................14

2.2.3. Probes Connected to Modules .........................................................15

######### **2.3.**

######### **How to Add / Remove a Parameter ...............................................18**

2.3.1. How to Add a Parameter ..................................................................18

2.3.2. Reinitialization of RS485 Probes ......................................................19

2.3.3. How to Remove a Parameter ...........................................................20

######### **2.4.**

######### **Memory Re-initialization ................................................................21**

######### **2.5.**

######### **USB ..................................................................................................22**

2.5.1. How to Take Screenshots ................................................................22

2.5.2. How to Update the Software .............................................................23

######### **2.6.**

######### **Modbus Addresses ........................................................................24**

**3.**

######### **Troubleshooting ........................................................................................25**

######### **3.1.**

######### **General troubleshooting ................................................................25**

######### **3.2.**

######### **Measuring errors for external probes ...........................................26**

######### **3.3.**

######### **Screen Ribbon Troubleshooting ...................................................29**

**4.**

######### **General Specifications..............................................................................30**

Release F
Page|||4|||sur|||31|||


---

EL200 – Technical Manual|||
HAT France

###### **1.** ##### **Maintenance**

The maintenance of the EL200 controller is limited to the maintenance of the external probes such

as:

•

their cleaning if no automatic air cleaning is installed,

•

the refilling of the cleaning or reagent solution, depending on the configuration,

•

their replacement depending on the customer use.

The maintenance procedure and frequency are detailed for each external probe in **Table 1** .

**Table 1.** Maintenance procedures for each external probe.

**Probe**

**Maintenance procedure**

**Frequency of**

**maintenance**

Chlorine probe

Maintenance includes:

•

the cleaning of the electrode,

•

membrane cap replacement,

•

refreshing the Internal Fill Gel (IFG).

Conditioning is required at first time use after

membrane cap change and IFG replacement. Note

that a restarted probe needs about 4 hours to get an

accurate reading.

Depending on the use:
•|||
Replacement of IFG
every 3 to 6
months.
•|||
Replacement of the
membrane cap
every 12 months.

Conductivity

Maintenance includes:

•

the cleaning of the probe.

Do not touch the probe cell surface with any hard

object. If the probe cell surface is contaminated, soak

the probe cell portion in light detergent and mild acid

for about 15 min, respectively.

Depending on the use:
•|||
Weekly or monthly

Dissolved

Oxygen

Maintenance includes:

•

the cleaning of the probe,

•

the replacement of the head.

For the auto-cleaning probe option, it can be

automatically cleaned by sending pressurised air.

Depending on the use:

•

Weekly or monthly

cleaning.

•

Replacement of the

head recommended

every 12 months.

ORP

Maintenance includes:

•

the cleaning of the probe,

•

the replacement of the probe.

Contamination of the sensing element often results in

slow response and inaccurate readings. Clean the

electrode by one of the following procedures:

•

Inorganic deposits. Immerse the electrode tip in

0.1 N HCl for 10 minutes. Wash the tip with DI

water.

Depending on the use:

•

Weekly or monthly

cleaning.

•

Replacement of the

probe every 6

months.

Release F
Page|||5|||sur|||31|||


---

EL200 – Technical Manual|||
HAT France

•

Organic oil and grease films: wash electrode tip

and a liquid detergent and water.

•

After above treatment, soak the electrode tip in

alcohol for 5 minutes, then in quinhydrone

saturated pH4.01 for 15 minutes. Rinse with DI

water afterwards.

pH

Maintenance includes:

•

The cleaning of the electrode,

•

Calibration

•

Replacement of the electrode.

For electrode cleaning, do not use strong solvents

(e.g. acetone, carbon tetrachloride, etc) to clean the

pH electrode. Clean the electrode under warm tap

water using dish-washing detergent if the electrode

has become dirty with oil or grease. If the electrode

has been exposed to protein or similar materials,

soak it in acidic pepsin. Be sure to recalibrate the

electrode after cleaning.

If previous cleaning procedures failed to restore

response, soak the electrode on 0.1N HCl for 30

minutes. Rinse with DI water and recalibrate.

If electrode response is not restored yet, replace the

electrode.

Depending on the use:

•

Weekly to monthly

cleaning.

•

Replacement every

6 months.

Temperature

No maintenance is required.

TSS

No special maintenance, except from checking that

the windows are clean.

Turbidity

Maintenance includes:

•

The cleaning of the probes.

•

The cleaning of the laser and photodetector

windows for TURB200.

Do not touch the probe cell surface with any hard

object. If the probe cell surface is contaminated, soak

the probe cell portion in light detergent and mild acid

for about 15 min, respectively.

Regarding TURB200, be careful when cleaning the

windows not to scratch them.

Depending on the use:
•|||
Weekly or monthly
cleaning.

UV200

Maintenance includes:

•

The cleaning of the probe.

Passage of compress air is recommended to clean

the deposits that might stick to the windows. A 3 – 4

bar air jet for 10-20 seconds every 60-120 minutes is

recommended. However, these are optional settings

and can be adjusted as for the application.

Depending on the use:

•

Weekly or monthly

cleaning.

Release F
Page|||6|||sur|||31|||


---

EL200 – Technical Manual|||
HAT France

###### **2.** ##### **Procedures**

######## **2.1. Calibration**

######### **2.1.1. Calibration Screen**

The calibration screen below enables to recalibrate the measurement channel.
Recommendations for recalibration are given after the following screen description.

![image_117](./vol/documents/imgs\page7_117.png)

![image_119](./vol/documents/imgs\page7_119.png)

4

![image_121](./vol/documents/imgs\page7_121.png)

![image_123](./vol/documents/imgs\page7_123.png)

![image_125](./vol/documents/imgs\page7_125.png)

![image_127](./vol/documents/imgs\page7_127.png)

1

![image_128](./vol/documents/imgs\page7_128.png)

![image_130](./vol/documents/imgs\page7_130.png)

![image_132](./vol/documents/imgs\page7_132.png)

2

![image_134](./vol/documents/imgs\page7_134.png)

![image_136](./vol/documents/imgs\page7_136.png)

![image_138](./vol/documents/imgs\page7_138.png)

3

![image_140](./vol/documents/imgs\page7_140.png)

![image_142](./vol/documents/imgs\page7_142.png)

![image_144](./vol/documents/imgs\page7_144.png)

![image_146](./vol/documents/imgs\page7_146.png)

![image_148](./vol/documents/imgs\page7_148.png)

6

5

![image_150](./vol/documents/imgs\page7_150.png)

![image_152](./vol/documents/imgs\page7_152.png)

![image_154](./vol/documents/imgs\page7_154.png)

![image_156](./vol/documents/imgs\page7_156.png)

1

######### **Last calibration window**

![image_158](./vol/documents/imgs\page7_158.png)

This window displays the 5 last calibrations done with the date, time and the new calibration factor.

![image_160](./vol/documents/imgs\page7_160.png)

![image_162](./vol/documents/imgs\page7_162.png)

2

######### **Scan last calibrations**

These two buttons allow to scroll up and down the 10 last calibration records.

3

######### **Calibration factor**

This field allows changing manually the calibration factor of the channel.

This factor is normally changed automatically while doing a calibration procedure by pressing on the

“CALIB” button.

Release F
Page|||7|||sur|||31|||


---

EL200 – Technical Manual|||
HAT France

![image_117](./vol/documents/imgs\page8_117.png)

![image_169](./vol/documents/imgs\page8_169.png)

4

######### **Zero**

![image_121](./vol/documents/imgs\page8_121.png)

This button enables to do the zero. Be sure that the probe is immersed on pure water before pressing

on this button.

Note: When pressing this button, optical signals are accessible only for TURB200 and UV200 probes.

![image_171](./vol/documents/imgs\page8_171.png)

![image_173](./vol/documents/imgs\page8_173.png)

![image_175](./vol/documents/imgs\page8_175.jpeg)

5

######### **Calibration procedure**

![image_176](./vol/documents/imgs\page8_176.png)

Refer to|||section 2.1.2|||for detailed information.|||

![image_177](./vol/documents/imgs\page8_177.jpeg)

6

######### **Linearization curve**

Refer to **section 2.1.3** for detailed information.

######### **2.1.2. Calibration Procedure**

The button 5 of the “Calibration” screen starts a calibration procedure:

•

Screen 1 : The standard value must be entered.

•

Screen 2 : the last measured value is displayed and must be validated (or re-entered). Be sure

that the probe is immersed on the standard before pressing on the button SET TO.

When finished, a new calibration factor is determined and recorded on the calibration history.

Screen 1
Screen 2

######### **2.1.3. Linearization Curve**

As the Beer-Lambert law is not linear for high absorbance values, a linearization curve is entered to

automatically compensate this non-linearity. This button displays the linearization curve and enables

to enter or check the linearization values.

Release F
Page|||8|||sur|||31|||


---

EL200 – Technical Manual|||
HAT France

The Y-axis corresponds to the rough measurements entered on the M1 to M10 fields while the X-axis

corresponds to the standard or final measurement, entered on the S1 to S10 fields (See screen 1 ).

**The M1-M10 and S1-S10 values must be strictly increasing** . It is recommended to put 0.0 and 0.0

as starting values for S1 and M1. The final value is linearly extrapolated between these points (see

Screen 2 ). Unused points at the end of the table must strictly remain at 0.0 both for S and M.

In case a new linearization curve needs to be saved, proceed as follows:

a. In the “Calibration” screen shown before, make sure that the calibration factor is set to 1.

b. Select the button 6 of the “Calibration” screen. The screen 1 shown below is displayed.

c. Erase all previous values. Put 0 for all values except for S1 = 1 and M1 = 1.

d. Run a manual test on each standard solution.

e. Enter the values from S2 of the standards you used.

f. Enter the corresponding values measured by the analyser from M2.

g. Check that the linearisation curve is correct by manually running a standard.

Screen 1:

![image_182](./vol/documents/imgs\page9_182.png)

######### **2.1.4. Calibration Standards**

Calibration should be done before the first use. Periodical checking is also recommended, and a

recalibration might be necessary after several months, depending on the conditions of use. To

recalibrate the probes, first prepare the standard corresponding to the parameter as indicated in **Table**

**2** . Then do a manual measurement on this standard following the indications given in **section 2.1.2** .

The calibration is finished.  A new calibration factor has been calculated and has been recorded inside

the calibration history displayed on the check screen. This new calibration factor will be taken into

account for all further measurements.

Release F
Page|||9|||sur|||31|||


---

EL200 – Technical Manual|||
HAT France

**Table 2.** Standards and calibration guidance for each parameter.

**Parameter**

**Standard and Calibration Guidance**

Prepare a 20 mg/L free chlorine standard:

Weight 1.850 g dichloroisocyanuric acid sodium salt C 3 HCl 2 N 3 NaO 3 (CAS

number: 51580-86-0) and dilute in 1 litre of demineralized water to obtain

a mere solution of 1 g/L free Cl 2 . Then take 20 mL of this mere solution

and complete to 1 litre of demineralized water.

Chlorine probe

Put the electrode in demineralized water.

- Do manual measurements using the check screen, wait for the

stabilisation of the conductivity value (a few minutes if the electrode is new

or dry), then press on the ZERO key.

- Then put the electrode in a standard solution for conductivity (example

210 µS for 100 mg/L sodium chloride NaCl (CAS number: 7647-14-5) at

25°C).

- Do a manual measurement on this solution using the check screen, wait

for the stabilisation of the conductivity.

- Go on the calibration screen, press on the CALIB key, enter the standard

value on the keypad and press on SET TO.

The calibration is finished.  New offset and calibration factors have been

calculated and recorded on the calibration history displayed on the

calibration screen. These new offset and factors will be taken into account

for all further measurements.

Conductivity

Release F
Page|||10|||sur|||31|||


---

EL200 – Technical Manual|||
HAT France

The DO probe is factory calibrated and is normally stable for long period

of time (one year). It may be recalibrated if necessary.

Zero calibration:

- Put the probe on zero-oxygen solution.

A zero-oxygen solution can be prepared by dissolving 10 g sodium sulfite

Na 2 SO 3 (CAS number: 7757-83-7) into 300 mL of demineralized water

and eventually adding a shake of cobalt chloride that accelerates the

reaction. Allow a few minutes of reaction before using this solution. Do not

keep this solution more than a few hours.

- Do manual measurements using the check screen, wait for the value to

stabilize (it may take a few minutes). Then go to the calibration screen

and press on the ZERO key.

Full scale calibration on air:

- Put the electrode on ambient air.

- Do manual measurements using the check screen, wait for both the

value and the temperature to stabilize (it may take a few minutes).

- Then go to the calibration screen and press on the 100% key.

- Enter the atmospheric pressure read on a portable barometer.

The probe is internally recalibrated. There is no change on the calibration

factor.

Dissolved Oxygen

- Zeroing: Replace the ORP electrode on input terminal (J2 position if

PH500 module or J12 if direct connection on EL200 board) by a strap to

display 0 mV.

- Wait for the stabilization of the ORP value, then press on the ZERO key.

- Put the electrode in a standard buffer solution.

- Do a manual measurement on this standard using the check screen and

wait for the stabilisation of the ORP value.

- Then go to the calibration screen and press on the CALIB button.

Validate the last measured value and then enter the standard value on the

keypad.

Oxidation-Reduction

Potential (ORP)

-|||Put the electrode in a pH 7.0 buffer solution.
- Press on the pH=7 key of the calibration screen. Wait for the stabilisation
of the pH value, then press on the SET TO 7.0 key.|||
-|||Put the electrode in a pH 4.0 buffer solution.
- Press on the pH= … key of the calibration screen. Enter the standard
value, wait for the stabilisation of the pH, then press on the SET TO key.

pH

Release F
Page|||11|||sur|||31|||


---

EL200 – Technical Manual|||
HAT France

- Put the temperature probe in a Dewar filled of ice and water.

- Do manual measurement using the check screen, wait for the

stabilisation of the temperature value, and then press on the ZERO key.

- Put the temperature probe in a Dewar filled of water at a temperature

between 50 °C and 80 °C with a reference thermometer inside.

- Do manual measurement using the check screen, wait for the

stabilisation of the temperature value.

- Go to the calibration screen, then press on the CALIB key. Validate the

last measurement then enter the value given by the reference

thermometer on the keypad.

Temperature

Turbidity by

Absorbance (external

probe)

- Do a TSS laboratory measurement on a sample representative of the

measuring range.

- Do a manual measurement on the same sample using the check screen.

Turbidity by

nephelometry with

laser diode

Take a turbidity standard (formazine for example) representative of the

measuring range.

The analyser gives the result in absorbance by meter by default. No

calibration is required in this measuring mode regarding the accuracy of

flow cell optical path (± 0.1 mm).

If the measuring mode is in COD and after than the UV254-COD relation

has been tested, the analyser must be calibrated according to a COD

laboratory measurement as each kind of effluent has a specific UV254 /

COD ratio.

The default calibration in COD mode corresponds to river water with a

calibration factor of 0.5.

The calibration factor for municipal wastewater is around 10.

Note that many saturated organic compounds like glucose or alcohol do

not have UV absorption.

To recalibrate the analyser in COD mode, proceed as follows:

- Take a representative sample and bring it to a laboratory for a COD

measurement.

- Do a manual measurement on this sample using the check screen (it is

recommended to check first the zero).

- When the laboratory measurement is known, go on the calibration

screen and press on the CALIB button of the check screen. Enter the

measurement given by the analyser and then enter the laboratory value

on the keypad.

UV254 (UV200)


Release F
Page|||12|||sur|||31|||


---

EL200 – Technical Manual|||
HAT France

######## **2.2. How to Connect a Probe**

######### **2.2.1. Connections on the EL200 Electronic Board**

The drawing of the EL200 electronic board is explained below ( **Figure 1** ), with indications on where

and which external probes can be connected:

![image_188](./vol/documents/imgs\page13_188.jpeg)

**Figure 1.** Drawing of the EL200 electronic board explaining the connections.

Note on RS485 probes: the two RS485 connectors are connected in parallel, meaning that up to two

RS485 probes can be connected on each RS485 connector. **In total, four RS485 probes can be**

**connected in one EL200** (practically, two wires per terminal are the maximum for a secured

tightening).

Release F
Page|||13|||sur|||31|||


---

EL200 – Technical Manual|||
HAT France

######### **2.2.2. RS485 Probes**

The following probes are connected to the RS485 port:

**Probe**

**Probe Reference**

Dissolved Oxygen probe by fluorescence

DO-F

Dissolved Oxygen probe by fluorescence with autocleaning

DO-F-AC

Total Suspended probe high range

High range: 0 – 30000 mg/L TSS

EXT-TURB-H

Total Suspended probe low range

Low range: 0 – 1500 mg/L TSS

EXT-TURB-L

Nephelometric turbidity sensor low range

Range: 0 – 100 NTU

TURB200

UV200 high range
Range: 0 – 600 Abs/m (0 – 5000 mg/L COD on rough municipal
waste water)

UV200-H

UV200 low range
Range: 0 – 200 Abs/m (0 – 100 mg/L COD on rough municipal
waste water)

UV200-L

The Dissolved Oxygen probe by fluorescence has the following wiring:

![image_191](./vol/documents/imgs\page14_191.png)

Standard DO RS485 wiring

Plug 5 ways 3.5mm|||
Weidmuller BL 3.5/5

![image_193](./vol/documents/imgs\page14_193.png)

Pin 1: red|||
Pin 2: blue
Pin 3: yellow
Pin 4: black

![image_195](./vol/documents/imgs\page14_195.png)

![image_197](./vol/documents/imgs\page14_197.png)

J3&J11

Note: several probes can be connected in parallel, except for the

first time the probe is configured. It must be done one by one.

Once configured, the probes can be connected in parallel.

![image_199](./vol/documents/imgs\page14_199.png)


Release F
Page|||14|||sur|||31|||


---

EL200 – Technical Manual|||
HAT France

The UV200 probe has the following wiring:

![image_202](./vol/documents/imgs\page15_202.png)

The other RS485 probes have the following wiring:

![image_204](./vol/documents/imgs\page15_204.png)

RS485 probes wiring

Plug 5 ways 3.5mm|||
Weidmuller BL 3.5/5

![image_206](./vol/documents/imgs\page15_206.png)

Pin 1: red|||
Pin 2: green
Pin 3: white
Pin 4: black
Pin 5: Shielding

![image_208](./vol/documents/imgs\page15_208.png)

![image_210](./vol/documents/imgs\page15_210.png)

J3&J11

Note: several probes can be connected in parallel, except for the

first time the probe is configured. It must be done one by one.

Once configured, the probes can be connected in parallel.

![image_199](./vol/documents/imgs\page15_199.png)

######### **2.2.3. Probes Connected to Modules**

The following probes are connected to modules:

**Probe**

**Probe Reference**

**Module Reference**

Conductivity online electrode, K=1

Typical range: 0 - 10 mS

ELCOND

COND500

Conductivity online electrode, K=0.01

Typical range: 0 - 100 µS

ELCOND-0.01

COND500

Conductivity online electrode, K=0.1

Typical range: 0 - 1000 µS

ELCOND-0.1

COND500

Conductivity online electrode, K=10

Typical range: 0 - 100 mS

ELCOND-10

COND500

Inductive conductivity online probe

Range: 0 – 200 mS

ICOND

Internal IN4-20-500 (or

additional module)

Release F
Page|||15|||sur|||31|||


---

EL200 – Technical Manual|||
HAT France

Nephelometric turbidity probe high range

High range: 0 – 400 NTU

EXT-TURBNEPH-H

Internal IN4-20-500 (or

additional module)

Nephelometric turbidity probe low range

Low range: 0 – 40 NTU

EXT-TURBNEPH-L

Internal IN4-20-500 (or

additional module)

pH sensor, general purpose

ELPH

PH500

pH sensor, differential

ELPH-D

Internal IN4-20-500 (or

additional module)

ORP sensor, general purpose

ELORP

Internal IN4-20-500 (or

additional module)

Amperometric chlorine electrode

ELCHL

Internal IN4-20-500 (or

additional module)

Put the relevant module on one of the twelve sockets of the EL200 board. Screw the module with a

M3x6 screw.

![image_213](./vol/documents/imgs\page16_213.png)


![image_215](./vol/documents/imgs\page16_215.png)

Release F
Page|||16|||sur|||31|||


---

EL200 – Technical Manual|||
HAT France

![image_217](./vol/documents/imgs\page17_217.png)


![image_219](./vol/documents/imgs\page17_219.png)

![image_220](./vol/documents/imgs\page17_220.png)

![image_222](./vol/documents/imgs\page17_222.png)


Release F
Page|||17|||sur|||31|||


---

EL200 – Technical Manual|||
HAT France

######## **2.3. How to Add / Remove a Parameter**

######### **2.3.1. How to Add a Parameter**

In case you need to declare a new parameter, proceed as follows:

a. In the Main menu screen, select “Settings” to open the Settings screen, and then select “New”.

![image_225](./vol/documents/imgs\page18_225.png)


![image_226](./vol/documents/imgs\page18_226.png)

b. Enter the password 3333.

c. Select the parameter you want in the list and click on OK.

![image_227](./vol/documents/imgs\page18_227.png)

d. Choose the positions of the channel no. and multiplex, the position of the probe module, the

position of the 4-20 mA module.|||
The parameter is now added and appears on the Settings screen.

Release F
Page|||18|||sur|||31|||


---

EL200 – Technical Manual|||
HAT France

######### **2.3.2. Reinitialization of RS485 Probes**

In case additional RS485 probes are added or replaced on one EL200 controller, an error message

will appear on the second RS485 probe that was declared. A reinitialization has to be done to erase

this error message. To do so, proceed as follows:

a. Declare the parameters as previously explained.

b. Go on the SETTINGS of the second RS485 probe that was declared.

c. Press on COMMUNICATION, then select RS485 PROBES as shown below:

![image_229](./vol/documents/imgs\page19_229.png)

d. Disconnect the first RS485 probe that was declared. Only the second probe should be

connected.

e. Press on RESET:

![image_230](./vol/documents/imgs\page19_230.png)

f. Reconnect the first RS485 probe. Both values measured by the probes will now be displayed.

Release F
Page|||19|||sur|||31|||


---

EL200 – Technical Manual|||
HAT France

######### **2.3.3. How to Remove a Parameter**

In case you need to remove a parameter, proceed as follows:

a. On the Settings screen, select the parameter you want to remove.

![image_225](./vol/documents/imgs\page20_225.png)

b. Select “DEL” and confirm.

c. Enter the password 3333.

The parameter is now deleted.

Release F
Page|||20|||sur|||31|||


---

EL200 – Technical Manual|||
HAT France

######## **2.4. Memory Re-initialization**

This procedure erases all the configuration (channel, parameters, general settings…). It may be used

exceptionally in case of board replacement. The configuration must then be-reintroduced either

manually or from a configuration file saved on a USB key.

To do a memory re-initialization, proceed as follows:

![image_233](./vol/documents/imgs\page21_233.png)

a. In the Settings screen, select|||to open the second Settings screen:

![image_234](./vol/documents/imgs\page21_234.png)

b. Select MEMORY:

![image_235](./vol/documents/imgs\page21_235.png)

c. Select FULL RE-INITIALIZATION. Note that you can select SAVE CONFIG TO USB KEY

before doing the re-initialization.

Release F
Page|||21|||sur|||31|||


---

EL200 – Technical Manual|||
HAT France

######## **2.5. USB**

######### **2.5.1. How to Take Screenshots**

To take screenshots, proceed as follows:

a.  Select a parameter on the “Values process screen”. The following screen is displayed:

![image_237](./vol/documents/imgs\page22_237.png)

b. Select “COM”, then “USB”:

![image_225](./vol/documents/imgs\page22_225.png)


![image_229](./vol/documents/imgs\page22_229.png)

c. Select

![image_238](./vol/documents/imgs\page22_238.png)

|||From now on, a screenshot will be saved on your USB key when you insert it in the USB plug on the|||
EL200 controller. This configuration will last until you press|||again, or if you turn off the
controller. Then, do this procedure again to reactivate the USB screen copy.

![image_239](./vol/documents/imgs\page22_239.png)

Disconnect the USB key as soon as the operation is finished as USB connection is not

watertight and as it may block the analyser normal operation.

Release F
Page|||22|||sur|||31|||


---

EL200 – Technical Manual|||
HAT France

######### **2.5.2. How to Update the Software**

In case you need to update the software, proceed as follows:

a. Save the software file on a USB key.

b. Turn off the controller.

c. Plug in the USB key on the controller.

d. Press anywhere on the screen with your finger.

e. Turn on the controller.

f. Choose the version of software you want to download and press on START.

g. Once the downloading is finished, remove the USB stick. You can start using the controller.

Release F
Page|||23|||sur|||31|||


---

EL200 – Technical Manual|||
HAT France

######## **2.6. Modbus Addresses**

**Address**

**in**

**Decimal**

**Internal Name**

**Type**

**Description**

99
jb_clean
16-bit integer|||
Start a cleaning cycle when set
to 1 (back to 0 when finished)|||

100

invalid

Table of 16 16-bit integer

Channels

measuring

error

code (0=no error)

Channels process value (not

updated by measurements in

check screen)

132
process
Table of 16 IEEE float|||

196

calib_factor

Table of 16 IEEE float

Channels calibration factor

260
offset
Table of 16 IEEE float|||
Channels offset factor|||

324

active

Table of 16 16-bit integer

Channels in operation (1=in

operation, otherwise 0)

356

label

Table of 16 strings of 7 characters

Channels label name (null

character terminated)

468

unit

Table of 16 strings of 7 characters Channels

unit

name

(null

character terminated)


Release F
Page|||24|||sur|||31|||


---

EL200 – Technical Manual|||
HAT France

###### **3.** ##### **Troubleshooting**

######## **3.1. General troubleshooting**

![image_245](./vol/documents/imgs\page25_245.jpeg)

**Disconnect the power cord before servicing!**


**Symptoms**

**Checking / Origin**

- Check the power socket.

- Check J19 connector (mains input, high voltage!).

- Check J2 connector (24V DC output from the power

supply).

- Failure on the power supply of the EL200 board.

The screen remains totally black after

connecting the power cord.

**AND**

The red LED D8 on the EL200 board is

OFF.

The screen remains totally black after

connecting the power cord.

**AND**

The red LED D8 on the EL200 board is

ON.

- Failure off the EL200 board.

- Check the screen connector J1 on the bottom of the

EL200 board.

- Failure off the EL200 board.

If Bip when powered on but unstable

display.


Release F
Page|||25|||sur|||31|||


---

EL200 – Technical Manual|||
HAT France

######## **3.2. Measuring errors for external probes**

**Probes**

**Error**

**no**

**Signification**

**Origin / Remediation**

Conductivity

1

Over range

-

Check on pure water.

-

Failure on the conductivity board (replace).

pH

1

Over range

-

Probe disconnected.

-

Failure on the pH board (replace).

Temperature

1

Over range

(high)

-

Check the connection of the temperature probe.

2
Over range
(low)

-

Check the probe with an ohmmeter, the value must

be in a 100 to 120 Ohm range, if not replace the

probe.

-

Failure on the temperature module (replace).

TURB200

1

No connection

-

The probe is not connected or badly connected.

-

The probe is not properly configured.

-

**A special initialisation must be done when the**

**probe is used for the first time.**

2

Detector

default

-

Check wiring.

-

Failure on photodetector board (repair or replace).

3
The light level
is too high

-

Too much parasite light. Check that the cover is

properly closed.

-

Test on demineralized water.

-

Check that no air bubble is present in the flow cell.

If yes, check the fittings.

4

The light level

is too low

-

Check red light from the laser by removing the

three black knobs of the probe.

-

The sample is highly turbid. Check the probe on

tap water and/or standard solution (100 NTU

maximum)

-

Failure on the photodetector board (repair or

replace).

UV200

1

No connection

-

The probe is not connected or badly connected.

-

The probe is not properly configured.

-

**A special initialisation must be done when the**

**probe is used for the first time.**

2

Detector

default

-

Check wiring.

-

Failure on photodetector board (repair or replace).

Release F
Page|||26|||sur|||31|||


---

EL200 – Technical Manual|||
HAT France

3
Signal too high
on Led 1

-

Too much parasite light.

-

Protect from direct UV irradiation.

4
Signal too high
on Led 2

-

Too much parasite light.

-

Protect from direct UV irradiation.

5
Signal too low
on Led 1

-

Too much turbidity or organic matter in the water

sample.

-

Check on demineralized water.

6
Signal too low
on Led 2

-

Too much turbidity in the water sample.

-

Check on demineralized water.

TSS

1

No connection

-

The probe is not connected or badly connected.

-

The probe is not properly configured.

-

**A special initialisation must be done when the**

**probe is used for the first time.**

2

General default

-

Send for repair.

3

Out of range

-

Check the measuring range.

-

Test on a formazin standard or demineralized

water.

4

Negatives

values

-

Do the zero on demineralized water.

DO

Insight

1

No connection

-

The probe is not connected or badly connected.

-

The probe is not properly configured.

-

**A special initialisation must be done when the**

**probe is used for the first time.**

2
Light too high
on peak

-

Too much signal on the peak photodiode.

-

Check on demineralized water.

3

Bad signal on

the peak

photodiode

-

Check on demineralized water.

4

Light too high

on reference

-

Too much signal on the reference photodiode.

-

Check on demineralized water.

Release F
Page|||27|||sur|||31|||


---

EL200 – Technical Manual|||
HAT France

5

Bad signal on

the reference

photodiode

-

Check on demineralized water.

6

Temperature

default

-

Check on demineralized water.

-

Send for repair.

7

Temperature

default

-

Check on demineralized water.

-

Send for repair.

DO

aurora

1

No connection

-

The probe is not connected or badly connected.

-

The probe is not properly configured.

-

**A special initialisation must be done when the**

**probe is used for the first time.**

2

Default

-

Check on demineralized water.

-

Send for repair.

3

Temperature

default

-

Check on demineralized water.

-

Send for repair.

4

Default

-

Check on demineralized water.

-

Send for repair.

5

Default

-

Check on demineralized water.

-

Send for repair.

6

Default

-

Check on demineralized water.

-

Send for repair.

7

Default

-

Check on demineralized water.

-

Send for repair.


Release F
Page|||28|||sur|||31|||


---

EL200 – Technical Manual|||
HAT France

######## **3.3. Screen Ribbon Troubleshooting**

In very rare cases, the screen display might be malfunctioning. If it happens, check the connection of

the screen ribbon. To do so, proceed as follows:

a. Check the two grey connectors shown on the left picture ( Figure 2 ).|||
b. Pull them off as on the right picture ( Figure 2 ).
c. Put back the ribbon.
d. Push the two grey connectors to their initial position.

![image_252](./vol/documents/imgs\page29_252.jpeg)

**Figure 2.** Positions of the grey connectors of the screen ribbon.


Release F
Page|||29|||sur|||31|||


---

EL200 – Technical Manual|||
HAT France

###### **4.** ##### **General Specifications**

Dimensions (HxWxD):
140 x 140 x 91 mm|||
Weight:
2 kg
Mounting:
Wall|||
Rating:|||
Nema 4X
Display:
Colour LCD, 480 x 272 pixels, 4.3", LED backlight|||
For outdoor:
An enclosure is required

Altitude:|||
Less than 2000 m

Humidity:
85% or lower

Pollution degree:|||
2

Storage temperature:|||
- 25 °C to + 65 °C

Power supply :|||
100 - 240 VAC ± 10% / maxi 20 VA / 50 / 60 Hz

Overvoltage category:

II

Connected on power systems:

TT

Analog 4-20 mA outputs:

2 (expendable to 4 if no other module), galvanic isolation

Analog 4-20 mA inputs:

2 (expendable to 4 if no other module), galvanic isolation plus

isolated 15 V DC output

RS485 connector for probes:

2 (up to 4x RS485 probes) for DO, TSS

pH/ORP input:

1 (expendable to 3 if no other module), galvanic isolation

Conductivity input:

0 (expendable to 2 if no other module), galvanic isolation

Security:

Two level passwords

Relay:

4 x electromechanical SPDT (form C) contact, 5 A

Relay function:

High & low alarm, default (power safe mode selectable)

Communication:

MODBUS RS232 and RS485

USB:

For configuration backup/restore, download and software

update, screencopy

Safety standard:

EN 61010-1:2010

EMC standard:

EN 61326-1:2013, IEC61000-3-2, IEC61000-3-3, IEC61000-4-

Release F
Page|||30|||sur|||31|||


---

EL200 – Technical Manual|||
HAT France

2, IEC61000-4-3, IEC61000-4-4, IEC61000-4-5, IEC61000-4-6,

IEC61000-4-11

------

Release F
Page|||31|||sur|||31|||


---

