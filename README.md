# Fish Intelligence Platform — Master Spec (ตามลิสต์ครบ + ใช้ทำระบบจริงได้)

เอกสารนี้เป็น **System Specification** สำหรับสร้างแพลตฟอร์ม Fish Intelligence แบบครบวงจร รองรับการแตกเป็น:
- Mobile App
- Web App
- Admin Web
- SaaS Platform
- API Platform

—

## 0) Core Flow ของแพลตฟอร์ม

`Scan → Identify → Verify → Learn → Farm Manage → Sell → Analyze → API / Government / Enterprise`

—

## 1) Mobile App สำหรับผู้ใช้ทั่วไป

### 1.1 ระบบบัญชี
- สมัครสมาชิก
- Login Google / Apple / เบอร์โทร
- Guest Mode
- โปรไฟล์ผู้ใช้
- ประวัติการสแกน
- ระดับผู้ใช้ / Badge
- ตั้งค่าความเป็นส่วนตัว
- ลบบัญชี

### 1.2 ระบบสแกนสัตว์น้ำ
- ถ่ายรูปจากกล้อง
- อัปโหลดจากเครื่อง
- ถ่ายหลายมุม
- ตรวจรูปเบลอ
- ตรวจแสงมืด/สว่างเกิน
- ครอปตัวปลาอัตโนมัติ
- AI แยกชนิดปลา
- AI แยกกุ้ง/ปู/หอย/พืชน้ำ
- แสดง Top 5 ผลลัพธ์
- แสดงเปอร์เซ็นต์ความมั่นใจ
- เตือนเมื่อ AI ไม่มั่นใจ
- แนะนำให้ถ่ายเพิ่มมุมหัว/หาง/ครีบ

### 1.3 หน้าผลลัพธ์
- ชื่อไทย / ชื่ออังกฤษ / ชื่อวิทยาศาสตร์
- ความมั่นใจของ AI
- รูปเปรียบเทียบ
- ลักษณะเด่น
- แหล่งที่พบ
- กินได้ไหม
- มีพิษไหม
- สถานะอนุรักษ์
- กฎหมายที่เกี่ยวข้อง
- ปุ่ม “AI ตอบผิด”
- ปุ่ม “ส่งให้ผู้เชี่ยวชาญตรวจ”

—

## 2) ระบบ Fish Wiki / ฐานข้อมูลปลา

### 2.1 Species Database
- ชื่อไทย / ชื่อท้องถิ่น / ชื่ออังกฤษ / ชื่อวิทยาศาสตร์
- หมวดหมู่
- น้ำจืด/น้ำเค็ม/น้ำกร่อย
- จังหวัดที่พบ
- ฤดูที่พบ
- ขนาดโตเต็มวัย
- น้ำหนักเฉลี่ย
- พฤติกรรม
- อาหาร
- การสืบพันธุ์
- ความเสี่ยงต่อคน
- ความเสี่ยงต่อระบบนิเวศ

### 2.2 ระบบค้นหา
- ค้นหาด้วยชื่อ
- ค้นหาด้วยรูป
- ค้นหาด้วยสี
- ค้นหาด้วยรูปร่าง
- ค้นหาตามจังหวัด
- ค้นหาตามแหล่งน้ำ
- ค้นหาชนิดคล้ายกัน

### 2.3 ระบบเปรียบเทียบ
- เทียบปลา 2-4 ชนิด
- จุดต่างของหัว / ปาก / ครีบ / หาง / ลายตัว / ถิ่นอาศัย

—

## 3) ระบบ AI Core

### 3.1 Computer Vision AI
- Species Classification
- Object Detection
- Segmentation
- Similarity Search
- Disease Detection
- Freshness Detection
- Size Estimation
- Weight Estimation
- Quality Grade A/B/C

### 3.2 Context AI
- ใช้ GPS ช่วยตัดตัวเลือก
- ใช้จังหวัดช่วยประเมิน
- ใช้ประเภทน้ำช่วยกรอง
- ใช้ฤดูกาลช่วยเดา
- ใช้ขนาดปลาช่วยแยกชนิด
- ใช้ประวัติพื้นที่ช่วยเพิ่มความแม่น

### 3.3 Confidence System
- คะแนนความมั่นใจ
- ระดับความเสี่ยงคำตอบ
- ตอบ “ไม่แน่ใจ” ได้
- ขอรูปเพิ่มได้
- ส่งเข้า human review อัตโนมัติ
- กัน AI มั่วแบบมั่นหน้า

### 3.4 Model Management
- Model Version
- Model Registry
- A/B Testing
- Shadow Testing
- Rollback Model
- Accuracy Per Species
- Confusion Matrix
- Error Queue
- Retraining Pipeline

