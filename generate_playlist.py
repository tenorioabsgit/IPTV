"""
IPTV Playlist Generator
Executa automaticamente via GitHub Actions

URL fixa: https://raw.githubusercontent.com/tenorioabsgit/iptv/main/playlist.m3u
"""

import re
import requests
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor, as_completed
import multiprocessing

# ============================================================
# CONFIGURACAO
# ============================================================

SOURCES = {
    # ============================================================
    # BRASIL
    # ============================================================

    # Brasil (apsattv.com)
    'samsung_br': {
        'name': 'Samsung TV Plus Brasil',
        'url': 'https://www.apsattv.com/ssungbra.m3u',
        'region': 'BR',
    },
    'lg_br': {
        'name': 'LG Channels Brasil',
        'url': 'https://www.apsattv.com/brlg.m3u',
        'region': 'BR',
    },
    'tcl_br': {
        'name': 'TCL Brasil',
        'url': 'https://www.apsattv.com/tclbr.m3u',
        'region': 'BR',
    },
    'soultv_br': {
        'name': 'Soul TV Brasil',
        'url': 'https://www.apsattv.com/soultv.m3u',
        'region': 'BR',
    },
    'redeitv_br': {
        'name': 'Rede iTV Brasil',
        'url': 'https://www.apsattv.com/redeitv.m3u',
        'region': 'BR',
    },
    'movieark_br': {
        'name': 'Movieark Brasil',
        'url': 'https://www.apsattv.com/moviearkbr.m3u',
        'region': 'BR',
    },
    'vidaa_br': {
        'name': 'Vidaa TV',
        'url': 'https://www.apsattv.com/vidaa.m3u',
        'region': 'BR',
    },

    # Brasil (GitHub agregadores)
    'iptv_org_br': {
        'name': 'IPTV-Org Brasil',
        'url': 'https://iptv-org.github.io/iptv/countries/br.m3u',
        'region': 'BR',
    },
    'freetv_br': {
        'name': 'Free-TV Brasil',
        'url': 'https://raw.githubusercontent.com/Free-TV/IPTV/master/playlists/playlist_brazil.m3u8',
        'region': 'BR',
    },
    'fta_br': {
        'name': 'FTA-IPTV Brasil',
        'url': 'https://raw.githubusercontent.com/joaoguidugli/FTA-IPTV-Brasil/master/playlist.m3u8',
        'region': 'BR',
    },

    # Brasil (BuddyChewChew)
    'plutotv_br': {
        'name': 'Pluto TV Brasil',
        'url': 'https://raw.githubusercontent.com/BuddyChewChew/app-m3u-generator/refs/heads/main/playlists/plutotv_br.m3u',
        'region': 'BR',
    },

    # Lingua Portuguesa - todos os paises (GitHub)
    'iptv_org_por': {
        'name': 'IPTV-Org Português',
        'url': 'https://iptv-org.github.io/iptv/languages/por.m3u',
        'region': 'BR',
    },

    # ============================================================
    # EUA
    # ============================================================

    # EUA (apsattv.com)
    'localnow_us': {
        'name': 'Local Now',
        'url': 'https://www.apsattv.com/localnow.m3u',
        'region': 'US',
    },
    'distrotv': {
        'name': 'DistroTV',
        'url': 'https://www.apsattv.com/distro.m3u',
        'region': 'US',
    },
    'vizio_us': {
        'name': 'Vizio TV',
        'url': 'https://www.apsattv.com/vizio.m3u',
        'region': 'US',
    },
    'firetv_us': {
        'name': 'Amazon Fire TV',
        'url': 'https://www.apsattv.com/firetv.m3u',
        'region': 'US',
    },
    'lg_us': {
        'name': 'LG Channels US',
        'url': 'https://www.apsattv.com/uslg.m3u',
        'region': 'US',
    },
    'metax_us': {
        'name': 'Metax',
        'url': 'https://www.apsattv.com/metax.m3u',
        'region': 'US',
    },
    'hp_us': {
        'name': 'HP Fast Channels',
        'url': 'https://www.apsattv.com/hp.m3u',
        'region': 'US',
    },
    'tablo_us': {
        'name': 'Tablo',
        'url': 'https://www.apsattv.com/tablo.m3u',
        'region': 'US',
    },

    # EUA (BuddyChewChew)
    'samsung_us': {
        'name': 'Samsung TV Plus US',
        'url': 'https://raw.githubusercontent.com/BuddyChewChew/app-m3u-generator/refs/heads/main/playlists/samsungtvplus_us.m3u',
        'region': 'US',
    },
    'roku_us': {
        'name': 'Roku Channel',
        'url': 'https://raw.githubusercontent.com/BuddyChewChew/app-m3u-generator/refs/heads/main/playlists/roku_all.m3u',
        'region': 'US',
    },
    'plex_us': {
        'name': 'Plex TV US',
        'url': 'https://raw.githubusercontent.com/BuddyChewChew/app-m3u-generator/refs/heads/main/playlists/plex_us.m3u',
        'region': 'US',
    },
    'tubi_us': {
        'name': 'Tubi TV',
        'url': 'https://raw.githubusercontent.com/BuddyChewChew/app-m3u-generator/refs/heads/main/playlists/tubi_all.m3u',
        'region': 'US',
    },
    'plutotv_us': {
        'name': 'Pluto TV US',
        'url': 'https://raw.githubusercontent.com/BuddyChewChew/app-m3u-generator/refs/heads/main/playlists/plutotv_us.m3u',
        'region': 'US',
    },

    # EUA (GitHub agregadores)
    'iptv_org_us': {
        'name': 'IPTV-Org US',
        'url': 'https://iptv-org.github.io/iptv/countries/us.m3u',
        'region': 'US',
    },
    'freetv_us': {
        'name': 'Free-TV USA',
        'url': 'https://raw.githubusercontent.com/Free-TV/IPTV/master/playlists/playlist_usa.m3u8',
        'region': 'US',
    },

    # ============================================================
    # CANADA
    # ============================================================

    'lg_ca': {
        'name': 'LG Channels CA',
        'url': 'https://www.apsattv.com/calg.m3u',
        'region': 'CA',
    },
    'samsung_ca': {
        'name': 'Samsung TV Plus CA',
        'url': 'https://raw.githubusercontent.com/BuddyChewChew/app-m3u-generator/refs/heads/main/playlists/samsungtvplus_ca.m3u',
        'region': 'CA',
    },
    'plex_ca': {
        'name': 'Plex TV CA',
        'url': 'https://raw.githubusercontent.com/BuddyChewChew/app-m3u-generator/refs/heads/main/playlists/plex_ca.m3u',
        'region': 'CA',
    },
    'plutotv_ca': {
        'name': 'Pluto TV CA',
        'url': 'https://raw.githubusercontent.com/BuddyChewChew/app-m3u-generator/refs/heads/main/playlists/plutotv_ca.m3u',
        'region': 'CA',
    },
    'iptv_org_ca': {
        'name': 'IPTV-Org CA',
        'url': 'https://iptv-org.github.io/iptv/countries/ca.m3u',
        'region': 'CA',
    },
    'freetv_ca': {
        'name': 'Free-TV Canada',
        'url': 'https://raw.githubusercontent.com/Free-TV/IPTV/master/playlists/playlist_canada.m3u8',
        'region': 'CA',
    },

    # ============================================================
    # UK
    # ============================================================

    'lg_gb': {
        'name': 'LG Channels UK',
        'url': 'https://www.apsattv.com/gblg.m3u',
        'region': 'GB',
    },
    'samsung_gb': {
        'name': 'Samsung TV Plus UK',
        'url': 'https://raw.githubusercontent.com/BuddyChewChew/app-m3u-generator/refs/heads/main/playlists/samsungtvplus_gb.m3u',
        'region': 'GB',
    },
    'plex_gb': {
        'name': 'Plex TV UK',
        'url': 'https://raw.githubusercontent.com/BuddyChewChew/app-m3u-generator/refs/heads/main/playlists/plex_gb.m3u',
        'region': 'GB',
    },
    'plutotv_gb': {
        'name': 'Pluto TV UK',
        'url': 'https://raw.githubusercontent.com/BuddyChewChew/app-m3u-generator/refs/heads/main/playlists/plutotv_gb.m3u',
        'region': 'GB',
    },
    'iptv_org_gb': {
        'name': 'IPTV-Org UK',
        'url': 'https://iptv-org.github.io/iptv/countries/uk.m3u',
        'region': 'GB',
    },
    'freetv_gb': {
        'name': 'Free-TV UK',
        'url': 'https://raw.githubusercontent.com/Free-TV/IPTV/master/playlists/playlist_uk.m3u8',
        'region': 'GB',
    },

    # ============================================================
    # AUSTRALIA
    # ============================================================

    'samsung_au': {
        'name': 'Samsung TV Plus AU',
        'url': 'https://www.apsattv.com/ssungaus.m3u',
        'region': 'AU',
    },
    'lg_au': {
        'name': 'LG Channels AU',
        'url': 'https://www.apsattv.com/aulg.m3u',
        'region': 'AU',
    },
    '9fast_au': {
        'name': '9Fast AU',
        'url': 'https://www.apsattv.com/9fast.m3u',
        'region': 'AU',
    },
    'kogantvplus_au': {
        'name': 'Kogantvplus AU',
        'url': 'https://www.apsattv.com/kogantvplus.m3u',
        'region': 'AU',
    },
    'plex_au': {
        'name': 'Plex TV AU',
        'url': 'https://raw.githubusercontent.com/BuddyChewChew/app-m3u-generator/refs/heads/main/playlists/plex_au.m3u',
        'region': 'AU',
    },
    'iptv_org_au': {
        'name': 'IPTV-Org AU',
        'url': 'https://iptv-org.github.io/iptv/countries/au.m3u',
        'region': 'AU',
    },
    'freetv_au': {
        'name': 'Free-TV Australia',
        'url': 'https://raw.githubusercontent.com/Free-TV/IPTV/master/playlists/playlist_australia.m3u8',
        'region': 'AU',
    },

    # ============================================================
    # NOVA ZELANDIA
    # ============================================================

    'samsung_nz': {
        'name': 'Samsung TV Plus NZ',
        'url': 'https://www.apsattv.com/ssungnz.m3u',
        'region': 'NZ',
    },
    'lg_nz': {
        'name': 'LG Channels NZ',
        'url': 'https://www.apsattv.com/nzlg.m3u',
        'region': 'NZ',
    },
    'plex_nz': {
        'name': 'Plex TV NZ',
        'url': 'https://raw.githubusercontent.com/BuddyChewChew/app-m3u-generator/refs/heads/main/playlists/plex_nz.m3u',
        'region': 'NZ',
    },
    'iptv_org_nz': {
        'name': 'IPTV-Org NZ',
        'url': 'https://iptv-org.github.io/iptv/countries/nz.m3u',
        'region': 'NZ',
    },

    # ============================================================
    # PORTUGAL
    # ============================================================

    'samsung_pt': {
        'name': 'Samsung TV Plus PT',
        'url': 'https://www.apsattv.com/ssungpor.m3u',
        'region': 'PT',
    },
    'lg_pt': {
        'name': 'LG Channels PT',
        'url': 'https://www.apsattv.com/ptlg.m3u',
        'region': 'PT',
    },
    'm3upt': {
        'name': 'M3UPT Portugal',
        'url': 'https://raw.githubusercontent.com/LITUATUI/M3UPT/main/M3U/M3UPT.m3u',
        'region': 'PT',
    },
    'iptv_org_pt': {
        'name': 'IPTV-Org PT',
        'url': 'https://iptv-org.github.io/iptv/countries/pt.m3u',
        'region': 'PT',
    },
    'freetv_pt': {
        'name': 'Free-TV Portugal',
        'url': 'https://raw.githubusercontent.com/Free-TV/IPTV/master/playlists/playlist_portugal.m3u8',
        'region': 'PT',
    },

    # ============================================================
    # LUSOFONIA AFRICANA
    # ============================================================

    'iptv_org_ao': {
        'name': 'IPTV-Org Angola',
        'url': 'https://iptv-org.github.io/iptv/countries/ao.m3u',
        'region': 'AO',
    },
    'iptv_org_mz': {
        'name': 'IPTV-Org Moçambique',
        'url': 'https://iptv-org.github.io/iptv/countries/mz.m3u',
        'region': 'MZ',
    },
    'iptv_org_cv': {
        'name': 'IPTV-Org Cabo Verde',
        'url': 'https://iptv-org.github.io/iptv/countries/cv.m3u',
        'region': 'CV',
    },

    # ============================================================
    # MULTI-REGIAO / GLOBAL
    # ============================================================

    'whaletvplus': {
        'name': 'Whale TV Plus',
        'url': 'https://www.apsattv.com/whaletvplus_all.m3u',
        'region': 'US',
    },
    'tclplus': {
        'name': 'TCL TV Plus Global',
        'url': 'https://www.apsattv.com/tclplus.m3u',
        'region': 'US',
    },
    'freelivesports': {
        'name': 'Free Live Sports',
        'url': 'https://www.apsattv.com/freelivesports.m3u',
        'region': 'US',
    },
    'samsungtvplus_all': {
        'name': 'Samsung TV Plus All',
        'url': 'https://raw.githubusercontent.com/BuddyChewChew/app-m3u-generator/refs/heads/main/playlists/samsungtvplus_all.m3u',
        'region': 'US',
    },
    'plex_all': {
        'name': 'Plex TV All',
        'url': 'https://raw.githubusercontent.com/BuddyChewChew/app-m3u-generator/refs/heads/main/playlists/plex_all.m3u',
        'region': 'US',
    },
    'plutotv_all': {
        'name': 'Pluto TV All',
        'url': 'https://raw.githubusercontent.com/BuddyChewChew/app-m3u-generator/refs/heads/main/playlists/plutotv_all.m3u',
        'region': 'US',
    },
}

