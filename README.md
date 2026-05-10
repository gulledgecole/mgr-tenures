# A study of manager tenures across sports. 

References: Scraping https://www.sports-reference.com/ to start.

# EPL Manager Tenure Analysis — Project Spec

**Version:** 0.1 (draft)
**Last updated:** 2026-05-09

## 1. Research question

Are English Premier League managers being dismissed more quickly than they used to be? If so, by how much, and what factors correlate with shorter tenures?

## 2. Hypothesis

Average managerial tenure in the EPL has decreased over time. Managers are given fewer matches to demonstrate competence before being dismissed, controlling for performance.

## 3. Scope

- **League:** English Premier League only (top flight, 1992–93 onward).
- **Time window:** 1992–93 season through the most recently completed season.
- **Subjects:** All managers who held a permanent (non-caretaker) role for at least one match in the EPL.

## 4. Key definitions

- **Tenure start:** Date of first competitive match in charge of the club's first team in the EPL.
- **Tenure end:** Date of departure announcement, or final match in charge — whichever is documented in the source.
- **Departure types:**
  - *Sacked* — explicit dismissal.
  - *Mutual consent* — treated as a dismissal in primary analysis (per common practice).
  - *Resigned for another job* — voluntary; tracked separately.
  - *Retired / contract end / health* — tracked separately.
  - *Caretaker* — excluded from primary analysis but kept in the dataset with a flag.
- **Forced departure:** Sacked + mutual consent. This is the primary "firing" category.

## 5. Primary metric

**Median days in role at time of forced departure**, grouped by year of appointment (or 5-year buckets to reduce noise).

## 6. Supporting metrics

- Mean and median matches managed before forced departure.
- Forced departures per season, league-wide.
- Points-per-match at time of departure vs. club's long-run average.
- Share of all departures that are forced (vs. voluntary).

## 7. Planned data layers

| Layer | Content | Priority | Likely source |
|---|---|---|---|
| 1. Tenure | Manager, club, dates, departure reason, matches | Must-have (v1) | Wikipedia "List of [Club] managers" pages |
| 2. Performance | Points, position, results during tenure | High | football-data.co.uk (free CSV match data) |
| 3. Club context | Wealth, ownership changes, league position trend | Medium | Deloitte Money League, Wikipedia |
| 4. Trophies | Domestic and European honors during tenure | Medium | Wikipedia |
| 5. Sentiment | Press / fan sentiment near time of departure | Low (v2+) | News archives, possibly headline scraping |

## 8. Analytical approach (v1)

1. Build the tenure dataset.
2. Plot median tenure length by year of appointment over time.
3. Test for a statistically significant trend (linear regression on year vs. tenure length, with appropriate handling for right-censoring of currently-active managers).
4. Survival analysis (Kaplan-Meier) treating forced departure as the event, voluntary departure as censoring.

## 9. Out of scope for v1

- Lower divisions and non-English leagues.
- Caretaker spells.
- Causal claims about *why* tenure has changed (only descriptive trends).
- Predictive modeling of individual firings.

## 10. Success criteria

- A clean tenure dataset of ~600–800 rows covering all EPL clubs since 1992.
- A reproducible notebook that produces the headline chart (median tenure over time) from raw inputs.
- A clear yes/no answer to the headline question with quantified effect size and uncertainty.

## 11. Open questions

- How to handle the same manager returning to the same club (e.g., separate spells)? — Treat as separate tenure rows.
- How to handle interim-then-permanent appointments? — Tenure starts when permanent role begins; track interim period as a flagged note.
- Cutoff for "manager" vs. "head coach" given the recent director-of-football model? — Use whoever is publicly named as senior matchday decision-maker.