[app]
title = JARVIS AI
package.name = jarvisai
package.domain = com.boss.jarvisai
source.dir =.
source.include_exts = py,png,jpg,kv,atlas
version = 1.0
requirements = python3,kivy==2.3.0
orientation = portrait
fullscreen = 0
android.permissions = INTERNET,RECORD_AUDIO,WRITE_EXTERNAL_STORAGE,READ_EXTERNAL_STORAGE
android.api = 33
android.minapi = 21
android.sdk = 33
android.ndk = 25b
android.accept_sdk_license_agreements = True
p4a.accept_sdk_license_agreements = True

[buildozer]
log_level = 2
