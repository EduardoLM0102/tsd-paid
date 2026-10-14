#!/usr/bin/env python3
"""
Google Ads Ratos - Create operations (11 subcommands)
Subcommands: campaign, ad-group, keyword, rsa, sitelink, callout, negative,
             location, video-campaign, video-ad-group, video-ad

REGRA: Tudo e criado com status PAUSED. Revisar antes de ativar.
"""

import argparse
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from lib import (
    init_client,
    resolve_customer_id,
    print_json,
    print_error,
    handle_google_error_decorator,
    add_customer_arg,
    safe_delay,
)


# ---------------------------------------------------------------------------
# 1. campaign
# ---------------------------------------------------------------------------

@handle_google_error_decorator
def cmd_campaign(args):
    """Cria campanha PAUSED (Search, Display, PMax)."""
    client = init_client()
    customer_id = resolve_customer_id(args.customer_id)

    campaign_service = client.get_service("CampaignService")
    campaign_budget_service = client.get_service("CampaignBudgetService")

    # 1. Create budget
    budget_operation = client.get_type("CampaignBudgetOperation")
    budget = budget_operation.create
    import time
    budget.name = f"Budget-{args.name}-{int(time.time())}"
    budget.amount_micros = int(args.budget) * 10000  # budget in centavos -> micros
    budget.delivery_method = client.enums.BudgetDeliveryMethodEnum.STANDARD
    budget.explicitly_shared = False

    budget_response = campaign_budget_service.mutate_campaign_budgets(
        customer_id=customer_id, operations=[budget_operation]
    )
    budget_resource = budget_response.results[0].resource_name
    print(f"Budget criado: {budget_resource}", file=sys.stderr)
    safe_delay()

    # 2. Create campaign
    operation = client.get_type("CampaignOperation")
    campaign = operation.create
    campaign.name = args.name
    campaign.campaign_budget = budget_resource
    campaign.status = client.enums.CampaignStatusEnum.PAUSED

    # EU political advertising (required in API v23+)
    campaign.contains_eu_political_advertising = 3  # DOES_NOT_CONTAIN_EU_POLITICAL_ADVERTISING

    # Campaign type
    channel_type = args.type.upper()
    if channel_type == "SEARCH":
        campaign.advertising_channel_type = client.enums.AdvertisingChannelTypeEnum.SEARCH
        campaign.network_settings.target_google_search = True
        campaign.network_settings.target_search_network = bool(args.include_search_partners)
        campaign.network_settings.target_content_network = False
    elif channel_type == "DISPLAY":
        campaign.advertising_channel_type = client.enums.AdvertisingChannelTypeEnum.DISPLAY
    elif channel_type in ("PMAX", "PERFORMANCE_MAX"):
        campaign.advertising_channel_type = client.enums.AdvertisingChannelTypeEnum.PERFORMANCE_MAX
    else:
        campaign.advertising_channel_type = client.enums.AdvertisingChannelTypeEnum.SEARCH

    # Bidding strategy
    if args.target_cpa:
        campaign.target_cpa.target_cpa_micros = int(float(args.target_cpa) * 1_000_000)
    elif args.maximize_conversions:
        campaign.maximize_conversions.target_cpa_micros = 0
    else:
        campaign.manual_cpc.enhanced_cpc_enabled = False

    response = campaign_service.mutate_campaigns(
        customer_id=customer_id, operations=[operation]
    )
    result = response.results[0]
    print_json({
        "status": "created",
        "resource_name": result.resource_name,
        "campaign_name": args.name,
        "note": "Campanha criada com status PAUSED. Revise antes de ativar."
    })


# ---------------------------------------------------------------------------
# 2. ad-group
# ---------------------------------------------------------------------------

