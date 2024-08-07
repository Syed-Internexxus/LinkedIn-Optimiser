import os
from dotenv import load_dotenv
import csv
import json
import requests
from concurrent.futures import ThreadPoolExecutor
from tqdm import tqdm
from termcolor import colored
from apify_client import ApifyClient

# Load environment variables from .env file
load_dotenv()

TOKEN = os.getenv("API_TOKEN")

def get_profile_info(slug):


    # Initialize the ApifyClient with your API token
    client = ApifyClient("apify_api_NQWaTzbbYPzvhqYK1PefxagwaKwJro08RVTI")

    # Prepare the Actor input
    run_input = {
        "minDelay": 15,
        "maxDelay": 60,
        "urls": [slug],
            "cookie": [
    {
        "domain": ".linkedin.com",
        "expirationDate": 1729712399,
        "hostOnly": False,
        "httpOnly": False,
        "name": "_gcl_au",
        "path": "/",
        "sameSite": "unspecified",
        "secure": False,
        "session": False,
        "storeId": "0",
        "value": "1.1.2109540563.1717374673",
        "id": 1
    },
    {
        "domain": ".linkedin.com",
        "expirationDate": 1725150673,
        "hostOnly": False,
        "httpOnly": False,
        "name": "_gcl_aw",
        "path": "/",
        "sameSite": "unspecified",
        "secure": False,
        "session": False,
        "storeId": "0",
        "value": "GCL.1717374673.Cj0KCQjwsPCyBhD4ARIsAPaaRf34OQhqAO7XVC1lU1tT44yjixjkAvho_b3JrTwDTWrXWr9tAnHDRnsaAuAvEALw_wcB",
        "id": 2
    },
    {
        "domain": ".linkedin.com",
        "expirationDate": 1725150673,
        "hostOnly": False,
        "httpOnly": False,
        "name": "_gcl_dc",
        "path": "/",
        "sameSite": "unspecified",
        "secure": False,
        "session": False,
        "storeId": "0",
        "value": "GCL.1717374673.Cj0KCQjwsPCyBhD4ARIsAPaaRf34OQhqAO7XVC1lU1tT44yjixjkAvho_b3JrTwDTWrXWr9tAnHDRnsaAuAvEALw_wcB",
        "id": 3
    },
    {
        "domain": ".linkedin.com",
        "expirationDate": 1725150672,
        "hostOnly": False,
        "httpOnly": False,
        "name": "_gcl_gs",
        "path": "/",
        "sameSite": "unspecified",
        "secure": False,
        "session": False,
        "storeId": "0",
        "value": "2.1.k1$i1717374669",
        "id": 4
    },
    {
        "domain": ".linkedin.com",
        "expirationDate": 1727385167.784093,
        "hostOnly": False,
        "httpOnly": False,
        "name": "_guid",
        "path": "/",
        "sameSite": "no_restriction",
        "secure": True,
        "session": False,
        "storeId": "0",
        "value": "c17f22b6-9247-41fe-aa87-d9e59a9570bd",
        "id": 5
    },
    {
        "domain": ".linkedin.com",
        "expirationDate": 1751070672,
        "hostOnly": False,
        "httpOnly": False,
        "name": "_uetvid",
        "path": "/",
        "sameSite": "unspecified",
        "secure": False,
        "session": False,
        "storeId": "0",
        "value": "945d2b70214011ef89e659ecd984bd9d",
        "id": 6
    },
    {
        "domain": ".linkedin.com",
        "expirationDate": 1724528400,
        "hostOnly": False,
        "httpOnly": False,
        "name": "aam_uuid",
        "path": "/",
        "sameSite": "unspecified",
        "secure": False,
        "session": False,
        "storeId": "0",
        "value": "91796952455259285263966865141562689876",
        "id": 7
    },
    {
        "domain": ".linkedin.com",
        "expirationDate": 1737487516,
        "hostOnly": False,
        "httpOnly": False,
        "name": "AMCV_14215E3D5995C57C0A495C55%40AdobeOrg",
        "path": "/",
        "sameSite": "unspecified",
        "secure": False,
        "session": False,
        "storeId": "0",
        "value": "-637568504%7CMCIDTS%7C19930%7CMCMID%7C91997226936498077494017789110038805151%7CMCAAMLH-1722540316%7C7%7CMCAAMB-1722540316%7C6G1ynYcLPuiQxYZrsz_pkqfLG9yMXBpb2zX5dvJdYQJzPXImdj0y%7CMCOPTOUT-1721942716s%7CNONE%7CvVersion%7C5.1.1",
        "id": 8
    },
    {
        "domain": ".linkedin.com",
        "hostOnly": False,
        "httpOnly": False,
        "name": "AMCVS_14215E3D5995C57C0A495C55%40AdobeOrg",
        "path": "/",
        "sameSite": "unspecified",
        "secure": False,
        "session": True,
        "storeId": "0",
        "value": "1",
        "id": 9
    },
    {
        "domain": ".linkedin.com",
        "expirationDate": 1724513168.287969,
        "hostOnly": False,
        "httpOnly": False,
        "name": "AnalyticsSyncHistory",
        "path": "/",
        "sameSite": "no_restriction",
        "secure": True,
        "session": False,
        "storeId": "0",
        "value": "AQIuyFhlrpMYfwAAAZDqf-O-670HWRf0PxMi7VuzRJU_dx73rd2BpQ1CEpbCBbUB0dyA-qb6gJS5VTBxziOXlg",
        "id": 10
    },
    {
        "domain": ".linkedin.com",
        "expirationDate": 1753503561.95445,
        "hostOnly": False,
        "httpOnly": False,
        "name": "bcookie",
        "path": "/",
        "sameSite": "no_restriction",
        "secure": True,
        "session": False,
        "storeId": "0",
        "value": "\"v=2&6b89df8f-21f5-47e1-89b5-0ee0ae93d001\"",
        "id": 11
    },
    {
        "domain": ".linkedin.com",
        "expirationDate": 1751145168.835713,
        "hostOnly": False,
        "httpOnly": True,
        "name": "dfpfpt",
        "path": "/",
        "sameSite": "lax",
        "secure": True,
        "session": False,
        "storeId": "0",
        "value": "300e24edeeae4302bf77a94ee344afe4",
        "id": 12
    },
    {
        "domain": ".linkedin.com",
        "hostOnly": False,
        "httpOnly": True,
        "name": "fptctx2",
        "path": "/",
        "sameSite": "lax",
        "secure": True,
        "session": True,
        "storeId": "0",
        "value": "taBcrIH61PuCVH7eNCyH0HyAAKgSb15ZEqidLg30r8MvdAyQsB%252byGXycG21v5XUsHDyt9D6aP7MuQn%252bL4UR5b8%252bu8Bk%252fM5p8KUrzx2KB6%252bWTUkAbbm%252fPNV0j%252bjPYUs1sbVsWhfInj2YQvW2mWZRUeiyXGb6HDE%252fS6TLApubGxLk3a6%252bYLAicls3CqzH%252b4c47f4jmcjvcYrkRhkn0ItA6psNmayqzrQvl6ow4Qw93Uwo2aT3gyqwf0VVPpDnYDJqnqTBqAHpIsS6qfeG1%252fVK2l9jDatyuVVlKAm%252fnsW17tsyLhytrTdwS1ykhX1uykJd5fmzA%252f%252bgW7lVPPwhzcxCwFRrNV8lTbo%252fGSoE6U4c5VYo%253d",
        "id": 13
    },
    {
        "domain": ".linkedin.com",
        "expirationDate": 1737524352,
        "hostOnly": False,
        "httpOnly": False,
        "name": "gpv_pn",
        "path": "/",
        "sameSite": "unspecified",
        "secure": False,
        "session": False,
        "storeId": "0",
        "value": "www.linkedin.com%2Fcompany%2Fid-redacted%2Fadmin%2Fdashboard%2F",
        "id": 14
    },
    {
        "domain": ".linkedin.com",
        "hostOnly": False,
        "httpOnly": False,
        "name": "lang",
        "path": "/",
        "sameSite": "no_restriction",
        "secure": True,
        "session": True,
        "storeId": "0",
        "value": "v=2&lang=en-us",
        "id": 15
    },
    {
        "domain": ".linkedin.com",
        "expirationDate": 1729743561.954367,
        "hostOnly": False,
        "httpOnly": False,
        "name": "li_sugr",
        "path": "/",
        "sameSite": "no_restriction",
        "secure": True,
        "session": False,
        "storeId": "0",
        "value": "33395861-98d6-40bd-ad1a-c5e069d68286",
        "id": 16
    },
    {
        "domain": ".linkedin.com",
        "expirationDate": 1729712430.424907,
        "hostOnly": False,
        "httpOnly": False,
        "name": "liap",
        "path": "/",
        "sameSite": "no_restriction",
        "secure": True,
        "session": False,
        "storeId": "0",
        "value": "true",
        "id": 17
    },
    {
        "domain": ".linkedin.com",
        "expirationDate": 1722037920.546026,
        "hostOnly": False,
        "httpOnly": False,
        "name": "lidc",
        "path": "/",
        "sameSite": "no_restriction",
        "secure": True,
        "session": False,
        "storeId": "0",
        "value": "\"b=OB23:s=O:r=O:a=O:p=O:g=4529:u=198:x=1:i=1721967558:t=1722037919:v=2:sig=AQEoPzRJqgnaRXSHw-nGIhGLJ9vU7tOH\"",
        "id": 18
    },
    {
        "domain": ".linkedin.com",
        "expirationDate": 1724513168.537733,
        "hostOnly": False,
        "httpOnly": False,
        "name": "lms_ads",
        "path": "/",
        "sameSite": "no_restriction",
        "secure": True,
        "session": False,
        "storeId": "0",
        "value": "AQHXtyKDHb3dkQAAAZDqf-SjkQI7Ol1zNHAsloItDbaEzcnDioBIEeUFbojrTws2OuV9Qiz-FTFLT3PA60imL7Pk9Ncp1Lj5",
        "id": 19
    },
    {
        "domain": ".linkedin.com",
        "expirationDate": 1724513168.537863,
        "hostOnly": False,
        "httpOnly": False,
        "name": "lms_analytics",
        "path": "/",
        "sameSite": "no_restriction",
        "secure": True,
        "session": False,
        "storeId": "0",
        "value": "AQHXtyKDHb3dkQAAAZDqf-SjkQI7Ol1zNHAsloItDbaEzcnDioBIEeUFbojrTws2OuV9Qiz-FTFLT3PA60imL7Pk9Ncp1Lj5",
        "id": 20
    },
    {
        "domain": ".linkedin.com",
        "expirationDate": 1732926673,
        "hostOnly": False,
        "httpOnly": False,
        "name": "mbox",
        "path": "/",
        "sameSite": "no_restriction",
        "secure": True,
        "session": False,
        "storeId": "0",
        "value": "session#820f407afb4747fdac5d7d70e82a01af#1717376533|PC#820f407afb4747fdac5d7d70e82a01af.34_0#1732926673",
        "id": 21
    },
    {
        "domain": ".linkedin.com",
        "expirationDate": 1752076349,
        "hostOnly": False,
        "httpOnly": False,
        "name": "mp_d67960141aa910b0612c66ad7f230278_mixpanel",
        "path": "/",
        "sameSite": "unspecified",
        "secure": False,
        "session": False,
        "storeId": "0",
        "value": "%7B%22distinct_id%22%3A%20%22190982d96843ed-0d5da2fed4bcca-19525637-13c680-190982d968716bb%22%2C%22%24device_id%22%3A%20%22190982d96843ed-0d5da2fed4bcca-19525637-13c680-190982d968716bb%22%2C%22%24initial_referrer%22%3A%20%22%24direct%22%2C%22%24initial_referring_domain%22%3A%20%22%24direct%22%7D",
        "id": 22
    },
    {
        "domain": ".linkedin.com",
        "hostOnly": False,
        "httpOnly": False,
        "name": "s_cc",
        "path": "/",
        "sameSite": "unspecified",
        "secure": False,
        "session": True,
        "storeId": "0",
        "value": "true",
        "id": 23
    },
    {
        "domain": ".linkedin.com",
        "expirationDate": 1737524352,
        "hostOnly": False,
        "httpOnly": False,
        "name": "s_fid",
        "path": "/",
        "sameSite": "unspecified",
        "secure": False,
        "session": False,
        "storeId": "0",
        "value": "506A3DF2D194D3E6-1E8AEBB9C57CACE7",
        "id": 24
    },
    {
        "domain": ".linkedin.com",
        "expirationDate": 1737524352,
        "hostOnly": False,
        "httpOnly": False,
        "name": "s_ips",
        "path": "/",
        "sameSite": "unspecified",
        "secure": False,
        "session": False,
        "storeId": "0",
        "value": "813",
        "id": 25
    },
    {
        "domain": ".linkedin.com",
        "hostOnly": False,
        "httpOnly": False,
        "name": "s_plt",
        "path": "/",
        "sameSite": "unspecified",
        "secure": False,
        "session": True,
        "storeId": "0",
        "value": "3.25",
        "id": 26
    },
    {
        "domain": ".linkedin.com",
        "hostOnly": False,
        "httpOnly": False,
        "name": "s_pltp",
        "path": "/",
        "sameSite": "unspecified",
        "secure": False,
        "session": True,
        "storeId": "0",
        "value": "www.linkedin.com%2Fcompany%2Fid-redacted%2Fadmin%2Fdashboard%2F",
        "id": 27
    },
    {
        "domain": ".linkedin.com",
        "hostOnly": False,
        "httpOnly": False,
        "name": "s_ppv",
        "path": "/",
        "sameSite": "unspecified",
        "secure": False,
        "session": True,
        "storeId": "0",
        "value": "www.linkedin.com%2Fcompany%2Fid-redacted%2Fadmin%2Fdashboard%2F%2C28%2C28%2C813%2C1%2C3",
        "id": 28
    },
    {
        "domain": ".linkedin.com",
        "hostOnly": False,
        "httpOnly": False,
        "name": "s_sq",
        "path": "/",
        "sameSite": "unspecified",
        "secure": False,
        "session": True,
        "storeId": "0",
        "value": "lnkdprod%3D%2526c.%2526a.%2526activitymap.%2526page%253Dwww.linkedin.com%25252Fcompany%25252Fid-redacted%25252Fadmin%25252Fdashboard%25252F%2526link%253D1%2525201%252520new%252520network%252520update%252520notification%252520My%252520Network%2526region%253Dglobal-nav%2526pageIDType%253D1%2526.activitymap%2526.a%2526.c%2526pid%253Dwww.linkedin.com%25252Fcompany%25252Fid-redacted%25252Fadmin%25252Fdashboard%25252F%2526pidt%253D1%2526oid%253Dhttps%25253A%25252F%25252Fwww.linkedin.com%25252Fmynetwork%25252F%25253F%2526ot%253DA",
        "id": 29
    },
    {
        "domain": ".linkedin.com",
        "expirationDate": 1737524352,
        "hostOnly": False,
        "httpOnly": False,
        "name": "s_tp",
        "path": "/",
        "sameSite": "unspecified",
        "secure": False,
        "session": False,
        "storeId": "0",
        "value": "2870",
        "id": 30
    },
    {
        "domain": ".linkedin.com",
        "expirationDate": 1737524352,
        "hostOnly": False,
        "httpOnly": False,
        "name": "s_tslv",
        "path": "/",
        "sameSite": "unspecified",
        "secure": False,
        "session": False,
        "storeId": "0",
        "value": "1721972352450",
        "id": 31
    },
    {
        "domain": ".linkedin.com",
        "hostOnly": False,
        "httpOnly": False,
        "name": "sdsc",
        "path": "/",
        "sameSite": "no_restriction",
        "secure": True,
        "session": True,
        "storeId": "0",
        "value": "1%3A1SZM1shxDNbLt36wZwCgPgvN58iw%3D",
        "id": 32
    },
    {
        "domain": ".linkedin.com",
        "hostOnly": False,
        "httpOnly": False,
        "name": "SID",
        "path": "/",
        "sameSite": "unspecified",
        "secure": False,
        "session": True,
        "storeId": "0",
        "value": "0fdf685f-ee45-4fe2-951d-781e30b6b27f",
        "id": 33
    },
    {
        "domain": ".linkedin.com",
        "expirationDate": 1724559557,
        "hostOnly": False,
        "httpOnly": False,
        "name": "UserMatchHistory",
        "path": "/",
        "sameSite": "no_restriction",
        "secure": True,
        "session": False,
        "storeId": "0",
        "value": "AQKHd95RrfN2HAAAAZDtQ701Aytho9EUClC26XOrp5uLmYX-Xetw9NTCsL2GeY9rJdhB1PDCLFTVeUadl7dDVoWHIJMd81nMDQLK-4CCR8-Tfe2HhFx9qGHONgkvTBMBdvnGvDrFii37Q6-bP0_D-JNFC6jFe_3_XbAtCQHa2BDtRZyxIBQAM7SRHlCPt6moNKaZCi1F50zsD1XRgI-tmuBeLEm5crrJ8L9tw1CSK0xJBo8Y38OOwqDyyhJ7KeuUM1R6F7tt1PNpjnCFNpoY1hKpzCKr7qD4yZ2LT0_V-7LYK2Wl2nCOncXFBlgGsl38XNjaVqsHS5AtFqapEtnsiPP5xDlanbaeJeloNsY0dz-o4ZIs8Q",
        "id": 34
    },
    {
        "domain": ".linkedin.com",
        "expirationDate": 1748910671.182951,
        "hostOnly": False,
        "httpOnly": False,
        "name": "VID",
        "path": "/",
        "sameSite": "unspecified",
        "secure": False,
        "session": False,
        "storeId": "0",
        "value": "V_2024_06_03_00_482696",
        "id": 35
    },
    {
        "domain": ".linkedin.com",
        "expirationDate": 1756495514.867733,
        "hostOnly": False,
        "httpOnly": False,
        "name": "visit",
        "path": "/",
        "sameSite": "no_restriction",
        "secure": True,
        "session": False,
        "storeId": "0",
        "value": "v=1&M",
        "id": 36
    },
    {
        "domain": ".www.linkedin.com",
        "expirationDate": 1753472431.425365,
        "hostOnly": False,
        "httpOnly": True,
        "name": "bscookie",
        "path": "/",
        "sameSite": "no_restriction",
        "secure": True,
        "session": False,
        "storeId": "0",
        "value": "\"v=1&2024053117094708519bbb-7e23-4576-834d-a28a573f99e6AQG1CG2AzY1pwcnNJSILbysndmGwGq3T\"",
        "id": 37
    },
    {
        "domain": ".www.linkedin.com",
        "expirationDate": 1729712430.424996,
        "hostOnly": False,
        "httpOnly": False,
        "name": "JSESSIONID",
        "path": "/",
        "sameSite": "no_restriction",
        "secure": True,
        "session": False,
        "storeId": "0",
        "value": "\"ajax:8784419394741201488\"",
        "id": 38
    },
    {
        "domain": ".www.linkedin.com",
        "expirationDate": 1753472430.424439,
        "hostOnly": False,
        "httpOnly": True,
        "name": "li_at",
        "path": "/",
        "sameSite": "no_restriction",
        "secure": True,
        "session": False,
        "storeId": "0",
        "value": "AQEDAS-OfNcBFQS-AAABkOtoxN4AAAGRD3VI3lYAK665JytsY__2iU9WLs1ps22eszffqI2Y-8ykfuegW1pHgOqQGPlzYJrza-9zrSdcaNxr1lfkbITY2zafTbK67UrUe4I-PMMiTWAa7NmlWz7fSCs_",
        "id": 39
    },
    {
        "domain": ".www.linkedin.com",
        "expirationDate": 1753472430.424439,
        "hostOnly": False,
        "httpOnly": True,
        "name": "li_rm",
        "path": "/",
        "sameSite": "no_restriction",
        "secure": True,
        "session": False,
        "storeId": "0",
        "value": "AQExa8tzoQq6GAAAAZDrWscYNjQh7AWiZsqdtwuXjAocW2xS-xwe1xNAlXecWQ42rGJIoxLf_Jl1l_oOxMH3LJInJDszDrPxlK0DwPmwaDOsypq1GRE6LtK9GqjuSgGAiNbfdToXIqPnD-in3VsRMdudhl8tbH1nYQiAOqyaciVpdqRtS3RT3eRGA2GzJDCZCkN1DXBgbKXQuZrZOUky79MgtZ2kUHptTF2Q2aYMnGQemh-tYvsZ0YvgD05XvdYbf3_TnB5wAyY3WBjMdV_qzBu21szB4Mdvw6joy53ZifM5frdWWOKytT8h2NoKyusYNrjZ5UsuNvm5ZvrKcPQ",
        "id": 40
    },
    {
        "domain": ".www.linkedin.com",
        "expirationDate": 1737523157,
        "hostOnly": False,
        "httpOnly": False,
        "name": "li_theme",
        "path": "/",
        "sameSite": "unspecified",
        "secure": True,
        "session": False,
        "storeId": "0",
        "value": "light",
        "id": 41
    },
    {
        "domain": ".www.linkedin.com",
        "expirationDate": 1737523157,
        "hostOnly": False,
        "httpOnly": False,
        "name": "li_theme_set",
        "path": "/",
        "sameSite": "unspecified",
        "secure": True,
        "session": False,
        "storeId": "0",
        "value": "app",
        "id": 42
    },
    {
        "domain": ".www.linkedin.com",
        "expirationDate": 1723177157,
        "hostOnly": False,
        "httpOnly": False,
        "name": "timezone",
        "path": "/",
        "sameSite": "unspecified",
        "secure": True,
        "session": False,
        "storeId": "0",
        "value": "America/Chicago",
        "id": 43
    },
    {
        "domain": "www.linkedin.com",
        "expirationDate": 1722540334.598891,
        "hostOnly": True,
        "httpOnly": False,
        "name": "fcookie",
        "path": "/",
        "sameSite": "no_restriction",
        "secure": True,
        "session": False,
        "storeId": "0",
        "value": "AQGLLQdk16ku7gAAAZDrWxn8f-APQFT6PAUa0s5eIu0TXx81E32_QpYmSqd_y87SyvShfrEvBOv1pwX7SUfIwr5zTCf5F0QPZQ_j-xSYjSDaccQvRoIsKFIkYr_en6ohLcQVANdeA0sSZM8mJiWIX8_pS9v9eOEoRv4YCVS10hwLuujcW6Z1Qb932SMwe7VKe24vQV5X2KbM0IPwVwYXkrEmRfJXKh7qN8jPPip3HWaovOsibgY-DtEDiwIrKJpEImL9ymUcj/05hoM5mAZKeE4v4ZZavtgK1BKylPWf9DU1tjY/RYn8105bIpknGiishvBqV5l7zReF0Ctg==",
        "id": 44
    },
    {
        "domain": "www.linkedin.com",
        "expirationDate": 1722540319.439539,
        "hostOnly": True,
        "httpOnly": False,
        "name": "fid",
        "path": "/",
        "sameSite": "unspecified",
        "secure": False,
        "session": False,
        "storeId": "0",
        "value": "AQGGPYDb5MdNFgAAAZDrWt5lkGKk3sg5tjo166rHRMNDl5150mrFxWrnAn12CKXaG1pONnzlqmEXDQ",
        "id": 45
    },
    {
        "domain": "www.linkedin.com",
        "expirationDate": 1737487518,
        "hostOnly": True,
        "httpOnly": False,
        "name": "g_state",
        "path": "/",
        "sameSite": "unspecified",
        "secure": False,
        "session": False,
        "storeId": "0",
        "value": "{\"i_l\":1,\"i_p\":1721942718559}",
        "id": 46
    },
    {
        "domain": "www.linkedin.com",
        "expirationDate": 1753473083,
        "hostOnly": True,
        "httpOnly": False,
        "name": "li_alerts",
        "path": "/",
        "sameSite": "no_restriction",
        "secure": True,
        "session": False,
        "storeId": "0",
        "value": "e30=",
        "id": 47
    },
    {
        "domain": "www.linkedin.com",
        "hostOnly": True,
        "httpOnly": True,
        "name": "PLAY_SESSION",
        "path": "/",
        "sameSite": "lax",
        "secure": True,
        "session": True,
        "storeId": "0",
        "value": "eyJhbGciOiJIUzI1NiJ9.eyJkYXRhIjp7ImZsb3dUcmFja2luZ0lkIjoiWVo3dlNvclJROSsrQVpBVm85dFZiQT09In0sIm5iZiI6MTcyMTMzMDUzMywiaWF0IjoxNzIxMzMwNTMzfQ.zNL5adObPOv9hG9izSGwnYppym7E9s9WSjA8p3284UA",
        "id": 48
    }
]
    }


    # Run the Actor and wait for it to finish
    run = client.actor("PEgClm7RgRD7YO94b").call(run_input=run_input)

    profile_info = []
    # Fetch and print Actor results from the run's dataset (if there are any)
    for item in client.dataset(run["defaultDatasetId"]).iterate_items():
        profile_info.append(item)
    
    try:
        # Assume profile_info contains JSON serializable items
        update_json(slug, profile_info)
        return profile_info
    except Exception as e:
        print(f"Error processing profile info for {slug}: {str(e)}")
        return None
    

