@echo off
chcp 65001 >nul
echo ========================================
echo   imgcli - 批量图片处理工具
echo ========================================
echo.
echo 请把要处理的图片放到本目录下的 "input" 文件夹
echo.
pause

if not exist "input\" (
    mkdir input
    echo 已创建 input 文件夹，请把图片放进去再运行
    pause
    exit /b
)

echo.
echo 请选择操作：
echo  1 - 压缩图片（质量 70）
echo  2 - 压缩图片（限制 500KB）
echo  3 - 压缩图片（限制 1920x1080）
echo  4 - 转换格式为 PNG
echo  5 - 转换格式为 WebP
echo  6 - 添加文字水印
echo  7 - 批量重命名
echo.
set /p choice="输入数字（1-7）: "

if "%choice%"=="1" imgcli.exe compress -q 70 input -o output
if "%choice%"=="2" imgcli.exe compress --max-size 500000 input -o output
if "%choice%"=="3" imgcli.exe compress --max-width 1920 --max-height 1080 input -o output
if "%choice%"=="4" imgcli.exe convert -f png input -o output
if "%choice%"=="5" imgcli.exe convert -f webp -q 80 input -o output
if "%choice%"=="6" (
    set /p wmtext="输入水印文字: "
    imgcli.exe watermark text -t "%wmtext%" input -o output
)
if "%choice%"=="7" (
    set /p prefix="输入文件名前缀（默认 image）: "
    if "%prefix%"=="" set prefix=image
    copy input\*.* input_backup\ >nul 2>&1
    imgcli.exe rename counter -p %prefix% input
)

echo.
echo 处理完成！结果在 output 文件夹
pause