@handle_google_error_decorator
def cmd_ad_group(args):
    """Cria ad group PAUSED."""
    client = init_client()
    customer_id = resolve_customer_id(args.customer_id)

    ad_group_service = client.get_service("AdGroupService")
    campaign_service = client.get_service("GoogleAdsService")

    operation = client.get_type("AdGroupOperation")
    ad_group = operation.create
    ad_group.name = args.name
    ad_group.campaign = campaign_service.campaign_path(customer_id, args.campaign_id)
    ad_group.status = client.enums.AdGroupStatusEnum.PAUSED
    ad_group.type_ = client.enums.AdGroupTypeEnum.SEARCH_STANDARD

    if args.cpc_bid:
        ad_group.cpc_bid_micros = int(float(args.cpc_bid) * 1_000_000)

    response = ad_group_service.mutate_ad_groups(
        customer_id=customer_id, operations=[operation]
    )
    result = response.results[0]
    print_json({
        "status": "created",
        "resource_name": result.resource_name,
        "ad_group_name": args.name,
        "note": "Ad group criado com status PAUSED."
    })


# ---------------------------------------------------------------------------
# 3. keyword
# ---------------------------------------------------------------------------

@handle_google_error_decorator
def cmd_keyword(args):
    """Adiciona keyword a um ad group."""
    client = init_client()
    customer_id = resolve_customer_id(args.customer_id)

    service = client.get_service("AdGroupCriterionService")
    ga_service = client.get_service("GoogleAdsService")

    operation = client.get_type("AdGroupCriterionOperation")
    criterion = operation.create
    criterion.ad_group = ga_service.ad_group_path(customer_id, args.ad_group_id)
    criterion.status = client.enums.AdGroupCriterionStatusEnum.ENABLED
    criterion.keyword.text = args.text

    match_type = args.match_type.upper()
    if match_type == "EXACT":
        criterion.keyword.match_type = client.enums.KeywordMatchTypeEnum.EXACT
    elif match_type == "PHRASE":
        criterion.keyword.match_type = client.enums.KeywordMatchTypeEnum.PHRASE
    elif match_type == "BROAD":
        criterion.keyword.match_type = client.enums.KeywordMatchTypeEnum.BROAD
    else:
        criterion.keyword.match_type = client.enums.KeywordMatchTypeEnum.PHRASE

    if args.bid:
        criterion.cpc_bid_micros = int(float(args.bid) * 1_000_000)

    response = service.mutate_ad_group_criteria(
        customer_id=customer_id, operations=[operation]
    )
    result = response.results[0]
    print_json({
        "status": "created",
        "resource_name": result.resource_name,
        "keyword": args.text,
        "match_type": match_type,
    })


# ---------------------------------------------------------------------------
# 4. rsa (Responsive Search Ad)
# ---------------------------------------------------------------------------

@handle_google_error_decorator
def cmd_rsa(args):
    """Cria Responsive Search Ad (ate 15 headlines + 4 descriptions)."""
    client = init_client()
    customer_id = resolve_customer_id(args.customer_id)

    service = client.get_service("AdGroupAdService")
    ga_service = client.get_service("GoogleAdsService")

    operation = client.get_type("AdGroupAdOperation")
    ad_group_ad = operation.create
    ad_group_ad.ad_group = ga_service.ad_group_path(customer_id, args.ad_group_id)
    ad_group_ad.status = client.enums.AdGroupAdStatusEnum.PAUSED

    ad = ad_group_ad.ad
    ad.final_urls.append(args.url)

    # Headlines (pipe-separated)
    headlines = [h.strip() for h in args.headlines.split("|") if h.strip()]
    for text in headlines[:15]:
        headline = client.get_type("AdTextAsset")
        headline.text = text
        ad.responsive_search_ad.headlines.append(headline)

    # Descriptions (pipe-separated)
    descriptions = [d.strip() for d in args.descriptions.split("|") if d.strip()]
    for text in descriptions[:4]:
        desc = client.get_type("AdTextAsset")
        desc.text = text
        ad.responsive_search_ad.descriptions.append(desc)

    if args.path1:
        ad.responsive_search_ad.path1 = args.path1
    if args.path2:
        ad.responsive_search_ad.path2 = args.path2

    response = service.mutate_ad_group_ads(
        customer_id=customer_id, operations=[operation]
    )
    result = response.results[0]
    print_json({
        "status": "created",
        "resource_name": result.resource_name,
        "headlines_count": len(headlines[:15]),
        "descriptions_count": len(descriptions[:4]),
        "note": "RSA criado com status PAUSED. Revise antes de ativar."
    })


