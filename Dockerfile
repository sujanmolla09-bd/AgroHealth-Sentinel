# ১. লাইটওয়েট অফিশিয়াল পাইথন বেস ইমেজ ব্যবহার
FROM python:3.10-slim

# ২. সার্ভার কন্টেইনারের ভেতরের ওয়ার্কিং ডিরেক্টরি নির্ধারণ
WORKDIR /app

# ৩. সিস্টেম লেভেলের প্রয়োজনীয় লাইব্রেরি ও ডিপেনডেন্সি ক্যাশিং
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# ৪. ডিপেনডেন্সি ফাইল কপি ও আল্ট্রা-লো মেমরি ইন্সটলেশন
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# ৫. প্রজেক্টের সমস্ত কোর সোর্স কোড কন্টেইনারে ইমপোর্ট করা
COPY . .

# ৬. গ্লোবাল নেটওয়ার্কের জন্য এপিআই পোর্ট লকিং (FastAPI Default)
EXPOSE 8000

# 🔴 ৭. উটেরিকন প্রোডাকশন সার্ভার স্বয়ংক্রিয়ভাবে সচল করার কম্যান্ড
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
