from machine import Pin, PWM
import sys
import select

motor = None
current_pin = None
current_freq = None
current_duty = None

def read_serial():
    if sys.stdin in select.select([sys.stdin], [], [], 0)[0]:
        return sys.stdin.readline().strip()
    return None

def stop_motor():
    global motor
    if motor:
        motor.duty(0)
        motor.deinit()
        motor = None

def ask_pin():
    print("\n=== ตั้งค่าใหม่ ===")
    print("กรุณาใส่หมายเลข Pin (เช่น 12):")

def ask_freq():
    print("กรุณาใส่ความถี่ Hz (เช่น 1000):")

def ask_duty():
    print("กรุณาใส่ Duty Cycle 0-255:")

# State machine
STATE_PIN  = 0
STATE_FREQ = 1
STATE_DUTY = 2
STATE_RUN  = 3

state = STATE_PIN
ask_pin()

while True:
    line = read_serial()
    
    if line is not None:
        # กด e เพื่อรีเซ็ตได้ทุกสถานะ
        if line.lower() == 'e':
            stop_motor()
            current_pin  = None
            current_freq = None
            current_duty = None
            state = STATE_PIN
            print("\n🔄 รีเซ็ตค่าทั้งหมดแล้ว!")
            ask_pin()
            continue
        
        if state == STATE_PIN:
            try:
                pin_num = int(line)
                if 0 <= pin_num <= 39:
                    current_pin = pin_num
                    state = STATE_FREQ
                    print(f"✅ Pin = {current_pin}")
                    ask_freq()
                else:
                    print("❌ Pin ต้องอยู่ระหว่าง 0-39 กรุณาใส่ใหม่:")
            except ValueError:
                print("❌ กรุณาใส่ตัวเลขเท่านั้น!")

        elif state == STATE_FREQ:
            try:
                freq_val = int(line)
                if 1 <= freq_val <= 40000:
                    current_freq = freq_val
                    state = STATE_DUTY
                    print(f"✅ ความถี่ = {current_freq} Hz")
                    ask_duty()
                else:
                    print("❌ ความถี่ต้องอยู่ระหว่าง 1-40000 Hz กรุณาใส่ใหม่:")
            except ValueError:
                print("❌ กรุณาใส่ตัวเลขเท่านั้น!")

        elif state == STATE_DUTY:
            try:
                duty_val = int(line)
                if 0 <= duty_val <= 255:
                    current_duty = duty_val
                    
                    # สร้าง PWM ด้วยค่าที่กรอก
                    stop_motor()
                    motor = PWM(Pin(current_pin), freq=current_freq)
                    motor.duty(current_duty)
                    
                    state = STATE_RUN
                    print(f"✅ Duty Cycle = {current_duty}")
                    print(f"\n🚀 มอเตอร์ทำงานที่ Pin={current_pin}, Freq={current_freq}Hz, Duty={current_duty}")
                    print("พิมพ์ตัวเลข 0-255 เพื่อเปลี่ยน Duty | พิมพ์ e เพื่อรีเซ็ต")
                else:
                    print("❌ Duty Cycle ต้องอยู่ระหว่าง 0-255 กรุณาใส่ใหม่:")
            except ValueError:
                print("❌ กรุณาใส่ตัวเลขเท่านั้น!")

        elif state == STATE_RUN:
            try:
                duty_val = int(line)
                if 0 <= duty_val <= 255:
                    current_duty = duty_val
                    motor.duty(current_duty)
                    print(f"⚡ ปรับ Duty Cycle เป็น: {current_duty}")
                else:
                    print("❌ กรุณาใส่ 0-255 เท่านั้น!")
            except ValueError:
                print("❌ กรุณาใส่ตัวเลขเท่านั้น!")