# ---------------------------------------------------------------------------
# 5. sitelink
# ---------------------------------------------------------------------------

@handle_google_error_decorator
def cmd_sitelink(args):
    """Cria sitelink asset e vincula a campanha."""
    client = init_client()
    customer_id = resolve_customer_id(args.customer_id)

    asset_service = client.get_service("AssetService")
    ga_service = client.get_service("GoogleAdsService")

    # Create sitelink asset
    asset_operation = client.get_type("AssetOperation")
    asset = asset_operation.create
    asset.sitelink_asset.link_text = args.text
    asset.sitelink_asset.description1 = args.desc1 or ""
    asset.sitelink_asset.description2 = args.desc2 or ""
    asset.final_urls.append(args.url)

    asset_response = asset_service.mutate_assets(
        customer_id=customer_id, operations=[asset_operation]
    )
    asset_resource = asset_response.results[0].resource_name
    safe_delay()

    # Link to campaign
    campaign_asset_service = client.get_service("CampaignAssetService")
    link_operation = client.get_type("CampaignAssetOperation")
    link = link_operation.create
    link.campaign = ga_service.campaign_path(customer_id, args.campaign_id)
    link.asset = asset_resource
    link.field_type = client.enums.AssetFieldTypeEnum.SITELINK

    link_response = campaign_asset_service.mutate_campaign_assets(
        customer_id=customer_id, operations=[link_operation]
    )
    result = link_response.results[0]
    print_json({
        "status": "created",
        "asset_resource": asset_resource,
        "link_resource": result.resource_name,
        "sitelink_text": args.text,
    })


# ---------------------------------------------------------------------------
# 6. callout
# ---------------------------------------------------------------------------

@handle_google_error_decorator
def cmd_callout(args):
    """Cria callout asset e vincula a campanha."""
    client = init_client()
    customer_id = resolve_customer_id(args.customer_id)

    asset_service = client.get_service("AssetService")
    ga_service = client.get_service("GoogleAdsService")

    # Create callout asset
    asset_operation = client.get_type("AssetOperation")
    asset = asset_operation.create
    asset.callout_asset.callout_text = args.text

    asset_response = asset_service.mutate_assets(
        customer_id=customer_id, operations=[asset_operation]
    )
    asset_resource = asset_response.results[0].resource_name
    safe_delay()

    # Link to campaign
    campaign_asset_service = client.get_service("CampaignAssetService")
    link_operation = client.get_type("CampaignAssetOperation")
    link = link_operation.create
    link.campaign = ga_service.campaign_path(customer_id, args.campaign_id)
    link.asset = asset_resource
    link.field_type = client.enums.AssetFieldTypeEnum.CALLOUT

    link_response = campaign_asset_service.mutate_campaign_assets(
        customer_id=customer_id, operations=[link_operation]
    )
    result = link_response.results[0]
    print_json({
        "status": "created",
        "asset_resource": asset_resource,
        "link_resource": result.resource_name,
        "callout_text": args.text,
    })


# ---------------------------------------------------------------------------
# 7. negative
# ---------------------------------------------------------------------------

