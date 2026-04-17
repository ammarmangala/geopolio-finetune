"""Shared dataset constants and helpers for the Geopolio workflow."""

from __future__ import annotations

import json
import random
from collections import Counter
from pathlib import Path


INSTRUCTION = "Analyze the geopolitical risk of the following situation for European retail investors."
IMPACTS = {range(1, 4): "Low", range(4, 6): "Moderate", range(6, 9): "High", range(9, 11): "Critical"}

CATEGORIES = [
    "Energy Security",
    "Regional Conflict",
    "Financial Contagion",
    "Trade Disruption",
    "Resource Security",
    "Political Fragmentation",
    "Cyber Warfare",
    "Nuclear Proliferation",
    "Alliance Cohesion",
    "Resource Nationalism",
    "Migration and Border Security",
    "Technology Governance",
]

REGION_DETAILS = {
    "Europe": {
        "actors": ["the European Commission", "a coalition of eurozone governments", "the ECB and national regulators", "several EU interior ministries"],
        "companies": ["Siemens", "Airbus", "Volkswagen", "BNP Paribas"],
        "indices": ["EURO STOXX 50", "MSCI Europe", "CAC 40", "DAX"],
        "sectors": ["banks", "industrials", "transport operators", "consumer cyclicals"],
    },
    "Middle East": {
        "actors": ["Iran", "Saudi Arabia", "a Gulf shipping coalition", "a regional militia network"],
        "companies": ["Shell", "BP", "TotalEnergies", "Lufthansa"],
        "indices": ["Stoxx Europe 600 Oil & Gas", "EURO STOXX 50", "FTSE 100", "DAX"],
        "sectors": ["airlines", "refiners", "chemicals producers", "shipping firms"],
    },
    "East Asia": {
        "actors": ["China", "Taiwanese authorities", "a regional naval command", "Japanese trade officials"],
        "companies": ["ASML", "Infineon", "SAP", "Stellantis"],
        "indices": ["MSCI World Technology", "DAX", "AEX", "EURO STOXX Technology"],
        "sectors": ["semiconductors", "automotive manufacturers", "electronics importers", "industrial exporters"],
    },
    "Southeast Asia": {
        "actors": ["ASEAN trade officials", "a military-led government", "a regional port authority", "a commodities ministry"],
        "companies": ["Maersk", "Adidas", "Puma", "H&M"],
        "indices": ["Stoxx Europe 600", "DAX", "OMX Copenhagen 25", "MSCI Europe Consumer Discretionary"],
        "sectors": ["apparel supply chains", "shipping", "consumer brands", "electronics assemblers"],
    },
    "Central Asia": {
        "actors": ["Kazakh energy officials", "a pipeline consortium", "regional security services", "an Eurasian customs bloc"],
        "companies": ["OMV", "Eni", "Raiffeisen Bank", "BASF"],
        "indices": ["ATX", "FTSE MIB", "DAX", "MSCI Europe Energy"],
        "sectors": ["pipeline operators", "fertilizer producers", "banks", "energy traders"],
    },
    "Latin America": {
        "actors": ["a Latin American finance ministry", "Brazilian trade officials", "an Andean mining regulator", "a regional protest movement"],
        "companies": ["Santander", "BBVA", "Glencore", "Iberdrola"],
        "indices": ["IBEX 35", "EURO STOXX 50", "FTSE 100", "MSCI Europe Materials"],
        "sectors": ["banks", "miners", "utilities", "agribusiness exporters"],
    },
    "Sub-Saharan Africa": {
        "actors": ["a military junta", "regional peacekeepers", "a sovereign debt office", "a telecom regulator"],
        "companies": ["Orange", "TotalEnergies", "Heidelberg Materials", "Vodafone"],
        "indices": ["CAC 40", "FTSE 100", "MSCI Europe", "Stoxx Europe 600 Telecom"],
        "sectors": ["telecoms", "cement producers", "energy majors", "frontier debt holders"],
    },
    "North Africa": {
        "actors": ["Algerian energy officials", "Egyptian canal authorities", "a North African protest coalition", "a border security command"],
        "companies": ["Eni", "Naturgy", "CMA CGM", "Engie"],
        "indices": ["FTSE MIB", "IBEX 35", "CAC 40", "MSCI Europe Utilities"],
        "sectors": ["gas importers", "shipping", "utilities", "tourism operators"],
    },
    "West Africa": {
        "actors": ["a Sahel junta", "ECOWAS officials", "a uranium export agency", "a coastal port authority"],
        "companies": ["Orano", "EDF", "Engie", "Bollore"],
        "indices": ["CAC 40", "EURO STOXX Utilities", "MSCI Europe Industrials", "AEX"],
        "sectors": ["nuclear utilities", "logistics", "miners", "infrastructure contractors"],
    },
    "Transatlantic": {
        "actors": ["US trade officials", "NATO diplomats", "Washington sanctions authorities", "a transatlantic technology task force"],
        "companies": ["Airbus", "SAP", "ArcelorMittal", "ASML"],
        "indices": ["EURO STOXX 50", "DAX", "CAC 40", "Stoxx Europe 600"],
        "sectors": ["industrials", "technology exporters", "steelmakers", "defense contractors"],
    },
    "Arctic": {
        "actors": ["Arctic shipping authorities", "a Nordic defense command", "Russian resource agencies", "an LNG consortium"],
        "companies": ["Equinor", "Neste", "Aker BP", "Maersk"],
        "indices": ["OBX", "OMX Copenhagen 25", "MSCI Europe Energy", "Stoxx Europe 600"],
        "sectors": ["LNG", "shipping", "offshore drilling", "defense logistics"],
    },
    "Eastern Europe": {
        "actors": ["Russia", "Ukrainian authorities", "a Black Sea security command", "a regional gas transit operator"],
        "companies": ["MOL", "Raiffeisen Bank", "PKN Orlen", "CEZ"],
        "indices": ["WIG20", "DAX", "MSCI Europe Energy", "ATX"],
        "sectors": ["utilities", "banks", "refiners", "grain logistics"],
    },
    "Northern Europe": {
        "actors": ["Nordic defense officials", "Baltic regulators", "a subsea cable operator", "a shipping insurer consortium"],
        "companies": ["Saab", "Maersk", "Nokia", "Ericsson"],
        "indices": ["OMX Stockholm 30", "OMX Copenhagen 25", "Stoxx Europe 600", "MSCI Europe Industrials"],
        "sectors": ["shipping", "telecom equipment", "defense", "renewables"],
    },
    "South Asia": {
        "actors": ["Indian trade officials", "Pakistan's security establishment", "a regional port operator", "a South Asian central bank"],
        "companies": ["Unilever", "Maersk", "HSBC", "AstraZeneca"],
        "indices": ["FTSE 100", "Stoxx Europe 600", "MSCI Europe Health Care", "OMX Copenhagen 25"],
        "sectors": ["consumer staples", "ports", "banks", "pharmaceuticals"],
    },
    "Western Balkans": {
        "actors": ["Serbian authorities", "Kosovo security forces", "EU accession negotiators", "a regional utility regulator"],
        "companies": ["Erste Group", "OMV", "Wienerberger", "Telekom Austria"],
        "indices": ["ATX", "DAX", "MSCI Europe", "Stoxx Europe 600 Banks"],
        "sectors": ["banks", "utilities", "construction materials", "telecoms"],
    },
    "Central Africa": {
        "actors": ["a mining ministry", "a presidential guard faction", "a cobalt export board", "regional customs officials"],
        "companies": ["Glencore", "Umicore", "BASF", "Stellantis"],
        "indices": ["BEL 20", "DAX", "MSCI Europe Materials", "EURO STOXX Autos"],
        "sectors": ["battery materials", "miners", "chemical processors", "EV supply chains"],
    },
    "East Africa": {
        "actors": ["Ethiopian officials", "Red Sea maritime authorities", "a sovereign debt office", "a regional telecoms ministry"],
        "companies": ["MSC", "Vodafone", "Orange", "Nestle"],
        "indices": ["Stoxx Europe 600", "CAC 40", "FTSE 100", "MSCI Europe Consumer Staples"],
        "sectors": ["shipping", "telecoms", "consumer staples", "infrastructure lenders"],
    },
    "Space": {
        "actors": ["a major space agency", "a satellite operator consortium", "a cyber command", "a launch regulator"],
        "companies": ["Airbus", "SES", "Thales", "Eutelsat"],
        "indices": ["CAC 40", "EURO STOXX Aerospace & Defense", "Stoxx Europe 600", "MSCI Europe Communications"],
        "sectors": ["satellites", "defense electronics", "telecom networks", "navigation services"],
    },
}

