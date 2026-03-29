# BUU Exam Schedule Sync (Serverless) 📅 🎓

ระบบเชื่อมต่อตารางสอบคณะวิทยาการสารสนเทศ มหาวิทยาลัยบูรพา เข้ากับปฏิทิน (Apple, Google, Outlook) อัตโนมัติแบบ **Real-time** ผ่าน Vercel Serverless Functions

## 🚀 จุดเด่นของระบบ
- **Real-time Sync**: ข้อมูลถูกดึงสดๆ จากระบบ `sms.informatics.buu.ac.th` ทุกครั้งที่มีการเรียกใช้
- **Clean URL**: ใช้งานง่ายเพียงแค่เติมรหัสนิสิตต่อท้าย URL
- **iCalendar (.ics) Support**: รองรับการใช้งานกับทุกอุปกรณ์ (iPhone, iPad, Mac, Android, Windows)
- **Zero Maintenance**: รันฟรีบน Vercel ไม่ต้องมี Server และไม่ต้องรอรันสคริปต์ตอนเช้า

---

## 🛠 วิธีใช้งาน (สำหรับนิสิต)

คุณสามารถเข้าถึงไฟล์ปฏิทินได้ทันทีผ่าน URL:
`https://<your-vercel-domain>.vercel.app/<รหัสนิสิต>`

**ตัวอย่าง:**
`https://sms-if-buu-sync.vercel.app/67160072`

### **ขั้นตอนการติดตั้งใน iPhone / iPad**
1. คัดลอก URL ด้านบน (ที่เปลี่ยนเป็นรหัสของคุณแล้ว)
2. ไปที่ **Settings (การตั้งค่า)** > **Calendar (ปฏิทิน)**
3. เลือก **Accounts (บัญชี)** > **Add Account (เพิ่มบัญชี)**
4. เลือก **Other (อื่นๆ)** > **Add Subscribed Calendar (เพิ่มปฏิทินที่สมัครรับ)**
5. วาง URL ลงในช่อง Server แล้วกด **Next** และ **Save**

### **ขั้นตอนการติดตั้งใน Mac**
1. เปิดแอพ **Calendar**
2. เลือกเมนู **File** > **New Calendar Subscription...**
3. วาง URL แล้วกด **Subscribe**

---

## 💻 สำหรับนักพัฒนา (Developer)

### **Stack ที่ใช้**
- **Language**: Python 3.10
- **Library**: `requests`, `beautifulsoup4`, `icalendar`, `pytz`
- **Infrastructure**: Vercel Serverless Functions

### **โครงสร้างโฟลเดอร์**
- `api/index.py`: ตัวจัดการคำขอ HTTP และลอจิก Serverless
- `scraper.py`: ส่วนการดึงข้อมูลจากเว็บไซต์มหาลัย
- `calendar_gen.py`: ส่วนการแปลงข้อมูลเป็นรูปแบบ `.ics`
- `vercel.json`: การตั้งค่า Clean URL และ Routing
- `public/`: เก็บหน้า Landing Page สำหรับคำแนะนำการใช้งาน

### **การติดตั้งเพื่อพัฒนาต่อ**
1. Clone repository
2. ติดตั้ง dependencies: `pip install -r requirements.txt`
3. รัน Vercel dev สำหรับทดสอบ: `vercel dev`

---

## ⚖️ License
โปรเจกต์นี้สร้างขึ้นเพื่ออำนวยความสะดวกแก่นิสิตคณะวิทยาการสารสนเทศ มหาวิทยาลัยบูรพา ห้ามนำไปใช้ในเชิงพาณิชย์

**Developed by:** [TAHPAPANGKORN](https://github.com/TAHPAPANGKORN)