@handle_google_error_decorator
def cmd_negative(args):
    """Adiciona negative keyword (campaign ou ad group level)."""
    client = init_client()
    customer_id = resolve_customer_id(args.customer_id)
    ga_service = client.get_service("GoogleAdsService")

    match_type_str = args.match_type.upper()
    match_type_map = {
        "EXACT": client.enums.KeywordMatchTypeEnum.EXACT,
        "PHRASE": client.enums.KeywordMatchTypeEnum.PHRASE,
        "BROAD": client.enums.KeywordMatchTypeEnum.BROAD,
    }
    match_type = match_type_map.get(match_type_str, client.enums.KeywordMatchTypeEnum.PHRASE)

    if args.ad_group_id:
        # Ad group level negative
        service = client.get_service("AdGroupCriterionService")
        operation = client.get_type("AdGroupCriterionOperation")
        criterion = operation.create
        criterion.ad_group = ga_service.ad_group_path(customer_id, args.ad_group_id)
        criterion.negative = True
        criterion.keyword.text = args.text
        criterion.keyword.match_type = match_type

        response = service.mutate_ad_group_criteria(
            customer_id=customer_id, operations=[operation]
        )
        level = "ad_group"
    else:
        # Campaign level negative
        service = client.get_service("CampaignCriterionService")
        operation = client.get_type("CampaignCriterionOperation")
        criterion = operation.create
        criterion.campaign = ga_service.campaign_path(customer_id, args.campaign_id)
        criterion.negative = True
        criterion.keyword.text = args.text
        criterion.keyword.match_type = match_type

        response = service.mutate_campaign_criteria(
            customer_id=customer_id, operations=[operation]
        )
        level = "campaign"

    result = response.results[0]
    print_json({
        "status": "created",
        "resource_name": result.resource_name,
        "keyword": args.text,
        "match_type": match_type_str,
        "level": level,
    })


# ---------------------------------------------------------------------------
# 8. location (geo-target criterion, works on any campaign type)
# ---------------------------------------------------------------------------

@handle_google_error_decorator
def cmd_location(args):
    """Adiciona um geo-target (cidade/condado/CEP) a uma campanha."""
    client = init_client()
    customer_id = resolve_customer_id(args.customer_id)

    service = client.get_service("CampaignCriterionService")
    ga_service = client.get_service("GoogleAdsService")
    geo_service = client.get_service("GeoTargetConstantService")

    raw_id = str(args.geo_target_id)
    geo_resource = raw_id if raw_id.startswith("geoTargetConstants/") else geo_service.geo_target_constant_path(raw_id)

    operation = client.get_type("CampaignCriterionOperation")
    criterion = operation.create
    criterion.campaign = ga_service.campaign_path(customer_id, args.campaign_id)
    criterion.location.geo_target_constant = geo_resource

    response = service.mutate_campaign_criteria(
        customer_id=customer_id, operations=[operation]
    )
    result = response.results[0]
    print_json({
        "status": "created",
        "resource_name": result.resource_name,
        "geo_target_constant": geo_resource,
    })


# ---------------------------------------------------------------------------
# 9. video-campaign (YouTube Ads)
# ---------------------------------------------------------------------------