REGIONS = list(REGION_DETAILS.keys())

CATEGORY_DETAILS = {
    "Energy Security": {
        "triggers": [
            "has suspended critical fuel exports after a pricing dispute",
            "has imposed emergency quotas on gas and oil shipments",
            "has redirected LNG cargoes away from European buyers",
            "has restricted pipeline flows during a diplomatic standoff",
            "has delayed maintenance on a strategic energy corridor",
        ],
        "channel": "higher fuel, power, and transport costs across Europe",
        "score_range": (6, 9),
    },
    "Regional Conflict": {
        "triggers": [
            "has mobilized forces near a disputed border",
            "has exchanged artillery fire with a neighboring state",
            "has launched cross-border drone strikes on logistics hubs",
            "has declared a limited military exclusion zone",
            "has placed reserve units on high alert after clashes",
        ],
        "channel": "sanctions risk, transport disruption, and a confidence shock",
        "score_range": (6, 9),
    },
    "Financial Contagion": {
        "triggers": [
            "has requested emergency liquidity support after a debt rollover failure",
            "has frozen withdrawals at several mid-sized banks",
            "has delayed sovereign bond payments pending restructuring talks",
            "has imposed capital controls during a currency panic",
            "has suffered a disorderly sell-off in local debt markets",
        ],
        "channel": "spread widening, bank exposure, and eurozone risk repricing",
        "score_range": (5, 8),
    },
    "Trade Disruption": {
        "triggers": [
            "has tightened inspections on cargo moving through a strategic chokepoint",
            "has halted container traffic after a security incident",
            "has imposed emergency customs checks on high-value imports",
            "has limited access to a major export corridor",
            "has forced shippers to reroute around an unstable maritime zone",
        ],
        "channel": "delays, freight inflation, and inventory shortages",
        "score_range": (5, 9),
    },
    "Resource Security": {
        "triggers": [
            "has restricted exports of a critical industrial input",
            "has suspended mining licenses pending a national review",
            "has diverted strategic raw materials to domestic buyers",
            "has revised royalty rules for key metals and minerals",
            "has delayed shipments of uranium, copper, or rare materials",
        ],
        "channel": "scarcity in European industrial and energy supply chains",
        "score_range": (5, 8),
    },
    "Political Fragmentation": {
        "triggers": [
            "has triggered a coalition collapse ahead of a budget vote",
            "has called a snap election after mass protests",
            "has failed to pass a constitutional reform package",
            "has entered a prolonged standoff between parliament and the executive",
            "has seen regional leaders reject a central government deal",
        ],
        "channel": "policy uncertainty and weaker investor confidence",
        "score_range": (4, 7),
    },
    "Cyber Warfare": {
        "triggers": [
            "has suffered a cyberattack on energy and transport networks",
            "has blamed a foreign actor for disabling payment rails",
            "has detected malware inside satellite and telecom infrastructure",
            "has reported coordinated ransomware attacks on customs systems",
            "has lost access to strategic data centers after a breach",
        ],
        "channel": "operational outages, payment disruption, and digital trust erosion",
        "score_range": (5, 8),
    },
    "Nuclear Proliferation": {
        "triggers": [
            "has accelerated a contested nuclear enrichment program",
            "has blocked inspectors from visiting sensitive facilities",
            "has tested delivery systems tied to nuclear signaling",
            "has withdrawn from a major non-proliferation understanding",
            "has expanded military nuclear rhetoric during a crisis",
        ],
        "channel": "energy market stress, sanctions escalation, and defense repricing",
        "score_range": (7, 10),
    },
    "Alliance Cohesion": {
        "triggers": [
            "has vetoed a major security initiative inside an allied bloc",
            "has delayed joint defense planning over procurement disputes",
            "has threatened to suspend intelligence sharing with partners",
            "has blocked emergency funding for a collective mission",
            "has publicly challenged treaty commitments during a summit",
        ],
        "channel": "higher security uncertainty and slower coordinated response",
        "score_range": (4, 7),
    },
    "Resource Nationalism": {
        "triggers": [
            "has nationalized strategic assets held by foreign investors",
            "has raised export taxes on metals and energy products",
            "has forced foreign operators to cede majority ownership",
            "has rewritten concession contracts in favor of the state",
            "has threatened confiscation unless firms expand local processing",
        ],
        "channel": "margin compression and weaker legal certainty for multinationals",
        "score_range": (5, 8),
    },
    "Migration and Border Security": {
        "triggers": [
            "has seen border crossings surge after a regional security breakdown",
            "has tightened border controls following migrant pressure",
            "has suspended asylum processing amid an emergency influx",
            "has accused a neighbor of weaponizing migrant flows",
            "has redirected police and military resources toward border management",
        ],
        "channel": "political pressure, labor disruption, and fiscal strain",
        "score_range": (4, 7),
    },
    "Technology Governance": {
        "triggers": [
            "has imposed export controls on advanced chips and industrial software",
            "has banned critical digital platforms from public infrastructure",
            "has tightened licensing for semiconductor tools and cloud capacity",
            "has mandated local storage rules for sensitive industrial data",
            "has restricted AI, telecom, or surveillance technology transfers",
        ],
        "channel": "costlier compliance and slower technology supply chains",
        "score_range": (5, 8),
    },
}