# Function to update the JSON file
def update_json(slug, profile_info):
    try:
        # Read existing results.json or create new if not exists
        if os.path.exists('results.json') and os.stat('results.json').st_size > 0:
            with open('results.json', 'r', encoding='utf-8') as json_file:
                result_dict = json.load(json_file)
        else:
            result_dict = {}

        result_dict[slug] = profile_info

        with open('results.json', 'w', encoding='utf-8') as json_file:
            json.dump(result_dict, json_file, ensure_ascii=False, indent=2)

    except Exception as e:
        print(f"Error updating results.json for {slug}: {str(e)}")

# Read the CSV file with profile slugs
csv_file = 'extract.csv'
failed_rows = []

try:
    with open('failed_rows.txt', 'r', encoding='utf-8') as failed_file:
        failed_rows = [int(line.strip()) for line in failed_file]
except FileNotFoundError:
    pass

with open(csv_file, mode='r', encoding='utf-8') as file:
    csv_reader = csv.reader(file)
    header = next(csv_reader)  # Save the header
    rows = list(csv_reader)   # Save the rows

# Progress bar for processing rows
with ThreadPoolExecutor(max_workers=1) as executor:
    for i, row in tqdm(enumerate(rows, start=1), total=len(rows), desc="Processing Rows", unit="row"):
        if not row or len(row) < 1:
            # Skip empty rows or rows with insufficient data
            continue
        
        slug = row[0]

        # Check if the slug already exists in the JSON
        try:
            if os.path.exists('results.json') and os.stat('results.json').st_size > 0:
                with open('results.json', 'r', encoding='utf-8') as json_file:
                    result_dict = json.load(json_file)
            else:
                result_dict = {}

            if slug not in failed_rows:
                # Before making the API request, check if it has not already been sent
                if slug not in result_dict:
                    profile_info = executor.submit(get_profile_info, slug).result()
                    if profile_info:
                        # No need to add to the dictionary here, as it is handled by the get_profile_info function
                        pass
                    else:
                        failed_rows.append(i)

        except Exception as e:
            print(f"Error processing slug {slug}: {str(e)}")
            failed_rows.append(i)

# Save the list of failed rows for the next run
with open('failed_rows.txt', 'w', encoding='utf-8') as file:
    file.write('\n'.join(map(str, failed_rows)))

print(colored("Script execution completed successfully.", "green"))
