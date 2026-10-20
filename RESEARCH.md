# Research —20 October2026

Demand is **inferred**, not a verified request for this tool. Keeping only the cheapest arrival at a junction can discard the incoming edge needed to take a legal next turn.

## Observed comparables

Query `turn restrictions routing`, GitHub repository search sorted by Most stars: [exact search](https://github.com/search?q=turn+restrictions+routing&type=repositories&s=stars&o=desc). The highest-star relevant comparable found in this research pool is `Project-OSRM/osrm-backend`; this is not an exhaustive global ranking.

| Repository | Stars observed | Last push | License metadata | Workflow / scope |
| --- | ---: | --- | --- | --- |
| [Project-OSRM/osrm-backend](https://github.com/Project-OSRM/osrm-backend) | 8155 | 2026-10-17T18:33:22Z | BSD-2-Clause | C++ OSM routing engine with HTTP/library services and explicit restriction fixtures. |
| [graphhopper/graphhopper](https://github.com/graphhopper/graphhopper) | 6737 | 2026-10-19T15:12:43Z | Apache-2.0 | Java routing library/server with OSM/GTFS and map matching. |
| [valhalla/valhalla](https://github.com/valhalla/valhalla) | 6342 | 2026-10-19T19:20:21Z | NOASSERTION | OSM routing engine, matrices, isochrones and matching. |

## Workflow choice and tradeoffs

Routing developers reproducing a turn-restriction bug on a small extracted directed graph. Find minimum integer-cost routes over incoming-edge states with exact forbidden consecutive-edge pairs and compare an unrestricted baseline.

gpx-dwell-report analyzes recorded motion, redirect-graph checks web redirects and capacity-cut-report solves allocation flow. This is a route feasibility/cost witness for incoming-edge restrictions, not a map service.

This is a bounded dedicated report with an invented fixture and zero runtime dependencies. The established tools are broader; choose them when their ecosystem, formats or capabilities match the job. Our own installed example proves only our documented behavior. Competitor clean installs, time to first useful result, support response times, reliability and equivalent-workload performance were not measured. Current docs offer install/usage guidance; sampled issue activity is preserved as evidence, not a support-quality score. No feature absence or superiority is claimed.

## Coverage and evidence

The keyword search includes irrelevant results (SQL knowledge graphs, CSS critical paths, routing deployment projects and regex engines). Relevant comparables were also found directly; filtering was based on current README scope. [Exact dated metadata and issue samples](RESEARCH_PROVENANCE.json). Own acceptance and distinction: [brief](BRIEF.json). No implementation, branding or prose was copied.
