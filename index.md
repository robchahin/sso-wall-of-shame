---
---
<script src="assets/js/sort.js"></script>
<script src="assets/js/search.js"></script>
<script src="assets/js/popover.js"></script>

Single sign-on (SSO) is how your team logs in once to securely access all their applications. You’ve used it if you’ve logged in with Okta, Google, or your social network accounts to other websites.

For <strong>users</strong>, SSO is convenient: one password, one time, maybe a security key if you’re lucky, gets you everywhere. It’s easy, quick, and you don’t have to think about it.

For <strong>IT and Security teams</strong>, SSO is invaluable. A modern company uses dozens, if not hundreds, of software vendors. SSO provides a single place to onboard, manage, and offboard users. It centralizes security controls like strong authentication, logging, and account recovery.

For <strong>software vendors</strong>, it lets your customers be responsible for their own esoteric security demands. Some jazzy new hardware authenticator that’s only existed for three weeks? You don’t need to support it – that’s up to the SSO provider. 

<strong>SSO is a core security requirement for any company with more than five employees.</strong>

Some vendors exploit this. They offer competitive starter plans and  gate SSO behind an "Enterprise" paywall bundled with unnecessary features or large minimum seat counts. This can inflate the cost by 3x, 5x, 10x, or more, forcing smaller companies to choose between a secure environment and an affordable budget.

This pricing strategy punishes growing businesses and encourages dangerous security shortcuts. If a company claims to "take your security seriously," SSO should be included in all plans or available for a reasonable charge.

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

