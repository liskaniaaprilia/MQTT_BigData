```
Nama : Liskania Aprilia
Nim : 312210383
Kelas : TI.22.C.3
Mata Kuliah : Big Data
```

Tugas : 

1. Buat MQTT server untuk routing topic
2. Buat database untuk save data
3. Buat dummy service untuk service data sensor
4. Semua hal diatas kemudian bungkus dalam docker
5. Konfigurasi docker untuk network routingnya

# Membuat MQTT Server untuk Routing Topic

### 1. Buat folder proyek utama:  
   Misalnya, di direktori `~/Project_Big_Data`.

### 2. Buat folder untuk MQTT:  
   Di dalam proyek, buat folder `mqtt/`:
   ```bash
   mkdir -p ~/Project_Big_Data/mqtt
   ```

### 3. Buat file `Dockerfile` untuk Mosquitto di dalam folder `mqtt/`:
   - Isi dengan:
     ```Dockerfile
     FROM eclipse-mosquitto:latest
     COPY mosquitto.conf /mosquitto/config/mosquitto.conf
     EXPOSE 1883
     CMD ["/usr/sbin/mosquitto", "-c", "/mosquitto/config/mosquitto.conf"]
     ```

### 4. Buat file `mosquitto.conf` di dalam folder `mqtt/`:
   - Isi file `mosquitto.conf` dengan pengaturan broker, misalnya:
     ```
     listener 1883
     allow_anonymous true
     ```

# Membuat database untuk save data

### 1. Buat folder untuk database:  
   Misalnya, `~/Project_Big_Data/database/`.

### 2. Gunakan image MongoDB standar dari Docker

sehingga Anda tidak perlu membuat `Dockerfile` sendiri untuk database. Image ini akan digunakan di file `docker-compose.yml` nanti.

# Buat dummy service untuk service data sensor

### 1. Buat folder untuk dummy service:  
   Misalnya, `~/Project_Big_Data/dummy_service/`.

### 2. Buat file `dummy_service.py` di dalam folder `dummy_service/`:
   - Script ini akan mengirim data sensor ke MQTT:

     ```python
     import paho.mqtt.client as mqtt
     import random
     import time

     def publish_sensor_data():
         client = mqtt.Client()
         client.connect("mqtt", 1883, 60)
         while True:
             sensor_value = random.uniform(20.0, 30.0)
             client.publish("sensor/data", sensor_value)
             time.sleep(5)

     if __name__ == "__main__":
         publish_sensor_data()
     ```

### 3. Buat file `Dockerfile` untuk dummy service di dalam folder `dummy_service/`:

   - Isi dengan:

     ```Dockerfile
     FROM python:3.9-slim
     WORKDIR /app
     COPY . .
     RUN pip install paho-mqtt
     CMD ["python", "dummy_service.py"]
     ```

# Semua hal diatas kemudian bungkus dalam docker

Setelah semua komponen siap, Anda bisa membungkus semuanya dalam Docker menggunakan **Docker Compose**.

### 1. Buat file `docker-compose.yml` di folder proyek utama `~/Project_Big_Data/`:

   - Isi dengan:

     ```yaml
     version: '3'
     services:
       mqtt:
         build: ./mqtt
         ports:
           - "1883:1883"
         networks:
           - sensor_net

       database:
         image: mongo
         ports:
           - "27017:27017"
         volumes:
           - ./data:/data/db
         networks:
           - sensor_net

       dummy_service:
         build: ./dummy_service
         depends_on:
           - mqtt
         networks:
           - sensor_net

     networks:
       sensor_net:
         driver: bridge
     ```

### 2. Struktur folder setelah ini:

   ```
   ~/Project_Big_Data/
   ├── mqtt/
   │   ├── Dockerfile
   │   └── mosquitto.conf
   ├── database/
   ├── dummy_service/
   │   ├── Dockerfile
   │   └── dummy_service.py
   └── docker-compose.yml
   ```

# Konfigurasi docker untuk network routingnya

Di dalam file `docker-compose.yml`, Anda sudah mendefinisikan jaringan menggunakan **Docker bridge network** di bagian ini:

```yaml
networks:
  sensor_net:
    driver: bridge
```

Ini memungkinkan setiap kontainer (MQTT, database, dan dummy service) untuk berkomunikasi di jaringan yang sama, sehingga dummy service dapat mengakses MQTT broker dengan hostname `mqtt` dan database dapat diakses dengan hostname `database`.

---

### **Cara Menjalankan Proyek:**

1. **Buka terminal** dan navigasikan ke folder proyek:
   ```bash
   cd ~/my_project/
   ```

2. **Jalankan Docker Compose**:
   ```bash
   docker-compose up --build
   ```

Docker akan mengunduh image yang diperlukan (jika belum ada), membangun image dari `Dockerfile` yang Anda buat, dan menjalankan kontainer untuk Mosquitto, MongoDB, dan dummy service.

# FINISH