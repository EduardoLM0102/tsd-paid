#!/usr/bin/env python3
"""
Google Ads Ratos - Read operations (11 subcommands)
CLI for reading Google Ads data via google-ads SDK with GAQL queries.
"""

import argparse
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from lib import (
    init_client,
    resolve_customer_id,
    run_query,
    print_json,
    print_error,
    handle_google_error_decorator,
    add_customer_arg,
    add_date_args,
    add_limit_arg,
    add_campaign_filter,
    build_date_clause,
)


# ---------------------------------------------------------------------------
# 1. accounts
# ---------------------------------------------------------------------------

@handle_google_error_decorator
def cmd_accounts(args):
    """Lista contas acessiveis via MCC."""
    client = init_client()
    service = client.get_service("CustomerService")
    response = service.list_accessible_customers()
    accounts = []
    for resource_name in response.resource_names:
        customer_id = resource_name.split("/")[-1]
        # Try to get account details
        try:
            query = """
                SELECT
                    customer.id,
                    customer.descriptive_name,
                    customer.currency_code,
                    customer.time_zone,
                    customer.manager
                FROM customer
                LIMIT 1
            """
            rows = run_query(customer_id, query)
            if rows:
                accounts.append(rows[0].get("customer", {"id": customer_id}))
            else:
                accounts.append({"id": customer_id})
        except Exception:
            accounts.append({"id": customer_id})
    print_json(accounts)


# ---------------------------------------------------------------------------
# 2. campaigns
# ---------------------------------------------------------------------------

@handle_google_error_decorator
def cmd_campaigns(args):
    """Lista campanhas com status, tipo e orcamento."""
    customer_id = resolve_customer_id(args.customer_id)
    date_clause = build_date_clause(args)

    query = f"""
        SELECT
            campaign.id,
            campaign.name,
            campaign.status,
            campaign.advertising_channel_type,
            campaign_budget.amount_micros,
            metrics.cost_micros,
            metrics.impressions,
            metrics.clicks,
            metrics.conversions,
            metrics.ctr,
            metrics.average_cpc,
            metrics.cost_per_conversion
        FROM campaign
        WHERE campaign.status != 'REMOVED'
            AND {date_clause}
        ORDER BY metrics.cost_micros DESC
    """
    if args.limit:
        query += f"\nLIMIT {args.limit}"

    results = run_query(customer_id, query)
    print_json(results)


# ---------------------------------------------------------------------------
# 3. ad-groups
# ---------------------------------------------------------------------------

@handle_google_error_decorator
def cmd_ad_groups(args):
    """Lista ad groups de uma campanha."""
    customer_id = resolve_customer_id(args.customer_id)
    date_clause = build_date_clause(args)

    query = f"""
        SELECT
            ad_group.id,
            ad_group.name,
            ad_group.status,
            ad_group.type,
            ad_group.cpc_bid_micros,
            campaign.id,
            campaign.name,
            metrics.cost_micros,
            metrics.impressions,
            metrics.clicks,
            metrics.conversions
        FROM ad_group
        WHERE ad_group.status != 'REMOVED'
            AND {date_clause}
    """
    if args.campaign_id:
        query += f"\n            AND campaign.id = {args.campaign_id}"
    query += "\n        ORDER BY metrics.cost_micros DESC"
    if args.limit:
        query += f"\n        LIMIT {args.limit}"

    results = run_query(customer_id, query)
    print_json(results)


# ---------------------------------------------------------------------------
# 4. keywords
# ---------------------------------------------------------------------------

@handle_google_error_decorator
def cmd_keywords(args):
    """Lista keywords com Quality Score, match type e metricas."""
    customer_id = resolve_customer_id(args.customer_id)
    date_clause = build_date_clause(args)

    query = f"""
        SELECT
            ad_group_criterion.keyword.text,
            ad_group_criterion.keyword.match_type,
            ad_group_criterion.status,
            ad_group_criterion.quality_info.quality_score,
            ad_group.name,
            campaign.name,
            metrics.impressions,
            metrics.clicks,
            metrics.cost_micros,
            metrics.conversions,
            metrics.ctr,
            metrics.average_cpc
        FROM keyword_view
        WHERE ad_group_criterion.status != 'REMOVED'
            AND {date_clause}
    """
    if args.campaign_id:
        query += f"\n            AND campaign.id = {args.campaign_id}"
    query += "\n        ORDER BY metrics.cost_micros DESC"
    if args.limit:
        query += f"\n        LIMIT {args.limit}"

    results = run_query(customer_id, query)
    print_json(results)


# ---------------------------------------------------------------------------
# 5. ads
# ---------------------------------------------------------------------------