@handle_google_error_decorator
def cmd_video_campaign(args):
    """Cria campanha de video (YouTube) PAUSED. Bidding = Target CPM (efficient reach), o padrao para campanhas de brand awareness."""
    client = init_client()
    customer_id = resolve_customer_id(args.customer_id)

    campaign_service = client.get_service("CampaignService")
    campaign_budget_service = client.get_service("CampaignBudgetService")

    # 1. Budget
    budget_operation = client.get_type("CampaignBudgetOperation")
    budget = budget_operation.create
    import time
    budget.name = f"Budget-{args.name}-{int(time.time())}"
    budget.amount_micros = int(args.budget) * 10000  # centavos -> micros
    budget.delivery_method = client.enums.BudgetDeliveryMethodEnum.STANDARD
    budget.explicitly_shared = False

    budget_response = campaign_budget_service.mutate_campaign_budgets(
        customer_id=customer_id, operations=[budget_operation]
    )
    budget_resource = budget_response.results[0].resource_name
    print(f"Budget criado: {budget_resource}", file=sys.stderr)
    safe_delay()

    # 2. Campaign
    operation = client.get_type("CampaignOperation")
    campaign = operation.create
    campaign.name = args.name
    campaign.campaign_budget = budget_resource
    campaign.status = client.enums.CampaignStatusEnum.PAUSED
    campaign.contains_eu_political_advertising = 3  # DOES_NOT_CONTAIN_EU_POLITICAL_ADVERTISING

    campaign.advertising_channel_type = client.enums.AdvertisingChannelTypeEnum.VIDEO
    campaign.network_settings.target_youtube = True
    if args.target_video_partners:
        campaign.network_settings.target_content_network = True

    # Objetivo: VIEWS = Target CPV (Video views campaign, paga por view/engajamento).
    #           REACH = Target CPM (efficient reach, paga por impressao, foco em alcance puro).
    # SetInParent() ativa o oneof sem setar sub-campos (o wrapper do SDK nao expoe CopyFrom).
    objective = args.objective.upper()
    if objective == "REACH":
        campaign._pb.target_cpm.SetInParent()
        bidding_label = "TARGET_CPM (efficient reach)"
    else:
        campaign._pb.target_cpv.SetInParent()
        bidding_label = "TARGET_CPV (video views)"

    response = campaign_service.mutate_campaigns(
        customer_id=customer_id, operations=[operation]
    )
    result = response.results[0]
    print_json({
        "status": "created",
        "resource_name": result.resource_name,
        "campaign_name": args.name,
        "bidding": bidding_label,
        "note": "Campanha de video criada com status PAUSED. Adicione geo-targets (create.py location), um ad group (create.py video-ad-group) e um anuncio (create.py video-ad) antes de ativar."
    })


# ---------------------------------------------------------------------------
# 10. video-ad-group
# ---------------------------------------------------------------------------

@handle_google_error_decorator
def cmd_video_ad_group(args):
    """Cria ad group de video PAUSED (in-stream pulavel ou bumper de 6s)."""
    client = init_client()
    customer_id = resolve_customer_id(args.customer_id)

    ad_group_service = client.get_service("AdGroupService")
    ga_service = client.get_service("GoogleAdsService")

    operation = client.get_type("AdGroupOperation")
    ad_group = operation.create
    ad_group.name = args.name
    ad_group.campaign = ga_service.campaign_path(customer_id, args.campaign_id)
    ad_group.status = client.enums.AdGroupStatusEnum.PAUSED

    fmt = args.format.upper()
    if fmt == "BUMPER":
        ad_group.type_ = client.enums.AdGroupTypeEnum.VIDEO_BUMPER
    else:
        ad_group.type_ = client.enums.AdGroupTypeEnum.VIDEO_TRUE_VIEW_IN_STREAM

    response = ad_group_service.mutate_ad_groups(
        customer_id=customer_id, operations=[operation]
    )
    result = response.results[0]
    print_json({
        "status": "created",
        "resource_name": result.resource_name,
        "ad_group_name": args.name,
        "format": fmt,
        "note": "Ad group de video criado com status PAUSED."
    })


# ---------------------------------------------------------------------------
# 11. video-ad
# ---------------------------------------------------------------------------

