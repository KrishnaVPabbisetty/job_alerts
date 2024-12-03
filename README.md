
# **Job Alert Notification System**

---

### **Project Overview**
The **Job Alert Notification System** is an automated script designed to scrape job listings from Amazon's job portal for specific roles and send email notifications about newly posted jobs updated within the last hour. This project leverages Selenium for web scraping, SMTP for email delivery, and environment variables to handle sensitive data securely.

---

### **Features**
- **Automated Job Scraping**: Extracts job information (title, location, job ID, posting date) for specific roles from Amazon's job portal.
- **Time-sensitive Filtering**: Identifies jobs updated within the last hour.
- **Email Notifications**: Sends personalized email notifications with job details.
- **Secure Data Handling**: Sensitive information like email credentials and recipient emails are managed securely through environment variables.
- **Responsive Email Format**: HTML-styled email layout for a user-friendly display of job details.

---

### **Technologies Used**
- **Programming Language**: Python
- **Web Scraping**: Selenium, ChromeDriver
- **Email Notifications**: `smtplib`, `email.mime`
- **Dependency Management**: `dotenv`, `webdriver-manager`
- **HTML Email Styling**: Custom CSS
- **Task Automation**: Compatible with GitHub Actions or any other CI/CD pipeline

---

### **Setup Instructions**

#### 1. **Clone the Repository**
```bash
git clone https://github.com/syam888/job_notifications.git
cd job_notifications
```

#### 2. **Install Required Packages**
```bash
pip install -r requirements.txt
```

#### 3. **Environment Variables**
Create a `.env` file in the root directory and add the following keys:

```env
SENDER_EMAIL=your-email@example.com
EMAIL_PASSWORD=your-email-password
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
RECEIVER_EMAILS=email1@example.com,email2@example.com,email3@example.com
```

#### 4. **Run the Script**
Execute the script using:
```bash
python jobalert.py
```

#### 5. **Automate with GitHub Actions (Optional)**
- Add the environment variables as **Repository Secrets** in GitHub.
- Configure the provided `action.yml` file to schedule the script.

---

### **Customization**
- Update the `urls` variable in the `scrape_amazon_jobs_selenium()` function to target different job portals or roles.
- Modify email formatting in the `notify_jobs_by_email()` function to customize the content.

---

### **Security Best Practices**
- **Do not hardcode sensitive information** like passwords or API keys.
- Use `.env` files or GitHub Secrets to manage sensitive data.
- Ensure `.env` is listed in `.gitignore`.

---

### **Future Enhancements**
- Add support for multiple job portals.
- Implement email subscription preferences for recipients.
- Enhance job filtering with more criteria (e.g., location, seniority).
- Introduce logging and error monitoring for better debugging.

---

### **Contributors**
- **[Gana Syam Reddy Mandepudi]**  
  [GitHub Profile](https://github.com/syam888)

Feel free to open issues or contribute enhancements to the repository!

---

### **License**
This project is licensed under the [MIT License](LICENSE).
