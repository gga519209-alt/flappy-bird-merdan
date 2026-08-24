[app]

title = Merdan Flappy Bird
package.name = merdanflappybird
package.domain = org.merdan
source.dir = .
source.include_exts = py,png,jpg,jpeg,wav,ogg
version = 1.0
requirements = python3,pygame
orientation = landscape
fullscreen = 1

# Android ayarları
android.api = 35
android.minapi = 23
android.ndk = 27c
android.accept_sdk_license = True

# APK olarak üret
android.debug_artifact = apk
android.release_artifact = apk

[buildozer]

log_level = 2
warn_on_root = 1