@handle_google_error_decorator
def cmd_ads(args):
    """Lista anuncios RSA com headlines e descriptions."""
    customer_id = resolve_customer_id(args.customer_id)
    date_clause = build_date_clause(args)

    query = f"""
        SELECT
            ad_group_ad.ad.id,
            ad_group_ad.ad.name,
            ad_group_ad.status,
            ad_group_ad.ad.type,
            ad_group_ad.ad.responsive_search_ad.headlines,
            ad_group_ad.ad.responsive_search_ad.descriptions,
            ad_group_ad.ad.final_urls,
            ad_group.name,
            campaign.name,
            metrics.impressions,
            metrics.clicks,
            metrics.cost_micros,
            metrics.conversions
        FROM ad_group_ad
        WHERE ad_group_ad.status != 'REMOVED'
            AND {date_clause}
    """
    if args.campaign_id:
        query += f"\n            AND campaign.id = {args.campaign_id}"
    query += "\n        ORDER BY metrics.cost_micros DESC"
    if args.limit:
        query += f"\n        LIMIT {args.limit}"

    results = run_query(customer_id, query)
    print_json(results)


# ---------------------------------------------------------------------------
# 6. search-terms
# ---------------------------------------------------------------------------

@handle_google_error_decorator
def cmd_search_terms(args):
    """Lista termos de busca com metricas."""
    customer_id = resolve_customer_id(args.customer_id)
    date_clause = build_date_clause(args)

    query = f"""
        SELECT
            search_term_view.search_term,
            search_term_view.status,
            campaign.name,
            ad_group.name,
            metrics.impressions,
            metrics.clicks,
            metrics.cost_micros,
            metrics.conversions,
            metrics.ctr,
            metrics.average_cpc
        FROM search_term_view
        WHERE {date_clause}
            AND metrics.impressions > 0
        ORDER BY metrics.cost_micros DESC
    """
    if args.limit:
        query += f"\nLIMIT {args.limit}"
    else:
        query += "\nLIMIT 100"

    results = run_query(customer_id, query)
    print_json(results)


# ---------------------------------------------------------------------------
# 7. extensions
# ---------------------------------------------------------------------------

@handle_google_error_decorator
def cmd_extensions(args):
    """Lista assets/extensoes (sitelinks, callouts, etc)."""
    customer_id = resolve_customer_id(args.customer_id)

    query = """
        SELECT
            asset.id,
            asset.name,
            asset.type,
            asset.sitelink_asset.description1,
            asset.sitelink_asset.description2,
            asset.sitelink_asset.link_text,
            asset.callout_asset.callout_text,
            asset.structured_snippet_asset.header,
            asset.structured_snippet_asset.values
        FROM asset
        WHERE asset.type IN ('SITELINK', 'CALLOUT', 'STRUCTURED_SNIPPET')
    """
    if args.limit:
        query += f"\nLIMIT {args.limit}"

    results = run_query(customer_id, query)
    print_json(results)


# ---------------------------------------------------------------------------
# 8. negative-keywords
# ---------------------------------------------------------------------------

@handle_google_error_decorator
def cmd_negative_keywords(args):
    """Lista negative keywords (campaign e ad group level)."""
    customer_id = resolve_customer_id(args.customer_id)
    all_results = []

    # Campaign level negatives
    query_campaign = """
        SELECT
            campaign_criterion.keyword.text,
            campaign_criterion.keyword.match_type,
            campaign_criterion.criterion_id,
            campaign.id,
            campaign.name
        FROM campaign_criterion
        WHERE campaign_criterion.negative = TRUE
            AND campaign_criterion.type = 'KEYWORD'
    """
    rows = run_query(customer_id, query_campaign)
    for row in rows:
        row["_level"] = "campaign"
    all_results.extend(rows)

    # Ad group level negatives
    query_adgroup = """
        SELECT
            ad_group_criterion.keyword.text,
            ad_group_criterion.keyword.match_type,
            ad_group_criterion.criterion_id,
            ad_group.id,
            ad_group.name,
            campaign.id,
            campaign.name
        FROM ad_group_criterion
        WHERE ad_group_criterion.negative = TRUE
            AND ad_group_criterion.type = 'KEYWORD'
    """
    rows = run_query(customer_id, query_adgroup)
    for row in rows:
        row["_level"] = "ad_group"
    all_results.extend(rows)

    print_json(all_results)


# ---------------------------------------------------------------------------
# 9. quality-scores
# ---------------------------------------------------------------------------

