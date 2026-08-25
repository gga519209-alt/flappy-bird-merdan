[app]

# Uygulamanın adı
title = Merdan Flappy Bird

# Python dosyanın bulunduğu klasör
package.name = merdanflappybird

# Paket kimliği
package.domain = org.merdan

# Python dosyan
source.dir = .

# APK'ya dahil edilecek dosyalar
source.include_exts = py,png,jpg,jpeg,wav,ogg,ttf

# Başlangıç dosyası
entrypoint = flappy_bird_merdan_v3.py

# Sürüm
version = 1.0

# Gerekli Python paketleri
requirements = python3,pygame

# Ekran yönü
orientation = landscape

# Tam ekran
fullscreen = 1

# Android ayarları
android.api = 34
android.minapi = 23
android.ndk = 28c
android.ndk_api = 23

# Android mimarisi
android.archs = arm64-v8a

# APK türü
android.release_artifact = apk

# Uygulama adı
android.entrypoint = org.libsdl.app.SDLActivity

# Gereksiz dosyaları temizle
android.add_src =

# Python-for-Android dalı
p4a.branch = master

[buildozer]

# Log seviyesi
log_level = 2
