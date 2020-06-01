---
---
<details open>
<summary>
Why does this exist?
</summary>
Single sign-on (SSO) is a mechanism for outsourcing the authentication for your website (or other product) to a third party identity provider, such as Google, Azure AD, Okta, PingFederate, etc.

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

<table>
<thead>
<tr><th>Vendor</th><th>Base Pricing</th><th>SSO Pricing</th><th>% Increase</th><th>Source</th><th>Date Updated</th></tr>
</thead>
<tbody>
{% for vendor in site.data.vendors %}
<tr>
<td markdown="span"><a href="{{ vendor.url }}">{{ vendor.name }}</a></td>
<td markdown="span">{{ vendor.base_pricing }}</td>
<td markdown="span">{{ vendor.sso_pricing }}</td>
<td markdown="span">{{ vendor.percent_increase }}</td>
<td>
{% for source in vendor.pricing_source %}
{% if forloop.first == false %}
&amp;
{% endif %}
<a href="{{ source }}">&#128279;</a>
{% endfor %}
{{ vendor.pricing_note }}</td>
<td>{{ vendor.updated_at }}</td>
</tr>
{% endfor %}
</tbody>
</table>

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

<details>
<summary>
But it costs money to provide SAML support, so we can't offer it for free!
</summary>
  While I'd like people to really consider it a <em>bare minimum</em> feature for business SaaS, I'm OK with it costing a little extra to cover maintenance costs. If your SSO support is a 10% price hike, you're not on this list. But these percentage increases are not maintenance costs, they're revenue generation because you know your customers have no good options.
</details>

## Footnotes
{% for vendor in site.data.vendors %}
{{ vendor.footnotes }}
{% endfor %}
