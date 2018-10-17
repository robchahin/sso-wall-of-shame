# The SSO Wall of Shame

<details>
  <summary><strong>Why does this exist?</strong></summary>
  <p>Single sign-on (SSO) is a mechanism for outsourcing your website (or other product's) authentication to a third party identity provider, such as Google, Facebook, Okta, PingFederate, etc.</p>

<p>In this context, SSO refers to a SaaS or similar vendor allowing a business client to manage user accounts via their own identity provider, without having to rely on the vendor to provide strong authentication with audit logs, and with the ability to create and delete user accounts centrally, for all users, across all software in use by that org.</p>

<p>Beyond a handful of employees, this feature is critical for IT and Security teams to be able to effectively manage user accounts across dozens or hundreds of vendors, many of which don't support features like TOTP 2FA or U2F. In the event that an employee leaves the company, the IT team can immediately disable their access to all applications, rather than logging into 100 different user management portals.</p>

<p>Basically: SSO is a core security requirement for any company with more than five employees.</p>

<p>SaaS vendors appear not to have received this message, however. SSO is often only available as part of "Enterprise" pricing which assumes either a huge number of users (minimum seat count), or it's force-bundled with other "Enterprise" features which may have no value to the company using the software.</p>

<p>If companies claim to "take your security seriously", then SSO should be available either:</p>
<ol>
  <li>as a core product feature, or</li>
  <li>as an optional paid extra, for a reasonable delta, or</li>
  <li>the gap between the non-SSO tier and the SSO tier should be naturally small.</li>
</ol>

<p>Many vendors charge 2x, 3x, or 4x the base product pricing for access to SSO, which disincentivizes its use, and encourages poor security practices.</p>
</details>

## The List

Vendor | Base Pricing | SSO Pricing | % Increase | Source | Date Added
------ | ------------ | ----------- | ---------- |------ | ----------
DocuSign | $25 per u/m | $50 per u/m | 100% | [🔗](https://www.docusign.com/products-and-pricing) Quote | 2018-10-17
Expensify | $5 per u/m | $9 per u/m | 80% | [🔗](https://www.expensify.com/pricing#features) | 2018-10-17
Lucidchart | $7 per u/m | $CALL | ??? | [🔗](https://www.lucidchart.com/users/registerLevel) | 2017-10-17
PagerDuty | $9 per u/m | $39 per u/m | 333% | [🔗](https://www.pagerduty.com/pricing/) | 2018-10-17
RingCentral | $25 per u/m | $35 per u/m | 40% | [🔗](https://www.ringcentral.com/office/plansandpricing.html) | 2018-10-17
VictorOps | $9 per u/m | $49 per u/m | 544% | [🔗](https://victorops.com/pricing) | 2018-10-17

## FAQs

<details>
  <summary><strong>This doesn't scale linearly for number of seats!</strong></summary>
  <p>Correct. Since we don't know who's reading the page, it's easiest to just assume a team in the lowest pricing tier.</p>
</details>

<details>
  <summary><strong>How is base pricing determined?</strong></summary>
  <p>Disregard free tier pricing, as we can assume these aren't intended for long term business customer use. Probably also disregard "single person" pricing, and assume that we're looking on behalf of a team of 5, 10 or more people.</p>
</details>


<details>
  <summary><strong>What does "Call Us!" mean?</strong></summary>
<p>Many vendors do not list pricing for Enterprise-tier pricing, so to avoid calling all of them to get this data, "Call Us" may be listed as a placeholder. If you have numbers, please share them.</p>
  </details>

<details>
  <summary><strong>What does "Quote" mean in the Source column?</strong></summary>
<p>If a vendor doesn't list pricing but a user has submitted pricing based on a quote, it can be included here. If a vendor feels that their actual pricing is inaccurately reflected by this quote, feel free to let me know and I'll update the page.</p>
</details>
  
  
<details>
  <summary><strong>I'm a vendor and this data is wrong!</strong></summary>
<p>Please feel free to PR this page, or reach out at sso @ myGitHubUsername dotcom. I only want this data to be accurate.</p>
</details>
<details>
  <summary><strong>I'm a vendor and this doesn't reflect the value-add of our Enterprise tier!</strong></summary>
<p>That's the point. Decouple your security features from your value-added services, price them separately.</p>
</details>
