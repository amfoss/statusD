# statusD

An automated daemon for managing daily status updates in the amFOSS club.
`statusD` sends daily reminder emails and tracks member responses through email, integrating with the [root](github.com/amfoss/root) API for status tracking.

---

## 🧭 Overview

`statusD` automates the status update workflow by:

- Sending daily reminder emails to the mailing list at **18:00 (6 PM)** with the status update template
- Fetching email responses to the thread at **05:00 (5 AM)** the next day  
- Updating root with members who submitted their status updates  


## ⚙️ Features

- **Automated Email Reminders** - Sends structured status update templates to a mailing list  
- **Email Response Tracking** - Monitors inbox for status update replies  
- **Root Integration** - Updates member status records via GraphQL mutations  
- **Scheduled Execution** - Uses cron-based scheduling for reliable daily operations  


## 📦 Prerequisites

- Python **3.13+**  
- Gmail account with **app-specific password** enabled  
- Access to **amFOSS Root API**

---

## 🚀 Installation

### 1. Clone the repository

```bash
git clone https://github.com/amfoss/statusD.git
cd statusD
```

### 2. Setup the environment
```bash
cp .env.sample .env
```
* You can obtain the app password from [here](https://support.google.com/mail/answer/185833?hl=en).
### 3. Run the program
```bash
python app.py
```