—

## 4) ระบบ Dataset / Training

### 4.1 Image Dataset
- เก็บรูปจากผู้ใช้
- เก็บรูปจาก expert
- เก็บรูปจากแหล่งเปิด
- แยก train/validation/test
- ลบรูปซ้ำ
- ตรวจรูปคุณภาพต่ำ
- ตรวจภาพสแปม
- Blur ข้อมูลส่วนตัว

### 4.2 Labeling System
- Label ชนิดสัตว์น้ำ
- Label อวัยวะปลา (หัว หาง ครีบ เกล็ด)
- Label โรค
- Label ขนาด
- Label แหล่งน้ำ
- Label ความสด
- Label โดย crowd
- Label โดย expert
- Label final โดย admin

### 4.3 Data Versioning
- Dataset version
- Label version
- Source tracking
- Consent tracking
- Audit log
- Export dataset
- Import dataset

—

## 5) ระบบ Community Verification

### 5.1 ระบบยืนยันผล
- ผู้ใช้ส่งเคสให้ชุมชน
- โหวตชนิดปลา
- คอมเมนต์เหตุผล
- แนบรูปเปรียบเทียบ
- Expert ยืนยันคำตอบสุดท้าย
- สถานะ: รอตรวจ / โหวตอยู่ / ยืนยันแล้ว / ไม่แน่ใจ

### 5.2 Reputation
- แต้มความแม่นยำ
- Badge
- Level
- น้ำหนักโหวตตามความน่าเชื่อถือ
- ลงโทษคนตอบมั่ว
- ประวัติการยืนยัน

### 5.3 Moderation
- รายงานรูปไม่เหมาะสม
- รายงานข้อมูลผิด
- รายงานสแปม
- ซ่อนโพสต์
- Ban user
- Appeal ban

—

## 6) ระบบ Expert

### 6.1 Expert Profile
- สมัครเป็นผู้เชี่ยวชาญ
- แนบเอกสาร/ผลงาน
- สาขาความเชี่ยวชาญ
- ประวัติการตรวจ
- คะแนนความแม่น
- ค่าบริการตรวจเคส
- Verified Badge

### 6.2 Expert Workbench
- คิวเคสรอตรวจ
- ตรวจชนิดปลา
- ตรวจโรคปลา
- ตรวจข้อมูล Wiki
- แก้ Label
- ให้เหตุผลประกอบ
- แนบเอกสารอ้างอิง
- ปิดเคส

### 6.3 Expert Payment
- รายได้ต่อเคส
- ถอนเงิน
- ประวัติรายรับ
- Revenue Share
- ใบเสร็จ/ภาษี

—

## 7) ระบบแผนที่ / Geo Intelligence

### 7.1 Observation Map
- จุดพบสัตว์น้ำ
- Heatmap
- กรองตามชนิด / จังหวัด / ฤดู / ประเภทน้ำ / สถานะยืนยัน

### 7.2 Privacy Map
- ซ่อนพิกัดจริงโดย default
- แสดงระดับอำเภอ/จังหวัด
- ป้องกันสัตว์หายากถูกล่า
- ตั้งค่าความละเอียดของตำแหน่ง
- Anti-poaching rule

### 7.3 Geo Analytics
- แนวโน้มการพบปลา
- Species migration
- Invasive species alert
- พื้นที่เสี่ยงโรคระบาด
- พื้นที่น้ำเสื่อมโทรม
- Seasonal prediction

—

## 8) ระบบ Farm OS

### 8.1 Farm Account
- สร้างฟาร์ม
- สมาชิกในฟาร์ม
- สิทธิ์แต่ละคน
- หลายฟาร์มต่อบัญชี
- โปรไฟล์ฟาร์ม
- เอกสารฟาร์ม

### 8.2 Pond Management
- เพิ่มบ่อ
- ขนาดบ่อ
- ประเภทบ่อ
- ปริมาณน้ำ
- ชนิดปลา
- จำนวนปลาตั้งต้น
- วันที่ลงปลา
- รอบการเลี้ยง
- สถานะบ่อ

### 8.3 Feeding System
- ตารางให้อาหาร
- บันทึกอาหาร
- ปริมาณอาหาร
- ประเภทอาหาร
- ต้นทุนอาหาร
- FCR
- แจ้งเตือนให้อาหาร
- AI แนะนำปริมาณอาหาร

### 8.4 Water Quality
- pH / DO / อุณหภูมิ / แอมโมเนีย / ไนไตรท์ / ความเค็ม / ความขุ่น
- บันทึกย้อนหลัง
- กราฟ
- แจ้งเตือนค่าเสี่ยง
- เชื่อม IoT Sensor