@handle_google_error_decorator
def cmd_quality_scores(args):
    """Lista Quality Score decomposto (creative, landing page, expected CTR)."""
    customer_id = resolve_customer_id(args.customer_id)

    query = """
        SELECT
            ad_group_criterion.keyword.text,
            ad_group_criterion.keyword.match_type,
            ad_group_criterion.quality_info.quality_score,
            ad_group_criterion.quality_info.creative_quality_score,
            ad_group_criterion.quality_info.post_click_quality_score,
            ad_group_criterion.quality_info.search_predicted_ctr,
            ad_group.name,
            campaign.name,
            metrics.impressions,
            metrics.clicks,
            metrics.cost_micros
        FROM keyword_view
        WHERE ad_group_criterion.status = 'ENABLED'
            AND campaign.status != 'REMOVED'
            AND ad_group.status != 'REMOVED'
        ORDER BY metrics.cost_micros DESC
    """
    if args.limit:
        query += f"\nLIMIT {args.limit}"
    else:
        query += "\nLIMIT 50"

    results = run_query(customer_id, query)
    print_json(results)


# ---------------------------------------------------------------------------
# 10. locations (geo-target criteria per campaign)
# ---------------------------------------------------------------------------

@handle_google_error_decorator
def cmd_locations(args):
    """Lista os geo-targets (cidade/condado/CEP) configurados nas campanhas."""
    customer_id = resolve_customer_id(args.customer_id)

    where = ["campaign_criterion.type = 'LOCATION'", "campaign.status != 'REMOVED'"]
    if args.campaign_id:
        where.append(f"campaign.id = {args.campaign_id}")

    query = f"""
        SELECT
            campaign.id,
            campaign.name,
            campaign.status,
            campaign_criterion.criterion_id,
            campaign_criterion.location.geo_target_constant,
            campaign_criterion.negative
        FROM campaign_criterion
        WHERE {' AND '.join(where)}
        ORDER BY campaign.name
    """
    rows = run_query(customer_id, query)

    geo_ids = set()
    for row in rows:
        gtc = row.get("campaign_criterion", {}).get("location", {}).get("geo_target_constant")
        if gtc:
            geo_ids.add(gtc.split("/")[-1])

    name_map = {}
    if geo_ids:
        name_query = f"""
            SELECT geo_target_constant.id, geo_target_constant.canonical_name, geo_target_constant.target_type
            FROM geo_target_constant
            WHERE geo_target_constant.id IN ({','.join(geo_ids)})
        """
        for row in run_query(customer_id, name_query):
            gt = row.get("geo_target_constant", {})
            name_map[str(gt.get("id"))] = {
                "canonical_name": gt.get("canonical_name"),
                "target_type": gt.get("target_type"),
            }

    output = []
    for row in rows:
        campaign = row.get("campaign", {})
        cc = row.get("campaign_criterion", {})
        gtc = cc.get("location", {}).get("geo_target_constant")
        geo_id = gtc.split("/")[-1] if gtc else None
        info = name_map.get(geo_id, {})
        output.append({
            "campaign_id": campaign.get("id"),
            "campaign_name": campaign.get("name"),
            "campaign_status": campaign.get("status"),
            "negative": cc.get("negative", False),
            "geo_target_id": geo_id,
            "location": info.get("canonical_name"),
            "target_type": info.get("target_type"),
        })
    print_json(output)


# ---------------------------------------------------------------------------
# 11. geo-search (look up geo target constant IDs by name)
# ---------------------------------------------------------------------------

@handle_google_error_decorator
def cmd_geo_search(args):
    """Busca geo_target_constant IDs por nome de local (cidade, condado, CEP...)."""
    client = init_client()
    service = client.get_service("GeoTargetConstantService")

    request = client.get_type("SuggestGeoTargetConstantsRequest")
    request.locale = args.locale
    if args.country_code:
        request.country_code = args.country_code
    request.location_names.names.extend([n.strip() for n in args.names.split("|") if n.strip()])

    response = service.suggest_geo_target_constants(request=request)
    output = []
    for suggestion in response.geo_target_constant_suggestions:
        gtc = suggestion.geo_target_constant
        output.append({
            "id": gtc.id,
            "name": gtc.name,
            "canonical_name": gtc.canonical_name,
            "target_type": gtc.target_type,
            "country_code": gtc.country_code,
            "resource_name": gtc.resource_name,
        })
    print_json(output)


# ---------------------------------------------------------------------------
# 12. local-services-leads (LSA lead-level data, separate from PPC metrics)
# ---------------------------------------------------------------------------

