
[app]
title = JARVIS 4.0 Full AI
package.name = jarvisai
package.domain = com.baddy.jarvis
source.dir = .
source.include_exts = py,png,jpg,kv,atlas,json
version = 4.0
requirements = python3,kivy,requests,plyer,pyjnius,android,urllib3,certifi,charset-normalizer,idna
orientation = portrait
fullscreen = 0
android.permissions = INTERNET, CAMERA, RECORD_AUDIO, WRITE_EXTERNAL_STORAGE, READ_EXTERNAL_STORAGE, FLASHLIGHT, VIBRATE, ACCESS_FINE_LOCATION, READ_CONTACTS, SEND_SMS, CALL_PHONE
android.api = 33
android.minapi = 21
android.ndk = 25b
android.accept_sdk_license_agreements = True
android.ant = auto

[buildozer]
log_level = 2
warn_on_root = 1