### 8.5 Fish Health
- บันทึกปลาตาย
- อัตรารอด
- AI ตรวจโรคจากภาพ
- บันทึกอาการ
- ประวัติการรักษา
- ยาที่ใช้
- แจ้งเตือนโรคระบาด
- ส่ง Expert ตรวจ

### 8.6 Growth & Harvest
- น้ำหนักเฉลี่ย
- ขนาดเฉลี่ย
- อัตราโต
- คาดการณ์วันจับขาย
- คาดการณ์ผลผลิต
- Harvest plan
- Yield report

### 8.7 Farm Finance
- ต้นทุนลูกปลา / อาหาร / ยา / ค่าแรง / ค่าไฟ / ค่าน้ำ
- รายรับ
- กำไรต่อรอบ
- กำไรต่อบ่อ
- รายงาน PDF/Excel

—

## 9) ระบบ Marketplace

### 9.1 Seller
- ฟาร์มลงขายปลา
- จำนวนกิโล
- ขนาดปลา
- ราคา
- วันที่พร้อมส่ง
- รูปสินค้า
- ใบรับรอง
- สถานะสินค้า

### 9.2 Buyer
- ร้านอาหาร / ตลาด / โรงงาน / ผู้ค้าส่ง
- ค้นหาสินค้า
- ต่อรองราคา
- สั่งซื้อ
- รีวิวผู้ขาย

### 9.3 Matching Engine
- จับคู่ฟาร์มกับผู้ซื้อ
- คำนวณระยะทาง
- เทียบราคา
- เทียบปริมาณ
- แนะนำดีลที่เหมาะสุด
- ลดการขายผ่านคนกลาง

### 9.4 Price Intelligence
- ราคากลางรายวัน
- ราคาตามจังหวัด
- ราคาตามตลาด
- กราฟย้อนหลัง
- Forecast ราคา
- แจ้งเตือนราคาดี
- แนะนำขาย/รอขาย

—

## 10) ระบบ Logistics

### 10.1 Delivery
- จองรถขนส่ง
- ประเภทขนส่ง
- ระยะทาง
- ค่าขนส่ง
- สถานะจัดส่ง
- Tracking
- Proof of delivery

### 10.2 Cold Chain
- อุณหภูมิระหว่างขนส่ง
- แจ้งเตือนอุณหภูมิผิดปกติ
- ภาพรับของ/ส่งของ
- Quality check ตอนรับสินค้า

### 10.3 Partner Driver
- สมัครคนขับ
- ตรวจเอกสาร
- รับงาน
- รายได้
- Rating

—

## 11) ระบบ Research / Government / Enterprise

### 11.1 Research Dashboard
- Export observation
- Export species dataset
- Export map data
- Filter by date/location/species
- API access
- Citation-ready report

### 11.2 Government Dashboard
- ความหลากหลายทางชีวภาพ
- สัตว์น้ำหายาก
- Invasive species
- Illegal species report
- พื้นที่เสี่ยงโรค
- แผนที่เชิงนโยบาย

### 11.3 Enterprise
- Private workspace
- Private dataset
- Custom model
- SLA
- Team management
- Audit logs
- API quota

—

## 12) ระบบ Admin Panel

### 12.1 Dashboard
- ผู้ใช้ทั้งหมด
- จำนวนสแกน
- Accuracy
- เคสผิดพลาด
- เคสรอตรวจ
- รายได้
- Active farms
- Marketplace volume
- System health

### 12.2 User Management
- จัดการผู้ใช้
- Role
- Permission
- Ban/Suspend
- KYC expert
- KYC seller
- Audit user action

### 12.3 Species Management
- เพิ่มชนิดปลา
- แก้ไขข้อมูล
- จัดการรูป
- จัดการชื่อท้องถิ่น
- จัดการข้อมูลกฎหมาย
- Publish/Unpublish
- Revision history

### 12.4 AI Management
- ดู prediction log
- ดู model accuracy
- ดู species ที่พลาดบ่อย
- ตั้ง threshold
- ส่งเคสเข้า labeling
- Deploy model
- Rollback model

### 12.5 Content Management
- บทความ
- ข่าวสาร
- คู่มือฟาร์ม
- Disease guide
- FAQ
- Banner
- Notification campaign

### 12.6 Marketplace Management
- ตรวจสินค้า
- ตรวจผู้ขาย
- จัดการคำสั่งซื้อ
- จัดการข้อพิพาท
- Refund
- Commission

—

## 13) ระบบ Payment / Billing

### 13.1 Subscription
- Free
- Pro User
- Farm Pro
- Expert Pro
- Enterprise
- Government Plan

### 13.2 Payment
- PromptPay
- QR Payment
- Credit/Debit Card
- Bank Transfer
- Wallet
- Invoice
- Receipt