@handle_google_error_decorator
def cmd_video_ad(args):
    """Cria o anuncio de video (in-stream pulavel ou bumper) a partir de um video ja publicado no YouTube."""
    client = init_client()
    customer_id = resolve_customer_id(args.customer_id)

    asset_service = client.get_service("AssetService")
    ad_group_ad_service = client.get_service("AdGroupAdService")
    ga_service = client.get_service("GoogleAdsService")

    # 1. Video asset (referencia o video ja hospedado no YouTube)
    asset_operation = client.get_type("AssetOperation")
    asset = asset_operation.create
    asset.youtube_video_asset.youtube_video_id = args.youtube_video_id

    asset_response = asset_service.mutate_assets(
        customer_id=customer_id, operations=[asset_operation]
    )
    asset_resource = asset_response.results[0].resource_name
    safe_delay()

    # 2. Ad
    operation = client.get_type("AdGroupAdOperation")
    ad_group_ad = operation.create
    ad_group_ad.ad_group = ga_service.ad_group_path(customer_id, args.ad_group_id)
    ad_group_ad.status = client.enums.AdGroupAdStatusEnum.PAUSED

    ad = ad_group_ad.ad
    ad.final_urls.append(args.url)
    ad.video_ad.video.asset = asset_resource

    fmt = args.format.upper()
    if fmt == "BUMPER":
        ad.video_ad.bumper.action_button_label = args.action_button_label
        ad.video_ad.bumper.action_headline = args.action_headline
    else:
        ad.video_ad.in_stream.action_button_label = args.action_button_label
        ad.video_ad.in_stream.action_headline = args.action_headline

    response = ad_group_ad_service.mutate_ad_group_ads(
        customer_id=customer_id, operations=[operation]
    )
    result = response.results[0]
    print_json({
        "status": "created",
        "resource_name": result.resource_name,
        "video_asset_resource": asset_resource,
        "youtube_video_id": args.youtube_video_id,
        "format": fmt,
        "note": "Anuncio de video criado com status PAUSED. Revise antes de ativar."
    })


# ---------------------------------------------------------------------------
# CLI parser
# ---------------------------------------------------------------------------

