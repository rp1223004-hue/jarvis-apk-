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
android.permissions = INTERNET,RECORD_AUDIO
android.api = 33
android.minapi = 21
android.accept_sdk_license_agreement = True

[buildozer]
log_level = 2
warn_on_root = 1
