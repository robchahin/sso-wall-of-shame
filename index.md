---
---
<details open>
<summary>
Why does this exist?
</summary>
Single sign-on (SSO) is a mechanism for outsourcing the authentication for your website (or other product) to a third party identity provider, such as Google, Facebook, Okta, PingFederate, etc.

In this context, SSO refers to a SaaS or similar vendor allowing a business client to manage user accounts via the client's own identity provider, without having to rely on the vendor to provide strong authentication with audit logs, and with the ability to create and delete user accounts centrally, for all users, across all software in use by that client.

For organizations with more than a handful of employees, this feature is critical for IT and Security teams to be able to effectively manage user accounts across dozens or hundreds of vendors, many of which don't support features like TOTP 2FA or U2F. In the event that an employee leaves the company, it allows the IT team to immediately disable their access to all applications, rather than logging into 100 different user management portals.

In short: SSO is a core security requirement for any company with more than five employees.

SaaS vendors appear not to have received this message, however. SSO is often only available as part of "Enterprise" pricing, which assumes either a huge number of users (minimum seat count) or is force-bundled with other "Enterprise" features which may have no value to the company using the software.

If companies claim to "take your security seriously", then SSO should be available as a feature that is either:

1. part of the core product, or
1. an optional paid extra for a reasonable delta, or
1. attached to a price tier, but with a reasonably small gap between the non-SSO tier and SSO tiers.

Many vendors charge 2x, 3x, or 4x the base product pricing for access to SSO, which disincentivizes its use and encourages poor security practices.
</details>

## The List

Vendor | Base Pricing | SSO Pricing | % Increase | Source | Date Updated
------ | ------------ | ----------- | ---------- | ------ | ----------
[Airtable](https://airtable.com) | $10 per u/m | Call Us! | 100%+ | [🔗](https://airtable.com/pricing) | 2018-10-17
[Box](https://www.box.com) | $5 per u/m | $15 per u/m | 200% | [🔗](https://www.box.com/pricing) | 2018-10-17
[CloudSploit](https://cloudsploit.com) | $36 pcm | $99 pcm | 175% | [🔗](https://cloudsploit.com) | 2018-10-20
[DocuSign](https://www.docusign.com) | $25 per u/m | $50 per u/m | 100% | [🔗](https://www.docusign.com/products-and-pricing) Quote | 2018-10-17
[Dropbox](https://www.dropbox.com) | $15 per u/m | $25 per u/m | 67% |  [🔗](https://www.dropbox.com/business/pricing) | 2018-10-17
[Expensify](https://www.expensify.com) | $5 per u/m | $9 per u/m | 80% | [🔗](https://www.expensify.com/pricing#features) | 2018-10-17
[Github](https://www.github.com) | $9 per u/m | $21 per u/m | 133% | [🔗](https://github.com/pricing) | 2018-10-19
[Lucidchart](https://www.lucidchart.com) | $7 per u/m | Call Us! | ??? | [🔗](https://www.lucidchart.com/users/registerLevel) | 2018-10-17
[Netlify](https://www.netlify.com/) | $9 per u/m | Call Us! | ??? | [🔗](https://www.netlify.com/pricing/) | 2018-10-20
[New Relic Infrastructure](https://newrelic.com/products/infrastructure) | $0.60 - $7.20 per host-month[^newrelic-price] | $1.20 - $14.40 per host-month | 100% | [🔗](https://newrelic.com/products/infrastructure/pricing) | 2018-10-18
[PagerDuty](https://www.pagerduty.com) | $9 per u/m | $39 per u/m | 333% | [🔗](https://www.pagerduty.com/pricing/) | 2018-10-17
[RingCentral](https://www.ringcentral.com) | $25 per u/m | $35 per u/m | 40% | [🔗](https://www.ringcentral.com/office/plansandpricing.html) | 2018-10-17
[Sentry](https://sentry.io) | $26 for 100K events | $80 for 100K events | 208% | [🔗](https://sentry.io/pricing/) | 2018-10-20
[Slack](https://slack.com) | $6.67 per u/m | $12.50 per u/m | 87% | [🔗](https://slack.com/pricing) | 2018-10-17
[SumoLogic](https://www.sumologic.com) | $90 per GB/m | $150 per GB/m | 67% | [🔗](https://www.sumologic.com/pricing/) | 2018-10-19
[Trello](https://trello.com) | $10 per u/m | $21 per u/m | 110% | [🔗](https://trello.com/pricing) | 2018-10-17
[VictorOps](https://victorops.com) | $9 per u/m | $49 per u/m | 544% | [🔗](https://victorops.com/pricing) | 2018-10-17
[Zendesk Support](https://www.zendesk.com/support/) | $19 per u/m | $49 per u/m | 157% | [🔗](https://www.zendesk.com/support/compare/) | 2018-10-19

## FAQs

<details>
<summary>
This doesn't scale linearly for number of seats!
</summary>
Correct. Since we don't know who's reading the page, it's easiest to just assume a team with no volume discount.
</details>

<details>
<summary>
How is base pricing determined?
</summary>
We disregard free tier pricing, as we can assume these aren't intended for long term business customer use. We also disregard "single person" pricing, under the assumption that we're looking on behalf of a team of 5, 10, or more people.
</details>

<details>
<summary>
What does "Call Us!" mean?
</summary>
Many vendors do not list pricing for Enterprise-tier pricing. To avoid needing to call all of them to get this data, "Call Us!" may be listed as a placeholder. If you have numbers, please share them.
</details>

<details>
<summary>
What does "Quote" mean in the Source column?
</summary>
If a vendor doesn't list pricing but a user has submitted pricing based on a quote, it can be included here. If a vendor feels that their actual pricing is inaccurately reflected by this quote, feel free to let me know and I'll update the page.
</details>

<details>
<summary>
I'm a vendor and this data is wrong!
</summary>
Please feel free to submit a PR to this page, or reach out at sso @ myGitHubUsername dotcom. I only want this data to be accurate.
</details>

<details>
<summary>
I'm a vendor and this doesn't reflect the value-add of our Enterprise tier!
</summary>
That's the point. Decouple your security features from your value-added services. They should be priced separately.
</details>

[^newrelic-price]: Pricing varies by host size. The SSO cost increase does not.