DECADES = [
    {
        "label": "2000-2010",
        "years": list(range(2000, 2011)),
        "contexts": [
            "as post-9/11 security costs were still reshaping trade and insurance",
            "while early eurozone integration was still being tested by external shocks",
            "amid fragile post-crisis bank balance sheets and volatile commodity prices",
            "during a phase of rapid EU enlargement and uneven market integration",
        ],
    },
    {
        "label": "2010-2020",
        "years": list(range(2010, 2021)),
        "contexts": [
            "as eurozone debt stress was already influencing risk premiums",
            "while global supply chains were becoming more interdependent",
            "amid rising populism, sanctions cycles, and tariff disputes",
            "during a period of repeated central bank intervention and political volatility",
        ],
    },
    {
        "label": "2020-2024",
        "years": list(range(2020, 2025)),
        "contexts": [
            "while supply chains remained fragile after the pandemic shock",
            "amid elevated inflation, sanctions, and tighter monetary policy",
            "as energy and shipping markets were already facing repeated disruptions",
            "during a period of faster geopolitical decoupling in technology and trade",
        ],
    },
]

GENERATION_DECADES = [
    (
        "2000-2010",
        [
            "9/11 economic aftermath and War on Terror impact on markets",
            "2003 Iraq War and oil price shock",
            "2004-2007 EU enlargement with Poland and Baltic states",
            "2006 Russia-Ukraine gas dispute",
            "2007 Estonia cyberattack by Russia",
            "2007-2008 Global financial crisis and Lehman Brothers",
            "2008 Russia-Georgia war over South Ossetia",
            "2005 Hurricane Katrina oil supply disruption",
            "2004 Madrid bombings economic impact",
            "2009 Dubai World debt crisis",
            "2001 Argentina sovereign default",
            "2003 SARS outbreak supply chain disruption",
            "2006 Israel-Lebanon war shipping disruption",
            "2008 Zimbabwe hyperinflation contagion fears",
            "2009 Greek debt crisis early signs",
        ],
    ),
    (
        "2010-2020",
        [
            "2010 Greek sovereign debt crisis and eurozone contagion",
            "2011 Arab Spring and North African instability",
            "2011 Fukushima nuclear disaster supply chain impact",
            "2012 Iran nuclear sanctions and oil embargo",
            "2013 Cyprus banking crisis and bail-in",
            "2014 Russia annexation of Crimea and Ukraine crisis",
            "2015 Greek debt referendum and Grexit fears",
            "2016 Brexit referendum shock",
            "2016 Turkey coup attempt and lira crisis",
            "2017 Qatar diplomatic blockade by Gulf states",
            "2018 US-China trade war tariffs",
            "2019 Hong Kong protests and Chinese market impact",
            "2019 Saudi Aramco drone attack",
            "2015 Refugee crisis and European border tensions",
            "2018 Italian populist government bond crisis",
        ],
    ),
    (
        "2020-2024",
        [
            "2020 COVID-19 pandemic supply chain collapse",
            "2021 Suez Canal Ever Given blockage",
            "2021 Belarus migrant crisis at Polish border",
            "2022 Russia invasion of Ukraine energy crisis",
            "2022 Nord Stream pipeline sabotage",
            "2022 Taiwan Strait military exercises",
            "2023 Houthi Red Sea shipping attacks",
            "2023 Wagner Group mutiny in Russia",
            "2023 Israel-Hamas war regional escalation",
            "2024 Chinese rare earth export restrictions",
            "2024 US chip export controls on ASML",
            "2023 Niger coup and Sahel instability",
            "2022 Sri Lanka sovereign default",
            "2023 Silicon Valley Bank collapse contagion",
            "2024 EU Carbon Border Adjustment Mechanism",
        ],
    ),
]

