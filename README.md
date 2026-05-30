# imgcli — 批处理图片 CLI 工具

一行命令搞定图片批量压缩、格式转换、水印添加、重命名。

## 安装

### 方式一：下载 exe（推荐，无需 Python）

从 [Releases](../../releases) 下载 `imgcli.exe`，放到任意目录直接使用。

### 方式二：pip 安装

```bash
pip install imgcli
```

## 使用

### 压缩图片

```bash
# 按质量压缩（默认 85）
imgcli compress -q 70 ./图片目录

# 压缩到 500KB 以下
imgcli compress --max-size 500000 ./图片目录

# 限制最大尺寸
imgcli compress --max-width 1920 --max-height 1080 ./图片目录

# 递归处理子目录
imgcli compress -r ./图片目录
```

### 格式转换

```bash
# 全部转成 PNG
imgcli convert -f png ./图片目录

# 转成 WebP 并指定质量
imgcli convert -f webp -q 80 ./图片目录
```

### 添加水印

```bash
# 文字水印
imgcli watermark text -t "© 我的水印" ./图片目录

# 图片水印
imgcli watermark image -w logo.png ./图片目录

# 平铺水印
imgcli watermark image -w logo.png -p tile ./图片目录
```

### 批量重命名

```bash
# 按计数器重命名：image001.jpg, image002.jpg ...
imgcli rename counter -p photo ./图片目录

# 按模板重命名
imgcli rename pattern -p "img_{n}{ext}" ./图片目录

# 清理文件名（特殊字符替换为下划线）
imgcli rename sanitize ./图片目录
```

### 通用选项

所有命令支持：

| 选项 | 说明 |
|------|------|
| `-o, --output` | 输出目录（默认 `_output`） |
| `-r, --recursive` | 递归处理子目录 |
| `--dry-run` | 预览模式，不实际执行 |

## 构建 exe

```bash
pip install pyinstaller
pyinstaller --onefile --name imgcli --add-data "imgcli;imgcli" run.py
```

## 闲鱼销售

把 `dist/imgcli.exe` 打包成 ZIP，闲鱼上架。建议售价 19.9-39.9 元。
