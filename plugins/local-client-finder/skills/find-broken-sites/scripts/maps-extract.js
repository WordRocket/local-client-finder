// Google Maps results → lead rows. Run it in the browser tab that shows a Google Maps search
// (https://www.google.com/maps/search/<niche>+in+<city>) with your browser tool's "run JavaScript" action.
// It scrolls the results list to the end (or MAX results), then returns JSON rows:
// {name, rating, reviews, category, website, phone, lat, lng, maps_url, sponsored}
// website = the hostname behind the listing's "Website" button, or "" when the listing has none.
(async () => {
  const MAX = 80;
  const feed = document.querySelector('div[role="feed"]');
  if (!feed) return JSON.stringify({error: 'No results list found. Open a Google Maps SEARCH (not a single place) and try again.'});
  const sleep = (ms) => new Promise((r) => setTimeout(r, ms));
  let last = 0, still = 0;
  for (let i = 0; i < 40; i++) {
    feed.scrollBy(0, 4000);
    await sleep(1500);
    const n = feed.querySelectorAll('a[href*="/maps/place/"]').length;
    if (n >= MAX || /end of the list/i.test(feed.innerText)) break;
    still = n === last ? still + 1 : 0;
    if (still >= 3) break;
    last = n;
  }
  const rows = [];
  const seen = new Set();
  for (const a of feed.querySelectorAll('a[href*="/maps/place/"]')) {
    const card = a.closest('div[role="feed"] > div');
    const name = (a.getAttribute('aria-label') || '').trim();
    if (!card || !name || seen.has(name)) continue;
    seen.add(name);
    const text = card.innerText;
    const lines = text.split('\n').map((s) => s.trim()).filter(Boolean);
    const rm = text.match(/(\d[.,]\d)\s*\(([\d,.\s]+)\)/);
    const web = [...card.querySelectorAll('a')].find((x) =>
      x.getAttribute('data-value') === 'Website' || /website/i.test(x.getAttribute('aria-label') || '') || x.innerText.trim() === 'Website');
    let website = '';
    if (web) { try { website = new URL(web.href).hostname.replace(/^www\./, ''); } catch (e) { website = 'yes'; } }
    const ph = text.match(/(\+?\(?\d[\d\s().-]{7,}\d)/);
    const ll = a.href.match(/!3d(-?\d+\.\d+)!4d(-?\d+\.\d+)/);
    // The category is the line after the rating ("4.8(105)" or "No reviews"), sometimes followed by " · address".
    const ri = lines.findIndex((l) => /^\d[.,]\d\s*\(/.test(l) || /^No reviews/i.test(l));
    const after = ri >= 0 ? lines[ri + 1] || '' : '';
    const cat = /^(Open|Closed|Closes|Opens|Temporarily|Permanently)/i.test(after) ? '' : after;
    rows.push({
      name,
      rating: rm ? Number(rm[1].replace(',', '.')) : null,
      reviews: rm ? Number(rm[2].replace(/[,.\s]/g, '')) : 0,
      category: cat.split('·')[0].trim(),
      website,
      phone: ph ? ph[1].trim() : '',
      lat: ll ? Number(ll[1]) : null,
      lng: ll ? Number(ll[2]) : null,
      maps_url: a.href.split('?')[0],
      sponsored: /Sponsored/.test(text),
    });
  }
  return JSON.stringify({query: document.title.replace(/ - Google Maps$/, ''), total: rows.length,
    no_website: rows.filter((r) => !r.website).length, rows});
})();
