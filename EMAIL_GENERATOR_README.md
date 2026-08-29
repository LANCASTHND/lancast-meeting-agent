# 📧 LANCAST EMAIL GENERATOR - QUICK START GUIDE

## ⚡ 5-MINUTE SETUP

### **Step 1: Download Files (Already Created)**

You have 4 files ready:
```
✓ EMAIL_TEMPLATES_PRESEED_SEED.md (full templates)
✓ LANCAST_INVESTOR_LIST_TEMPLATE.csv (investor list)
✓ generate_investor_emails.py (email generator script)
✓ EMAIL_GENERATOR_README.md (this file)
```

---

### **Step 2: Update Investor List**

Open `LANCAST_INVESTOR_LIST_TEMPLATE.csv` in Excel/Google Sheets.

**Replace these with YOUR actual investors:**

```csv
name,email,firm,type,platform,initial_date,priority,notes
Varad Patel,varad@zacuaventures.com,Zacua Ventures,seed_vc,direct,2026-08-29,HIGH,"YOUR LEAD INVESTOR"
John Smith,john@techventures.com,Tech Ventures,micro_vc,forge,2026-08-29,HIGH,"REPLACE WITH REAL NAME"
[Add 15-20 more investors]
```

**Key columns:**
- `name`: Full name
- `email`: Email address (critical!)
- `firm`: VC/Angel fund name
- `type`: `angel`, `micro_vc`, `seed_vc`, `accelerator`
- `platform`: `direct`, `angellist`, `ourcrowd`, `republic`, `forge`
- `priority`: `HIGH` or `MEDIUM` (only these get emailed)

**Save as:** `investors_to_contact.csv`

---

### **Step 3: Run Python Script**

**Option A: Mac/Linux Terminal**
```bash
python3 generate_investor_emails.py --input investors_to_contact.csv --output emails_ready.csv
```

**Option B: Windows PowerShell**
```powershell
python generate_investor_emails.py --input investors_to_contact.csv --output emails_ready.csv
```

**Output:** `emails_ready.csv` with all personalized emails

```
✓ Generated 45 email sequences
  • 15 initial emails
  • 15 follow-up #1
  • 15 follow-up #2
```

---

### **Step 4: Send Emails**

**Option A: Gmail (Free, Native)**
1. Open Gmail
2. Copy subject + body from CSV into new email
3. Send manually to each investor
4. Set calendar reminders for follow-ups

**Option B: Lemlist (Automated, Best)**
1. Import `emails_ready.csv` to Lemlist
2. Set up email sequences (auto follow-ups)
3. Track opens + clicks
4. Send campaigns
5. Auto-follow-up on day 3 and day 5

**Option C: HubSpot (CRM, Most Professional)**
1. Import CSV to HubSpot Contacts
2. Create email sequence workflow
3. Auto-send with timing
4. Track all metrics

---

## 📊 EMAIL SEQUENCE TIMING

