import lgpio
import time

LED_PIN = 18

try:
    print("GPIO 테스트 시작...")
    h = lgpio.gpiochip_open(0)
    lgpio.gpio_claim_output(h, LED_PIN)
    
    print(f"GPIO {LED_PIN} 핀 제어 시작")
    
    for _ in range(10):  # 10번 반복
        print("HIGH")
        lgpio.gpio_write(h, LED_PIN, 1)
        time.sleep(1)
        print("LOW")
        lgpio.gpio_write(h, LED_PIN, 0)
        time.sleep(1)
        
except Exception as e:
    print(f"에러 발생: {e}")
finally:
    print("테스트 종료")
    lgpio.gpio_write(h, LED_PIN, 0)
    lgpio.gpiochip_close(h)