TARGET_REGIONS = ['BR', 'US', 'GB', 'CA', 'AU', 'NZ', 'PT', 'AO', 'MZ', 'CV']
OUTPUT_FILE = 'playlist.m3u'

# Canais extras (VH1 e MTV) adicionados manualmente
EXTRA_CHANNELS = [
    # VH1 - Pluto TV US
    {'name': 'VH1 Classics', 'url': 'https://service-stitcher.clusters.pluto.tv/v1/stitch/embed/hls/channel/6076cd1df8576d0007c82193/master.m3u8?deviceId=channel&deviceModel=web&deviceVersion=1.0&appVersion=1.0&deviceType=web&deviceMake=web&deviceDNT=1', 'region': 'US', 'source': 'Pluto TV US'},
    {'name': 'VH1 I Love Reality', 'url': 'https://service-stitcher.clusters.pluto.tv/v1/stitch/embed/hls/channel/5d7154fa8326b6ce4ec31f2e/master.m3u8?deviceId=channel&deviceModel=web&deviceVersion=1.0&appVersion=1.0&deviceType=web&deviceMake=web&deviceDNT=1', 'region': 'US', 'source': 'Pluto TV US'},
    {'name': 'VH1 Hip Hop Family', 'url': 'https://service-stitcher.clusters.pluto.tv/v1/stitch/embed/hls/channel/5d71561df6f2e6d0b6493bf5/master.m3u8?deviceId=channel&deviceModel=web&deviceVersion=1.0&appVersion=1.0&deviceType=web&deviceMake=web&deviceDNT=1', 'region': 'US', 'source': 'Pluto TV US'},
    {'name': 'VH1 Queens of Reality', 'url': 'https://service-stitcher.clusters.pluto.tv/v1/stitch/embed/hls/channel/66abefe5d2d50d00082c7d12/master.m3u8?deviceId=channel&deviceModel=web&deviceVersion=1.0&appVersion=1.0&deviceType=web&deviceMake=web&deviceDNT=1', 'region': 'US', 'source': 'Pluto TV US'},
    # VH1 - Pluto TV Italia
    {'name': 'VH1+ Music Legends', 'url': 'https://service-stitcher.clusters.pluto.tv/v1/stitch/embed/hls/channel/62e8cc10ca869f00078efca8/master.m3u8?deviceId=channel&deviceModel=web&deviceVersion=1.0&appVersion=1.0&deviceType=web&deviceMake=web&deviceDNT=1', 'region': 'IT', 'source': 'Pluto TV IT'},
    {'name': "VH1+ Back to 90's", 'url': 'https://service-stitcher.clusters.pluto.tv/v1/stitch/embed/hls/channel/6552085aab05240008b05f6c/master.m3u8?deviceId=channel&deviceModel=web&deviceVersion=1.0&appVersion=1.0&deviceType=web&deviceMake=web&deviceDNT=1', 'region': 'IT', 'source': 'Pluto TV IT'},
    {'name': 'VH1+ Rock!', 'url': 'https://service-stitcher.clusters.pluto.tv/v1/stitch/embed/hls/channel/636a4173e34fd50007534542/master.m3u8?deviceId=channel&deviceModel=web&deviceVersion=1.0&appVersion=1.0&deviceType=web&deviceMake=web&deviceDNT=1', 'region': 'IT', 'source': 'Pluto TV IT'},
    {'name': 'VH1+ Dance', 'url': 'https://service-stitcher.clusters.pluto.tv/v1/stitch/embed/hls/channel/65e5d9d2ec9fda0008c35f91/master.m3u8?deviceId=channel&deviceModel=web&deviceVersion=1.0&appVersion=1.0&deviceType=web&deviceMake=web&deviceDNT=1', 'region': 'IT', 'source': 'Pluto TV IT'},
    {'name': 'VH1+ Classici', 'url': 'https://service-stitcher.clusters.pluto.tv/v1/stitch/embed/hls/channel/6690f892d51259000880d1c4/master.m3u8?deviceId=channel&deviceModel=web&deviceVersion=1.0&appVersion=1.0&deviceType=web&deviceMake=web&deviceDNT=1', 'region': 'IT', 'source': 'Pluto TV IT'},
    # VH1 - Outros
    {'name': 'VH1 Italia', 'url': 'https://content.uplynk.com/channel/36953f5b6546464590d2fcd954bc89cf.m3u8', 'region': 'IT', 'source': 'iptv-org'},
    # MTV - MoveOnJoy (alta confiabilidade)
    {'name': 'MTV East', 'url': 'https://fl1.moveonjoy.com/MTV/index.m3u8', 'region': 'US', 'source': 'MoveOnJoy'},
    {'name': 'MTV2', 'url': 'https://fl1.moveonjoy.com/MTV_2/index.m3u8', 'region': 'US', 'source': 'MoveOnJoy'},
    {'name': 'MTV Live', 'url': 'https://fl1.moveonjoy.com/MTV_LIVE/index.m3u8', 'region': 'US', 'source': 'MoveOnJoy'},
    {'name': 'mtvU', 'url': 'https://fl1.moveonjoy.com/MTV_U/index.m3u8', 'region': 'US', 'source': 'MoveOnJoy'},
    # MTV - Pluto TV US
    {'name': "MTV Spankin' New", 'url': 'http://cfd-v4-service-channel-stitcher-use1-1.prd.pluto.tv/stitch/hls/channel/5d14fdb8ca91eedee1633117/master.m3u8?appName=web&appVersion=unknown&deviceDNT=0&deviceId=mtv-spankin&deviceMake=Chrome&deviceModel=web&deviceType=web&deviceVersion=unknown&includeExtendedEvents=false&serverSideAds=false', 'region': 'US', 'source': 'Pluto TV US'},
    {'name': 'MTV en Español', 'url': 'http://cfd-v4-service-channel-stitcher-use1-1.prd.pluto.tv/stitch/hls/channel/5cf96d351652631e36d4331f/master.m3u8?appName=web&appVersion=unknown&deviceDNT=0&deviceId=mtv-espanol&deviceMake=Chrome&deviceModel=web&deviceType=web&deviceVersion=unknown&includeExtendedEvents=false&serverSideAds=false', 'region': 'US', 'source': 'Pluto TV US'},
    {'name': 'MTV Flow Latino', 'url': 'http://cfd-v4-service-channel-stitcher-use1-1.prd.pluto.tv/stitch/hls/channel/5d3609cd6a6c78d7672f2a81/master.m3u8?appName=web&appVersion=unknown&deviceDNT=0&deviceId=mtv-flow&deviceMake=Chrome&deviceModel=web&deviceType=web&deviceVersion=unknown&includeExtendedEvents=false&serverSideAds=false', 'region': 'US', 'source': 'Pluto TV US'},
    # MTV - Pluto TV Europa
    {'name': 'MTV Music', 'url': 'http://cfd-v4-service-channel-stitcher-use1-1.prd.pluto.tv/stitch/hls/channel/6245d15062cd1f00070a2338/master.m3u8?appName=web&appVersion=unknown&deviceDNT=0&deviceId=mtv-music&deviceMake=Chrome&deviceModel=web&deviceType=web&deviceVersion=unknown&includeExtendedEvents=false&serverSideAds=false', 'region': 'DE', 'source': 'Pluto TV DE'},
    {'name': 'MTV Classics FR', 'url': 'http://cfd-v4-service-channel-stitcher-use1-1.prd.pluto.tv/stitch/hls/channel/5f92b56a367e170007cd43f4/master.m3u8?appName=web&appVersion=unknown&deviceDNT=0&deviceId=mtv-classics-fr&deviceMake=Chrome&deviceModel=web&deviceType=web&deviceVersion=unknown&includeExtendedEvents=false&serverSideAds=false', 'region': 'FR', 'source': 'Pluto TV FR'},
    {'name': 'MTV Originals ES', 'url': 'https://service-stitcher.clusters.pluto.tv/stitch/hls/channel/5f1aadf373bed3000794d1d7/master.m3u8?advertisingId=&appName=web&appVersion=DNT&deviceDNT=0&deviceId=mtv-originals&deviceMake=web&deviceModel=web&deviceType=web&deviceVersion=DNT&includeExtendedEvents=false&serverSideAds=false', 'region': 'ES', 'source': 'Pluto TV ES'},
    # MTV - Streams adicionais
    {'name': 'MTV 00s', 'url': 'http://myott.top/stream/DT6QU63K5VX/165.m3u8', 'region': 'INT', 'source': 'myott'},
    {'name': 'MTV 80s', 'url': 'http://myott.top/stream/DT6QU63K5VX/87.m3u8', 'region': 'INT', 'source': 'myott'},
    {'name': 'MTV 90s', 'url': 'http://myott.top/stream/DT6QU63K5VX/88.m3u8', 'region': 'INT', 'source': 'myott'},
    {'name': 'MTV Hits', 'url': 'http://myott.top/stream/DT6QU63K5VX/302.m3u8', 'region': 'INT', 'source': 'myott'},
    # Notícias BR - canais extras
    {'name': 'BandNews TV', 'url': 'https://evpp.mm.uol.com.br/geob_band/bandnewstv/playlist.m3u8', 'region': 'BR', 'source': 'Band'},
    # Rock/Metal - Pluto TV US
    {'name': 'XITE Rock x Metal', 'url': 'http://cfd-v4-service-channel-stitcher-use1-1.prd.pluto.tv/stitch/hls/channel/623a1b5188ecdc0007c9ef5a/master.m3u8?appName=web&appVersion=unknown&deviceDNT=0&deviceId=rock&deviceMake=Chrome&deviceModel=web&deviceType=web&deviceVersion=unknown&includeExtendedEvents=false&serverSideAds=false', 'region': 'US', 'source': 'Pluto TV US'},
    {'name': 'Vevo Rock', 'url': 'http://cfd-v4-service-channel-stitcher-use1-1.prd.pluto.tv/stitch/hls/channel/61d4b38226b8a50007fe03a6/master.m3u8?appName=web&appVersion=unknown&deviceDNT=0&deviceId=rock&deviceMake=Chrome&deviceModel=web&deviceType=web&deviceVersion=unknown&includeExtendedEvents=false&serverSideAds=false', 'region': 'US', 'source': 'Pluto TV US'},
    {'name': 'Live Music', 'url': 'http://cfd-v4-service-channel-stitcher-use1-1.prd.pluto.tv/stitch/hls/channel/5873fc21cad696fb37aa9054/master.m3u8?appName=web&appVersion=unknown&deviceDNT=0&deviceId=rock&deviceMake=Chrome&deviceModel=web&deviceType=web&deviceVersion=unknown&includeExtendedEvents=false&serverSideAds=false', 'region': 'US', 'source': 'Pluto TV US'},
    # Rock/Metal - Stingray (Stirr OTT)
    {'name': 'Stingray Classic Rock', 'url': 'https://stirr.ott-channels.stingray.com/101/master.m3u8', 'region': 'US', 'source': 'Stirr/Stingray'},
    {'name': 'Stingray Rock Alternative', 'url': 'https://stirr.ott-channels.stingray.com/102/master.m3u8', 'region': 'US', 'source': 'Stirr/Stingray'},
    # Rock/Metal - Stingray (Lotus/Samsung)
    {'name': 'Stingray Classic Rock INT', 'url': 'https://lotus.stingray.com/manifest/ose-101ads-montreal/samsungtvplus/master.m3u8', 'region': 'INT', 'source': 'Stingray/Samsung'},
    {'name': 'Stingray Rock Alternative INT', 'url': 'https://lotus.stingray.com/manifest/ose-102ads-montreal/samsungtvplus/master.m3u8', 'region': 'INT', 'source': 'Stingray/Samsung'},
    # Rock/Metal - Canais independentes
    {'name': 'Rock TV Romania', 'url': 'https://tv.broadcasting.ro/rocktv/85c83a80-4f71-4f2d-a8d6-43f676896bcb.m3u8', 'region': 'RO', 'source': 'broadcasting.ro'},
    {'name': 'Rock TV Macedonia', 'url': 'https://stream.nasatv.com.mk/rocktv/hls/rocktv_live.m3u8', 'region': 'MK', 'source': 'nasatv.com.mk'},
    {'name': 'DJING Electro Rock', 'url': 'https://www.djing.com/tv/s-28676-05-electro-rock.m3u8', 'region': 'FR', 'source': 'DJing.com'},
    {'name': 'Now Rock AU', 'url': 'https://lightningnow90-samsungau.amagi.tv/playlist.m3u8', 'region': 'AU', 'source': 'Now Music/Amagi'},
]

