#!/usr/bin/env python3
"""
LANCAST EMAIL GENERATOR
Generates personalized email sequences for pre-seed + seed round fundraising

Usage:
    python generate_investor_emails.py --input investors.csv --output emails_to_send.csv

    Then copy emails to Lemlist, Gmail, or HubSpot for sending
"""

import csv
import sys
from datetime import datetime, timedelta
from pathlib import Path

class EmailGenerator:
    def __init__(self):
        self.templates = {
            'angel': {
                'initial': {
                    'subject': "LANCAST: AI Construction Automation (Pre-Seed 🚀)",
                    'body': """Hi {name},

I saw you invest in construction tech on {platform}.

Quick intro: LANCAST is AI-powered construction automation. We automate
contractor workflows (irrigation, lighting, project management) using computer
vision + IoT sensors.

Why now:
→ 1 paying client live (Honduras, $3K/month recurring)
→ Próspera ZEDE backing (Tim Draper ecosystem)
→ $50B+ TAM in construction (700K+ US contractors, <2% with AI)

Pre-seed round: $200K-$400K close by Sept 1
├─ Valuation: $8M cap
├─ Structure: SAFE w/ 20% discount
└─ Infinita Startup Week (Sept 1-7) field demo + investor meetings

Happy to share deck or jump on a call?

Best,
Mario
LANCAST LLC
+1 (954) 669-2788
mario@lancast.biz"""
                },
                'followup_1': {
                    'subject': "Re: LANCAST - Quick question on timing?",
                    'body': """Hi {name},

Quick follow-up on my email from {initial_date}.

Pre-seed round is moving fast. We have interest from multiple investors on
{platform}, and we're aiming to close by Sept 1 for Infinita Week
(Honduras field research summit).

If you're interested in participating, now is the time.

Valuation: $8M cap | Structure: SAFE w/ 20% discount

Infinita Week (Sept 1-7) is a great window to meet us + see the market
firsthand (live automation demo on job site).

Deck attached. Let me know if you want to chat this week.

Best,
Mario
+1 (954) 669-2788"""
                },
                'followup_2': {
                    'subject': "Last spot in LANCAST pre-seed (closes Sept 1)",
                    'body': """Hi {name},

Final follow-up. Pre-seed closes Sept 1 (tomorrow), down to last spot.

If you've been considering it, now is the time.

→ $200K-$400K round
→ $8M cap (SAFE)
→ Closes Sept 1

Call me directly: +1 (954) 669-2788 (I'm available all day)

Or reply to this email.

Best,
Mario"""
                }
            },
            'micro_vc': {
                'initial': {
                    'subject': "Pre-Seed Opportunity: ConTech + Honduras Innovation Hub",
                    'body': """Hi {name},

I'm Mario from LANCAST. We're raising $200K-$400K pre-seed
(close: Sept 1-7, 2026 at Infinita Startup Week in Honduras).

Why {firm} should look:
→ Pre-seed ConTech with 1 paying client already
→ Operating model validated (14 years construction ops)
→ Próspera ZEDE backing (Tim Draper, Coinbase Ventures ecosystem)
→ Infinita Week (Sept 1-7) = perfect diligence window

Quick facts:
├─ Business model: B2B SaaS (tiered $1.5K-$100K/customer)
├─ Traction: 1 client paying $3K/month (expanding to more)
├─ Market: $50B+ TAM (700K+ US contractors, <2% AI adoption)
├─ Team: 2 founders (operations expert + AI engineer)
└─ Valuation: $8M cap (SAFE)

Infinita Startup Week is Sept 1-7 in La Ceiba, Honduras. We're hosting
live field research sessions + investor meetings. Would {firm} want to
participate?

Deck + financials + traction proof attached.

Happy to jump on a call this week.

Best,
Mario
LANCAST LLC
+1 (954) 669-2788
mario@lancast.biz

P.S. Infinita Week info: freecitiesconference.com/infinita-week"""
                },
                'followup_1': {
                    'subject': "Re: LANCAST pre-seed - {firm} participation",
                    'body': """Hi {name},

Quick follow-up on LANCAST pre-seed (closing Sept 1 at Infinita Week).

{firm} is exactly the type of investor we want - you fund pre-seed ConTech
with operating teams.

Pre-seed snapshot:
├─ Amount: $200K-$400K
├─ Valuation: $8M cap (SAFE)
├─ Close: Sept 1-7 (Infinita Week, Honduras)
├─ Use: 12-week field research sprint + market expansion
└─ Next: Seed round $1M-$2M (Jan 2027 + Varad Patel/Zacua lead)

Infinita Week timing is critical - gives {firm} time to do diligence
on-site (meet team, see Client #1 live, meet contractors).

Are you in? Let me know if you want to move forward.

Best,
Mario
+1 (954) 669-2788"""
                },
                'followup_2': {
                    'subject': "Final call: LANCAST pre-seed closes Sept 1",
                    'body': """Hi {name},

Last update: Pre-seed closes Sept 1 (tomorrow). This is the last spot.

If {firm} wants to participate, now's the time.

$200K-$400K round | $8M cap | Closes Sept 1

Call me: +1 (954) 669-2788 (available all day)

Best,
Mario"""
                }
            },
            'seed_vc': {
                'initial': {
                    'subject': "Infinita Startup Week - Come See LANCAST Live",
                    'body': """Hi {name},

Infinita Startup Week is happening in Próspera August 31 - September 7.

I want you there. Not as an investor watching from the sidelines,
but as a mentor + potential partner.

Here's why:

You said you want to see field research on construction workflows, product
repeatability, and software-led economics. Infinita Week is the perfect
setting because:

→ 100+ founders + investors in one place (Próspera, La Ceiba)
→ LANCAST will be presenting our progress on construction AI
→ You'll see the market (contractors, builders attending too)
→ You'll see the ecosystem (Tim Draper, Coinbase Ventures, other VCs)
→ 1 week to do deep research + due diligence

But more importantly: I want you to see our Client #1 live on a job site.
Come for 2-3 days during the week, spend time with us in the field,
then attend Infinita's investor sessions.

I'll handle everything:
→ Flights/accommodation
→ Site visits (Client #1 working live)
→ Field research + contractor interviews
→ Infinita Week pass (investor/mentor tier)

By end of week, you'll have seen exactly what you said you need to see,
in the context of the broader Próspera ecosystem and startup community.

Then we can talk investment.

Are you in?

Best,
Mario
LANCAST LLC
(954) 669-2788
mario@lancast.biz"""
                },
                'followup_1': {
                    'subject': "Follow-up: Infinita Week Sept 1-7 (Varad confirmed coming)",
                    'body': """Hi {name},

Just wanted to follow up on the Infinita Week invitation.

Quick update: Pre-seed round is closing Aug 31, and seed round lead
(Zacua Ventures / Varad Patel) has confirmed attendance for full week.

This creates perfect timing for seed discussions:
→ Pre-seed close announced Sept 1
→ Field research visible all week
→ Investor summit (50+ VCs) creates FOMO + validation
→ Investment conversation Sept 4-5

Are you coming to Infinita Week? If so, let's schedule time for
field visit + 1-on-1.

Best,
Mario
+1 (954) 669-2788"""
                },
                'followup_2': {
                    'subject': "Last reminder: Infinita Week starts tomorrow (Aug 31)",
                    'body': """Hi {name},

Last reminder: Infinita Week starts tomorrow (Aug 31).

If you're planning to attend, looking forward to seeing you there.

Field research visit: Aug 31-Sept 1
Infinita sessions: Sept 2-5
Investment meeting: Sept 4-5

Contact me when you arrive: +1 (954) 669-2788

Best,
Mario"""
                }
            }
        }

    def get_template(self, investor_type, email_type):
        """Get email template for investor type and email sequence"""
        return self.templates.get(investor_type, {}).get(email_type, {})

    def generate_email(self, investor, email_type='initial', days_delay=0):
        """Generate personalized email from template"""

        name = investor.get('name', 'Investor')
        email = investor.get('email', '')
        firm = investor.get('firm', 'Your Company')
        inv_type = investor.get('type', 'angel').lower()
        platform = investor.get('platform', 'AngelList')
        initial_date = investor.get('initial_date', '2026-08-29')

        # Calculate send date
        base_date = datetime.strptime(initial_date, '%Y-%m-%d')
        send_date = (base_date + timedelta(days=days_delay)).strftime('%Y-%m-%d')

        template = self.get_template(inv_type, email_type)

        if not template:
            return None

        # Personalize template
        subject = template.get('subject', '').format(
            name=name,
            firm=firm,
            platform=platform
        )
        body = template.get('body', '').format(
            name=name.split()[0],  # First name only
            firm=firm,
            platform=platform,
            initial_date=initial_date
        )

        return {
            'send_date': send_date,
            'name': name,
            'email': email,
            'firm': firm,
            'type': inv_type,
            'platform': platform,
            'subject': subject,
            'body': body,
            'email_sequence': email_type,
            'days_after_initial': days_delay
        }

    def process_investors(self, csv_path):
        """Read investor list and generate all emails"""
        emails = []

        if not Path(csv_path).exists():
            print(f"❌ Error: {csv_path} not found")
            return emails

        with open(csv_path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                if not row.get('name') or row.get('name').startswith('#'):
                    continue  # Skip empty rows and comments

                priority = row.get('priority', 'MEDIUM').upper()

                # Only process HIGH and MEDIUM priority
                if priority not in ['HIGH', 'MEDIUM']:
                    continue

                # Generate email sequence for this investor
                # Initial email (day 0)
                email_0 = self.generate_email(row, 'initial', days_delay=0)
                if email_0:
                    emails.append(email_0)

                # Follow-up 1 (day 3)
                email_1 = self.generate_email(row, 'followup_1', days_delay=3)
                if email_1:
                    emails.append(email_1)

                # Follow-up 2 (day 5)
                email_2 = self.generate_email(row, 'followup_2', days_delay=5)
                if email_2:
                    emails.append(email_2)

        return emails

    def export_csv(self, emails, output_path):
        """Export emails to CSV"""
        if not emails:
            print("❌ No emails to export")
            return

        fieldnames = [
            'send_date', 'name', 'email', 'firm', 'type', 'platform',
            'email_sequence', 'days_after_initial', 'subject', 'body'
        ]

        with open(output_path, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(emails)

        print(f"✓ Exported {len(emails)} emails to {output_path}")
        return output_path


def main():
    import argparse

    parser = argparse.ArgumentParser(description='Generate LANCAST investor emails')
    parser.add_argument('--input', default='LANCAST_INVESTOR_LIST_TEMPLATE.csv',
                       help='Input CSV with investor list')
    parser.add_argument('--output', default='LANCAST_EMAILS_READY_TO_SEND.csv',
                       help='Output CSV with generated emails')

    args = parser.parse_args()

    print("🚀 LANCAST Email Generator")
    print(f"📥 Input: {args.input}")
    print(f"📤 Output: {args.output}")
    print()

    generator = EmailGenerator()
    emails = generator.process_investors(args.input)

    if emails:
        print(f"✓ Generated {len(emails)} email sequences")
        print(f"  • {len([e for e in emails if e['email_sequence'] == 'initial'])} initial emails")
        print(f"  • {len([e for e in emails if e['email_sequence'] == 'followup_1'])} follow-up #1")
        print(f"  • {len([e for e in emails if e['email_sequence'] == 'followup_2'])} follow-up #2")
        print()

        generator.export_csv(emails, args.output)
        print(f"✓ Ready to send! Import {args.output} to Lemlist/Gmail/HubSpot")
    else:
        print("❌ No emails generated. Check your input CSV.")


if __name__ == '__main__':
    main()
