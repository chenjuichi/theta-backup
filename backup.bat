@echo off

copy D:\vue\theta\babel.config.js C:\theta-backup\front\
copy D:\vue\theta\package.json C:\theta-backup\front\
copy D:\vue\theta\package-lock.json C:\theta-backup\front\
copy D:\vue\theta\vue.config.js C:\theta-backup\front\
copy D:\vue\theta\src\views\*.vue C:\theta-backup\front\src\views\
copy D:\vue\theta\src\views\menu\*.vue C:\theta-backup\front\src\views\menu\
copy D:\vue\theta\src\components\*.vue C:\theta-backup\front\src\components\
copy D:\vue\theta\src\mixin\*.js C:\theta-backup\front\src\mixin\
copy D:\vue\theta\src\mixin\api\*.js C:\theta-backup\front\src\mixin\api\
copy D:\vue\theta\src\router\*.js C:\theta-backup\front\src\router\
copy D:\vue\theta\src\store\*.js C:\theta-backup\front\src\store\
copy D:\vue\theta\src\assets\images\*.* C:\theta-backup\front\src\assets\images\*.*
copy D:\vue\theta\src\assets\css\*.* C:\theta-backup\front\src\assets\css\*.*
copy D:\vue\theta\src\assets\logo.png C:\theta-backup\front\src\assets\logo.png

copy C:\vue\theta\server\*.*  C:\theta-backup\server\
copy C:\vue\theta\server\database\*.py C:\theta-backup\server\database\
copy C:\vue\theta\server\ajax\*.py C:\theta-backup\server\ajax\
copy C:\vue\theta\server\modbus\*.* C:\theta-backup\server\modbus\
copy C:\vue\theta\server\celery\*.* C:\theta-backup\server\celery\
copy C:\vue\theta\.env C:\theta-backup\.env

@echo on