EXAMPLE = {
    "instruction": INSTRUCTION,
    "input": "Russia has completely cut off natural gas supplies to Poland and Bulgaria, citing non-payment in rubles.",
    "output": "{\"risk_score\": 8, \"region\": \"Eastern Europe\", \"category\": \"Energy Security\", \"impact\": \"High\", \"analysis\": \"The supply cutoff directly destabilizes energy markets across Central and Eastern Europe. Investors with exposure to European utilities and energy-intensive industrials face elevated downside risk. ETFs tracking the DAX and WIG20 are particularly vulnerable given Germany and Poland's historical dependency on Russian pipeline gas. Consider reducing exposure to MSCI Europe energy-heavy constituents until alternative supply routes are confirmed.\"}",
}

REGION_TEMPLATES = [
    "In {year}, {actor} triggered a {category_lower} shock in {region}, forcing European investors to reassess regional exposure {modifier}.",
    "During {year}, {actor} intensified a {category_lower} event across {region}, creating fresh market uncertainty for European portfolios {modifier}.",
    "In {year}, {actor} escalated a {category_lower} scenario in {region}, increasing risk for Europe-linked sectors and indices {modifier}.",
    "During {year}, {actor} pushed a {category_lower} dispute in {region}, causing European investors to revisit sector allocations {modifier}.",
]