def build_parser():
    parser = argparse.ArgumentParser(
        description="Google Ads Ratos - Create operations (always PAUSED)",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    sub = parser.add_subparsers(dest="command", required=True)

    # 1. campaign
    p = sub.add_parser("campaign", help="Create campaign (PAUSED)")
    add_customer_arg(p)
    p.add_argument("--name", required=True, help="Campaign name")
    p.add_argument("--type", default="SEARCH", help="Type: SEARCH, DISPLAY, PMAX (default: SEARCH)")
    p.add_argument("--budget", required=True, help="Daily budget in centavos (5000 = R$50)")
    p.add_argument("--target-cpa", help="Target CPA in reais (ex: 25.00)")
    p.add_argument("--maximize-conversions", action="store_true", help="Use maximize conversions bidding")
    p.add_argument("--include-search-partners", action="store_true", help="SEARCH campaigns only: also serve on Google Search Partners network (default: off, Google Search only)")
    p.set_defaults(func=cmd_campaign)

    # 2. ad-group
    p = sub.add_parser("ad-group", help="Create ad group (PAUSED)")
    add_customer_arg(p)
    p.add_argument("--campaign-id", required=True, help="Campaign ID")
    p.add_argument("--name", required=True, help="Ad group name")
    p.add_argument("--cpc-bid", help="Max CPC bid in reais (ex: 2.50)")
    p.set_defaults(func=cmd_ad_group)

    # 3. keyword
    p = sub.add_parser("keyword", help="Add keyword to ad group")
    add_customer_arg(p)
    p.add_argument("--ad-group-id", required=True, help="Ad group ID")
    p.add_argument("--text", required=True, help="Keyword text")
    p.add_argument("--match-type", default="PHRASE", help="EXACT, PHRASE, BROAD (default: PHRASE)")
    p.add_argument("--bid", help="CPC bid in reais (ex: 1.50)")
    p.set_defaults(func=cmd_keyword)

    # 4. rsa
    p = sub.add_parser("rsa", help="Create Responsive Search Ad (PAUSED)")
    add_customer_arg(p)
    p.add_argument("--ad-group-id", required=True, help="Ad group ID")
    p.add_argument("--headlines", required=True, help="Headlines pipe-separated (max 15): 'h1|h2|h3'")
    p.add_argument("--descriptions", required=True, help="Descriptions pipe-separated (max 4): 'd1|d2'")
    p.add_argument("--url", required=True, help="Final URL")
    p.add_argument("--path1", help="Display URL path 1")
    p.add_argument("--path2", help="Display URL path 2")
    p.set_defaults(func=cmd_rsa)

    # 5. sitelink
    p = sub.add_parser("sitelink", help="Create sitelink extension")
    add_customer_arg(p)
    p.add_argument("--campaign-id", required=True, help="Campaign ID")
    p.add_argument("--text", required=True, help="Sitelink text")
    p.add_argument("--url", required=True, help="Sitelink URL")
    p.add_argument("--desc1", help="Description line 1")
    p.add_argument("--desc2", help="Description line 2")
    p.set_defaults(func=cmd_sitelink)

    # 6. callout
    p = sub.add_parser("callout", help="Create callout extension")
    add_customer_arg(p)
    p.add_argument("--campaign-id", required=True, help="Campaign ID")
    p.add_argument("--text", required=True, help="Callout text")
    p.set_defaults(func=cmd_callout)

    # 7. negative
    p = sub.add_parser("negative", help="Add negative keyword")
    add_customer_arg(p)
    p.add_argument("--campaign-id", help="Campaign ID (for campaign-level negative)")
    p.add_argument("--ad-group-id", help="Ad group ID (for ad group-level negative)")
    p.add_argument("--text", required=True, help="Negative keyword text")
    p.add_argument("--match-type", default="PHRASE", help="EXACT, PHRASE, BROAD (default: PHRASE)")
    p.set_defaults(func=cmd_negative)

    # 8. location
    p = sub.add_parser("location", help="Add a geo-target criterion to any campaign (Search, PMax, Video, ...)")
    add_customer_arg(p)
    p.add_argument("--campaign-id", required=True, help="Campaign ID")
    p.add_argument("--geo-target-id", required=True, help="Geo target constant ID (ex: 1026339 for San Antonio, TX). Look up with read.py geo-search")
    p.set_defaults(func=cmd_location)

    # 9. video-campaign
    p = sub.add_parser("video-campaign", help="Create YouTube video campaign (PAUSED)")
    add_customer_arg(p)
    p.add_argument("--name", required=True, help="Campaign name")
    p.add_argument("--budget", required=True, help="Daily budget in centavos (10000 = R$100 / $100)")
    p.add_argument("--objective", default="VIEWS", help="VIEWS (default, Target CPV — pay per view/engagement) or REACH (Target CPM — pay per impression, pure awareness)")
    p.add_argument("--target-video-partners", action="store_true", help="Also target the Google video partner network (default: YouTube only)")
    p.set_defaults(func=cmd_video_campaign)

    # 10. video-ad-group
    p = sub.add_parser("video-ad-group", help="Create video ad group (PAUSED)")
    add_customer_arg(p)
    p.add_argument("--campaign-id", required=True, help="Video campaign ID")
    p.add_argument("--name", required=True, help="Ad group name")
    p.add_argument("--format", default="IN_STREAM", help="IN_STREAM (skippable, default) or BUMPER (6s non-skippable)")
    p.set_defaults(func=cmd_video_ad_group)

    # 11. video-ad
    p = sub.add_parser("video-ad", help="Create video ad (PAUSED) from a YouTube video already uploaded")
    add_customer_arg(p)
    p.add_argument("--ad-group-id", required=True, help="Video ad group ID")
    p.add_argument("--youtube-video-id", required=True, help="YouTube video ID (the 11-char id from the video URL)")
    p.add_argument("--url", required=True, help="Final URL (landing page)")
    p.add_argument("--format", default="IN_STREAM", help="IN_STREAM (skippable, default) or BUMPER — must match the ad group's format")
    p.add_argument("--action-headline", default="", help="Headline shown on the CTA overlay (optional)")
    p.add_argument("--action-button-label", default="Learn More", help="CTA button text — must match Google's allowed set exactly (e.g. 'Learn More', 'Visit Site', 'Shop Now', 'Sign Up', 'Get Quote', 'Contact Us'). Default: 'Learn More'")
    p.set_defaults(func=cmd_video_ad)

    return parser


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    parser = build_parser()
    args = parser.parse_args()
    args.func(args)
