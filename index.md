---
---
<script src="assets/js/sort.js"></script>
<script src="assets/js/search.js"></script>
<script src="assets/js/popover.js"></script>

<details open>
<summary>
Why does this exist?
</summary>
Single sign-on (SSO) is a mechanism for outsourcing the authentication for your website (or other product) to a third party identity provider, such as Google, Okta, Entra ID (Azure AD), PingFederate, etc.

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

{% assign all = site.vendors | sort: "name" %}
{% assign vendors = "" | split: ',' %}
{% assign call_us = "" | split: ',' %}
{% for vendor in all %}
	{% assign sso_lower = vendor.sso_pricing | downcase %}
	{% if sso_lower contains "call" or sso_lower contains "contact" or sso_lower contains "custom" or sso_lower contains "quote" %}
		{% assign call_us = call_us | push: vendor %}
	{% else %}
		{% assign vendors = vendors | push: vendor %}
	{% endif %}
{% endfor %}

<input id="vendor-search" type="search" placeholder="Filter by vendor name…" aria-label="Filter vendors by name">

## Price Increases

<table class="sortable">
<thead>
<tr><th>Vendor</th><th>Base Pricing</th><th>SSO Pricing</th><th>Increase</th><th>Source</th><th>Updated</th></tr>
</thead>
<tbody>
{% for vendor in vendors %}
<tr>
<td markdown="span"><a href="{{ vendor.vendor_url }}">{{ vendor.name }}</a>{% if vendor.vendor_note %} <button class="info-toggle" aria-label="Note about {{ vendor.name }}" data-note="{{ vendor.vendor_note | escape }}">&#9432;</button>{% endif %}</td>
<td markdown="span" data-label="Base">{{ vendor.base_pricing }}</td>
<td markdown="span" data-label="SSO">{{ vendor.sso_pricing }}</td>
<td markdown="span" data-label="Increase">{{ vendor.percent_increase }}</td>
<td data-label="Source">
{% for source in vendor.pricing_source %}
{% if forloop.first == false %}
&amp;
{% endif %}
<a href="{{ source }}" aria-label="Pricing source for {{ vendor.name }}" title="Pricing source for {{ vendor.name }}">&#128279;</a>
{% endfor %}
{% if vendor.pricing_source_info %}<button class="info-toggle" aria-label="Source info for {{ vendor.name }}" data-note="{{ vendor.pricing_source_info | escape }}">&#9432;</button>{% endif %}</td>
<td data-label="Updated">{{ vendor.updated_at }}</td>
</tr>
{% endfor %}
</tbody>
</table>
<p class="search-empty" style="display:none">No vendors in this list match your search.</p>

## Quotes Required
Some vendors simply do not list their pricing for SSO because the pricing is negotiated with an account manager. These vendors get their own table as we assume they apply a significant premium for SSO.

<table class="sortable">
<thead>
<tr><th>Vendor</th><th>Base Pricing</th><th>SSO Pricing</th><th>Increase</th><th>Source</th><th>Updated</th></tr>
</thead>
<tbody>
{% for vendor in call_us %}
<tr>
<td markdown="span"><a href="{{ vendor.vendor_url }}">{{ vendor.name }}</a>{% if vendor.vendor_note %} <button class="info-toggle" aria-label="Note about {{ vendor.name }}" data-note="{{ vendor.vendor_note | escape }}">&#9432;</button>{% endif %}</td>
<td markdown="span" data-label="Base">{{ vendor.base_pricing }}</td>
<td markdown="span" data-label="SSO">{{ vendor.sso_pricing }}</td>
<td markdown="span" data-label="Increase">{{ vendor.percent_increase }}</td>
<td data-label="Source">
{% for source in vendor.pricing_source %}
{% if forloop.first == false %}
&amp;
{% endif %}
<a href="{{ source }}" aria-label="Pricing source for {{ vendor.name }}" title="Pricing source for {{ vendor.name }}">&#128279;</a>
{% endfor %}
{% if vendor.pricing_source_info %}<button class="info-toggle" aria-label="Source info for {{ vendor.name }}" data-note="{{ vendor.pricing_source_info | escape }}">&#9432;</button>{% endif %}</td>
<td data-label="Updated">{{ vendor.updated_at }}</td>
</tr>
{% endfor %}
</tbody>
</table>
<p class="search-empty" style="display:none">No vendors in this list match your search.</p>

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
What does the ⓘ icon next to a source mean?
</summary>
If a vendor doesn't publicly list their SSO pricing but a user has submitted pricing based on a quote or other non-public source, a note will be shown next to the source link. If a vendor feels that their actual pricing is inaccurately reflected, feel free to let me know and I'll update the page.
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

