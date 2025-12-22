"""
RSS News Fetcher - Бесплатные RSS-фиды со всего мира.
Безлимитный источник новостей без API ключей.
"""

import random
import feedparser
import httpx
from datetime import datetime, timedelta
from typing import Optional, List
from country_data import get_country_data

# Глобальные RSS-фиды со всего мира - МАКСИМАЛЬНАЯ КОЛЛЕКЦИЯ
# Новости, технологии, наука, спорт, развлечения, AI, крипто и многое другое!
RSS_FEEDS = {
    # ========== США ==========
    "us": [
        # Новости
        ("https://rss.nytimes.com/services/xml/rss/nyt/World.xml", "New York Times", "en"),
        ("https://rss.nytimes.com/services/xml/rss/nyt/Technology.xml", "NYT Tech", "en"),
        ("https://rss.nytimes.com/services/xml/rss/nyt/Science.xml", "NYT Science", "en"),
        ("https://feeds.washingtonpost.com/rss/world", "Washington Post", "en"),
        ("https://feeds.npr.org/1004/rss.xml", "NPR World", "en"),
        ("https://rss.cnn.com/rss/edition_world.rss", "CNN", "en"),
        ("https://feeds.bbci.co.uk/news/world/rss.xml", "BBC World", "en"),
        ("https://abcnews.go.com/abcnews/topstories", "ABC News", "en"),
        ("https://feeds.foxnews.com/foxnews/latest", "Fox News", "en"),
        ("https://feeds.nbcnews.com/nbcnews/public/news", "NBC News", "en"),
        # Reddit - главные сабреддиты
        ("https://www.reddit.com/r/worldnews/.rss", "Reddit WorldNews", "en"),
        ("https://www.reddit.com/r/news/.rss", "Reddit News", "en"),
        ("https://www.reddit.com/r/technology/.rss", "Reddit Technology", "en"),
        ("https://www.reddit.com/r/science/.rss", "Reddit Science", "en"),
        ("https://www.reddit.com/r/programming/.rss", "Reddit Programming", "en"),
        ("https://www.reddit.com/r/MachineLearning/.rss", "Reddit ML", "en"),
        ("https://www.reddit.com/r/artificial/.rss", "Reddit AI", "en"),
        ("https://www.reddit.com/r/gaming/.rss", "Reddit Gaming", "en"),
        ("https://www.reddit.com/r/movies/.rss", "Reddit Movies", "en"),
        ("https://www.reddit.com/r/music/.rss", "Reddit Music", "en"),
        ("https://www.reddit.com/r/sports/.rss", "Reddit Sports", "en"),
        ("https://www.reddit.com/r/space/.rss", "Reddit Space", "en"),
        ("https://www.reddit.com/r/Futurology/.rss", "Reddit Futurology", "en"),
        ("https://www.reddit.com/r/CryptoCurrency/.rss", "Reddit Crypto", "en"),
        ("https://www.reddit.com/r/wallstreetbets/.rss", "Reddit WSB", "en"),
        ("https://www.reddit.com/r/UpliftingNews/.rss", "Reddit Uplifting", "en"),
        # Технологии
        ("https://techcrunch.com/feed/", "TechCrunch", "en"),
        ("https://www.theverge.com/rss/index.xml", "The Verge", "en"),
        ("https://feeds.arstechnica.com/arstechnica/index", "Ars Technica", "en"),
        ("https://www.wired.com/feed/rss", "Wired", "en"),
        ("https://www.engadget.com/rss.xml", "Engadget", "en"),
        ("https://mashable.com/feeds/rss/all", "Mashable", "en"),
        ("https://gizmodo.com/rss", "Gizmodo", "en"),
        ("https://lifehacker.com/rss", "Lifehacker", "en"),
        ("https://www.cnet.com/rss/news/", "CNET", "en"),
        ("https://www.zdnet.com/news/rss.xml", "ZDNet", "en"),
        ("https://venturebeat.com/feed/", "VentureBeat", "en"),
        ("https://thenextweb.com/feed", "The Next Web", "en"),
        # AI и ML
        ("https://huggingface.co/blog/feed.xml", "Hugging Face Blog", "en"),
        ("https://openai.com/blog/rss/", "OpenAI Blog", "en"),
        ("https://blog.google/technology/ai/rss/", "Google AI Blog", "en"),
        ("https://ai.meta.com/blog/rss/", "Meta AI", "en"),
        ("https://blogs.nvidia.com/feed/", "NVIDIA Blog", "en"),
        ("https://www.deepmind.com/blog/rss.xml", "DeepMind", "en"),
        ("https://syncedreview.com/feed/", "Synced AI", "en"),
        ("https://www.marktechpost.com/feed/", "MarkTechPost AI", "en"),
        # Наука
        ("https://www.sciencedaily.com/rss/all.xml", "Science Daily", "en"),
        ("https://www.nature.com/nature.rss", "Nature", "en"),
        ("https://www.newscientist.com/feed/home/", "New Scientist", "en"),
        ("https://phys.org/rss-feed/", "Phys.org", "en"),
        ("https://www.space.com/feeds/all", "Space.com", "en"),
        ("https://www.nasa.gov/rss/dyn/breaking_news.rss", "NASA", "en"),
        ("https://www.scientificamerican.com/feed/", "Scientific American", "en"),
        # Бизнес и Финансы
        ("https://feeds.bloomberg.com/markets/news.rss", "Bloomberg", "en"),
        ("https://www.ft.com/rss/home", "Financial Times", "en"),
        ("https://feeds.content.dowjones.io/public/rss/mw_topstories", "MarketWatch", "en"),
        ("https://www.cnbc.com/id/100003114/device/rss/rss.html", "CNBC", "en"),
        ("https://fortune.com/feed/", "Fortune", "en"),
        ("https://www.forbes.com/innovation/feed/", "Forbes", "en"),
        # Крипто
        ("https://cointelegraph.com/rss", "Cointelegraph", "en"),
        ("https://www.coindesk.com/arc/outboundfeeds/rss/", "CoinDesk", "en"),
        ("https://decrypt.co/feed", "Decrypt", "en"),
        ("https://bitcoinmagazine.com/feed", "Bitcoin Magazine", "en"),
        # Игры
        ("https://www.ign.com/rss/articles", "IGN", "en"),
        ("https://www.gamespot.com/feeds/mashup/", "GameSpot", "en"),
        ("https://kotaku.com/rss", "Kotaku", "en"),
        ("https://www.polygon.com/rss/index.xml", "Polygon", "en"),
        # Развлечения
        ("https://variety.com/feed/", "Variety", "en"),
        ("https://www.hollywoodreporter.com/feed/", "Hollywood Reporter", "en"),
        ("https://deadline.com/feed/", "Deadline", "en"),
        ("https://ew.com/feed/", "Entertainment Weekly", "en"),
        # Спорт
        ("https://www.espn.com/espn/rss/news", "ESPN", "en"),
        ("https://rss.nytimes.com/services/xml/rss/nyt/Sports.xml", "NYT Sports", "en"),
    ],
    
    # ========== Великобритания ==========
    "gb": [
        ("https://feeds.bbci.co.uk/news/rss.xml", "BBC News", "en"),
        ("https://feeds.bbci.co.uk/news/technology/rss.xml", "BBC Tech", "en"),
        ("https://feeds.bbci.co.uk/sport/rss.xml", "BBC Sport", "en"),
        ("https://www.theguardian.com/world/rss", "The Guardian World", "en"),
        ("https://www.theguardian.com/uk/technology/rss", "Guardian Tech", "en"),
        ("https://www.theguardian.com/science/rss", "Guardian Science", "en"),
        ("https://www.independent.co.uk/news/world/rss", "The Independent", "en"),
        ("https://www.telegraph.co.uk/rss.xml", "The Telegraph", "en"),
        ("https://www.theregister.com/headlines.atom", "The Register", "en"),
        ("https://www.reddit.com/r/unitedkingdom/.rss", "Reddit UK", "en"),
    ],
    
    # ========== Германия ==========
    "de": [
        ("https://www.tagesschau.de/xml/rss2/", "Tagesschau", "de"),
        ("https://rss.sueddeutsche.de/rss/Topthemen", "Süddeutsche", "de"),
        ("https://www.spiegel.de/schlagzeilen/index.rss", "Der Spiegel", "de"),
        ("https://www.faz.net/rss/aktuell/", "FAZ", "de"),
        ("https://www.zeit.de/index", "Die Zeit", "de"),
        ("https://www.heise.de/rss/heise.rdf", "Heise", "de"),
        ("https://www.golem.de/rss.php?feed=ATOM1.0", "Golem.de", "de"),
        ("https://t3n.de/rss.xml", "t3n", "de"),
        ("https://www.reddit.com/r/de/.rss", "Reddit Germany", "de"),
    ],
    
    # ========== Франция ==========
    "fr": [
        ("https://www.lemonde.fr/rss/une.xml", "Le Monde", "fr"),
        ("https://www.lefigaro.fr/rss/figaro_actualites.xml", "Le Figaro", "fr"),
        ("https://www.france24.com/fr/rss", "France 24", "fr"),
        ("https://www.liberation.fr/rss/", "Libération", "fr"),
        ("https://www.20minutes.fr/feeds/rss-une.xml", "20 Minutes", "fr"),
        ("https://www.numerama.com/feed/", "Numerama", "fr"),
        ("https://www.frandroid.com/feed", "Frandroid", "fr"),
        ("https://www.reddit.com/r/france/.rss", "Reddit France", "fr"),
    ],
    
    # ========== Испания ==========
    "es": [
        ("https://feeds.elpais.com/mrss-s/pages/ep/site/elpais.com/portada", "El País", "es"),
        ("https://e00-elmundo.uecdn.es/elmundo/rss/portada.xml", "El Mundo", "es"),
        ("https://www.abc.es/rss/feeds/abc_ultima.xml", "ABC", "es"),
        ("https://www.lavanguardia.com/rss/home.xml", "La Vanguardia", "es"),
        ("https://www.xataka.com/index.xml", "Xataka", "es"),
        ("https://www.genbeta.com/index.xml", "Genbeta", "es"),
        ("https://www.reddit.com/r/spain/.rss", "Reddit Spain", "es"),
    ],
    
    # ========== Италия ==========
    "it": [
        ("https://www.repubblica.it/rss/homepage/rss2.0.xml", "La Repubblica", "it"),
        ("https://xml2.corriereobjects.it/rss/homepage.xml", "Corriere della Sera", "it"),
        ("https://www.ansa.it/sito/ansait_rss.xml", "ANSA", "it"),
        ("https://www.ilsole24ore.com/rss/mondo.xml", "Il Sole 24 Ore", "it"),
        ("https://www.tomshw.it/feed/", "Tom's Hardware IT", "it"),
        ("https://www.reddit.com/r/italy/.rss", "Reddit Italy", "it"),
    ],
    
    # ========== Нидерланды ==========
    "nl": [
        ("https://feeds.nos.nl/nosnieuwsalgemeen", "NOS Nieuws", "nl"),
        ("https://www.nu.nl/rss/Algemeen", "NU.nl", "nl"),
        ("https://www.rtlnieuws.nl/rss.xml", "RTL Nieuws", "nl"),
        ("https://tweakers.net/feeds/mixed.xml", "Tweakers", "nl"),
        ("https://www.reddit.com/r/thenetherlands/.rss", "Reddit NL", "nl"),
    ],
    
    # ========== Япония ==========
    "jp": [
        ("https://www3.nhk.or.jp/rss/news/cat0.xml", "NHK News", "ja"),
        ("https://assets.wor.jp/rss/rdf/yomiuri/world.rdf", "Yomiuri", "ja"),
        ("https://www.asahi.com/rss/asahi/newsheadlines.rdf", "Asahi", "ja"),
        ("https://gigazine.net/news/rss_2.0/", "GIGAZINE", "ja"),
        ("https://jp.techcrunch.com/feed/", "TechCrunch Japan", "ja"),
        ("https://www.reddit.com/r/japan/.rss", "Reddit Japan", "en"),
    ],
    
    # ========== Китай ==========
    "cn": [
        ("http://www.chinadaily.com.cn/rss/world_rss.xml", "China Daily", "en"),
        ("https://www.scmp.com/rss/91/feed", "South China Morning Post", "en"),
        ("https://www.globaltimes.cn/rss/outbrain.xml", "Global Times", "en"),
        ("https://www.reddit.com/r/China/.rss", "Reddit China", "en"),
    ],
    
    # ========== Южная Корея ==========
    "kr": [
        ("https://www.koreaherald.com/rss/020100000000.xml", "Korea Herald", "en"),
        ("https://en.yna.co.kr/RSS/news.xml", "Yonhap News", "en"),
        ("https://www.koreatimes.co.kr/www/rss/rss.xml", "Korea Times", "en"),
        ("https://www.reddit.com/r/korea/.rss", "Reddit Korea", "en"),
    ],
    
    # ========== Индия ==========
    "in": [
        ("https://timesofindia.indiatimes.com/rssfeeds/296589292.cms", "Times of India", "en"),
        ("https://www.thehindu.com/news/feeder/default.rss", "The Hindu", "en"),
        ("https://indianexpress.com/feed/", "Indian Express", "en"),
        ("https://www.ndtv.com/rss/top-stories", "NDTV", "en"),
        ("https://www.reddit.com/r/india/.rss", "Reddit India", "en"),
    ],
    
    # ========== Бразилия ==========
    "br": [
        ("https://g1.globo.com/rss/g1/", "G1 Globo", "pt"),
        ("https://www.uol.com.br/rss.xml", "UOL", "pt"),
        ("https://rss.tecmundo.com.br/feed", "TecMundo", "pt"),
        ("https://tecnoblog.net/feed/", "Tecnoblog", "pt"),
        ("https://www.reddit.com/r/brasil/.rss", "Reddit Brasil", "pt"),
    ],
    
    # ========== Россия ==========
    "ru": [
        ("https://tass.com/rss/v2.xml", "TASS", "en"),
        ("https://www.themoscowtimes.com/rss/news", "Moscow Times", "en"),
        ("https://meduza.io/rss/en/all", "Meduza", "en"),
        ("https://www.reddit.com/r/russia/.rss", "Reddit Russia", "en"),
    ],
    
    # ========== Мексика ==========
    "mx": [
        ("https://www.eluniversal.com.mx/rss.xml", "El Universal", "es"),
        ("https://www.milenio.com/rss", "Milenio", "es"),
        ("https://www.reddit.com/r/mexico/.rss", "Reddit Mexico", "es"),
    ],
    
    # ========== Аргентина ==========
    "ar": [
        ("https://www.lanacion.com.ar/arc/outboundfeeds/rss/", "La Nación", "es"),
        ("https://www.clarin.com/rss/lo-ultimo/", "Clarín", "es"),
        ("https://www.reddit.com/r/argentina/.rss", "Reddit Argentina", "es"),
    ],
    
    # ========== Австралия ==========
    "au": [
        ("https://www.abc.net.au/news/feed/2942460/rss.xml", "ABC News AU", "en"),
        ("https://www.smh.com.au/rss/feed.xml", "Sydney Morning Herald", "en"),
        ("https://www.news.com.au/feed/", "News.com.au", "en"),
        ("https://www.reddit.com/r/australia/.rss", "Reddit Australia", "en"),
    ],
    
    # ========== Канада ==========
    "ca": [
        ("https://www.cbc.ca/cmlink/rss-world", "CBC News", "en"),
        ("https://globalnews.ca/feed/", "Global News", "en"),
        ("https://www.theglobeandmail.com/arc/outboundfeeds/rss/", "Globe and Mail", "en"),
        ("https://www.reddit.com/r/canada/.rss", "Reddit Canada", "en"),
    ],
    
    # ========== Турция ==========
    "tr": [
        ("https://www.dailysabah.com/rssFeed/getTRSS", "Daily Sabah", "en"),
        ("https://www.hurriyetdailynews.com/rss", "Hurriyet Daily", "en"),
        ("https://www.reddit.com/r/Turkey/.rss", "Reddit Turkey", "en"),
    ],
    
    # ========== ОАЭ / Ближний Восток ==========
    "ae": [
        ("https://www.aljazeera.com/xml/rss/all.xml", "Al Jazeera", "en"),
        ("https://gulfnews.com/rss", "Gulf News", "en"),
        ("https://www.khaleejtimes.com/rss", "Khaleej Times", "en"),
    ],
    
    # ========== Израиль ==========
    "il": [
        ("https://www.timesofisrael.com/feed/", "Times of Israel", "en"),
        ("https://www.jpost.com/rss/rssfeedsfrontpage.aspx", "Jerusalem Post", "en"),
        ("https://www.haaretz.com/srv/haaretzrss", "Haaretz", "en"),
        ("https://www.reddit.com/r/Israel/.rss", "Reddit Israel", "en"),
    ],
    
    # ========== Южная Африка ==========
    "za": [
        ("https://www.news24.com/news24/TopStories/rss", "News24", "en"),
        ("https://www.iol.co.za/cmlink/1.640", "IOL News", "en"),
        ("https://www.reddit.com/r/southafrica/.rss", "Reddit SA", "en"),
    ],
    
    # ========== Польша ==========
    "pl": [
        ("https://tvn24.pl/najnowsze.xml", "TVN24", "pl"),
        ("https://www.polsatnews.pl/rss/wszystkie.xml", "Polsat News", "pl"),
        ("https://www.reddit.com/r/Polska/.rss", "Reddit Poland", "pl"),
    ],
    
    # ========== Швеция ==========
    "se": [
        ("https://www.svt.se/nyheter/rss.xml", "SVT Nyheter", "sv"),
        ("https://rss.aftonbladet.se/rss2/small/pages/sections/senastenytt/", "Aftonbladet", "sv"),
        ("https://www.reddit.com/r/sweden/.rss", "Reddit Sweden", "sv"),
    ],
    
    # ========== Норвегия ==========
    "no": [
        ("https://www.nrk.no/toppsaker.rss", "NRK", "no"),
        ("https://www.vg.no/rss/feed/", "VG", "no"),
        ("https://www.reddit.com/r/norway/.rss", "Reddit Norway", "en"),
    ],
    
    # ========== Финляндия ==========
    "fi": [
        ("https://feeds.yle.fi/uutiset/v1/recent.rss?publisherIds=YLE_UUTISET", "YLE News", "fi"),
        ("https://www.reddit.com/r/Finland/.rss", "Reddit Finland", "en"),
    ],
    
    # ========== Чехия ==========
    "cz": [
        ("https://ct24.ceskatelevize.cz/rss/hlavni-zpravy", "ČT24", "cs"),
        ("https://www.reddit.com/r/czech/.rss", "Reddit Czech", "en"),
    ],
    
    # ========== Греция ==========
    "gr": [
        ("https://www.kathimerini.gr/rss", "Kathimerini", "el"),
        ("https://www.reddit.com/r/greece/.rss", "Reddit Greece", "en"),
    ],
    
    # ========== Португалия ==========
    "pt": [
        ("https://feeds.publico.pt/PublicoRSS", "Público", "pt"),
        ("https://www.reddit.com/r/portugal/.rss", "Reddit Portugal", "pt"),
    ],
    
    # ========== Швейцария ==========
    "ch": [
        ("https://www.swissinfo.ch/eng/rss", "SWI swissinfo", "en"),
        ("https://www.20min.ch/rss/rss.tmpl?type=channel&get=1", "20 Minuten", "de"),
        ("https://www.reddit.com/r/Switzerland/.rss", "Reddit Switzerland", "en"),
    ],
    
    # ========== Австрия ==========
    "at": [
        ("https://www.derstandard.at/rss", "Der Standard", "de"),
        ("https://www.reddit.com/r/Austria/.rss", "Reddit Austria", "de"),
    ],
    
    # ========== Бельгия ==========
    "be": [
        ("https://www.rtbf.be/rss/info", "RTBF", "fr"),
        ("https://www.reddit.com/r/belgium/.rss", "Reddit Belgium", "en"),
    ],
    
    # ========== Сингапур ==========
    "sg": [
        ("https://www.straitstimes.com/news/asia/rss.xml", "Straits Times", "en"),
        ("https://www.channelnewsasia.com/rss/latest_cna_frontpage_rss.xml", "CNA", "en"),
        ("https://www.reddit.com/r/singapore/.rss", "Reddit Singapore", "en"),
    ],
    
    # ========== Малайзия ==========
    "my": [
        ("https://www.thestar.com.my/rss/News", "The Star", "en"),
        ("https://www.reddit.com/r/malaysia/.rss", "Reddit Malaysia", "en"),
    ],
    
    # ========== Индонезия ==========
    "id": [
        ("https://www.thejakartapost.com/rss", "Jakarta Post", "en"),
        ("https://www.reddit.com/r/indonesia/.rss", "Reddit Indonesia", "en"),
    ],
    
    # ========== Таиланд ==========
    "th": [
        ("https://www.bangkokpost.com/rss/data/most-recent.xml", "Bangkok Post", "en"),
        ("https://www.reddit.com/r/Thailand/.rss", "Reddit Thailand", "en"),
    ],
    
    # ========== Филиппины ==========
    "ph": [
        ("https://www.inquirer.net/fullfeed", "Inquirer", "en"),
        ("https://www.reddit.com/r/Philippines/.rss", "Reddit Philippines", "en"),
    ],
    
    # ========== Вьетнам ==========
    "vn": [
        ("https://e.vnexpress.net/rss/news.rss", "VnExpress", "en"),
        ("https://www.reddit.com/r/VietNam/.rss", "Reddit Vietnam", "en"),
    ],
    
    # ========== Египет ==========
    "eg": [
        ("https://english.ahram.org.eg/rss.aspx", "Ahram Online", "en"),
    ],
    
    # ========== Нигерия ==========
    "ng": [
        ("https://punchng.com/feed/", "Punch Nigeria", "en"),
        ("https://www.reddit.com/r/Nigeria/.rss", "Reddit Nigeria", "en"),
    ],
    
    # ========== Кения ==========
    "ke": [
        ("https://nation.africa/kenya/rss.xml", "Daily Nation", "en"),
    ],
    
    # ========== Украина ==========
    "ua": [
        ("https://www.kyivpost.com/feed", "Kyiv Post", "en"),
        ("https://www.reddit.com/r/ukraine/.rss", "Reddit Ukraine", "en"),
    ],
    
    # ========== Дания ==========
    "dk": [
        ("https://www.dr.dk/nyheder/service/feeds/allenyheder", "DR News", "da"),
        ("https://www.reddit.com/r/Denmark/.rss", "Reddit Denmark", "en"),
    ],
    
    # ========== Ирландия ==========
    "ie": [
        ("https://www.irishtimes.com/cmlink/news-1.1319192", "Irish Times", "en"),
        ("https://www.reddit.com/r/ireland/.rss", "Reddit Ireland", "en"),
    ],
    
    # ========== Новая Зеландия ==========
    "nz": [
        ("https://www.rnz.co.nz/rss/national.xml", "RNZ", "en"),
        ("https://www.reddit.com/r/newzealand/.rss", "Reddit NZ", "en"),
    ],
    
    # ========== Венгрия ==========
    "hu": [
        ("https://index.hu/24ora/rss/", "Index.hu", "hu"),
        ("https://www.reddit.com/r/hungary/.rss", "Reddit Hungary", "en"),
    ],
    
    # ========== Румыния ==========
    "ro": [
        ("https://www.digi24.ro/rss", "Digi24", "ro"),
        ("https://www.reddit.com/r/Romania/.rss", "Reddit Romania", "en"),
    ],
    
    # ========== Хорватия ==========
    "hr": [
        ("https://www.jutarnji.hr/rss/", "Jutarnji", "hr"),
        ("https://www.reddit.com/r/croatia/.rss", "Reddit Croatia", "en"),
    ],
    
    # ========== Словения ==========
    "si": [
        ("https://www.rtvslo.si/rss", "RTV Slovenija", "sl"),
    ],
    
    # ========== Словакия ==========
    "sk": [
        ("https://www.sme.sk/rss", "SME", "sk"),
    ],
    
    # ========== Болгария ==========
    "bg": [
        ("https://www.novinite.com/rss.php", "Novinite", "en"),
    ],
    
    # ========== Сербия ==========
    "rs": [
        ("https://www.blic.rs/rss", "Blic", "sr"),
    ],
    
    # ========== Колумбия ==========
    "co": [
        ("https://www.eltiempo.com/rss/portada.xml", "El Tiempo", "es"),
        ("https://www.reddit.com/r/Colombia/.rss", "Reddit Colombia", "es"),
    ],
    
    # ========== Чили ==========
    "cl": [
        ("https://www.emol.com/rss/rss.asp", "Emol", "es"),
        ("https://www.reddit.com/r/chile/.rss", "Reddit Chile", "es"),
    ],
    
    # ========== Перу ==========
    "pe": [
        ("https://elcomercio.pe/arcio/rss/", "El Comercio Peru", "es"),
    ],
    
    # ========== Венесуэла ==========
    "ve": [
        ("https://www.eluniversal.com/rss.xml", "El Universal VE", "es"),
    ],
    
    # ========== Эквадор ==========
    "ec": [
        ("https://www.eluniverso.com/rss/todas/", "El Universo", "es"),
    ],
    
    # ========== Пакистан ==========
    "pk": [
        ("https://www.dawn.com/feeds/home", "Dawn", "en"),
        ("https://www.reddit.com/r/pakistan/.rss", "Reddit Pakistan", "en"),
    ],
    
    # ========== Бангладеш ==========
    "bd": [
        ("https://www.thedailystar.net/frontpage/rss.xml", "Daily Star BD", "en"),
    ],
    
    # ========== Иран ==========
    "ir": [
        ("https://en.irna.ir/rss.aspx", "IRNA", "en"),
    ],
    
    # ========== Саудовская Аравия ==========
    "sa": [
        ("https://www.arabnews.com/rss.xml", "Arab News", "en"),
    ],
    
    # ========== Катар ==========
    "qa": [
        ("https://www.aljazeera.com/xml/rss/all.xml", "Al Jazeera", "en"),
    ],
    
    # ========== Марокко ==========
    "ma": [
        ("https://www.moroccoworldnews.com/feed/", "Morocco World News", "en"),
    ],
    
    # ========== Тунис ==========
    "tn": [
        ("https://www.tunisienumerique.com/feed/", "Tunisie Numerique", "fr"),
    ],
    
    # ========== Алжир ==========
    "dz": [
        ("https://www.algerie360.com/feed/", "Algerie360", "fr"),
    ],
    
    # ========== Гана ==========
    "gh": [
        ("https://www.myjoyonline.com/feed/", "Joy Online", "en"),
    ],
    
    # ========== Эфиопия ==========
    "et": [
        ("https://addisstandard.com/feed/", "Addis Standard", "en"),
    ],
    
    # ========== Танзания ==========
    "tz": [
        ("https://www.thecitizen.co.tz/feed", "The Citizen TZ", "en"),
    ],
}