# Mapeamento de região para nome do país
REGION_TO_COUNTRY = {
    'BR': 'Brasil',
    'US': 'USA',
    'GB': 'UK',
    'CA': 'Canada',
    'AU': 'Australia',
    'NZ': 'New Zealand',
    'PT': 'Português',
    'AO': 'Português',
    'MZ': 'Português',
    'CV': 'Português',
}

# ============================================================
# CLASSIFICACAO DE CANAIS
# ============================================================

# Classificação de canais brasileiros por categoria
# Ordem importa: a primeira categoria que bater ganha
BR_CATEGORIES = [
    ('BR Legislativo', [
        'tv câmara', 'tv camara', 'tv justiça', 'tv justica', 'alerj', 'almg', 'alesp',
        'canal gov', 'tv senado', 'erga omnes', 'câmara lins', 'camara lins',
    ]),
    ('BR Anime', [
        'naruto', 'death note', 'hunter x hunter', 'one piece', 'boruto', 'yu-gi-oh',
        'pokémon', 'pokemon', 'beyblade', 'inuyasha', 'jojo', 'anime', 'tokusato',
        'super onze', 'dragon ball', 'shippuden', 'otaku sign',
    ]),
    ('BR Kids', [
        'nick jr', 'nickelodeon', 'turma da mônica', 'turma da monica', 'bob esponja',
        'dpa', 'cocoricó', 'cocorico', 'teletubbies', 'smurfs', 'tartarugas ninja',
        'reino infantil', 'padrinhos mágicos', 'padrinhos magicos', 'popeye',
        'oggy', 'jetsons', 'inspetor bugiganga', 'icarly', 'kenan', 'babyfirst',
        'moranguinho', 'pluto tv junior', 'pluto tv kids', 'kids club',
        'gospel cartoon', 'ministério infantil', 'ministerio infantil', 'dm kids',
        'f. kids', 'kids mais',
    ]),
    ('BR Notícias', [
        'cnn brasil', 'jovem pan', 'record news', 'sbt news', 'bm&c news',
        '011 news', 'canal uol', 'norte news', 'bandnews',
        'tv 247', 'times brasil', 'canal rural', 'notícias agrícolas',
        'noticias agricolas', 'new brasil', 'terraviva', 'veja mais',
    ]),
    ('BR Esportes', [
        'fifa', 'dazn', 'pfl mma', 'fuel tv', 'racer', 'ge tv', 'sft combat',
        'kickboxing', 'esporte', 'sport', 'baseball', 'billiard', 'poker',
        'combat', 'horse', 'play tv horse', 'playtv horse', 'unique sports',
        'rs sports', 'trace sport', 'people are awesome', 'speedvision',
        'motorvision', 'pluto tv turbo', 'pluto tv esportes', 'auto tv',
    ]),
    ('BR Filmes', [
        'pluto tv cine', 'pluto tv filmes', 'filmelier', 'darkflix', 'cinemonde',
        'adrenalina pura', 'filmes suspense', 'cine sucessos', 'cine comédia',
        'cine comedia', 'cine drama', 'cine terror', 'cine clássicos', 'cine classicos',
        'cine romance', 'cine família', 'cine familia', 'ficção científica',
        'ficcao cientifica', 'filmes nacionais', 'filmes aventura', 'filmes ação',
        'filmes acão', 'filmes de luta', 'cine crime', 'cine inspiração',
        'cine inspiracao', 'sony one cinema', 'movieark', 'clube do terror',
        'terror trash', 'pluto tv bang bang', 'pluto tv policial', 'netmovies',
        'runtime', 'tu cine', 'freetv acción', 'freetv accion', 'freetv drama',
        'freetv terror', 'freetv familia', 'freetv sureño', 'freetv sureno',
        'spark tv luz', 'gospel movie',
    ]),
    ('BR Séries', [
        'walking dead', 'csi', 'ncis', 'charmed', 'macgyver', 'jornada nas estrelas',
        'star trek', 'z nation', 'rookie blue', 'numbers', 'feiticeira',
        'pluto tv séries', 'pluto tv series', 'séries classic', 'series classic',
        'diff\'rent strokes', 'pluto tv novelas', 'séries novelescas',
        'caçadora de relíquias', 'cacadora de reliquias', 'mistérios sem solução',
        'misterios sem solucao', 'pluto tv retrô', 'pluto tv retro',
        'pluto tv investigação', 'pluto tv investigacao', 'arquivos do fbi',
        'estado paranormal', 'caçadores de óvnis', 'cacadores de ovnis',
        'assombrações', 'assombracoes', 'pluto tv mistérios', 'pluto tv misterios',
        'pluto tv aliens', 'detetives médicos', 'detetives medicos',
        'pronto-socorro', 'acumuladores', 'pluto tv vida real', 'pluto tv curiosidade',
        'obsessão favorita', 'obsessao favorita', 'negócio fechado', 'negocio fechado',
        'homem que veio do céu', 'homem que veio do ceu',
    ]),
    ('BR Entretenimento', [
        'comedy central', 'failarmy', 'masterchef', 'south park',
        'pegadinhas', 'just for laughs', 'shark tank', 'encantador de cães',
        'encantador de caes', 'pluto tv animais', 'pet collective', 'fashiontv',
        'caras tv', 'pluto tv história', 'pluto tv historia', 'smithsonian',
        'pluto tv natureza', 'nature time', 'weatherspy', 'pluto tv cozinha',
        'kfood', 'gusto tv', 'receitas fast', 'tastemade', 'pluto tv viagens',
        'gousa', 'arirang', 'bet pluto', 'pluto tv gaming', 'realmadrid tv',
        'geekdot', 'salon line', 'sony one emoções', 'sony one emocoes',
        'malhacao', 'malhação', 'novela',
    ]),
    ('BR Religiosas', [
        'aparecida', 'canção nova', 'cancao nova', 'rit tv', 'rittv', 'evangelizar',
        'novo tempo', 'gospel', 'igreja', 'católica', 'catolica', 'cristão', 'cristao',
        'promessas', 'pai eterno', 'terceiro anjo', 'avivando', 'apóstolos', 'apostolos',
        'imjc', 'kuriakos', 'adorador', 'adorar', 'katholika', 'família de jesus',
        'familia de jesus', 'maanaim', 'manancial', 'tv sbn', 'angel tv',
        'caminho antigo', 'tv alpha', 'web tv catolica', 'unifé', 'unife',
        'tv feliz', 'tenda tv',
    ]),
    ('BR Música', [
        'stingray', 'karaokê', 'karaoke', 'forró', 'forro', 'sertanejo',
        'pop retrô', 'pop retro', 'rock show', 'qwest tv', 'hits', 'kpop',
        'classique tv', 'rede blitz',
        'rádio forró', 'radio forro', 'hip-hop', 'hip hop', 'caipira',
        'pluto tv shows por stingray', 'pluto tv paisagens', 'pluto tv karaokê',
        'tikitok radio', 'tiktok radio',
    ]),
    ('BR TV Aberta', [
        'recordtv', 'record tv', 'rede tv', 'redetv', 'sbt ', 'tv cultura',
        'tv brasil', 'band ', 'rede globo', 'globo ', 'tv gazeta',
        'tv bahia', 'tv grande natal', 'tv arapuan', 'tv marajoara',
        'tv padre cicero', 'tv do povo', 'tv brusque', 'tv clube',
        'tv aldeia', 'tv alternativa', 'tv futuro', 'tv guará',
        'tv max', 'tv mais maricá', 'tv maná', 'sic tv',
        'amazon sat', 'rede ngt', 'rede sptv', 'tv difusora',
        'tv aliança', 'tv encontro das aguas', 'tv cidade verde',
        'tv life america', 'cultura pará', 'canal educação',
        'canal do inter', 'canal 38', 'fala litoral', 'sertão tv',
        'plena tv', 'primer tv', 'catve', 'chroma tv',
        'conectv', 'conexão tv', 'demais tv', 'despertar tv',
        'eutv', 'elytv', 'fonte tv', 'nova era tv', 'stz tv',
        'boas novas', 'com brasil', 'bdc tv', 'awtv', 'adesso tv',
        'mytime movie', 'tv a folha',
    ]),
    ('BR Educação', [
        'canal educação', 'tv escola', 'univesp', 'futura', 'canal saúde',
        'canal saude', 'tv ufmg', 'tv usp',
    ]),
]

