[app]

title = MonitorApp
package.name = monitorapp
package.domain = org.test

source.dir = .
source.include_exts = py,png,jpg,kv,atlas

version = 0.1

requirements = python3,kivy

orientation = portrait
fullscreen = 0

android.permissions = READ_LOGS,DUMP,PACKAGE_USAGE_STATS

android.api = 34
android.minapi = 24
android.ndk = 25b

android.enable_androidx = True
android.accept_sdk_license = True


[buildozer]

log_level = 2
warn_on_root = 1
