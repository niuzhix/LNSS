<!--
 * @discription  : Copyright © 2021-2025 Blue Summer Studio. All rights reserved.
 * @Author       : Niu zhixin
 * @Date         : 2025-02-01 16:23:13
 * @LastEditTime : 2025-02-02 15:08:22
 * @LastEditors  : Niu zhixin
-->


<!--
 * @English 英语（美国）
-->




# LNSS Chat System User Guide 📖

## Introduction 🌟
The LNSS (Local Network Socket Server) Chat System is a LAN-based chat application built with Python and Tkinter. It allows users to create and join chat servers within a local network, enabling real-time message exchange. The system supports multi-user chat, emoji sending, chat history saving, and more.

## Starting the Program 🚀
To start the LNSS Chat System, run the `LNSS.exe` file. Upon launching, you will see a user selection interface.

## User Registration and Login 🔑
When you run the program for the first time, the system will prompt you to register an admin user. After registration, you can select the registered user from the user selection interface to log in.

## Creating a Chat Server 🖥️
After logging in, you can choose to create a chat server. Follow these steps:
1. Select the "Server" tab in the main interface.
2. Choose the password type:
   - Custom Password: Enter a password consisting of 6 to 8 characters, numbers, or underscores.
   - Random Password: The system will automatically generate a random password.
3. Click the "Create" button to start the chat server.

## Joining a Chat Server 🌐
To join an existing chat server, follow these steps:
1. Select the "Client" tab in the main interface.
2. Enter the server's IP address and password.
3. Click the "Join" button to connect to the chat server.

## Chatting 💬
Once connected to a chat server, you can send and receive messages in the chat window. The chat window includes the following components:
- Message Display Area: Displays all chat messages.
- Online User List: Shows the currently online users.
- Message Input Box: Enter the message you want to send.
- Send Button: Send the message.
- Emoji Button: Open the emoji selection window to choose and send emojis.

## Sending Emojis 😀
Click the emoji button to open the emoji selection window. Select an emoji, and it will be inserted into the message input box. You can continue typing text or send the emoji directly.

## Saving Chat History 💾
You can save the chat history to a local file. Follow these steps:
1. In the menu bar, select "More(M)" -> "Save Chat(S)".
2. Choose the location and name of the file to save.
3. The system will encrypt the chat history and save it to the specified file.

## Encryption and Decryption 🔐
The LNSS Chat System uses RSA and Fernet algorithms to encrypt and decrypt chat history. The encrypted file contains the private key and the encrypted chat history. During decryption, the system will use the private key to decrypt the chat history.

## Settings ⚙️
You can change language options in the settings interface. Follow these steps:
1. Click the "Settings..." button in the main interface.
2. Select the language in the settings interface.
3. Click the "Apply" button to save the settings.

## About ℹ️
To learn more about the LNSS Chat System, select "About(A)" -> "About...(A)" or "Help(H)" in the menu bar.

## Exiting the Program ❌
To exit the program, close the main window or select "Exit" in the menu bar. Note that exiting the program will disconnect all connections and cannot be restored.

## Code Structure 🧩
The `main.py` file's code structure is as follows:
- Import Libraries and Modules
- Global Variables and Configuration
- Server Class
- Client Class
- Login Class
- Main Interface Class
- Image Load Class
- Network Scan Class
- Main Function

## Detailed Code Explanation 📜
Here is a detailed explanation of each part of the code:

### Import Libraries and Modules 📚
These import statements bring in the necessary libraries and modules for the program, including Tkinter, SQLite, cryptography libraries, and more.

### Global Variables and Configuration 🌐
These global variables and configurations store the program's settings and state, including language options, encryption keys, database connections, and more.

### Server Class 🖥️
The server class is responsible for creating and managing the chat server, handling client connections, sending and receiving messages, managing online users, and more.

### Client Class 💻
The client class is responsible for connecting to the chat server, sending and receiving messages, managing online users, and more.

### Login Class 🔑
The login class handles user login and registration functionality.

### Main Interface Class 🖼️
The main interface class sets up the main window and its components, including the server and client tabs, settings, and more.

### Image Load Class 🖼️
The image load class handles loading and displaying images in the application.

### Network Scan Class 🌐
The network scan class scans the local network for available IP addresses.

### Main Function 🚀
The main function initializes the program and starts the main loop.

By following this user guide, you should be able to quickly get started with the LNSS Chat System and utilize its features effectively.










