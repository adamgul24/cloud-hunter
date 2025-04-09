
# 🛰️ Cloud Hunter – AWS Threat Detection & Auto-Remediation System

**Cloud Hunter** is a full-scale, live-operational AWS security monitoring toolkit designed for cloud defenders, red teamers, and SOC analysts. It detects, logs, remediates, and visualizes AWS threat events in real time using Lambda, Terraform, Flask, and DynamoDB.

---

## 🧠 Features

### ✅ Detection Modules
- **IAM Abuse Detection**: Flags failed login attempts
- **S3 Exposure Detection**: Finds public buckets
- **EC2 Threat Detection**: Flags newly launched or suspicious instances

### ⚙️ Auto-Remediation
- S3: Buckets made private + tagged `"remediated"`
- EC2: Instances stopped + tagged `"rogue"`

### 🧾 Logging
- Events written to **DynamoDB** for historical tracking
- Lambda logging via `log_utils.py`

### 📊 Live Dashboard
- **ThreatBoard360** Flask app shows real-time events
- Auto-refreshes every 10 seconds
- Built-in `/api/events` endpoint for integrations

---

## 📂 Project Structure

```
cloud-hunter/
├── lambda/
│   ├── detect_iam_abuse.py
│   ├── detect_s3_exposure.py
│   ├── detect_ec2_threat.py
│   ├── log_utils.py
├── terraform/
│   ├── main.tf
│   ├── variables.tf
│   ├── outputs.tf
│   └── backend.tf
├── alerts/              # SNS/Slack/Email scripts
├── dashboard/           # Flask SIEM dashboard
│   ├── app.py
│   └── templates/index.html
├── reports/
├── requirements.txt
├── .env.example
└── README.md
```

---

## 🛠️ Setup Instructions

### 1. 🧪 Lambda Packaging
```bash
cd lambda
zip detect_iam_abuse.zip detect_iam_abuse.py
```

### 2. ⚙️ Terraform Deploy
```bash
cd terraform
terraform init
terraform apply
```

### 3. 🧠 Run ThreatBoard360 Dashboard
```bash
cd dashboard
pip install flask boto3
export DYNAMO_TABLE=CloudHunterThreatLogs
python app.py
```

Visit: [http://localhost:5001](http://localhost:5001)

---

## 🚀 Deployment Options

| Platform | Method |
|----------|--------|
| **EC2** | SSH + run Flask locally |
| **Render** | Deploy `app.py` as a web service |
| **Vercel** | (Optional) React frontend version |

---

## 📘 Future Upgrades
- Slack + Discord webhooks
- STIX export support
- IAM key leak detection
- CloudFront and WAF integration
- Kinesis or S3 streaming pipeline

---

## 📜 License

MIT — built to defend, simulate, and secure real cloud environments.

Crafted with ☁️ and 🧠 by **Commander Cloud**