# Mapeamento de group-titles originais das fontes para categorias padrão
# (Pluto TV, Tubi, Vizio, DistroTV, IPTV-Org fornecem group-titles úteis)
GROUP_TITLE_MAP = {
    # News
    'news': 'News', 'news + opinion': 'News', 'news + opinión': 'News',
    'news & opinion': 'News', 'local news': 'News', 'national news': 'News',
    'business news': 'News', 'global news': 'News', 'desi news': 'News',
    'notícias': 'News', 'noticias': 'News',
    'news;weather': 'News', 'weather': 'News',
    # Sports
    'sports': 'Sports', 'live sports': 'Sports', 'sports on now': 'Sports',
    'esportes': 'Sports', 'mma & more': 'Sports', 'deportes': 'Sports',
    # Movies
    'movies': 'Movies', 'more movies': 'Movies', 'filmes': 'Movies',
    'movie channels': 'Movies', 'westerns': 'Movies', 'películas': 'Movies',
    'peliculas': 'Movies', 'classic shows & movies': 'Movies',
    # Series / Drama
    'drama': 'Series', 'crime drama': 'Series', 'bingeable drama': 'Series',
    'tv dramas': 'Series', 'classic tv': 'Series', 'séries': 'Series',
    'series': 'Series', 'classic tv comedy': 'Series',
    # Comedy
    'comedy': 'Comedy', 'comédia': 'Comedy', 'comedia': 'Comedy',
    # Entertainment / Reality
    'entertainment': 'Entertainment', 'reality': 'Entertainment',
    'reality tv': 'Entertainment', 'competition reality': 'Entertainment',
    'game shows': 'Entertainment', 'daytime + game shows': 'Entertainment',
    'daytime & talk shows': 'Entertainment', 'games & competition': 'Entertainment',
    'fun & games': 'Entertainment', 'pop culture': 'Entertainment',
    'entretenimiento': 'Entertainment', 'desi entertainment': 'Entertainment',
    'featured': 'Entertainment', 'new on pluto tv': 'Entertainment',
    # Kids
    'kids': 'Kids', 'kids + family': 'Kids', 'kids & family': 'Kids',
    'infantil': 'Kids', 'nickelodeon': 'Kids', 'animation': 'Kids',
    'animation;kids': 'Kids', 'education;kids': 'Kids',
    # Music
    'music': 'Music', 'music videos': 'Music', 'música': 'Music',
    'musica': 'Music', 'moods': 'Music', 'mood + ambiance': 'Music',
    # Crime / True Crime
    'true crime': 'Crime', 'crime': 'Crime',
    'investigação': 'Crime', 'investigacion': 'Crime',
    # Sci-Fi / Paranormal
    'sci-fi': 'Sci-Fi', 'sci-fi + fantasy': 'Sci-Fi',
    'sci-fi & fantasy': 'Sci-Fi', 'sci-fi & supernatural': 'Sci-Fi',
    'paranormal': 'Sci-Fi', 'mystery': 'Sci-Fi',
    'misterios y sobrenatural': 'Sci-Fi',
    'mistérios e sobrenatural': 'Sci-Fi',
    # Documentary / History
    'documentary': 'Documentary', 'documentaries': 'Documentary',
    'documentary + science': 'Documentary', 'history + science': 'Documentary',
    'history + docs': 'Documentary', 'documentales': 'Documentary',
    # Lifestyle / Food / Home
    'lifestyle': 'Lifestyle', 'lifestyle & wellness': 'Lifestyle',
    'home + food': 'Lifestyle', 'food & travel': 'Lifestyle',
    'food + travel': 'Lifestyle', 'living': 'Lifestyle', 'home': 'Lifestyle',
    'estilo de vida': 'Lifestyle', 'good eats': 'Lifestyle',
    'culture + lifestyle': 'Lifestyle', 'shopping': 'Lifestyle', 'shop': 'Lifestyle',
    'curiosidades': 'Lifestyle', 'tv brasileira': 'Lifestyle',
    # Nature / Outdoors
    'animals + nature': 'Nature', 'nature + science': 'Nature',
    'science & nature': 'Nature', 'natureza': 'Nature',
    'outdoors': 'Nature', 'outdoor': 'Nature',
    'real life adventure': 'Nature', 'nature': 'Nature',
    # Religious
    'religious': 'Religious', 'spirituality': 'Religious',
    'inspiration + faith': 'Religious',
    # Anime / Geek
    'anime': 'Anime', 'anime & geek': 'Anime',
    # Retro
    'retrô': 'Retro', 'retro': 'Retro',
    # En Español
    'en español': 'En Español', 'en espanol': 'En Español',
    'español': 'En Español', 'espanol': 'En Español',
    # Regional / Culture
    'african': 'Culture', 'culture': 'Culture', 'radio': 'Radio',
    # Education
    'education': 'Education', 'general': 'General',
    # South Park (Pluto)
    'south park': 'Comedy',
    # MTV (Pluto BR)
    'mtv': 'MTV',
    # Novelas
    'novelas': 'Series', 'novela': 'Series',
    # Investigação
    'investigação': 'Crime', 'investigacion': 'Crime',
    # Jornada nas Estrelas (Pluto BR)
    'jornada nas estrelas': 'Sci-Fi',
}