<!--
 * @SimpChinese 简体中文
-->




# LNSS 聊天系统用户指南 📖

## 简介 🌟
LNSS（本地网络套接字服务器）聊天系统是一个基于Python和Tkinter的局域网聊天应用程序。它允许用户在局域网内创建和加入聊天服务器，实现实时消息传递。该系统支持多用户聊天、表情发送、聊天记录保存等功能。

## 启动程序 🚀
要启动LNSS聊天系统，请运行`LNSS.exe`文件。启动后，您将看到一个用户选择界面。

## 用户注册和登录 🔑
首次运行程序时，系统会提示您注册一个管理员用户。注册完成后，您可以在用户选择界面选择已注册的用户进行登录。

## 创建聊天服务器 🖥️
登录后，您可以选择创建一个聊天服务器。请按照以下步骤操作：
1. 在主界面中选择“服务端”选项卡。
2. 选择密码类型：
   - 自定义密码：输入一个由6到8个字符、数字或下划线组成的密码。
   - 随机密码：系统将自动生成一个随机密码。
3. 点击“创建”按钮，启动聊天服务器。

## 加入聊天服务器 🌐
要加入一个已创建的聊天服务器，请按照以下步骤操作：
1. 在主界面中选择“客户端”选项卡。
2. 输入服务器的IP地址和密码。
3. 点击“加入”按钮，连接到聊天服务器。

## 聊天 💬
连接到聊天服务器后，您可以在聊天窗口中发送和接收消息。聊天窗口包括以下组件：
- 消息显示区域：显示所有聊天消息。
- 在线用户列表：显示当前在线的用户。
- 消息输入框：输入要发送的消息。
- 发送按钮：发送消息。
- 表情按钮：打开表情选择窗口，选择并发送表情。

## 发送表情 😀
点击表情按钮，打开表情选择窗口。选择一个表情后，表情将插入到消息输入框中。您可以继续输入文本或直接发送表情。

## 保存聊天记录 💾
您可以将聊天记录保存到本地文件。请按照以下步骤操作：
1. 在菜单栏中选择“更多(M)” -> “保存对话(S)”。
2. 选择保存文件的位置和文件名。
3. 系统将加密聊天记录并保存到指定文件。

## 加密和解密 🔐
LNSS聊天系统使用RSA和Fernet算法对聊天记录进行加密和解密。加密文件包含私钥和加密的聊天记录。解密时，系统会使用私钥解密聊天记录。

## 设置 ⚙️
您可以在设置界面中更改语言选项。请按照以下步骤操作：
1. 点击主界面中的“设置...”按钮。
2. 在设置界面中选择语言。
3. 点击“应用”按钮，保存设置。

## 关于 ℹ️
要了解有关LNSS聊天系统的更多信息，请在菜单栏中选择“关于(A)” -> “关于...(A)”或“帮助(H)”。

## 退出程序 ❌
要退出程序，请关闭主窗口或在菜单栏中选择“退出”。请注意，退出程序将断开所有连接，无法恢复。

## 代码结构 🧩
`main.py`文件的代码结构如下：
- 导入库和模块
- 全局变量和配置
- 服务器类
- 客户端类
- 登录类
- 主界面类
- 图像加载类
- 网络扫描类
- 主函数

## 详细代码说明 📜
以下是代码各部分的详细说明：

### 导入库和模块 📚
这些导入语句引入了程序所需的库和模块，包括Tkinter、SQLite、加密库等。

### 全局变量和配置 🌐
这些全局变量和配置存储了程序的设置和状态，包括语言选项、加密密钥、数据库连接等。

### 服务器类 🖥️
服务器类负责创建和管理聊天服务器，处理客户端连接、发送和接收消息、管理在线用户等。

### 客户端类 💻
客户端类负责连接到聊天服务器，发送和接收消息，管理在线用户等。

### 登录类 🔑
登录类处理用户登录和注册功能。

### 主界面类 🖼️
主界面类设置主窗口及其组件，包括服务器和客户端选项卡、设置等。

### 图像加载类 🖼️
图像加载类处理应用程序中图像的加载和显示。

### 网络扫描类 🌐
网络扫描类扫描本地网络中的可用IP地址。

### 主函数 🚀
主函数初始化程序并启动主循环。

通过遵循本用户指南，您应该能够快速上手LNSS聊天系统并有效利用其功能。