# Fish Intelligence Mobile App (iOS + Android)

โปรเจกต์ Flutter สำหรับทำแอพ Fish Intelligence ที่ใช้งานได้ทั้ง iOS และ Android

## โครงระบบในแอพ (MVP ที่ต่อยอดได้)
- Auth State: login/logout flow ผ่าน `AuthState`
- Scan: capture/upload/quality gate/top-5 confidence + result detail
- Scan Service: รองรับทั้ง Mock และ HTTP API จริงผ่าน `ScanService`
- HTTP Scan: รองรับ Authorization header จาก auth token
- Scan State: ใช้ `provider` จัดการ loading/result/error/history
- History: เก็บประวัติผลสแกนจาก state + กดดูผลย้อนหลังแบบละเอียด
- Wiki: species detail + search
- Community: verify + expert + reputation
- Farm OS: pond/feed/water/health/finance
- Market: listing/matching/pricing/logistics
- Settings: privacy/notification/billing/data export

## Run (Mock)
```bash
cd fish_app
flutter run --dart-define=USE_MOCK_SCAN=true
```

## Run (Real API)
```bash
cd fish_app
flutter run \
  --dart-define=USE_MOCK_SCAN=false \
  --dart-define=API_BASE_URL=https://your-api-domain
```

## Test
```bash
flutter test
```