YEAR_BUCKETS = [2003, 2006, 2008, 2011, 2014, 2016, 2019, 2021, 2023, 2024]
SCENARIO_MODIFIERS = [
    "after emergency cabinet talks",
    "after sanctions negotiations broke down",
    "after insurers repriced regional risk",
    "after trade officials failed to reach a compromise",
    "after security warnings disrupted investor sentiment",
    "after cross-border tensions hit logistics planning",
    "after commodity buyers started panic procurement",
    "after several European firms issued exposure warnings",
    "after transport operators cut guidance",
    "after policymakers warned of second-round market effects",
]

CATEGORY_ALIASES = {
    "Trade War": "Trade Disruption",
    "Trade Policy": "Trade Disruption",
    "Currency and Trade": "Financial Contagion",
    "Political Instability": "Political Fragmentation",
    "Geopolitical Realignment": "Alliance Cohesion",
}

SCENARIO_TEMPLATES = [
    "In {year}, {actor} {trigger} in {region}, {context}.",
    "During {year}, {actor} {trigger} across {region}, {context}.",
    "In {year}, {actor} {trigger}, creating renewed instability in {region} {context}.",
    "During {year}, {actor} {trigger}, raising market stress across {region} {context}.",
]


def load_json(path: Path) -> list[dict]:
    with path.open("r", encoding="utf-8") as handle:
        data = json.load(handle)
    if not isinstance(data, list):
        raise ValueError(f"{path} does not contain a JSON array.")
    return data


