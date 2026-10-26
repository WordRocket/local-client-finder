# Where new businesses show up (public sources)

Use what exists for the user's city; combine 2–3 sources. Always note the source and date for each lead.

## 1. City open data: new business licenses (best)
Official and dated, usually updated daily or weekly.
- Socrata portals: `scripts/new_licenses.py find "<city>"`. Seen working (Oct 2026): Chicago (data.cityofchicago.org
  `r5kz-chrr`, use `--where "application_type='ISSUE'"`), Calgary (data.calgary.ca `vdjc-pybd`, has a home-occupation
  flag), Seattle, Cincinnati, New Orleans, Norfolk, Berkeley, Winnipeg, Delaware.
- Other portals: web search `"<city>" open data "business license"`. ArcGIS Hub and CKAN portals (e.g. Toronto's
  open.toronto.ca) offer CSV downloads; read the CSV and sort by the issue date.
- Watch for: renewals vs new issues, add-on licenses (patio, gaming, signage), chains.

## 2. State / provincial business registries
Some publish new registrations or let you search by date for free; many charge. Registrations often show a
registered agent or a home address: never use either for outreach. Use the registry only to learn the business
name, then find its public business channels.

## 3. Google Maps
New listings: very few reviews, a first review in the last weeks, "Opened <month>" or "New" labels. Confirm with a
second source before calling it new.

## 4. Yelp "Hot and New"
Restaurants, cafés, bars, shops. Filter Yelp search results by "Hot and New" for the city.

## 5. News and chambers
Web search, last 30–60 days: `"grand opening" <city>`, `"now open" <city>`, `"ribbon cutting" <city> chamber`.
Local business journals and city newsletters often list new openings.

## Privacy
Public business information only. No home addresses, no owners' personal phones or emails, no registered agents.
If a business only exists as a person's name at a home address, skip it.
