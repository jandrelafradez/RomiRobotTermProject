# **ME 405 Romi Term Project Portfolio**
This repository outlines our Romi term project that was completed by Roy Cabrera and Jandre Lafradez during the Winter 2025 Quarter at Cal Poly, San Luis Obispo. Code files are attached above, with explanations of each file to follow later within this section. Hardware components are also attached with their links for anyone interested in recreating their own Romi project.   
  
![Romi](romi_diagonalview.jpg)
## **Table of Contents**
1) [Required Materials](#required-materials)  
2) [Romi Assembly](#romi-assembly)  
3) [Wiring Diagram](#wiring-diagram)  
4) [State Transition Diagram](#state-transition-diagram)  
5) [Finite State Machines](#finite-state-machines)  
6) [Explanations of each class](#explanations-of-each-class)  
  a) [motor.py](#motor-py)    
  b) [Encoder.py](#encoder-py)    
  c) [cotask.py](#cotask-py)  
  d) [task_share.py](#task_share-py)  
  e) [centroid.py](#centroid-py)  
  f) [linesensor.py](#linesensor-py)  
  g) [bumper.py](#bumper-py)  
  h) [main.py](#main-py)
7) [Game Track and Results](#game-track-and-results)

## **Required Materials**  
| Qty | Part Name |  
|----|------------------|  
|6|[M2.5x8mm Standoff](https://www.amazon.com/HELIFOUNER-Standoffs-Assortment-Threaded-Motherboard/dp/B0B7SNCFF1/ref=sr_1_1_sspa?crid=39OOL49HOZYYP&dib=eyJ2IjoiMSJ9.R1Y_pSmTsEnF_05yeQt1b1YjhKCs4NhWuFRgfXSsDssx-KmbAemXNTopqg4CKNWrmaA8Pmw2e66j5ImR7Gt_fbRGj9pkZPNdl-IHEEpk43dNwjfptE6TDrp-QfjS8Xcba_eb-2qHPMGShj-8W_WtNERCt2DZxnnTG3PQlH01jAO3FVd8RTZKCcbuMoO5glIGVDWpPZngLRrsE5BHLZlRekkx_u90gSv7gjzTS6ieVDyX5zJbnl660Qb16T9KO3iPwvxvXNYG70tcPl-i2T7G83VI1eNPsVo8y6cOGovxvEg.FfXshduiA5rxLbjgs7EEgRl-YFgDpzXczNs5eAmqFOs&dib_tag=se&keywords=m2.5%2Bstandoffs&qid=1741826716&s=industrial&sprefix=m2.5%2Bstandoffds%2Cindustrial%2C193&sr=1-1-spons&sp_csd=d2lkZ2V0TmFtZT1zcF9hdGY&th=1)|  
|8|M2.5x10mm Standoff|
|4|M2.5x30mm Standoff|
|4|[M2.5x6mm Socket Head Cap Screw](https://www.amazon.com/Pieces-Washers-Sutemribor-Assortment-Threaded/dp/B0CXQ4QTGT/ref=sr_1_1_sspa?crid=35K93HSFV9742&dib=eyJ2IjoiMSJ9.oNdkffsvE5kZ1Y7M7vl0Zy5KpEbfg83e__Bac_QSh3wlPoA0gKf3QLy2TaosdxQFixN_OTaaGohJ7jObLJ57jtrxzWN1mZAV73Dz29BIU25LjqyvqXEiZofI0wh3YU3IlCOFAR2BjP_eiuDgeH6a-MwDvSTalHfSpvzw-0io4rLKqGoJwMPz2v1xGlV8dYl84R6guQFgVDev_Yp-o9kY9UwBmKGqBS3sgqFb9IrZVBo.GjWp1EXV3KZLIBNgqLPnsou2wgunYguo-pKMavuUyMc&dib_tag=se&keywords=M2.5%2BSocket%2BHead%2BCap%2BScrew&qid=1741827025&sprefix=m2.5%2Bsocket%2Bhead%2Bcap%2Bscrew%2Caps%2C184&sr=8-1-spons&sp_csd=d2lkZ2V0TmFtZT1zcF9hdGY&th=1)|
|4|M2.5x8mm Socket Head Cap Screw|
|4|M2.5x10mm Socket Head Cap Screw|
|8|[M2.5 Nylon Lock Nuts](https://www.amazon.com/binifiMux-100pcs-0-45mm-Stainless-Locking/dp/B07LC4LZB6/ref=sr_1_4?crid=2O4MVOP42T7G3&dib=eyJ2IjoiMSJ9.0MhNLCmDLtUikKjKopiJRs738OPapNh77Zm5Beqzhut7BqvPIgnKpMlyyooo-1ahel137SIX3B8PHkdSuBINWilSLMfyljooj77Nji2SKdvAhJCpV_NiiQSUo5hsSGY2qgvlA0o3T0-vGbDKYaBOSA5gTKSO8iXuWNlx_YzuiRi2m0ygL75-EZ_gMYZzZ7RuRvuo3-SblD1EWIwm3ngKQVFU3sTaFX5oFWAFOGP3GyNtgx2bQ8jFIyH8yk9856x1-Kj-n1JAsJzPkGSxanJPdiIXvKPUcER9Fsf3Cm4lyjiRHPxwgy212WCnm3vVU4ORVW4iH_Y6kumA4-Do4P7ZXr2cTdGqiI6sa-D4joyjCQU.exCEzy71gPITLcO9G4eUsAqVDnKylt4Z2GRT2uAKVuk&dib_tag=se&keywords=M2.5+Nylon+Lock+Nuts&qid=1741827096&s=industrial&sprefix=m2.5+nylon+lock+nuts%2Cindustrial%2C224&sr=1-4)|
|8|[M2.5 Nylon Washer](https://www.amazon.com/uxcell-Washers-Thickness-Sealing-Gasket/dp/B014UB5TNM/ref=sr_1_4?crid=17DUM5FLADKEZ&dib=eyJ2IjoiMSJ9.JY2TmpQ3L0ybLY3dqW-BQesQMPyz-J9ngdf-ohiZwlDVkpvHWTMmyD6Pfs_gJ-xnUYR0DCxPdGy30ommgFn6wjO4gRtunFqe5YluoxM6VkxZNdXumCQGy-2_Hj3FZhq0jjQHBF8_-MMG2IuLEVwDuXINLXbMd60gaey3EFymNUc6pDtGmkkhva5y3_7q5iNa7B0etqiB9c9htWzz7HzQd6BGJSRsxxDYbTN4H7P8SnY.FoLVg3QeswNZ39HxPLTqCkwhgqn9q32jnHgwzZ2gRGU&dib_tag=se&keywords=M2.5%2BNylon%2BWasher&qid=1741827139&sprefix=m2.5%2Bnylon%2Bwasher%2Caps%2C542&sr=8-4&th=1)|
|1|Acrylic Romi-to-Shoe Adapter|
|1|[BNO055 IMU Breakout Board](https://www.adafruit.com/product/2472)|
|1|Modified Shoe of Brian|
|1|[Nucleo L476RG](https://www.amazon.com/STM32-Nucleo-64-Development-STM32L476RG-NUCLEO-L476RG/dp/B01IO3N646/ref=asc_df_B01IO3N646?tag=bingshoppinga-20&linkCode=df0&hvadid=80883013965175&hvnetw=o&hvqmt=e&hvbmt=be&hvdev=c&hvlocint=&hvlocphy=&hvtargid=pla-4584482478710114&psc=1&msclkid=a6354354cadc109814112486e7d457d3)|
|1|[Romi Chassis w/ Wheels and Casters](https://www.pololu.com/product/3504)|
|1|[120pc Dupont Ribbon](https://www.amazon.com/dp/B07GCY6CH7)|
|1|[HC-05 Bluetooth Module](https://www.amazon.com/dp/B01MQKX7VP)|
|6|[AA Batteries](https://www.amazon.com/Coppertop-Batteries-Ingredients-Long-lasting-Household/dp/B000IZQO7U/ref=sr_1_4?crid=2MKA0OT2RUVJ7&dib=eyJ2IjoiMSJ9.bVDHrtnE9UWilTlB-nv1XPqOW_2BDVUEJAEK28lWbTsdTqoyTHxxgvU2pJfok-iawYULS5jA0PsM3LiJf2k5toI8T3nylWQ0GcF1FwP6UFHAIjcf6IWfo-o9-4UdXACN0uj_EDWWLjvZZIcb4k9j4oc9OI66DgNum_-Zirt7SdAZdHwLQ5t5ptK6yQGAtRZDopWlr3K4bCMdFV384hIa9jnvSta-uN9jGt0XWvpKpWFME-BB8SCvPdJGvU5mMCFwLHuUyZVZbDneiJ89elfZO6uwIyVUXlCR3tbiwzSBK9STK_Bfb3Wcs-Xyv-VesiaPQISaw5JfYNjWXMZKh6NQ0ZjCAdRHnbtCqt6Ae-QgWgs.p4gI1OKLANbg2qd9lzlz36GsgeNm0M0NGe2qoGeBEmo&dib_tag=se&keywords=aa+batteries+pack+of+6&qid=1741827500&rdc=1&s=electronics&sprefix=aa+batteries+pack+of+%2Celectronics%2C173&sr=1-4)|
|1|[IR Reflectance Sensor](https://www.pololu.com/product/4248)|
|1|[Left Bump Sensor](https://www.pololu.com/product/3673)|
|1|[Right Bump Sensor](https://www.pololu.com/product/3674)|
|1|[USB-Mini-B to USB-C Cable](https://www.amazon.com/dp/B08GG47H8T?th=1)|

## **Romi Assembly**
**Initial Steps**  
To learn how to attach the attach the Shoe of Brian, nucleo, encoders, motors, and IMU, please refer to the attached [Romi Assembly](RomiAssembly.pdf) file that was handed to us during lab.

**Attaching the IR Sensor**  
![IR Sensor](IR_Sensor.png) ![IR Sensor](IR_Sensor.png)

**Attaching the Bump Sensor**

## **Wiring Diagram**  
The following wiring diagram shows how we were able to wire our power, bump sensors, IR sensor, IMU, encoders, and motors to our Nucleo L476RG. Please note that for ease of view, each connected part has its own respective color. However, ground and power remain black and red for each part it applies to.  

![Wiring Diagram](wiringdiagram.png)
## **State Transition Diagram**
### **Motor Class**
### **IR Sensor Class**
## **Finite State Machines**
## **Explanations of each class**
### *motor py*
The *motor.py* file defines a class for running the Romi motors and setting the duty cycle for each motor. It enables the motors to spin according to the specified duty cycle.
### *Encoder py*
The *encoder.py* file contains the class to read the encoder of both the left and right wheel. It contains methods to update the encoders and returns the position and delta values, which can be used to determine the velocity of each wheel. The end of the class also contains a method to zero Romi's position. 
### *cotask py*
The *cotask.py* file contains the class and the methods to run the scheduler, which runs the tasks based on the specified period and priority of each task specified by the user that were described in the [State Transition Diagram](#state-transition-diagram) portion previously mentioned. These periods and priorities are also set by the user in the [main py](#main-py) file.
### *task_share py*
The *task_share.py* file depicts a class that allows share and queue variables to be created. This allows data to be shared between share the wheels and user control tasks.
### *centroid py*
The *centroid.py* file contains a class that allows our infared (IR) sensors to create a centroid in order to calculate where the middle of the black line is at while our Romi follows the game track. 
### *linesensor py*
The *linesensor.py* file allows us to calibrate our IR sensors to differentiate between white and black colors. It also computes an error based off our PID values that were determined by the user and the differentiation from the centroid. This error allows for motor speed for each wheel to be corrected in order to keep Romi on a line. 
### *bumper py*
The *bumper.py* file contains a class that disables efforts to our motor once the buttons are depressed. This causes our Romi to pivot and is vital to the wall portion of the game track. 
### *main py*
The *main.py* file is where all of the previously mentioned files are able to come together and communicate to one another. The user is also able to set Romi's base motor speed and adjust proportional-integral-derivative (PID) gain values in order to optomize Romi's performance for the game track.   
## **Game Track and Results**
### **Game Track and Strategy**

**Beginning: Start-Diamond**  
The game track requires IR sensors for a majority of the path. For our purposes, we started the game track by the use of line following with our IR sensor. We then hard coded our encoder values in the area right before the diamond path to get Romi to "turn off" line sensor mode. Once this new mode is started, Romi has been manually programmed to go forard at an effort of 30% for 1.5 seconds.   

**Path Following: Checkpoints 1-4**  
Once Checkpoint 1 is hit, Romi then goes back to line sensing mode until the grid portion at Checkpoint 4. During this stretch between checkpoints 1-4, Romi utilizes PID control in order to account for corrections and stay within the path of the black line.  

**Grid Portion: Checkpoints 4-5**  
Once at Checkpoint 4, we switched to using the IMU in order to track our heading to keep our Romi straight (180 degrees away from our start position heading). At this checkpoint, we then hardcoded encoder tick counts that allowed our robot to go straight until the end of the grid where it would then pivot to reach Checkpoint 5.  

**Last Stretch: Checkpoint 5-Finish**  
Once Romi pivots at Checkpoint 5, our IR Sensors task will start again and the line will be followed up until the bump sensors are pressed once Romi makes contact with the wall. Once here, Romi will then pivot clockwise 90 degrees, use encoder ticks to go straight until the 5s time deduction cup is hit, pivot counterclockwise 90 degrees, and use encoder ticks to go straight until a black line is read by our IR sensor. Once here, Romi will then rotate 90 degrees counterclockwise and use IR sensors until the finish line is reached.  

![Game Track](game_trackv3.png)

### **Results**
A video depicting our best run is shown here. Meanwhile, during lab, we presented 3 trials in front of our class to demonstrate our Romi's capabilities of being able to complete the game path. However, as shown in the following table, we were unable to complete any trial successfully.  

|Trial|Checkpoint 1|Checkpoint 2|Checkpoint 3|Checkpoint 4|Checkpoint 5|Total Time|Cups Hit|  
|-----|------------|------------|------------|------------|------------|----------|--------|
|1|0:00|0:00|0:00|0:00|0:00|0:00|0|
|2|0:00|0:00|0:00|0:00|0:00|0:00|0|
|3|0:00|0:00|0:00|0:00|0:00|0:00|0|





