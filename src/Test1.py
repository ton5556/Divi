from machine import Pin, PWM
import sys
import select

# ตั้งค่า PWM
MOTOR_PIN = 12
FREQ = 1000      # ความถี่ 1kHz
RESOLUTION = 255 # 8-bit (0-255)

motor = PWM(Pin(MOTOR_PIN), freq=FREQ)
motor.duty(0)

print("--- ESP32 Motor Control ---")
print("พิมพ์ตัวเลข 0 - 255 แล้วกด Enter เพื่อปรับความเร็ว:")

while True:
    # ตรวจสอบว่ามีข้อมูลจาก Serial หรือไม่
    if sys.stdin in select.select([sys.stdin], [], [], 0)[0]:
        line = sys.stdin.readline().strip()
        
        if line:
            try:
                speed_value = int(line)
                
                if 0 <= speed_value <= 255:
                    motor.duty(speed_value)
                    print("กำลังปรับความเร็วไปที่:", speed_value)
                else:
                    print("กรุณาใส่ตัวเลขระหว่าง 0 ถึง 255 เท่านั้น!")
                    
            except ValueError:
                print("กรุณาใส่ตัวเลขเท่านั้น!")
