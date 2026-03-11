from fastapi import FastAPI, UploadFile, Form
import pandas as pd
import smtplib
from email.mime.text import MIMEText

app = FastAPI()

@app.post("/upload")
async def upload(file: UploadFile, email: str = Form(...)):

    df = pd.read_csv(file.file)

    total_revenue = df["Revenue"].sum()
    total_units = df["Units_Sold"].sum()
    top_region = df["Region"].mode()[0]

    summary = f"""
Sales Summary

Total Revenue: {total_revenue}
Total Units Sold: {total_units}
Top Region: {top_region}
"""

    # email bhejna
    sender_email = "mehakgupta2318@gmail.com"
    app_password = "exwj qjyk tryo hkxb"

    msg = MIMEText(summary)
    msg["Subject"] = "Sales Data Summary"
    msg["From"] = sender_email
    msg["To"] = email

    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(sender_email, app_password)
    server.sendmail(sender_email, email, msg.as_string())
    server.quit()

    return {"message": "Summary sent to email", "summary": summary}