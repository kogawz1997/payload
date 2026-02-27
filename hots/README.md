# VPN Helper Scanner (Educational Tool)

ภาษา: Python 3.10+

โปรเจกต์นี้เป็นเครื่องมือทดลองสำหรับค้นหา subdomain, ตรวจสอบการตอบสนองเบื้องต้น และสร้าง payload template สำหรับนำไปใช้ศึกษาโครงสร้างเครือข่ายและ HTTP/WebSocket handshake เท่านั้น

## การติดตั้ง

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

## การใช้งาน

```bash
python main.py
```

1. กรอกโดเมนหลัก เช่น `ais.co.th`
2. เลือกประเภทการสแกน (WebSocket / Direct)
3. (อัปชัน) ใส่ Proxy list ในช่องด้านบนรูปแบบ `ip:port,ip:port` ถ้าต้องการใช้งานผ่าน Proxy/Cloudflare
4. เลื่อน Timeout slider ระหว่าง 3–5 วินาที ตามที่ต้องการ
5. ถ้าต้องการใช้ลิสต์ host เอง:
   - กดปุ่ม `Load Sample` เพื่อโหลดลิสต์ตัวอย่างจากไฟล์ `sample_hosts.txt` (สามารถแก้ไขไฟล์นี้เองได้)
   - หรือวางลิสต์ host ทีละบรรทัดลงในช่อง `Custom hosts list` เอง
   - กดปุ่ม `Scan Custom List` เพื่อให้โปรแกรมเช็คว่าจากเน็ตของคุณ ติดต่อ host ไหนได้บ้าง
6. กดปุ่ม Scan Auto เพื่อให้โปรแกรม:
   - ดึง subdomain จาก crt.sh + brute force prefix ยอดนิยม
   - สแกนหลายเธรด พร้อม Multi-Port (80, 443, 8080, 8880)
   - แสดง log แบบ real-time พร้อมพอร์ตที่ตอบสนอง
   - สร้าง payload ตัวอย่างสำหรับ host ที่ตอบสนองดี
7. คลิกเลือก host จากผลลัพธ์ด้านขวาเพื่อสร้าง payload หรือกดปุ่ม Save Hosts เพื่อบันทึกเป็นไฟล์ข้อความ
8. ปุ่ม `Quick Net Test` ใช้ทดสอบอินเทอร์เน็ตของเครื่อง (latency และการเข้าถึงปลายทางสาธารณะพื้นฐาน) ก่อนสแกนจริง

> ใช้งานเพื่อการศึกษาเท่านั้น ห้ามสแกนหรือโจมตีระบบที่คุณไม่มีสิทธิ์อย่างชัดเจน

