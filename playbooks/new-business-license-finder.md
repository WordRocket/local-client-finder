# Where 30 cities publish brand-new businesses

A business that opened last week needs a website, a Google profile, reviews and a way to book, and nobody's pitching
it yet. Most big cities publish every new license or business registration as open data. Here's where to find them in
30 cities across the US and Canada, each one opened and checked on November 6, 2026.

---

## How to use any of these in 3 steps

1. **Open the link and filter the date field** to the last 14–30 days. Always add "date is on or before today": several
   files have typo dates in the future. Sort newest first.
2. **Keep only the new ones.** Use the "Keep only" column below (for example Chicago's `APPLICATION TYPE` = ISSUE).
   "Pending" or "in progress" means they haven't opened yet: the best moment to show up with a preview.
3. **Pick the categories that fit what you sell** (restaurants, salons, contractors, shops), check each one on Google
   Maps (listed? website? reviews?) and put the best 5 in your lead tracker.

On most portals (Chicago, NYC, LA, SF, Seattle, Texas, Calgary, Edmonton…) the filter is under **Actions › Query data**
or **Filter**, then **Export › CSV**. On map-style portals (DC, Denver, Sacramento, Miami-Dade, Fort Worth): **View data
table**, filter, then **Download › CSV**.

**Privacy, always:** many files also list owner names and home-based businesses. Skip home-based and sole-owner rows,
pitch the business at its business address or through its public phone or email, and never repost anyone's personal
details. Before emailing, follow CAN-SPAM (US) or CASL (Canada).

---

## US cities where every business registers

| City | Open this | Filter on | Keep only | Updates |
|---|---|---|---|---|
| Chicago, IL | [Business Licenses](https://data.cityofchicago.org/Community-Economic-Development/Business-Licenses/r5kz-chrr) | `DATE ISSUED` | `APPLICATION TYPE` = ISSUE (new) | daily |
| Los Angeles, CA | [Listing of Active Businesses](https://data.lacity.org/Administration-Finance/Listing-of-Active-Businesses/6rrh-rzua) | `LOCATION START DATE` (use 45 days) | by `PRIMARY NAICS DESCRIPTION` | monthly |
| San Francisco, CA | [Registered Business Locations](https://data.sf.gov/Economy-and-Community/Registered-Business-Locations-San-Francisco/g8m3-pdis) | `Location Start Date` | `Location End Date` blank | daily |
| Seattle, WA | [Active Business License Tax Certificate](https://data.seattle.gov/City-Administration/Active-Business-License-Tax-Certificate/wnbq-64tb) | `License Start Date` (text, YYYYMMDD) | by `NAICS Description` | daily |
| Washington, DC | [Basic Business License in Last 30 Days](https://opendata.dc.gov/datasets/a9ac9f8d9d1546e8bd6610b48cb29810_1) | `INITIALISSUEDATE` | skip Housing and Lodging | daily |
| Philadelphia, PA | [L&I Business Licenses](https://opendataphilly.org/datasets/licenses-and-inspections-business-licenses/) | `initialissuedate` | skip Rental and Vacant Residential | daily |
| New Orleans, LA | [Occupational Business Licenses](https://data.nola.gov/Economy-and-Workforce/Occupational-Business-Licenses/hjcd-grvu) | `BusinessStartDate` | skip Special Events and Flea Market | daily |
| Orlando, FL | [Business Tax Receipts](https://data.cityoforlando.net/Permitting/Business-Tax-Receipts/7388-4re5) | `Business Open Date` | active, by `License Category` | daily |
| Miami-Dade County, FL | [Local Business Tax](https://gis-mdc.opendata.arcgis.com/datasets/fba37cce964e4c55bd6a1614c6f789a0_0) | `BUSSDATE` (use 60 days) | `NEWBUS` = Yes, `BUSCITY` = your city | ~6 weeks behind |
| San Diego, CA | [Business Tax Certificates](https://data.sandiego.gov/datasets/business-tax-certificates/) | `date_account_creation` | "Active certificates" file | daily |
| Sacramento, CA | [Business Operation Tax Information](https://data.cityofsacramento.org/datasets/f4ee567a01fb4b1d95303c8446a999fa_0) | `Business_Start_Date` | Active or Pending | daily |
| Long Beach, CA | [Business Licenses (BizMap)](https://www.arcgis.com/home/item.html?id=54d45ca9c4554062a02df49ec1ea2b2a) | `ISSDTTM` | Issued, `HOMEBASED` = No (Intake = opening soon) | nightly |
| Tucson, AZ | [Business License Downloads](https://www.tucsonaz.gov/Departments/Business-Services-Department/Taxpayer-Assistance/Business-License-and-Tax-Information/Business-License-Downloads) | the newest monthly file | already only new businesses | monthly |
| Las Vegas, NV | [CLV Business Licenses](https://opendataportal-lasvegas.opendata.arcgis.com/datasets/f6b923ee5eb9450baf6adebaf0f307ed_0) | no date column: use `Status` | Pending (about to open) or Issued | irregular |

## Texas (no city business license, so use the state's sales-tax permits)

| City | Open this | Filter on | Keep only | Updates |
|---|---|---|---|---|
| Houston, Dallas, Austin, San Antonio (any Texas city) | [Active Sales Tax Permit Holders](https://data.texas.gov/Government-and-Taxes/Active-Sales-Tax-Permit-Holders/jrea-zgmq) | `Outlet Permit Issue Date` | `Outlet City` = your city; NAICS 722 (restaurants), 812 (personal services) | monthly |
| Fort Worth | [Certificates of Occupancy](https://data.fortworthtexas.gov/datasets/62085ec02e2440c3b1ea4a67e30f6b00_0) | `CODate` | `ApplicationType` = Occupancy | daily |

## US cities that publish part of the picture

| City | Open this | What it covers | Keep only | Updates |
|---|---|---|---|---|
| New York City | [Restaurant Inspection Results](https://data.cityofnewyork.us/Health/DOHMH-New-York-City-Restaurant-Inspection-Results/43nn-pn8j) · [Issued Licenses](https://data.cityofnewyork.us/Business/Issued-Licenses/w7w3-xahh) | new restaurants · licensed trades (contractors, electronics, garages…) | restaurants: `INSPECTION DATE` = 1900-01-01 (new, not yet inspected) · licenses: `Initial Issuance Date`, Premises | daily · weekly |
| Denver, CO | [Pending Business Licenses](https://opendata-geospatialdenver.hub.arcgis.com/datasets/59cc60ee6c0a4928a64ca97f890f4630_46) | food, liquor and other licensed types | `LICENSE_TYPE` = Retail Food (about to open) | daily |
| Boston, MA | [Active Food Establishment Licenses](https://data.boston.gov/dataset/active-food-establishment-licenses) | food only | newest `license_add_dt_tm` | daily |
| Portland, OR | [New Businesses Registered Last Month](https://data.oregon.gov/business/New-Businesses-Registered-Last-Month/esjy-u4fc) | every new Oregon registration | `City` = PORTLAND; check it's a storefront | monthly |
| Nashville, TN | [Beer Permit Locations](https://data.nashville.gov/datasets/44e9268cd0d548648980418dafdb42da_0) | restaurants, bars, markets | `Date_Entered` = applied recently | daily |

## Canada

| City | Open this | Filter on | Keep only | Updates |
|---|---|---|---|---|
| Toronto, ON | [Business Licences and Permits](https://open.toronto.ca/dataset/municipal-licensing-and-standards-business-licences-and-permits/) | `Issued` | `Cancel Date` blank; skip taxi and driving-school categories | daily |
| Vancouver, BC | [Business licences](https://opendata.vancouver.ca/explore/dataset/business-licences/) | `IssuedDate` | `LicenceRevisionNumber` = 00 (new); late Nov–Jan is renewal season | daily |
| Calgary, AB | [Calgary Business Licences](https://data.calgary.ca/Business-and-Economic-Activity/Calgary-Business-Licenses/vdjc-pybd) | `FIRST_ISS_DT` | `HOMEOCCIND` = N (skip home-based) | daily |
| Edmonton, AB | [Business Licences](https://data.edmonton.ca/Urban-Planning-Economy/City-of-Edmonton-Business-Licences/qhi4-bdpu) | `Original Issue Date` | by licence category | daily |
| Winnipeg, MB | [Business Licenses](https://data.winnipeg.ca/Neighbourhood-Liveability-Property-Standards-Licen/Business-Licenses/d5k3-sfzx) | `Issue Date` (use 60 days) | Personal Services (salons, spas) | monthly |
| Montréal, QC | [Établissements alimentaires](https://donnees.montreal.ca/dataset/etablissements-alimentaires) | `date_statut` | `statut` = Ouvert or En traitement (opening soon) | weekly |

---

## Your city isn't here?

- **State and provincial registries** (new LLCs and corporations; many are holding companies or home addresses, so
  check for a storefront or a Google listing first): [Colorado](https://data.colorado.gov/Business/Business-Entities-in-Colorado/4ykn-tg5h)
  (daily) · [Connecticut](https://data.ct.gov/Business/Connecticut-Business-Registry-Business-Master/n7gp-d28j) (daily) ·
  [Florida Sunbiz daily filings](https://dos.fl.gov/sunbiz/other-services/data-downloads/daily-data/) ·
  [Oregon](https://data.oregon.gov/business/New-Businesses-Registered-Last-Month/esjy-u4fc) (monthly) ·
  [Texas permits](https://data.texas.gov/Government-and-Taxes/Active-Sales-Tax-Permit-Holders/jrea-zgmq) (any Texas city) ·
  [Québec REQ](https://www.donneesquebec.ca/recherche/dataset/registre-des-entreprises) (bulk file) ·
  [Ontario Business Registry](https://www.ontario.ca/page/ontario-business-registry) (search only).
- **A nearby city often publishes:** for the Phoenix area, [Scottsdale](https://data.scottsdaleaz.gov/datasets/cf568f1934cc40f48c3c2a390b2c918c_6);
  in Orange County, [Anaheim's new licences](https://data-anaheim.opendata.arcgis.com/datasets/6f8709b334534538b8f993111f6bbc83_0).
- **Other "just opened" signals:** Google Maps listings with only a few, very recent reviews, Yelp's "Hot and New", local
  news "grand opening" posts, and "coming soon" signs on storefronts.
- **Searched and found nothing public (Nov 2026), so don't waste an evening:** Phoenix, San Jose, Oakland, Minneapolis,
  St. Paul, Detroit, Columbus, Baltimore, Charlotte, Raleigh, Indianapolis, Jacksonville, Tampa, Ottawa. Kansas City and
  Atlanta publish old snapshots only.

---

**Do it faster:** the free `find-new-businesses` skill checks city license data, Google Maps, Yelp "Hot and New" and
grand-opening news for you, then checks which ones have no website: github.com/WordRocket/local-client-finder. Or use
prompt 6 in "20 Claude prompts to land local clients". Portals change their links and fields; if one moves, search the
city's open-data site for "business license". Results vary.