```
TODAY (AUG 29):
├─ Send "initial" emails to 15 investors (morning)
└─ Result: 15 investors contacted by EOD

FRI AUG 30:
├─ Monitor for replies
└─ Result: 3-5 replies expected

SUN SEPT 1:
├─ INFINITA WEEK starts
├─ Field research with Varad begins
└─ In-person meetings with investors

WED SEPT 4:
├─ Send "followup_1" emails (auto if using Lemlist)
└─ Result: 2-3 additional confirmations

SAT SEPT 7:
├─ Send "followup_2" emails (final push)
└─ Result: Pre-seed closes $200K-$400K

---

## 🎯 EXPECTED RESPONSE RATES

**Initial Email:**
- Open rate: 40-50% (6-8 opens)
- Reply rate: 15-20% (2-3 replies)
- Interest: 50% of replies (1-2 serious)

**Follow-up #1 (Day 3):**
- Open rate: 50-60% (adds 7-9 new opens)
- Reply rate: 20-25% (adds 2-3 new replies)
- Interest: 60% of new replies (1-2 additional)

**Follow-up #2 (Day 5):**
- Open rate: 45-50% (adds 6-7 final opens)
- Reply rate: 15-20% (final 2-3 replies)
- Interest: 70% of replies (2-3 final commitments)

**Total Expected:**
- Replies: 6-8 serious conversations
- Conversion: 3-5 investors ($50K-$200K committed)
- Close rate: 30-40%

---

## 📋 WHAT'S IN THE CSV OUTPUT

Each row = ONE email ready to send:

```
send_date: 2026-08-29      ← When to send (auto if using Lemlist)
name: John Smith           ← Investor name (for "Hi John,")
email: john@example.com    ← Send TO this email
firm: Tech Ventures        ← Their company
type: micro_vc             ← Type (affects template)
platform: forge            ← Where you found them
subject: "Pre-Seed Opportunity: ConTech + Honduras"
body: [Full personalized email body]
email_sequence: initial    ← initial, followup_1, or followup_2
days_after_initial: 0      ← Send on day 0, 3, or 5
```

---

## 🚀 SENDING OPTIONS COMPARISON

| Option | Cost | Time | Automation | Tracking |
|--------|------|------|-----------|----------|
| **Gmail** | Free | 30 min | None | Manual |
| **Lemlist** | $29/mo | 10 min | Full | Excellent |
| **HubSpot** | Free tier | 20 min | Full | Good |
| **SendGrid** | $20/mo | 15 min | Full | Good |

**Recommended:** Lemlist (best ROI for startup fundraising)

---

## 📧 LEMLIST SETUP (5 MINUTES)

1. **Sign up:** lemlist.com (free trial)
2. **Import CSV:** Campaigns → Import Contacts
3. **Create sequence:**
   - Email 1: Send immediately
   - Email 2: Send after 3 days (if no reply)
   - Email 3: Send after 5 days (if still no reply)
4. **Personalization:** Lemlist auto-personalizes names
5. **Send:** Click "Launch Campaign"
6. **Track:** See opens, clicks, replies in dashboard

---

## 🎯 MANUAL SENDING (NO TOOL)

If you want to send manually via Gmail:

1. **Export emails to CSV**
2. **Open each email in CSV**
3. **Copy subject line → Gmail subject field**
4. **Copy body → Gmail compose field**
5. **Paste recipient email → To field**
6. **Review once, send**
7. **Set calendar reminder** for follow-ups (day 3, day 5)

**Time:** ~2-3 minutes per email × 15 = 30-45 minutes total

---

## ❓ CUSTOMIZATION

### **Change Email Templates**

Edit `generate_investor_emails.py` and modify templates:

```python
'angel': {
    'initial': {
        'subject': "YOUR NEW SUBJECT HERE",
        'body': """YOUR NEW BODY HERE
        
Can include {name}, {firm}, {platform} placeholders"""
    }
}
```

Then re-run script.

### **Add New Investor Types**

Add to CSV with new `type`:

```
name,email,firm,type,platform,initial_date,priority
John,john@example.com,Firm,corporate_vc,direct,2026-08-29,HIGH
```

Then add template in script:

```python
'corporate_vc': {
    'initial': {
        'subject': "Corporate VC Template",
        'body': "..."
    }
}
```

---

## ⚠️ COMMON MISTAKES TO AVOID

❌ **DON'T:** Send all emails at once (no spacing = spam)
✅ **DO:** Space out over 3 days (batch of 5/day) or use Lemlist

❌ **DON'T:** Generic "Dear Investor" greetings
✅ **DO:** Personalize with {name} placeholder (auto-filled)

❌ **DON'T:** Skip follow-ups (80% of interest is in follow-ups)
✅ **DO:** Send all 3 emails (initial + 2 follow-ups)

❌ **DON'T:** Send on Friday-Sunday
✅ **DO:** Send Tue-Thu for best open rates

❌ **DON'T:** Use formatting/HTML in plain CSV emails
✅ **DO:** Keep it plain text (works better in email)

---

## 📱 GMAIL TIPS

**Send time:** Tuesday-Thursday, 9-11am (investor coffee-check time)

**Subject line A/B testing:**
- Subject A: "LANCAST: AI Construction Automation (Pre-Seed)"
- Subject B: "Pre-Seed Opportunity: ConTech + Honduras"
→ See which gets higher open rate

**Follow-up timing:**
- Initial: Day 1 (Tuesday)
- Follow-up 1: Day 4 (Friday morning)
- Follow-up 2: Day 6 (Sunday night for Monday morning)

---

## 🔄 WORKFLOW EXAMPLE

**Your actual workflow (15 investors):**

```
THURSDAY 8/29 (10am):
└─ Run script: python3 generate_investor_emails.py
   └─ Get: LANCAST_EMAILS_READY_TO_SEND.csv (45 rows)

THURSDAY 8/29 (10:15am):
└─ Send batch 1 (initial): 5 angels (copy/paste into Gmail)
└─ Set reminder: Friday check inbox

FRIDAY 8/30 (10am):
└─ Send batch 2 (initial): 5 micro-VCs
└─ Monitor replies

MONDAY 9/2 (10am):
└─ Auto send followup_1 (if using Lemlist)
└─ OR manually send via Gmail

WEDNESDAY 9/4 (10am):
└─ Auto send followup_2
└─ OR manually send via Gmail

RESULT: 15-25 investor conversations happening simultaneously
        3-5 commitments ($50K-$200K) by Sept 1
```

---

## 📞 QUICK REFERENCE

**Script command:**
```bash
python3 generate_investor_emails.py --input investors_to_contact.csv --output emails_ready.csv
```

**CSV columns you MUST fill:**
```
name, email, firm, type, platform, priority
```

**Types:** `angel`, `micro_vc`, `seed_vc`, `accelerator`

**Priority:** `HIGH` or `MEDIUM` (only these get emailed)

**Platform:** `direct`, `angellist`, `ourcrowd`, `republic`, `forge`, `kickstarter`

---

## 🎁 BONUS: GOOGLE SHEETS TRACKER

Create a Google Sheet to track responses:

```
| Name | Email | Firm | Sent Date | Status | Response | Next Action | Amount |
|------|-------|------|-----------|--------|----------|------------|---------|
| John | john@ | Tech | 8/29 | Replied | "Interested" | Call 9/2 | $50K |
| Sarah | sar@  | VC   | 8/29 | No reply | — | Followup 9/1 | — |
```

→ Share this with team to track progress in real-time

---

## ✅ FINAL CHECKLIST

Before sending:

- [ ] CSV updated with 15+ real investor emails
- [ ] No typos in email addresses
- [ ] Script ran successfully (45 emails generated)
- [ ] Lemlist account created OR Gmail ready
- [ ] Calendar reminders set for follow-ups
- [ ] Team knows about email campaign
- [ ] Varad's email is priority #1
- [ ] Pre-seed messaging tested on 1-2 friends first

---

## 🚀 YOU'RE READY!

**Next step:** 
1. Update `investors_to_contact.csv` with your list
2. Run script: `python3 generate_investor_emails.py`
3. Send initial batch TODAY
4. Follow up day 3, day 5
5. Close pre-seed by Sept 1 ✓

**Questions?** All templates + script are in this folder.

**Expected result:** $200K-$400K pre-seed closed in 2-4 weeks

Let's go! 🚀