# Classificação genérica por palavras-chave no NOME do canal
# Usada quando o group-title original é inútil (Plex, Roku, Samsung, etc.)
# Ordem importa: mais específico primeiro
NAME_CATEGORIES = [
    # Anime (antes de Kids para evitar conflito)
    ('Anime', [
        'anime', 'crunchyroll', 'funimation', 'tokusato',
    ]),
    # News
    ('News', [
        'news', 'cnn', 'msnbc', 'cnbc', 'bloomberg', 'al jazeera', 'reuters',
        'france 24', 'euronews', 'newsy', 'court tv', 'c-span', 'cspan',
        'sky news', 'bbc news', 'abc news', 'cbs news', 'nbc news', 'fox news',
        'newsmax', 'newsnation', 'weather channel', 'accuweather',
        'notícias', 'noticias', 'jornal', 'telejornal',
        'fox weather', 'livenow from fox', 'today all day', 'yahoo! finance',
        'telemundo al dia', 'thegrio', 'oan ', 'roi tv',
    ]),
    # Sports
    ('Sports', [
        'espn', 'nfl network', 'nba tv', 'mlb network', 'nhl network',
        'fox sport', 'bein sport', 'dazn', 'fuel tv', 'stadium',
        'motorsport', 'racing', 'ufc', 'wwe', 'boxing',
        'cricket', 'surfing', 'x games', 'outdoor channel',
        'fight', 'pfl mma', 'sft combat', 'kickboxing',
        'wired2fish', 'waypoint tv', 'outdoor america',
    ]),
    # Kids
    ('Kids', [
        'nick jr', 'nickelodeon', 'cartoon', 'disney', 'pbs kids', 'baby',
        'junior', 'sesame', 'kids', 'children', 'lego', 'toon',
        'mr. bean', 'three stooges', 'alf',
    ]),
    # Movies
    ('Movies', [
        'movie', 'cinema', 'film', 'hollywood', 'thriller',
        'filmrise', 'fandango', 'amc',
        'horror machine', 'screambox', 'scream factory', 'dark matter tv',
        'cowboy classics', 'old west tv', 'wild west tv', 'lone star',
        'urban action', 'conflict',
    ]),
    # Comedy
    ('Comedy', [
        'comedy', 'laugh', 'funny', 'stand-up', 'standup', 'south park',
        'failarmy', 'just for laughs', 'roast',
        'america\'s funniest', 'trailer park boys', 'red green show',
    ]),
    # Series / Drama
    ('Series', [
        'classic tv', 'retro tv', 'drama', 'soap', 'novela', 'telenovela',
        'bold and the beautiful', 'jump street', 'operation repo',
        'deal or no deal',
    ]),
    # Music
    ('Music', [
        'music', 'vevo', 'stingray', 'karaoke', 'hits', 'radio',
        'hip hop', 'country music', 'jazz', 'classical music', 'reggae',
        'kpop', 'latin music', 'concert', 'non-stop \'90s',
    ]),
    # Documentary / History
    ('Documentary', [
        'discovery', 'national geographic', 'nat geo', 'history channel',
        'smithsonian', 'documentary', 'science channel',
        'magellantv', 'cosmic frontiers', 'popular science',
        'true history', 'history & warfare',
    ]),
    # Crime
    ('Crime', [
        'true crime', 'crime', 'investigation discovery', 'forensic',
        'dateline', 'cold case', 'mysteria',
    ]),
    # Sci-Fi
    ('Sci-Fi', [
        'sci-fi', 'sci fi', 'syfy', 'paranormal', 'alien', 'supernatural',
        'mystery science theater',
    ]),
    # Lifestyle / Home / Food
    ('Lifestyle', [
        'food', 'cooking', 'travel', 'home & garden', 'hgtv', 'design',
        'fashion', 'beauty', 'health', 'fitness', 'yoga', 'diy',
        'magnolia', 'bon appétit', 'bon appetit', 'tastemade',
        'property', 'real estate', 'interior',
        'gusto tv', 'homeful', 'at home with', 'spend smart', 'family handyman',
        'popstar', 'loupe art', 'rvtv',
    ]),
    # Nature / Animals
    ('Nature', [
        'nature', 'animal', 'wildlife', 'planet earth', 'ocean',
        'national park', 'safari',
        'dog whisperer', 'pet collective', 'bark tv',
        'great american adventures', 'wildest',
    ]),
    # Religious
    ('Religious', [
        'church', 'gospel', 'faith', 'christian', 'catholic', 'prayer',
        'worship', 'daystar', 'tbn', 'god tv', 'hillsong', 'jesus',
        'ewtn', 'hope channel', 'inspiration', 'uplift',
        'joel osteen', 'jltv',
    ]),
    # Entertainment (catchall amplo - deve ficar por último)
    ('Entertainment', [
        'reality', 'game show', 'talk show', 'entertainment', 'bet ',
        'bravo', 'e! ', 'tmz', 'buzzfeed', 'vice',
        'drone tv', 'awe plus', 'envoy', 'the first',
        'black enterprise', 'shout! tv',
    ]),
]