@handle_google_error_decorator
def cmd_local_services_leads(args):
    """Lista leads de Local Services Ads: tipo, status, cobranca, categoria.

    So retorna dados se a conta tiver uma campanha LOCAL_SERVICES (mesma
    conta da PPC, ou uma conta LSA dedicada — ver contas.yaml)."""
    customer_id = resolve_customer_id(args.customer_id)

    if args.since and args.until:
        since, until = args.since, args.until
    else:
        from datetime import date, timedelta
        until_d = date.today()
        since_d = until_d - timedelta(days=args.days)
        since, until = since_d.isoformat(), until_d.isoformat()

    query = f"""
        SELECT
            local_services_lead.id,
            local_services_lead.lead_type,
            local_services_lead.lead_status,
            local_services_lead.lead_charged,
            local_services_lead.creation_date_time,
            local_services_lead.category_id,
            local_services_lead.service_id,
            local_services_lead.locale,
            local_services_lead.credit_details.credit_state,
            local_services_lead.credit_details.credit_state_last_update_date_time
        FROM local_services_lead
        WHERE local_services_lead.creation_date_time >= '{since} 00:00:00'
            AND local_services_lead.creation_date_time <= '{until} 23:59:59'
        ORDER BY local_services_lead.creation_date_time DESC
    """
    if args.limit:
        query += f"\nLIMIT {args.limit}"

    results = run_query(customer_id, query)
    print_json(results)


# ---------------------------------------------------------------------------
# CLI parser
# ---------------------------------------------------------------------------

def build_parser():
    parser = argparse.ArgumentParser(
        description="Google Ads Ratos - Read operations",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    sub = parser.add_subparsers(dest="command", required=True)

    # 1. accounts
    p = sub.add_parser("accounts", help="List accessible customer accounts")
    p.set_defaults(func=cmd_accounts)

    # 2. campaigns
    p = sub.add_parser("campaigns", help="List campaigns with status, type, budget")
    add_customer_arg(p)
    add_date_args(p)
    add_limit_arg(p)
    p.set_defaults(func=cmd_campaigns)

    # 3. ad-groups
    p = sub.add_parser("ad-groups", help="List ad groups of a campaign")
    add_customer_arg(p)
    add_date_args(p)
    add_limit_arg(p)
    add_campaign_filter(p)
    p.set_defaults(func=cmd_ad_groups)

    # 4. keywords
    p = sub.add_parser("keywords", help="List keywords with QS, match type, metrics")
    add_customer_arg(p)
    add_date_args(p)
    add_limit_arg(p)
    add_campaign_filter(p)
    p.set_defaults(func=cmd_keywords)

    # 5. ads
    p = sub.add_parser("ads", help="List ads with RSA details")
    add_customer_arg(p)
    add_date_args(p)
    add_limit_arg(p)
    add_campaign_filter(p)
    p.set_defaults(func=cmd_ads)

    # 6. search-terms
    p = sub.add_parser("search-terms", help="List search terms with metrics")
    add_customer_arg(p)
    add_date_args(p)
    add_limit_arg(p, default=100)
    p.set_defaults(func=cmd_search_terms)

    # 7. extensions
    p = sub.add_parser("extensions", help="List assets (sitelinks, callouts, snippets)")
    add_customer_arg(p)
    add_limit_arg(p)
    p.set_defaults(func=cmd_extensions)

    # 8. negative-keywords
    p = sub.add_parser("negative-keywords", help="List negative keywords (campaign + ad group)")
    add_customer_arg(p)
    p.set_defaults(func=cmd_negative_keywords)

    # 9. quality-scores
    p = sub.add_parser("quality-scores", help="Quality Score decomposed (creative, landing, ctr)")
    add_customer_arg(p)
    add_limit_arg(p, default=50)
    p.set_defaults(func=cmd_quality_scores)

    # 10. locations
    p = sub.add_parser("locations", help="List geo-target criteria configured on campaigns")
    add_customer_arg(p)
    add_campaign_filter(p)
    p.set_defaults(func=cmd_locations)

    # 11. geo-search
    p = sub.add_parser("geo-search", help="Look up geo_target_constant IDs by location name (no customer-id needed)")
    p.add_argument("--names", required=True, help="Location names pipe-separated: 'San Antonio, TX|New Braunfels, TX'")
    p.add_argument("--locale", default="en", help="Locale for results (default: en)")
    p.add_argument("--country-code", help="Optional 2-letter country code filter, e.g. US")
    p.set_defaults(func=cmd_geo_search)

    # 12. local-services-leads
    p = sub.add_parser("local-services-leads", help="List LSA lead-level data (type, status, charged, category) — requires a LOCAL_SERVICES campaign in the account")
    add_customer_arg(p)
    p.add_argument("--days", type=int, default=30, help="Janela em dias a partir de hoje (default: 30). Ignorado se --since/--until forem passados.")
    p.add_argument("--since", help="Data inicio (YYYY-MM-DD)")
    p.add_argument("--until", help="Data fim (YYYY-MM-DD)")
    add_limit_arg(p)
    p.set_defaults(func=cmd_local_services_leads)

    return parser


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    parser = build_parser()
    args = parser.parse_args()
    args.func(args)
