<p align="center">
  <a href="#pyblinkobot-english-version">English</a> •
  <a href="#pyblinkobot-中文版">中文</a>
</p>

---

# PyBlinkoBot (English Version)

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A powerful, Python-based Telegram bot that acts as a bridge to your self-hosted Blinko instance. Seamlessly archive text, images, files, and entire media groups from a designated chat. Built to work with the latest version of Blinko and designed for simple, reliable deployment using Docker Compose. The modern, maintained alternative.

## ✨ Features

-   **Save Text**: Receives plain text messages and creates new Blinko notes.
-   **Upload Files**: Handles images and various documents/files, uploading them as native attachments and creating corresponding notes.
-   **Media Group Support**: Correctly processes media groups (albums) with multiple images, combining all images and the caption into a **single** note.
-   **Instant Feedback**: Provides status updates like "Received, saving..." and confirms the result upon completion.
-   **Dockerized**: Deploys instantly with Docker and Docker Compose for easy management.
-   **Secure**: Configured via environment variables to keep your secrets safe.

## 🚀 Getting Started

### Prerequisites

Before you begin, ensure you have the following:
1.  **Docker** and **Docker Compose**.
2.  A running self-hosted instance of **Blinko**.
3.  A **Telegram Bot Token** (created via [@BotFather](https://t.me/BotFather)).
4.  Your own **Telegram Chat ID** (you can get it from [@userinfobot](https://t.me/userinfobot)).
5.  An **API Bearer Token** generated from your Blinko instance.

### Installation & Usage

1.  **Clone the repository**
    ```bash
    git clone https://github.com/ikofan/PyBlinkoBot.git
    cd PyBlinkoBot
    ```

2.  **Create and configure the `.env` file**
    Copy the example file to create your own configuration file.
    ```bash
    cp env.example .env
    ```
    Then, edit the `.env` file and fill in your credentials.
    ```ini
    TELEGRAM_BOT_TOKEN="YOUR_TELEGRAM_BOT_TOKEN"
    AUTHORIZED_CHAT_ID="YOUR_CHAT_ID"
    BLINKO_API_URL="http://your-blinko-instance.com"
    BLINKO_API_KEY="YOUR_BLINKO_BEARER_TOKEN"
    ```

3.  **Start the service**
    Launch the bot with a single Docker Compose command.
    ```bash
    docker-compose up -d
    ```

Your `PyBlinkoBot` is now running in the background!

### Managing the Bot

-   **View real-time logs**:
    ```bash
    docker-compose logs -f
    ```

-   **Stop and remove the container**:
    ```bash
    docker-compose down
    ```

-   **Update and redeploy after code changes**:
    ```bash
    docker-compose up -d --build
    ```

## 🤝 Contributing

Pull requests and issues are welcome to improve this project!

## 📄 License

This project is licensed under the [MIT License](LICENSE).

---
---

# PyBlinkoBot (中文版)

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

一个功能强大的 Telegram 机器人，它可以接收指定用户的消息、文件和媒体组，并自动将它们保存到您自托管的 [Blinko](https://github.com/blinkops/blinko) 笔记服务中。本项目使用 Python 实现，适配最新版 Blinko，并通过 Docker 进行部署。

## ✨ 功能特性

-   **文本保存**: 接收纯文本消息并创建新的 Blinko 笔记。
-   **文件上传**: 接收图片和各类文档（文件），将其作为原生附件上传并创建笔记。
-   **媒体组支持**: 能够正确处理包含多张图片的媒体组，将所有图片和文字说明合并到**一条**笔记中。
-   **即时反馈**: 发送“收到，正在保存...”等状态更新，并在完成后告知结果。
-   **Docker 化部署**: 使用 Docker 和 Docker Compose，实现一键启动和轻松管理。
-   **安全**: 通过环境变量配置密钥，避免敏感信息硬编码。

## 🚀 快速开始

### 先决条件

在开始之前，请确保您已准备好：
1.  **Docker** 和 **Docker Compose**。
2.  一个正在运行的 **Blinko** 自托管实例。
3.  一个 **Telegram 机器人 Token** (通过 [@BotFather](https://t.me/BotFather) 创建)。
4.  您自己的 **Telegram Chat ID** (通过 [@userinfobot](https://t.me/userinfobot) 获取)。
5.  从您的 Blinko 实例生成的 **API Bearer Token**。

### 安装与运行

1.  **克隆本仓库**
    ```bash
    git clone https://github.com/ikofan/PyBlinkoBot.git
    cd PyBlinkoBot
    ```

2.  **创建并配置 `.env` 文件**
    复制 `env.example` 文件，并将其重命名为 `.env`。
    ```bash
    cp env.example .env
    ```
    然后，编辑 `.env` 文件，填入您的个人信息。
    ```ini
    TELEGRAM_BOT_TOKEN="YOUR_TELEGRAM_BOT_TOKEN"
    AUTHORIZED_CHAT_ID="YOUR_CHAT_ID"
    BLINKO_API_URL="http://your-blinko-instance.com"
    BLINKO_API_KEY="YOUR_BLINKO_BEARER_TOKEN"
    ```

3.  **启动服务**
    使用 Docker Compose 一键启动机器人。
    ```bash
    docker-compose up -d
    ```

现在，您的 `PyBlinkoBot` 已经在后台运行了！

### 管理机器人

-   **查看实时日志**:
    ```bash
    docker-compose logs -f
    ```

-   **停止并移除容器**:
    ```bash
    docker-compose down
    ```

-   **更新代码后重新部署**:
    ```bash
    docker-compose up -d --build
    ```

## 🤝 贡献

欢迎提交 PR 或 Issue 来改进这个项目！

## 📄 许可证

本项目使用 [MIT License](LICENSE) 开源。