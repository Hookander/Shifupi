import RPi.GPIO as GPIO
import time

in1_middle = 17
in2_middle = 18
in3_middle = 27
in4_middle = 22

in1_ring = 23
in2_ring = 24
in3_ring = 25
in4_ring = 21


# careful lowering this, at some point you run into the mechanical limitation of how quick your motor can move
step_sleep = 0.0008

step_count_middle = 4096 # 5.625*(1/64) per step, 4096 steps is 360°
step_count_ring = 4096 # 5.625*(1/64) per step, 4096 steps is 360°

direction = False # True for clockwise, False for counter-clockwise
#direction_ring = False # True for clockwise, False for counter-clockwise


# defining stepper motor sequence (found in documentation http://www.4tronix.co.uk/arduino/Stepper-Motors.php)
step_sequence = [[1,0,0,1],
                 [1,0,0,0],
                 [1,1,0,0],
                 [0,1,0,0],
                 [0,1,1,0],
                 [0,0,1,0],
                 [0,0,1,1],
                 [0,0,0,1]]


# setting up
GPIO.setmode( GPIO.BCM )
GPIO.setup( in1_middle, GPIO.OUT )
GPIO.setup( in2_middle, GPIO.OUT )
GPIO.setup( in3_middle, GPIO.OUT )
GPIO.setup( in4_middle, GPIO.OUT )

GPIO.setup( in1_ring, GPIO.OUT )
GPIO.setup( in2_ring, GPIO.OUT )
GPIO.setup( in3_ring, GPIO.OUT )
GPIO.setup( in4_ring, GPIO.OUT )

# initializing
GPIO.output( in1_middle, GPIO.LOW )
GPIO.output( in2_middle, GPIO.LOW )
GPIO.output( in3_middle, GPIO.LOW )
GPIO.output( in4_middle, GPIO.LOW )

GPIO.output( in1_ring, GPIO.LOW )
GPIO.output( in2_ring, GPIO.LOW )
GPIO.output( in3_ring, GPIO.LOW )
GPIO.output( in4_ring, GPIO.LOW )

motor_pins_middle = [in1_middle,in2_middle,in3_middle,in4_middle]
motor_step_counter = 0

motor_pins_ring = [in1_ring,in2_ring,in3_ring,in4_ring]
#motor_step_counter_ring = 0 ;

def cleanup():
    GPIO.output( in1_middle, GPIO.LOW )
    GPIO.output( in2_middle, GPIO.LOW )
    GPIO.output( in3_middle, GPIO.LOW )
    GPIO.output( in4_middle, GPIO.LOW )
    
    GPIO.output( in1_ring, GPIO.LOW )
    GPIO.output( in2_ring, GPIO.LOW )
    GPIO.output( in3_ring, GPIO.LOW )
    GPIO.output( in4_ring, GPIO.LOW )
    GPIO.cleanup()

# the meat
try:
    i = 0
    for i in range(step_count_middle):
        for pin in range(0, len(motor_pins_middle)):
            GPIO.output( motor_pins_middle[pin], step_sequence[motor_step_counter][pin] )
            GPIO.output( motor_pins_ring[pin], step_sequence[motor_step_counter][pin] )    
        if direction==True:
            motor_step_counter = (motor_step_counter - 1) % 8
        elif direction==False:
            motor_step_counter = (motor_step_counter+ 1) % 8
        else: # defensive programming
            print( "uh oh... direction should *always* be either True or False" )
            cleanup()
            exit( 1 )
        time.sleep( step_sleep )

except KeyboardInterrupt:
    cleanup()
    exit( 1 )

cleanup()
exit( 0 )