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

# Разрешения Android для чтения логов
android.permissions = READ_LOGS, DUMP, PACKAGE_USAGE_STATS
android.api = 33
android.minapi = 21

[buildozer]
log_level = 2
warn_on_root = 1