# Ordem de relevância para BR Notícias (menor = mais relevante)
NEWS_RELEVANCE = [
    'cnn brasil',
    'record news',
    'bandnews',
    'jovem pan',
    'sbt news',
    'bm&c news',
    'times brasil',
    'canal uol',
    'canal rural',
    'terraviva',
    'new brasil',
    'veja mais',
    'notícias agrícolas',
    'noticias agricolas',
    'tv 247',
    '011 news',
    'norte news',
]

# Group-titles que são inúteis (genéricos demais, não indicam categoria)
USELESS_GROUPS = {
    '', 'plex', 'roku', 'uncategorized', 'undefined',
    'united states', 'united kingdom', 'canada', 'germany', 'france',
    'spain', 'italy', 'india', 'south korea', 'switzerland', 'austria',
    'sweden', 'norway', 'denmark', 'finland', 'netherlands', 'belgium',
    'ireland', 'luxembourg', 'brazil', 'brasil', 'portugal', 'australia',
    'new zealand', 'singapore', 'philippines', 'thailand', 'mexico',
    'general', 'other',
}


# ============================================================
# FUNCOES
# ============================================================

def clean_channel_name(name):
    """Remove números de canal, nomes de fontes, tags de resolução/status do nome."""
    if not name:
        return name

    # 1) Remove números de canal do início
    # Padrões: "123 Canal", "123. Canal", "123 - Canal", "123 | Canal", "#123 Canal"
    cleaned = re.sub(r'^[#]?\d{1,5}[\s.\-|:]+\s*', '', name).strip()
    if not cleaned:
        return name

    # 2) Remove nomes de fontes/plataformas
    source_patterns = [
        r'\s*[\-|]\s*(?:Pluto\s*TV|Samsung(?:\s*TV\s*Plus)?|Roku|Plex|Tubi|Stirr|DistroTV|Vizio|LG\s*Channels?|XUMO|Fire\s*TV)\s*$',
        r'\s*[(\[]\s*(?:Pluto\s*TV|Samsung|Roku|Plex|Tubi|DistroTV|Vizio)\s*[)\]]\s*$',
    ]
    for pattern in source_patterns:
        cleaned = re.sub(pattern, '', cleaned, flags=re.IGNORECASE).strip()

    # 3) Remove tags de resolução e status: (720p), (1080p), (1080i), [Geo-blocked], [Not 24/7]
    cleaned = re.sub(r'\s*\(\d{3,4}[pi]\)', '', cleaned).strip()
    cleaned = re.sub(r'\s*\[(?:Geo-blocked|Not 24/7|Offline|Downscaled)\]', '', cleaned, flags=re.IGNORECASE).strip()

    return cleaned if cleaned else name