### 13.3 Commission
- ค่าคอม marketplace
- ค่าตรวจ expert
- ค่าบริการ API
- Revenue share
- Payout

—

## 14) ระบบ Notification
- Push notification
- Email
- SMS/OTP
- LINE Notify/LINE OA
- แจ้งผลสแกน
- แจ้ง Expert ตอบแล้ว
- แจ้งน้ำเสี่ยง
- แจ้งปลาเริ่มป่วย
- แจ้งราคาดี
- แจ้งคำสั่งซื้อ
- แจ้งขนส่ง
- แจ้ง subscription

—

## 15) ระบบ Security / Privacy

### 15.1 Security
- JWT/Auth session
- MFA
- Rate limit
- Device management
- API key management
- Abuse detection
- Image spam detection
- Audit log
- Backup
- Disaster recovery

### 15.2 Privacy
- Consent การใช้รูปไปเทรน AI
- ลบข้อมูลส่วนตัว
- Blur metadata
- ซ่อนพิกัด
- Data retention policy
- PDPA compliance
- Export my data

—

## 16) ระบบ API Platform

### 16.1 Public API
- Species search
- Species detail
- Image predict
- Observation submit
- Fish Wiki API

### 16.2 Farm API
- Pond API
- Feeding API
- Water API
- Health API
- Finance API

### 16.3 Enterprise API
- Batch prediction
- Dataset export
- Geo analytics
- Model metrics
- Private API key
- Usage billing

—

## 17) ระบบหน้าเว็บ

### 17.1 Public Website
- หน้าแรก
- แนะนำแอพ
- Fish Wiki
- Pricing
- Blog
- Contact
- Download app
- Partner page

### 17.2 Web App
- Dashboard
- Scan upload
- History
- Wiki
- Community
- Map
- Farm OS
- Marketplace
- Billing
- Settings

### 17.3 Admin Web
- Admin Dashboard
- User
- Species
- AI
- Dataset
- Expert
- Farm
- Marketplace
- Payment
- Report
- System

—

## 18) โครง Role / Permission
- Guest: สแกนจำกัด, ดู Wiki
- User: สแกน, บันทึก, โหวต
- Pro User: สแกนเพิ่ม, history, export
- Farmer: ใช้ Farm OS
- Farm Manager: จัดการบ่อ/ทีม/รายงาน
- Buyer: ซื้อปลาในตลาด
- Seller: ลงขายสินค้า
- Expert: ตรวจเคส/แก้ label
- Researcher: export data
- Government: dashboard เชิงนโยบาย
- Admin: คุมระบบทั้งหมด
- Super Admin: คุม billing/security/model

—

## 19) ระบบแพ็กเกจ

### Free
- สแกนจำกัด
- ดู Wiki
- โหวตชุมชน
- ประวัติจำกัด

### Pro
- สแกนมากขึ้น
- วิเคราะห์หลายภาพ
- Export
- ไม่มีโฆษณา

### Farm Pro
- จัดการบ่อ
- น้ำ/อาหาร/สุขภาพ
- ต้นทุนกำไร
- รายงาน

### Market Pro
- ลงขายสินค้า
- ดูราคากลาง
- Buyer matching
- Boost listing

### Expert
- รับเคสตรวจ
- Workbench
- รายได้
- Profile verified

### Enterprise
- API
- Private dataset
- Team
- Dashboard
- SLA

—

## 20) Roadmap ทำจริง
- **Phase 1: MVP** — Login, Scan AI, Top 5 confidence, Fish Wiki, History, Report wrong answer, Admin Species
- **Phase 2: Community + Expert** — Community verify, Expert workbench, Reputation, Labeling queue, Dataset version
- **Phase 3: Farm OS** — Farm/Pond, Feeding, Water, Health, Finance, Reports
- **Phase 4: Market** — Seller listing, Buyer order, Price intelligence, Matching, Payment
- **Phase 5: Enterprise** — API, Government dashboard, Research export, Private model, Advanced analytics

—

## 21) จุดที่ทำให้เหนือกว่าชัด ๆ
- ไม่ใช่แค่สแกนปลา แต่เป็น Fish Operating System
- AI มีความมั่นใจและยอมรับว่าไม่รู้
- มี Expert ตรวจจริง
- มี Community ช่วยสอน AI
- มีระบบฟาร์มที่เกษตรกรใช้หาเงินได้
- มี Marketplace ที่ต่อยอดเป็นรายได้
- มีข้อมูลแผนที่/วิจัย/ภาครัฐ
- มี API ขายต่อได้
- มี Dataset Loop ทำให้ระบบฉลาดขึ้นเรื่อย ๆ
