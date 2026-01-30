#!/bin/bash

# AI简历应用开发工具安装脚本
# 适用于Linux系统（Ubuntu/Debian）

set -e  # 遇到错误立即退出

echo "========================================="
echo "AI简历应用开发工具安装脚本"
echo "========================================="

# 颜色定义
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# 检查是否为root用户
if [ "$EUID" -eq 0 ]; then
    echo -e "${RED}请勿使用root用户运行此脚本${NC}"
    exit 1
fi

# 更新系统
echo -e "${YELLOW}[1/9] 更新系统包...${NC}"
sudo apt update

# 安装Java JDK 17
echo -e "${YELLOW}[2/9] 安装Java JDK 17...${NC}"
if ! command -v java &> /dev/null; then
    sudo apt install -y openjdk-17-jdk
    echo 'export JAVA_HOME=/usr/lib/jvm/java-17-openjdk-amd64' >> ~/.bashrc
    echo -e "${GREEN}Java JDK 17 安装成功${NC}"
else
    echo -e "${GREEN}Java 已安装，跳过${NC}"
fi

# 安装Ruby
echo -e "${YELLOW}[3/9] 安装Ruby...${NC}"
if ! command -v ruby &> /dev/null; then
    sudo apt install -y ruby-full rubygems
    echo -e "${GREEN}Ruby 安装成功${NC}"
else
    echo -e "${GREEN}Ruby 已安装，跳过${NC}"
fi

# 安装Fastlane
echo -e "${YELLOW}[4/9] 安装Fastlane...${NC}"
if ! command -v fastlane &> /dev/null; then
    sudo gem install fastlane -NV
    echo -e "${GREEN}Fastlane 安装成功${NC}"
else
    echo -e "${GREEN}Fastlane 已安装，跳过${NC}"
fi

# 安装Android SDK基础工具
echo -e "${YELLOW}[5/9] 安装Android SDK工具...${NC}"
if ! command -v sdkmanager &> /dev/null; then
    sudo apt install -y android-sdk android-sdk-platform-tools
    echo 'export ANDROID_HOME=$HOME/Android/Sdk' >> ~/.bashrc
    echo 'export PATH=$PATH:$ANDROID_HOME/emulator' >> ~/.bashrc
    echo 'export PATH=$PATH:$ANDROID_HOME/tools' >> ~/.bashrc
    echo 'export PATH=$PATH:$ANDROID_HOME/tools/bin' >> ~/.bashrc
    echo 'export PATH=$PATH:$ANDROID_HOME/platform-tools' >> ~/.bashrc
    echo -e "${GREEN}Android SDK 安装成功${NC}"
else
    echo -e "${GREEN}Android SDK 已安装，跳过${NC}"
fi

# 安装Flutter
echo -e "${YELLOW}[6/9] 安装Flutter SDK...${NC}"
if ! command -v flutter &> /dev/null; then
    cd ~
    git clone https://github.com/flutter/flutter.git -b stable --depth 1
    echo 'export PATH="$PATH:$HOME/flutter/bin"' >> ~/.bashrc
    echo -e "${GREEN}Flutter SDK 安装成功${NC}"
else
    echo -e "${GREEN}Flutter 已安装，跳过${NC}"
fi

# 安装Appium
echo -e "${YELLOW}[7/9] 安装Appium...${NC}"
if ! command -v appium &> /dev/null; then
    npm install -g appium
    npm install -g appium-doctor
    echo -e "${GREEN}Appium 安装成功${NC}"
else
    echo -e "${GREEN}Appium 已安装，跳过${NC}"
fi

# 安装Docker（可选）
echo -e "${YELLOW}[8/9] 安装Docker（可选）...${NC}"
if ! command -v docker &> /dev/null; then
    read -p "是否安装Docker？(y/n) " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        curl -fsSL https://get.docker.com -o get-docker.sh
        sudo sh get-docker.sh
        sudo usermod -aG docker $USER
        echo -e "${GREEN}Docker 安装成功${NC}"
    else
        echo -e "${YELLOW}跳过Docker安装${NC}"
    fi
else
    echo -e "${GREEN}Docker 已安装，跳过${NC}"
fi

# 下载Charles Proxy
echo -e "${YELLOW}[9/9] 下载Charles Proxy...${NC}"
if [ ! -d "$HOME/Downloads/charles" ]; then
    cd ~/Downloads
    wget https://www.charlesproxy.com/assets/release/4.6.6/charles-proxy-4.6.6_amd64.tar.gz
    tar -xzf charles-proxy-4.6.6_amd64.tar.gz
    echo -e "${GREEN}Charles Proxy 下载成功${NC}"
else
    echo -e "${GREEN}Charles Proxy 已下载，跳过${NC}"
fi

# 重新加载环境变量
echo -e "${YELLOW}重新加载环境变量...${NC}"
source ~/.bashrc

# 验证安装
echo ""
echo "========================================="
echo "安装完成！验证工具版本："
echo "========================================="
java -version 2>&1 | head -1 || echo "Java: 未安装"
ruby -version || echo "Ruby: 未安装"
fastlane --version || echo "Fastlane: 未安装"
flutter --version || echo "Flutter: 未安装"
appium --version || echo "Appium: 未安装"
docker --version || echo "Docker: 未安装"

echo ""
echo -e "${GREEN}=========================================${NC}"
echo -e "${GREEN}安装完成！请运行以下命令重新加载环境变量：${NC}"
echo -e "${GREEN}source ~/.bashrc${NC}"
echo -e "${GREEN}=========================================${NC}"
echo ""
echo "接下来需要手动安装："
echo "1. Android Studio（用于完整Android开发）"
echo "2. Postman（API测试工具）"
echo "3. 配置Firebase项目（可选）"
echo ""
echo "详细配置请参考："
echo "- Charles Proxy: docs/CHARLES_PROXY_GUIDE.md"
echo "- 性能优化: docs/PERFORMANCE_OPTIMIZATION.md"
echo "- Fastlane配置: frontend/android/fastlane/Fastfile"