def get_news_relevance(channel_name):
    """Retorna prioridade de relevância para canais de notícias."""
    name_lower = channel_name.lower()
    for i, keyword in enumerate(NEWS_RELEVANCE):
        if keyword in name_lower:
            return i
    return 999


def classify_br_channel(channel_name):
    """Classifica um canal brasileiro em subcategoria."""
    name_lower = channel_name.lower()
    for category, keywords in BR_CATEGORIES:
        for kw in keywords:
            if kw in name_lower:
                return category
    return 'BR Variedades'


def normalize_group_title(original_group):
    """Normaliza o group-title original da fonte para uma categoria padrão."""
    if not original_group:
        return None
    group_lower = original_group.lower().strip()
    if group_lower in USELESS_GROUPS:
        return None
    return GROUP_TITLE_MAP.get(group_lower)


def classify_by_name(channel_name):
    """Classifica canal por palavras-chave no nome."""
    name_lower = channel_name.lower() if channel_name else ''
    for category, keywords in NAME_CATEGORIES:
        for kw in keywords:
            if kw in name_lower:
                return category
    return None


def get_final_group(original_group, region, channel_name=''):
    """Determina o grupo final baseado no país, categoria ou música."""
    name_lower = channel_name.lower() if channel_name else ''

    # VH1 e MTV são categorias globais (qualquer região)
    if 'vh1' in name_lower:
        return 'VH1'
    if re.search(r'\bmtv\b', name_lower):
        return 'MTV'

    # Rock/Metal é categoria global (qualquer região)
    rock_keywords = [
        'rock x metal', 'rock alternative', 'classic rock', 'electro rock',
        'now rock', 'vevo rock', 'live music', 'rock tv', 'rock show',
        'mtv rocks', 'rock!',
    ]
    if any(kw in name_lower for kw in rock_keywords):
        return 'Rock'

    # Se for Brasil, usa classificação detalhada existente
    if region.upper() == 'BR':
        return classify_br_channel(channel_name)

    # Para demais regiões: tentar classificar em subcategoria
    country = REGION_TO_COUNTRY.get(region, 'Other')

    # 1) Tentar mapear pelo group-title original da fonte
    category = normalize_group_title(original_group)

    # 2) Se não deu, classificar pelo nome do canal
    if not category:
        category = classify_by_name(channel_name)

    # 3) Se classificou, formata como "País Category"
    if category:
        # Music é global (não prefixar com país)
        if category == 'Music':
            return 'Music'
        if category == 'MTV':
            return 'MTV'
        return f'{country} {category}'

    # 4) Fallback: só o país
    return country


def extract_group_from_extinf(extinf_line):
    """Extrai o group-title de uma linha EXTINF."""
    match = re.search(r'group-title="([^"]*)"', extinf_line)
    return match.group(1) if match else ''


def extract_logo_from_extinf(extinf_line):
    """Extrai o tvg-logo de uma linha EXTINF."""
    match = re.search(r'tvg-logo="([^"]*)"', extinf_line)
    return match.group(1) if match else ''


