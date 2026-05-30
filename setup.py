from setuptools import setup, find_packages

setup(
    name="imgcli",
    version="1.0.0",
    description="批处理图片工具 - 压缩、格式转换、水印、重命名",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "click>=8.0",
        "Pillow>=10.0",
    ],
    entry_points={
        "console_scripts": [
            "imgcli=imgcli.cli:cli",
        ],
    },
    python_requires=">=3.8",
)
