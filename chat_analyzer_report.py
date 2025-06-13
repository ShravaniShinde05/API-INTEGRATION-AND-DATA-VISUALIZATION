import pandas as pd
import re
import matplotlib.pyplot as plt
from wordcloud import WordCloud
from collections import Counter
from fpdf import FPDF
import datetime

# ====== Load Your Chat Data (Replace with your .txt file) ======
chat_text = """
06/05/2025, 10:15 AM - Alice: Hey, good morning! ☀️
06/05/2025, 10:16 AM - Bob: Morning Alice! How are you?
06/05/2025, 10:17 AM - Alice: I’m doing well! Just finished the task.
06/05/2025, 10:18 AM - Charlie: Great job Alice 👏
06/05/2025, 10:20 AM - Bob: Did you guys see the updates?
06/05/2025, 10:21 AM - Alice: Not yet. Let me check.
06/05/2025, 10:22 AM - Charlie: Same here.
06/05/2025, 10:23 AM - Bob: 👍👍
"""

# ====== Parse Chat Using Regex ======
pattern = r'(\d{2}/\d{2}/\d{4}), (\d{2}:\d{2} [AP]M) - (.*?): (.+)'
matches = re.findall(pattern, chat_text)

df = pd.DataFrame(matches, columns=["Date", "Time", "Sender", "Message"])
df["Date"] = pd.to_datetime(df["Date"], format="%d/%m/%Y")

# ====== Save Parsed Data ======
df.to_csv("chat_data.csv", index=False)

# ====== Message Activity ======
sender_counts = df["Sender"].value_counts()
plt.figure(figsize=(6, 4))
sender_counts.plot(kind="bar", color="skyblue")
plt.title("Message Count by Sender")
plt.xlabel("Sender")
plt.ylabel("Messages")
plt.tight_layout()
plt.savefig("sender_activity.png")
plt.close()

# ====== Word Cloud ======
stopwords = set([
    "the", "is", "at", "which", "on", "and", "a", "to", "in", "let", "me", "how",
    "are", "you", "just", "i", "i’m", "yet", "guys", "see", "did", "not"
])

all_words = " ".join(df["Message"]).lower().split()
filtered_words = [word.strip(".,!?") for word in all_words if word not in stopwords]

wordcloud = WordCloud(width=600, height=400, background_color="white").generate(" ".join(filtered_words))
wordcloud.to_file("wordcloud.png")

# ====== Emoji Stats ======
emoji_pattern = re.compile("["
    u"\U0001F600-\U0001F64F"  # emoticons
    u"\U0001F300-\U0001F5FF"  # symbols & pictographs
    u"\U0001F680-\U0001F6FF"  # transport & map symbols
    u"\U0001F1E0-\U0001F1FF"  # flags
    "]+", flags=re.UNICODE)

emojis = [emoji for msg in df["Message"] for emoji in emoji_pattern.findall(msg)]
emoji_counts = Counter(emojis)
emoji_df = pd.DataFrame(emoji_counts.items(), columns=["Emoji", "Count"])
emoji_df.to_csv("emoji_usage.csv", index=False)

# ====== PDF Report Generator ======
class PDFReport(FPDF):
    def header(self):
        self.set_font("Arial", "B", 16)
        self.cell(0, 10, "Chat Analysis Report", ln=True, align="C")
        self.set_font("Arial", "", 12)
        self.cell(0, 10, f"Generated on: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", ln=True, align="C")
        self.ln(10)

    def chapter_title(self, title):
        self.set_font("Arial", "B", 14)
        self.cell(0, 10, title, ln=True)
        self.ln(4)

    def chapter_body(self, text):
        self.set_font("Arial", "", 12)
        self.multi_cell(0, 10, text)
        self.ln()

    def add_image(self, path, width=180):
        self.image(path, w=width)
        self.ln()

# ====== Generate PDF Report ======
pdf = PDFReport()
pdf.add_page()

# Intro
pdf.chapter_title("Overview")
pdf.chapter_body(
    "This report provides an automated analysis of a sample WhatsApp-style chat. It includes:\n"
    "- Message activity by sender\n"
    "- Most frequently used words (excluding stopwords)\n"
    "- Emoji usage statistics\n"
    "- Visual charts and summaries"
)

# Sender Chart
pdf.chapter_title("Message Activity by Sender")
pdf.add_image("sender_activity.png")

# Word Cloud
pdf.chapter_title("Most Common Words")
pdf.add_image("wordcloud.png")

# Emoji Stats (shown as codes)
pdf.chapter_title("Emoji Usage Statistics")
for index, row in emoji_df.iterrows():
    emoji_code = row['Emoji'].encode('unicode_escape').decode('utf-8')
    pdf.cell(0, 10, f"{emoji_code}: {row['Count']}", ln=True)

# Save report
pdf.output("chat_report.pdf")

print("✅ Report generated: chat_report.pdf")