def update_extinf_group(extinf_line, new_group):
    """Atualiza o group-title em uma linha EXTINF."""
    if 'group-title="' in extinf_line:
        return re.sub(r'group-title="[^"]*"', f'group-title="{new_group}"', extinf_line)
    else:
        # Adiciona group-title se não existir
        return extinf_line.replace('#EXTINF:-1 ', f'#EXTINF:-1 group-title="{new_group}" ')


def download_m3u(url, name):
    """Baixa uma playlist M3U."""
    print(f"  Baixando {name}...")
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}

    try:
        response = requests.get(url, headers=headers, timeout=30)
        response.raise_for_status()
        content = response.text
        channel_count = content.count('#EXTINF')
        print(f"    OK! ({channel_count} canais)")
        return content, channel_count
    except Exception as e:
        print(f"    ERRO: {e}")
        return None, 0


def update_extinf_name(extinf_line, new_name):
    """Atualiza o nome do canal na linha EXTINF (após a última vírgula)."""
    comma_idx = extinf_line.rfind(',')
    if comma_idx >= 0:
        return extinf_line[:comma_idx + 1] + new_name
    return extinf_line


def parse_m3u_to_channels(content, source_name, region):
    """Converte conteudo M3U em lista de canais."""
    lines = content.split('\n')
    channels = []
    current_extinf = None

    for line in lines:
        line = line.strip()
        if line.startswith('#EXTINF'):
            current_extinf = line
        elif line.startswith('http') and current_extinf:
            raw_name = current_extinf.split(',')[-1].strip() if ',' in current_extinf else 'Unknown'
            name = clean_channel_name(raw_name)
            original_group = extract_group_from_extinf(current_extinf)
            logo = extract_logo_from_extinf(current_extinf)
            # Atualizar extinf com nome limpo
            extinf = update_extinf_name(current_extinf, name)
            channels.append({
                'name': name,
                'url': line,
                'extinf': extinf,
                'source': source_name,
                'region': region,
                'original_group': original_group,
                'logo': logo
            })
            current_extinf = None

    return channels


def deduplicate_channels(channels):
    """Remove canais duplicados baseado na URL do stream."""
    seen_urls = set()
    unique = []
    for ch in channels:
        url = ch['url'].split('?')[0].rstrip('/')
        if url not in seen_urls:
            seen_urls.add(url)
            unique.append(ch)
    removed = len(channels) - len(unique)
    if removed:
        print(f"  Duplicados removidos: {removed}")
    print(f"  Canais unicos: {len(unique)}")
    return unique


def test_channel(channel, timeout=8):
    """Testa se um canal esta funcionando."""
    url = channel['url']
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}

    try:
        response = requests.get(url, headers=headers, timeout=timeout, stream=True)

        if response.status_code == 200:
            first_bytes = next(response.iter_content(1024), b'')
            response.close()

            if first_bytes:
                return {**channel, 'status': 'OK'}

        return {**channel, 'status': f'HTTP_{response.status_code}'}

    except:
        return {**channel, 'status': 'ERROR'}


def test_channels_parallel(channels):
    """Testa canais em paralelo."""
    cpu_count = multiprocessing.cpu_count()
    max_workers = max(4, cpu_count - 1)

    print(f"\nTestando {len(channels)} canais com {max_workers} workers...")

    results = []
    working = 0

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        future_to_channel = {executor.submit(test_channel, ch): ch for ch in channels}

        for i, future in enumerate(as_completed(future_to_channel), 1):
            result = future.result()
            results.append(result)

            if result['status'] == 'OK':
                working += 1

            if i % 100 == 0 or i == len(channels):
                print(f"  Progresso: {i}/{len(channels)} ({working} OK)")

    return results, working


def collect_all_channels():
    """Coleta canais de todas as fontes."""
    print("\nColetando canais...")

    all_channels = []

    # Download paralelo de todas as fontes
    def fetch_source(source_key, source):
        region = source.get('region', '')
        if region not in TARGET_REGIONS:
            return []
        content, count = download_m3u(source['url'], source['name'])
        if content:
            return parse_m3u_to_channels(content, source['name'], region)
        return []

    with ThreadPoolExecutor(max_workers=8) as executor:
        futures = {
            executor.submit(fetch_source, key, src): key
            for key, src in SOURCES.items()
        }
        for future in as_completed(futures):
            channels = future.result()
            all_channels.extend(channels)

    # Adicionar canais extras (VH1, MTV)
    if EXTRA_CHANNELS:
        print(f"\n  Adicionando {len(EXTRA_CHANNELS)} canais extras (VH1/MTV)...")
        for ch in EXTRA_CHANNELS:
            logo = ch.get('logo', '')
            extinf = f'#EXTINF:-1 tvg-name="{ch["name"]}" tvg-logo="{logo}",{ch["name"]}'
            all_channels.append({
                'name': ch['name'],
                'url': ch['url'],
                'extinf': extinf,
                'source': ch.get('source', 'Extra'),
                'region': ch.get('region', 'INT'),
                'original_group': '',
                'logo': logo
            })

    print(f"\nTotal coletados: {len(all_channels)}")
    all_channels = deduplicate_channels(all_channels)

    with_logo = sum(1 for ch in all_channels if ch.get('logo', '').strip())
    without_logo = len(all_channels) - with_logo
    print(f"  Canais com logo: {with_logo}")
    print(f"  Canais sem logo: {without_logo}")

    return all_channels


def generate_m3u_content(channels):
    """Gera conteudo M3U."""
    lines = ['#EXTM3U']
    lines.append(f'# Atualizado: {datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC")}')
    lines.append(f'# Canais: {len(channels)}')
    lines.append('')

    # Pré-calcular grupo final de cada canal
    enriched = []
    for ch in channels:
        original_group = ch.get('original_group', '')
        region = ch.get('region', '')
        channel_name = ch.get('name', '')
        final_group = get_final_group(original_group, region, channel_name)
        enriched.append((ch, final_group))

    # Ordenar BR Notícias por relevância
    enriched.sort(key=lambda x: get_news_relevance(x[0].get('name', '')) if x[1] == 'BR Notícias' else 999)

    for ch, final_group in enriched:
        updated_extinf = update_extinf_group(ch['extinf'], final_group)
        lines.append(updated_extinf)
        lines.append(ch['url'])

    return '\n'.join(lines)


# ============================================================
# MAIN
# ============================================================

def main():
    print("=" * 60)
    print("IPTV PLAYLIST GENERATOR")
    print("=" * 60)
    print(f"Data: {datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S UTC')}")

    # 1. Coletar canais
    all_channels = collect_all_channels()

    if not all_channels:
        print("Nenhum canal encontrado!")
        return

    # 2. Testar canais
    results, working = test_channels_parallel(all_channels)

    # Filtrar funcionando
    working_channels = [r for r in results if r['status'] == 'OK']

    print(f"\nResultado: {working}/{len(all_channels)} funcionando ({working*100//len(all_channels)}%)")

    # 3. Gerar playlist
    playlist_content = generate_m3u_content(working_channels)

    # 4. Salvar
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        f.write(playlist_content)

    print(f"\nPlaylist salva: {OUTPUT_FILE}")
    print(f"Total de canais: {len(working_channels)}")


if __name__ == '__main__':
    main()
