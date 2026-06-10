import cv2
import math
from ctypes import cast, POINTER
from comtypes import CoInitialize
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

try:
    from mediapipe.python.solutions import hands as mp_hands
    from mediapipe.python.solutions import drawing_utils as mp_drawing
except ImportError:
    from mediapipe import solutions as mp_sol
    mp_hands = mp_sol.hands
    mp_drawing = mp_sol.drawing_utils


cap = cv2.VideoCapture(0)


hands = mp_hands.Hands(
    static_image_mode=False,
    max_num_hands=1,
    min_detection_confidence=0.7,
    min_tracking_confidence=0.5
)
drawing = mp_drawing


try:
    CoInitialize()
    devices = AudioUtilities.GetSpeakers()
    
    volume = devices.EndpointVolume
    if volume is None:
        raise RuntimeError("EndpointVolume bulunamadı")
    
    volume_range = volume.GetVolumeRange()
    min_vol = volume_range[0]
    max_vol = volume_range[1]
    print(f"Ses kontrol hazır! Volume range: {min_vol}dB - {max_vol}dB")
except Exception as e:
    volume = None
    min_vol = -65.0
    max_vol = 0.0
    print(f"Ses kontrol cihazı bulunamadı! Hata: {e}")

# Başlangıç ayarları
prev_distance = 0
smoothing_factor = 0.5

# Ses kontrol modu için değişkenler
control_active = False  # Ses kontrolü aktif mi?
tap_count = 0  # Temas sayısı
last_tap_time = 0  # Son temas zamanı
is_touching = False  # Şu an parmaklar temas halinde mi?
touch_threshold = 30  # Temas mesafe eşiği (piksel)
tap_timeout = 1.0  # Temaslar arası maksimum süre (saniye)
locked_volume = None  # Kilitlenen ses seviyesi
import time

print("Kamera açılıyor...")
print("Başparmak + orta parmağı 2 kez değdirerek ses kontrolünü aç/kapat.")
print("Çıkış için 'q' tuşuna basın.")

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # 'q' tuşu kontrolü - frame okumadan hemen sonra
    key = cv2.waitKey(1) & 0xFF
    if key == ord('q') or key == 27:  # q veya ESC
        print("Çıkış yapılıyor...")
        break
    
    # Görüntüyü döndür (selfie kamerası için)
    frame = cv2.flip(frame, 1)
    h, w, c = frame.shape
    
    # MediaPipe işleme
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(rgb_frame)
    
    if results.multi_hand_landmarks:
        hand_landmarks = results.multi_hand_landmarks[0]
        
        # Başparmak (thumb), işaret (index) ve orta parmak (middle) uç noktaları
        thumb_finger = hand_landmarks.landmark[4]   # THUMB_TIP
        index_finger = hand_landmarks.landmark[8]   # INDEX_FINGER_TIP
        middle_finger = hand_landmarks.landmark[12] # MIDDLE_FINGER_TIP
        
        # Piksel koordinatlarına çevir
        thumb_pos = (int(thumb_finger.x * w), int(thumb_finger.y * h))
        index_pos = (int(index_finger.x * w), int(index_finger.y * h))
        middle_pos = (int(middle_finger.x * w), int(middle_finger.y * h))
        
        # Mod tetikleme için başparmak-orta mesafesi
        touch_distance = math.sqrt((thumb_pos[0] - middle_pos[0])**2 + (thumb_pos[1] - middle_pos[1])**2)
        # Ses ayarı için başparmak-işaret mesafesi
        volume_distance = math.sqrt((thumb_pos[0] - index_pos[0])**2 + (thumb_pos[1] - index_pos[1])**2)
        
        # Temas algılama ve sayma
        current_time = time.time()
        if touch_distance < touch_threshold:
            # Parmaklar temas halinde
            if not is_touching:
                is_touching = True
                # Yeni temas başladı
                if current_time - last_tap_time < tap_timeout:
                    tap_count += 1
                else:
                    tap_count = 1
                last_tap_time = current_time
                print(f"Temas {tap_count}")
                
                # 2 temas olduğunda modu değiştir
                if tap_count >= 2:
                    control_active = not control_active
                    tap_count = 0
                    if control_active:
                        print("✓ Ses kontrolü AKTİF - Parmakları aç/kapa")
                        locked_volume = None
                    else:
                        print("✗ Ses kontrolü KAPALI")
        else:
            # Parmaklar ayrı
            if is_touching:
                is_touching = False
                # Eğer kontrol aktifse ve ses ayarı yapılmışsa, sesi kilitle
                if control_active and locked_volume is None:
                    locked_volume = None  # Şu an için serbest bırak
        
        # Mesafeyi yumuşat (smoothing)
        if prev_distance != 0:
            volume_distance = smoothing_factor * volume_distance + (1 - smoothing_factor) * prev_distance
        prev_distance = volume_distance
        
        # Ses seviyesini ayarla - sadece kontrol aktifse
        if control_active and not is_touching:
            # Mesafeyi ses seviyesine dönüştür (0-100)
            min_distance = 30
            max_distance = 150
            volume_level = max(0, min(100, (volume_distance - min_distance) / (max_distance - min_distance) * 100))
            
            # Ses seviyesini ayarla
            if volume is not None and locked_volume is None:
                try:
                    # Volume level'ı dB'ye çevir
                    volume_db = min_vol + (volume_level / 100) * (max_vol - min_vol)
                    volume.SetMasterVolumeLevel(volume_db, None)
                except Exception as e:
                    pass
        else:
            # Kontrol aktif değilse mevcut sesi göster
            if volume is not None:
                try:
                    current_vol_db = volume.GetMasterVolumeLevel()
                    volume_level = ((current_vol_db - min_vol) / (max_vol - min_vol)) * 100
                except:
                    volume_level = 0
            else:
                volume_level = 0
        
        # Ekranda bilgi göster
        status = "AKTIF ✓" if control_active else "KAPALI ✗"
        color = (0, 255, 0) if control_active else (0, 0, 255)
        
        cv2.putText(frame, f"Mod: {status}", (10, 30), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, color, 2)
        cv2.putText(frame, f"Ses Mesafe: {int(volume_distance)}", (10, 60), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
        cv2.putText(frame, f"Ses: {int(volume_level)}%", (10, 90), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
        
        # Temas durumunu göster
        if is_touching:
            cv2.putText(frame, "TEMAS!", (10, 120), 
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2)
        
        # Parmakları çizimle göster
        thumb_color = (255, 0, 0) if not is_touching else (0, 255, 255)
        index_color = (0, 255, 0)
        middle_color = (255, 0, 255) if not is_touching else (0, 255, 255)
        line_color = (0, 0, 255) if not is_touching else (0, 255, 255)
        
        cv2.circle(frame, thumb_pos, 10, thumb_color, -1)
        cv2.circle(frame, index_pos, 10, index_color, -1)
        cv2.circle(frame, middle_pos, 10, middle_color, -1)
        # Ses ayarı çizgisi: başparmak-işaret
        cv2.line(frame, thumb_pos, index_pos, (0, 255, 0), 2)
        # Mod tetikleme çizgisi: başparmak-orta
        cv2.line(frame, thumb_pos, middle_pos, line_color, 3)
        
        # Elini çizimle göster
        drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
    
    # Görüntüyü göster
    cv2.imshow('Devonic - Ses Kontrolu', frame)

# Kapat
cap.release()
cv2.destroyAllWindows()
hands.close()
print("Program kapatıldı.")
