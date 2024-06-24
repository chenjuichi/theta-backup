@echo off

copy D:\vue\theta\*.config.js C:\theta-backup\front\
copy D:\vue\theta\*.json C:\theta-backup\front\

c:\windows\system32\xcopy D:\vue\theta\src\views\*.vue C:\theta-backup\front\src\views\ /E

copy D:\vue\theta\src\components\*.vue C:\theta-backup\front\src\components\

c:\windows\system32\xcopy D:\vue\theta\src\*.js C:\theta-backup\front\src\ /E

c:\windows\system32\xcopy D:\vue\theta\src\assets\*.* C:\theta-backup\front\src\assets\ /E

copy C:\vue\theta\server\*.*  C:\theta-backup\server\
c:\windows\system32\xcopy C:\vue\theta\server\*.py C:\theta-backup\server\ /E
copy C:\vue\theta\server\modbus\*.* C:\theta-backup\server\modbus\
copy C:\vue\theta\server\celery\*.* C:\theta-backup\server\celery\
copy C:\vue\theta\.env C:\theta-backup\.env

@echo on