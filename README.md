# Humanity Testnet 自动领取脚本

由 [雪糕战神@Xuegaogx](https://x.com/Xuegaogx) 编写  
自动执行 Humanity 测试网的每日 HP 领取、状态检查、积分查询等交互操作

---

## 🧾 功能说明

本脚本每轮自动完成以下步骤：

1. **加载 token 文件（支持多账号）**
2. 针对每个账号依次执行：
   - ✅ 查询用户昵称与钱包地址
   - ✅ 查询当前 HP 总积分
   - ✅ 检查是否已领取今日积分
   - ✅ 自动领取每日积分（若可领取）
   - ✅ 查询领取后最新积分余额
3. 完成所有账号后自动倒计时 24 小时，循环执行

---

## ✅ 使用前准备

### 环境要求

- Python 版本 >= 3.8
- 推荐操作系统：Linux / Mac / Windows / WSL
- 网络支持：直连或配置 http(s) 代理

---

### 克隆仓库

```bash
git clone https://github.com/GzGod/Humanity.git
cd Humanity
```

---

### 安装依赖

```bash
pip install -r requirements.txt
```

---

## 🛠 文件配置说明

### 1. Token 文件 `tokens.txt`

一行一个 Bearer Token（无需加 `Bearer ` 前缀）：

```
eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.xxxxxx...
eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.zzzzzz...
```

> ⚠️ Token 为登录后的身份凭证，请勿泄露或上传！

---

### 如何获取 Token？

1. 打开浏览器访问：https://testnet.humanity.org
2. 使用钱包登录（如 Metamask）
3. 登录成功后按 F12 打开开发者工具 → 进入 network（网络）
4. 如图所示，复制 Bearer 后的内容
<img width="658" alt="image" src="https://github.com/user-attachments/assets/5ec6f96a-600f-4512-83c8-8ede42b4ad8a" />
---

### 2. 代理文件 `proxy.txt`（可选）

一行一个 http(s) 代理地址，格式示例：

```
http://127.0.0.1:7890
http://user:pass@ip:port
```

如未提供该文件，则默认直连模式运行。

---

## ▶️ 运行脚本

```bash
python main.py
```

脚本将自动循环运行，每轮间隔 24 小时。建议使用 `screen` / `tmux` / `pm2` 后台运行。

---

## 📄 免责声明

- 本脚本仅用于 Humanity 测试网参与用途，**不构成任何投资建议**
- Token 使用风险由用户自行承担，脚本仅供学习与交流
- 使用本脚本即代表您已同意承担一切使用后果

---

## 🙋 联系作者

- TG频道：https://t.me/xuegaoz
- GitHub：https://github.com/Gzgod
- 推特：[@Xuegaogx](https://twitter.com/Xuegaogx)