def save_json(path: Path, payload: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as handle:
        json.dump(payload, handle, indent=2, ensure_ascii=False)


def normalize_key(sample: dict) -> str:
    return sample["input"].strip().lower()[:180]


def deduplicate(samples: list[dict]) -> list[dict]:
    seen: set[str] = set()
    unique: list[dict] = []
    for sample in samples:
        if not isinstance(sample, dict) or "input" not in sample:
            continue
        key = normalize_key(sample)
        if key in seen:
            continue
        seen.add(key)
        unique.append(sample)
    return unique


def impact_from_score(score: int) -> str:
    for score_range, label in IMPACTS.items():
        if score in score_range:
            return label
    return "High"


def validate_sample(sample: dict) -> bool:
    required_keys = {"instruction", "input", "output"}
    if not isinstance(sample, dict) or not required_keys.issubset(sample):
        return False

    if not isinstance(sample["instruction"], str) or not isinstance(sample["input"], str):
        return False

    try:
        output = json.loads(sample["output"])
    except (TypeError, json.JSONDecodeError):
        return False

    fields = {"risk_score", "region", "category", "impact", "analysis"}
    if not fields.issubset(output):
        return False

    return isinstance(output["risk_score"], int) and 1 <= output["risk_score"] <= 10


def summarize_distribution(samples: list[dict]) -> tuple[Counter, Counter]:
    categories: Counter = Counter()
    regions: Counter = Counter()

    for sample in samples:
        try:
            output = json.loads(sample["output"])
        except (TypeError, KeyError, json.JSONDecodeError):
            continue
        categories[output.get("category")] += 1
        regions[output.get("region")] += 1

    return categories, regions


def pick_underrepresented(counter: Counter, items: list[str]) -> str:
    lowest = min(counter.get(item, 0) for item in items)
    pool = [item for item in items if counter.get(item, 0) == lowest]
    return random.choice(pool)


def pick_decade() -> dict:
    return random.choices(DECADES, weights=[0.2, 0.3, 0.5], k=1)[0]


def build_analysis(region: str, category: str, score: int, channel: str) -> str:
    details = REGION_DETAILS[region]
    company_a, company_b = random.sample(details["companies"], 2)
    index_a, index_b = random.sample(details["indices"], 2)
    sector_a, sector_b = random.sample(details["sectors"], 2)
    impact = impact_from_score(score)

    return (
        f"This scenario increases {category.lower()} risk for European investors through {channel}. "
        f"Companies such as {company_a} and {company_b}, along with benchmarks like {index_a}, could see sharper volatility if the disruption persists. "
        f"Exposure is most visible in {sector_a} and {sector_b}, while {index_b} can act as a useful signal for broader sentiment spillover. "
        f"Near-term impact is likely {impact.lower()} for retail portfolios with concentrated regional or sector positions."
    )


def build_sample(region: str, category: str) -> dict:
    details = REGION_DETAILS[region]
    category_info = CATEGORY_DETAILS[category]
    decade = pick_decade()
    year = random.choice(decade["years"])
    actor = random.choice(details["actors"])
    trigger = random.choice(category_info["triggers"])
    context = random.choice(decade["contexts"])
    template = random.choice(SCENARIO_TEMPLATES)
    score = random.randint(*category_info["score_range"])
    impact = impact_from_score(score)

    scenario = template.format(
        year=year,
        actor=actor,
        trigger=trigger,
        region=region,
        context=context,
    )

    analysis = build_analysis(
        region=region,
        category=category,
        score=score,
        channel=category_info["channel"],
    )

    output = {
        "risk_score": score,
        "region": region,
        "category": category,
        "impact": impact,
        "analysis": analysis,
    }

    return {
        "instruction": INSTRUCTION,
        "input": scenario,
        "output": json.dumps(output, ensure_ascii=False),
    }


def quota_map(items: list, total: int) -> dict:
    base, remainder = divmod(total, len(items))
    return {item: base + (1 if index < remainder else 0) for index, item in enumerate(items)}


def canonical_category(category: str) -> str | None:
    if category in CATEGORIES:
        return category
    return CATEGORY_ALIASES.get(category)


def deduplicate_exact(samples: list[dict]) -> list[dict]:
    seen: set[str] = set()
    unique: list[dict] = []
    for sample in samples:
        key = sample["input"].strip().lower()
        if key in seen:
            continue
        seen.add(key)
        unique.append(sample)
    return unique


def normalize_sample(sample: dict) -> dict | None:
    if not validate_sample(sample):
        return None

    output = json.loads(sample["output"])
    category = canonical_category(output["category"])
    region = output["region"]
    risk_score = output["risk_score"]

    if category is None or region not in REGION_DETAILS or not 1 <= risk_score <= 10:
        return None

    output["category"] = category
    output["impact"] = impact_from_score(risk_score)

    normalized = dict(sample)
    normalized["output"] = json.dumps(output, ensure_ascii=False)
    return normalized


def score_targets(total: int) -> dict[int, int]:
    return quota_map(list(range(1, 11)), total)


def generate_assignment_plan(target_size: int) -> list[tuple[str, str, int]]:
    category_remaining = Counter(quota_map(CATEGORIES, target_size))
    region_remaining = Counter(quota_map(list(REGION_DETAILS), target_size))
    score_remaining = Counter(score_targets(target_size))

    assignments: list[tuple[str, str, int]] = []
    for _ in range(target_size):
        category = max(
            [item for item in CATEGORIES if category_remaining[item] > 0],
            key=lambda item: (category_remaining[item], random.random()),
        )
        region = max(
            [item for item in REGION_DETAILS if region_remaining[item] > 0],
            key=lambda item: (region_remaining[item], random.random()),
        )
        score = max(
            [item for item in range(1, 11) if score_remaining[item] > 0],
            key=lambda item: (score_remaining[item], random.random()),
        )

        assignments.append((category, region, score))
        category_remaining[category] -= 1
        region_remaining[region] -= 1
        score_remaining[score] -= 1

    return assignments


def sample_signature(sample: dict) -> tuple[str, str, int]:
    output = json.loads(sample["output"])
    return output["category"], output["region"], output["risk_score"]


def build_pool(samples: list[dict]) -> dict[tuple[str, str, int], list[dict]]:
    pool: dict[tuple[str, str, int], list[dict]] = {}
    for sample in samples:
        signature = sample_signature(sample)
        pool.setdefault(signature, []).append(sample)
    for items in pool.values():
        random.shuffle(items)
    return pool


def generate_new_sample(category: str, region: str, score: int, variant: int) -> dict:
    details = REGION_DETAILS[region]
    category_info = CATEGORY_DETAILS[category]
    scenario = random.choice(REGION_TEMPLATES).format(
        year=random.choice(YEAR_BUCKETS),
        actor=random.choice(details["actors"]),
        category_lower=category.lower(),
        region=region,
        modifier=f"{random.choice(SCENARIO_MODIFIERS)}, case variant {variant}",
    )
    output = {
        "risk_score": score,
        "region": region,
        "category": category,
        "impact": impact_from_score(score),
        "analysis": build_analysis(region, category, score, category_info["channel"]),
    }
    return {
        "instruction": INSTRUCTION,
        "input": scenario,
        "output": json.dumps(output, ensure_ascii=False),
    }


def build_balanced_dataset(source_samples: list[dict], target_size: int) -> list[dict]:
    plan = generate_assignment_plan(target_size)
    pool = build_pool(source_samples)
    result: list[dict] = []
    used_inputs: set[str] = set()
    variant = 1

    for category, region, score in plan:
        key = (category, region, score)
        chosen = None

        while pool.get(key):
            candidate = pool[key].pop()
            normalized_input = candidate["input"].strip().lower()
            if normalized_input in used_inputs:
                continue
            chosen = candidate
            break

        if chosen is None:
            for _ in range(50):
                candidate = generate_new_sample(category, region, score, variant)
                variant += 1
                normalized_input = candidate["input"].strip().lower()
                if normalized_input in used_inputs:
                    continue
                chosen = candidate
                break

        if chosen is None:
            raise RuntimeError(f"Could not generate unique sample for {(category, region, score)}")

        result.append(chosen)
        used_inputs.add(chosen["input"].strip().lower())

    balanced = deduplicate_exact(result)
    if len(balanced) == target_size:
        return balanced

    missing = target_size - len(balanced)
    variant = 100000
    while len(balanced) < target_size:
        category, region, score = plan[len(balanced)]
        chosen = None
        for _ in range(100):
            candidate = generate_new_sample(category, region, score, variant)
            variant += 1
            normalized_input = candidate["input"].strip().lower()
            if normalized_input in used_inputs:
                continue
            chosen = candidate
            break
        if chosen is None:
            raise RuntimeError(f"Could not restore missing unique samples: missing {missing}")
        balanced.append(chosen)
        used_inputs.add(chosen["input"].strip().lower())

    return balanced


def report(samples: list[dict]) -> dict[str, dict]:
    categories = Counter()
    regions = Counter()
    scores = Counter()
    for sample in samples:
        output = json.loads(sample["output"])
        categories[output["category"]] += 1
        regions[output["region"]] += 1
        scores[output["risk_score"]] += 1
    return {
        "categories": dict(categories),
        "regions": dict(regions),
        "risk_scores": dict(scores),
    }


__all__ = [
    "CATEGORY_ALIASES",
    "CATEGORY_DETAILS",
    "CATEGORIES",
    "DECADES",
    "EXAMPLE",
    "GENERATION_DECADES",
    "IMPACTS",
    "INSTRUCTION",
    "REGION_DETAILS",
    "REGIONS",
    "build_analysis",
    "build_balanced_dataset",
    "build_pool",
    "build_sample",
    "canonical_category",
    "deduplicate",
    "deduplicate_exact",
    "generate_assignment_plan",
    "generate_new_sample",
    "impact_from_score",
    "load_json",
    "normalize_key",
    "normalize_sample",
    "pick_decade",
    "pick_underrepresented",
    "quota_map",
    "report",
    "save_json",
    "sample_signature",
    "score_targets",
    "summarize_distribution",
    "validate_sample",
]