class RSSFetcher:
    """Фетчер новостей из RSS-фидов."""
    
    def __init__(self):
        self.client = httpx.AsyncClient(timeout=10.0, follow_redirects=True)
    
    async def fetch_random_news(self) -> Optional[dict]:
        """Получить случайную новость из RSS."""
        # Случайная страна
        country = random.choice(list(RSS_FEEDS.keys()))
        feeds = RSS_FEEDS[country]
        
        # Перемешиваем фиды
        random.shuffle(feeds)
        
        for feed_url, source_name, lang in feeds:
            try:
                result = await self._fetch_from_feed(feed_url, source_name, lang, country)
                if result:
                    return result
            except Exception as e:
                print(f"RSS error ({source_name}): {e}")
                continue
        
        return None
    
    async def _fetch_from_feed(self, url: str, source: str, lang: str, country: str) -> Optional[dict]:
        """Получить новость из конкретного RSS-фида."""
        try:
            # Загружаем RSS
            response = await self.client.get(url, headers={
                "User-Agent": "Mozilla/5.0 (compatible; RandomWorldNews/1.0)"
            })
            response.raise_for_status()
            
            # Парсим RSS
            feed = feedparser.parse(response.text)
            entries = feed.entries
            
            if not entries:
                return None
            
            # Фильтруем по дате (за последние 2 дня)
            two_days_ago = datetime.now() - timedelta(days=2)
            fresh_entries = []
            
            for entry in entries:
                pub_date = None
                if hasattr(entry, 'published_parsed') and entry.published_parsed:
                    pub_date = datetime(*entry.published_parsed[:6])
                elif hasattr(entry, 'updated_parsed') and entry.updated_parsed:
                    pub_date = datetime(*entry.updated_parsed[:6])
                
                if pub_date is None or pub_date > two_days_ago:
                    fresh_entries.append(entry)
            
            if not fresh_entries:
                fresh_entries = entries[:10]  # fallback
            
            # Фильтруем качество контента (отсеиваем мусор)
            quality_entries = []
            for entry in fresh_entries:
                if self._is_quality_entry(entry):
                    quality_entries.append(entry)
            
            if not quality_entries:
                quality_entries = fresh_entries[:5]  # fallback
            
            # Случайная статья
            entry = random.choice(quality_entries)
            
            # Извлекаем данные
            title = entry.get('title', '').strip()
            description = entry.get('summary', '') or entry.get('description', '')
            
            # Убираем HTML теги из description
            import re
            import html
            description = re.sub(r'<[^>]+>', '', description)
            
            # Декодируем HTML-сущности (&#32; -> пробел и т.д.)
            description = html.unescape(description)
            
            # Убираем Reddit-специфичный мусор
            description = re.sub(r'submitted by\s*/u/\w+', '', description, flags=re.IGNORECASE)
            description = re.sub(r'/u/\w+', '', description)
            description = re.sub(r'\[link\]', '', description, flags=re.IGNORECASE)
            description = re.sub(r'\[comments\]', '', description, flags=re.IGNORECASE)
            description = re.sub(r'\[комментарии\]', '', description, flags=re.IGNORECASE)
            description = re.sub(r'\[ссылка\]', '', description, flags=re.IGNORECASE)
            description = re.sub(r'представлено\s*', '', description, flags=re.IGNORECASE)
            
            # Убираем множественные пробелы и trim
            description = re.sub(r'\s+', ' ', description).strip()
            
            # Если описание слишком короткое или мусорное, используем title
            if len(description) < 50 or description.count('[') > 2:
                description = f"{title}. Читайте подробности по ссылке."
            elif len(description) > 800:
                description = description[:797] + "..."
            
            url = entry.get('link', '')
            
            # Изображение
            image = ''
            if hasattr(entry, 'media_content') and entry.media_content:
                image = entry.media_content[0].get('url', '')
            elif hasattr(entry, 'media_thumbnail') and entry.media_thumbnail:
                image = entry.media_thumbnail[0].get('url', '')
            elif hasattr(entry, 'enclosures') and entry.enclosures:
                for enc in entry.enclosures:
                    if enc.get('type', '').startswith('image'):
                        image = enc.get('href', '')
                        break
            
            # Дата публикации
            pub_date_str = ''
            if hasattr(entry, 'published'):
                pub_date_str = entry.published
            elif hasattr(entry, 'updated'):
                pub_date_str = entry.updated
            
            return {
                "title": title,
                "description": description,
                "url": url,
                "image": image,
                "source": source,
                "published_at": pub_date_str,
                "country": get_country_data(country),
                "language": lang,
                "api_source": "rss"
            }
            
        except Exception as e:
            print(f"RSS fetch error: {e}")
            return None
    
    def _is_quality_entry(self, entry) -> bool:
        """Проверить качество записи RSS."""
        title = entry.get('title', '')
        description = entry.get('summary', '') or entry.get('description', '')
        
        # Убираем HTML для анализа
        import re
        description = re.sub(r'<[^>]+>', '', description)
        
        # Отсеиваем если заголовок слишком короткий
        if len(title) < 10:
            return False
        
        # Отсеиваем если похоже на список заголовков (много двоеточий или переносов)
        if description.count(':') > 3:
            return False
        if description.count('\n') > 2:
            return False
        if description.count('...') > 2:
            return False
        
        # Отсеиваем если в title есть типичные признаки агрегатора
        bad_patterns = ['LIVE:', 'BREAKING:', 'WATCH:', 'VIDEO:', 'Podcast:', 'Newsletter']
        for pattern in bad_patterns:
            if pattern in title:
                return False
        
        # Отсеиваем очень длинный заголовок (возможно это несколько заголовков)
        if len(title) > 200:
            return False
            
        return True
    
    async def close(self):
        await self.client.aclose()


# Singleton
_rss_fetcher = None


def get_rss_fetcher() -> RSSFetcher:
    global _rss_fetcher
    if _rss_fetcher is None:
        _rss_fetcher = RSSFetcher()
    return _rss_fetcher
