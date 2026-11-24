"""
Management command: python manage.py populate_data
Populates every module with rich sample content.
All content is clearly marked as demonstration/educational material.
"""
from django.core.management.base import BaseCommand
from django.utils import timezone
from django.utils.text import slugify
from datetime import date, timedelta
import random


class Command(BaseCommand):
    help = 'Populate PolarConnect with comprehensive sample data across all modules'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('=== PolarConnect Data Population ===\n'))
        self._create_users()
        self._create_news_categories()
        self._create_news_articles()
        self._create_events()
        self._create_research()
        self._create_repository()
        self._create_learning_modules()
        self._create_quizzes()
        self._create_expeditions()
        self._create_media()
        self._create_stations()
        self._create_community()
        self.stdout.write(self.style.SUCCESS('\n✓ All sample data created successfully!'))
        self.stdout.write('  Visit http://127.0.0.1:8000/ to see the populated site.\n')

    # ------------------------------------------------------------------ users
    def _create_users(self):
        from accounts.models import CustomUser, Notification
        users_data = [
            dict(username='dr_sharma',    email='sharma@ncpor.res.in',    full_name='Dr. Priya Sharma',
                 institution='National Centre for Polar and Ocean Research',
                 designation='Senior Research Scientist', user_category='scientific_professional',
                 role='researcher', password='PolarUser@2024'),
            dict(username='prof_kumar',   email='kumar@iitd.ac.in',       full_name='Prof. Rajesh Kumar',
                 institution='Indian Institute of Technology, Delhi',
                 designation='Professor of Glaciology', user_category='researcher',
                 role='researcher', password='PolarUser@2024'),
            dict(username='ananya_edu',   email='ananya@polarlearn.in',   full_name='Ananya Singh',
                 institution='Kendriya Vidyalaya, New Delhi',
                 designation='Science Teacher', user_category='educator',
                 role='educator', password='PolarUser@2024'),
            dict(username='ravi_student', email='ravi@student.iitb.ac.in',full_name='Ravi Verma',
                 institution='IIT Bombay', designation='B.Tech Student',
                 user_category='student', role='student', password='PolarUser@2024'),
            dict(username='meera_pub',    email='meera@public.in',        full_name='Meera Nair',
                 institution='Citizen Scientist', designation='Science Enthusiast',
                 user_category='general_public', role='general_user', password='PolarUser@2024'),
            dict(username='content_mgr',  email='content@polarconnect.in', full_name='Content Manager',
                 institution='Ministry of Earth Sciences',
                 designation='Content Administrator', user_category='scientific_professional',
                 role='content_admin', password='PolarAdmin@2024'),
        ]
        created = 0
        for d in users_data:
            if not CustomUser.objects.filter(email=d['email']).exists():
                pw = d.pop('password')
                u = CustomUser(**d)
                u.set_password(pw)
                u.is_verified = True
                u.save()
                Notification.objects.create(
                    user=u, notification_type='general',
                    title='Welcome to PolarConnect!',
                    message=f'Hello {u.get_display_name()}, welcome to India\'s polar science portal.',
                    link='/dashboard/',
                )
                created += 1
        self.stdout.write(f'  ✓ Users: {created} created')

    # ------------------------------------------------------- news categories
    def _create_news_categories(self):
        from news.models import NewsCategory
        cats = [
            ('Research Announcement', 'research-announcement'),
            ('Expedition Update',     'expedition-update'),
            ('Climate Science',       'climate-science'),
            ('Policy & Governance',   'policy-governance'),
            ('Technology',            'technology'),
            ('Education',             'education-news'),
        ]
        for name, slug in cats:
            NewsCategory.objects.get_or_create(slug=slug, defaults={'name': name})
        self.stdout.write(f'  ✓ News categories: {len(cats)} ensured')

    # --------------------------------------------------------- news articles
    def _create_news_articles(self):
        from news.models import NewsArticle, NewsCategory
        from accounts.models import CustomUser
        author = CustomUser.objects.filter(role='content_admin').first() or \
                 CustomUser.objects.filter(is_staff=True).first()
        if not author:
            self.stdout.write('  ⚠ No author found for news articles')
            return

        articles = [
            dict(
                title='India Launches 43rd Antarctic Expedition with Record Team Size',
                slug='india-43rd-antarctic-expedition-2024',
                category_slug='expedition-update',
                summary='The Ministry of Earth Sciences has dispatched India\'s 43rd scientific expedition to Antarctica, carrying the largest team in recent years to conduct research at Maitri and Bharati stations.',
                content='''India's Ministry of Earth Sciences (MoES) has successfully launched the 43rd Indian Scientific Expedition to Antarctica (ISEA), marking another milestone in the country's decades-long commitment to polar research.

The expedition team comprises researchers from the National Centre for Polar and Ocean Research (NCPOR) and several premier Indian institutions including IITs, IISc and IISER. The team will conduct research across glaciology, oceanography, atmospheric science, geomagnetism and biological sciences.

**Research Priorities for This Expedition**

The 43rd expedition carries a focused scientific agenda:

- **Glaciological surveys** at both Maitri and Bharati stations, measuring ice mass balance and flow velocity
- **Atmospheric monitoring** including ozone depletion studies and greenhouse gas measurements
- **Marine biological surveys** in the Southern Ocean surrounding Antarctica
- **Geological sampling** from the Schirmacher Oasis region
- **Maintenance and upgradation** of scientific instruments at both stations

**India's Polar Research Legacy**

India has maintained an unbroken presence in Antarctica since its first expedition in 1981. The country currently operates two year-round stations — Maitri (since 1989) and Bharati (since 2012) — and also maintains the Himadri station in the Arctic at Ny-Ålesund, Svalbard.

This continuity of research has enabled India to contribute valuable long-term datasets to global climate science, particularly in areas such as atmospheric ozone monitoring, glacial retreat measurement and Southern Ocean circulation studies.

**[NOTE: This article contains demonstration content created for the PolarConnect portal. Specific numbers and personnel details are illustrative. Refer to official NCPOR communications for verified expedition information.]**''',
                is_featured=True,
                image_url='https://images.unsplash.com/photo-1517783999520-f068d7431a60?w=900&q=80',
            ),
            dict(
                title='New Study Shows Antarctic Ice Sheet Losing Mass Three Times Faster Than in 1990s',
                slug='antarctic-ice-loss-accelerating-2024',
                category_slug='climate-science',
                summary='An international research consortium has published findings showing that the Antarctic Ice Sheet is losing ice mass at an accelerating rate, with significant implications for global sea level projections.',
                content='''An international team of glaciologists has released a comprehensive assessment of Antarctic ice mass balance, revealing that the continent is losing ice at a rate approximately three times higher than observed in the 1990s.

The research, based on satellite altimetry, gravimetry and radar measurements spanning over three decades, provides the most detailed picture yet of ice dynamics across the continent.

**Key Findings**

The study identifies several concerning trends:

- **West Antarctic Ice Sheet (WAIS)**: Most vulnerable region, with the Thwaites and Pine Island glaciers accounting for a significant fraction of total mass loss
- **East Antarctic Ice Sheet (EAIS)**: Historically stable, but showing signs of increased melting in coastal regions
- **Antarctic Peninsula**: Continues to warm at nearly three times the global average rate; multiple ice shelves have collapsed since the 1990s

**Sea Level Implications**

The team's models suggest that if current trends continue, Antarctic ice loss alone could contribute between 17 and 40 centimetres of sea level rise by 2100. When combined with contributions from Greenland and thermal expansion of the oceans, total sea level rise could exceed one metre.

**India's Contribution to Antarctic Science**

Indian researchers at NCPOR have contributed mass balance data from both Maitri and Bharati stations to this international assessment. India's glaciological instruments at Bharati station in the Larsemann Hills provide continuous measurements of local ice dynamics and are part of the global monitoring network.

**[This article is demonstration content for the PolarConnect educational portal.]**''',
                is_featured=False,
                image_url='https://images.unsplash.com/photo-1508193638397-1c4234db14d8?w=900&q=80',
            ),
            dict(
                title='PolarConnect Portal Launched to Advance Polar Science Outreach in India',
                slug='polarconnect-portal-launch-2024',
                category_slug='education-news',
                summary='The Ministry of Earth Sciences has unveiled PolarConnect, a centralised digital platform connecting students, researchers and citizens with India\'s rich polar science heritage.',
                content='''The Ministry of Earth Sciences (MoES) has officially launched PolarConnect, an integrated polar science outreach, knowledge repository and media dissemination portal aimed at making India's polar research accessible to all citizens.

**What is PolarConnect?**

PolarConnect is a comprehensive digital ecosystem that brings together:

- A **Knowledge Repository** housing scientific papers, reports and educational documents
- A **Learning Centre** with interactive modules and quizzes for students at all levels
- A **Research Publications** database for peer-reviewed and institutional research
- An **Expedition Archive** documenting decades of Indian polar expeditions
- A **Media Gallery** showcasing photographs and videos from polar missions
- A **Community Forum** for researchers, educators and science enthusiasts
- An **Interactive Polar Map** displaying research stations and expedition sites

**Why Now?**

India has a forty-plus year history of Antarctic research, yet public awareness of this legacy remains limited. PolarConnect addresses this gap by creating a single, authoritative digital resource for polar science information in India.

The platform is designed to serve students from Class 6 upwards, undergraduate and postgraduate researchers, school and college educators, and science communicators and journalists.

**Getting Started**

Create a free account at polarconnect.moes.gov.in to access all learning resources, track your progress through learning modules, and join the community forum.

**[This article is demonstration content for the PolarConnect educational portal.]**''',
                is_featured=True,
                image_url='https://images.unsplash.com/photo-1467579424161-6bdd8ef27cfc?w=900&q=80',
            ),
            dict(
                title='India Signs Extended Protocol on Environmental Protection in Antarctica',
                slug='india-antarctic-protocol-2024',
                category_slug='policy-governance',
                summary='India reaffirms its commitment to the Antarctic Treaty System by signing an extended environmental protection framework, reinforcing sustainable practices at its research stations.',
                content='''India has renewed its commitment to the Antarctic Treaty System (ATS) by endorsing an extended environmental protection framework, reinforcing the country's obligations under the Protocol on Environmental Protection to the Antarctic Treaty (the Madrid Protocol).

**India and the Antarctic Treaty**

India acceded to the Antarctic Treaty in 1983 and was granted Consultative Party status in 1983, following its first expedition in 1981. As a Consultative Party, India participates in the annual Antarctic Treaty Consultative Meeting (ATCM) and helps shape the governance of the continent.

The Madrid Protocol, which came into force in 1998, designates Antarctica as a "natural reserve, devoted to peace and science" and prohibits mineral resource activities. It also requires Environmental Impact Assessments (EIAs) for all activities in Antarctica.

**India's Environmental Commitments**

At its Antarctic stations, India has implemented:

- Solar and wind power generation to reduce diesel consumption
- Advanced waste treatment and zero-discharge systems
- Biodegradable packaging for all materials taken to the continent
- Strict biosecurity protocols to prevent introduction of non-native species
- Comprehensive environmental monitoring programmes

**[This article is demonstration content for the PolarConnect educational portal.]**''',
                is_featured=False,
                image_url='https://images.unsplash.com/photo-1476610182048-b716b8518aae?w=900&q=80',
            ),
            dict(
                title='Arctic Sea Ice Hits Record September Low — Scientists Sound Alarm',
                slug='arctic-sea-ice-record-low-2024',
                category_slug='climate-science',
                summary='Satellite data reveals Arctic sea ice extent reached its lowest September minimum on record, prompting urgent calls from climate scientists for accelerated emissions reductions.',
                content='''Arctic sea ice extent at its annual September minimum has reached a record low, according to data released by the National Snow and Ice Data Center (NSIDC) and confirmed by multiple independent satellite monitoring programmes.

**The Numbers**

The September sea ice extent — the annual minimum — came in at approximately 3.2 million square kilometres, breaking the previous record set in 2012. The long-term average September extent (1981–2010) was 6.3 million square kilometres, meaning current ice extent is barely half of what it was three decades ago.

**Why September Matters**

September represents the end of the Arctic summer melt season — when sea ice is at its smallest. The trend of declining September sea ice is one of the most visible and unambiguous signals of climate change. Arctic sea ice has declined at a rate of approximately 13% per decade since satellite records began in 1979.

**The Albedo Feedback Loop**

As white sea ice is replaced by darker open ocean, more solar radiation is absorbed rather than reflected — a feedback mechanism called Arctic amplification. This is why the Arctic is warming two to four times faster than the global average.

**What Happens Next**

Scientists warn that the Arctic could see its first ice-free September as early as the 2030s under current emissions trajectories. An ice-free Arctic summer would fundamentally alter global weather patterns, disrupt Arctic ecosystems and accelerate the thawing of permafrost — which stores enormous quantities of methane, a potent greenhouse gas.

**India's Arctic Research**

India monitors Arctic conditions through its Himadri station at Ny-Ålesund, Svalbard. Data from Himadri contributes to international datasets on Arctic atmospheric chemistry, glaciology and marine biology.

**[This article is demonstration content for the PolarConnect educational portal.]**''',
                is_featured=False,
                image_url='https://images.unsplash.com/photo-1551009175-15bdf9dcb580?w=900&q=80',
            ),
            dict(
                title='NCPOR Develops AI-Powered System for Real-Time Iceberg Tracking',
                slug='ncpor-ai-iceberg-tracking-2024',
                category_slug='technology',
                summary='Researchers at the National Centre for Polar and Ocean Research have developed an artificial intelligence system that tracks Antarctic icebergs in real-time using satellite data, improving maritime safety.',
                content='''Scientists at India's National Centre for Polar and Ocean Research (NCPOR) have developed and deployed an AI-powered iceberg tracking system that provides real-time monitoring of large icebergs in the Southern Ocean.

**How It Works**

The system combines:

- **Synthetic Aperture Radar (SAR)** satellite imagery, which can detect icebergs regardless of cloud cover or darkness
- **Optical satellite data** for detailed surface analysis when conditions allow
- **A deep learning model** trained on thousands of labelled iceberg images to automatically detect and classify icebergs by size and shape
- **Ocean current modelling** to predict iceberg drift trajectories up to 10 days ahead

**Why Iceberg Tracking Matters**

Large icebergs — those exceeding 1 km in length — pose serious risks to shipping routes in the Southern Ocean. India's research vessels regularly transit these waters during annual Antarctic expeditions. Accurate tracking also helps scientists study iceberg calving events, which are linked to ice shelf instability and contribute to sea-level rise.

**Applications Beyond Safety**

Icebergs carry fresh water and nutrients that fertilise marine ecosystems as they melt. Tracking their trajectories helps oceanographers model nutrient distribution and understand phytoplankton blooms in the Southern Ocean — a key component of the global carbon cycle.

**[This article is demonstration content for the PolarConnect educational portal.]**''',
                is_featured=False,
                image_url='https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=900&q=80',
            ),
        ]

        created = 0
        for d in articles:
            if NewsArticle.objects.filter(slug=d['slug']).exists():
                continue
            cat = None
            try:
                cat = NewsCategory.objects.get(slug=d['category_slug'])
            except NewsCategory.DoesNotExist:
                pass
            art = NewsArticle(
                title=d['title'], slug=d['slug'], summary=d['summary'],
                content=d['content'], author=author, category=cat,
                status='published', is_featured=d.get('is_featured', False),
                published_at=timezone.now() - timedelta(days=random.randint(1, 60)),
            )
            art.save()
            created += 1
        self.stdout.write(f'  ✓ News articles: {created} created')

    # --------------------------------------------------------------- events
    def _create_events(self):
        from news.models import Event
        now = timezone.now()
        events = [
            dict(
                title='International Polar Science Webinar: Climate Tipping Points',
                slug='polar-webinar-tipping-points-2024',
                event_type='webinar',
                description='''Join leading polar scientists from India, Norway, USA and Australia for a live webinar on climate tipping points in the polar regions.

**Topics Covered:**
- West Antarctic Ice Sheet instability and tipping thresholds
- Arctic permafrost thaw and methane release
- Changes in the Atlantic Meridional Overturning Circulation (AMOC)
- Policy implications of polar tipping points

**Speakers (Demonstration):**
- Dr. Priya Sharma, NCPOR — Ice Sheet Dynamics
- Prof. Lars Eriksen, University of Oslo — Arctic Permafrost
- Dr. Sarah Chen, British Antarctic Survey — AMOC Changes

**Registration:** Free for all PolarConnect members. Certificate of participation provided.

[This is demonstration content for the PolarConnect portal.]''',
                start_datetime=now + timedelta(days=12),
                is_online=True,
                organizer='National Centre for Polar and Ocean Research (NCPOR)',
                is_featured=True,
                registration_link='https://ncpor.res.in',
            ),
            dict(
                title='National Polar Science Essay Competition 2024',
                slug='polar-essay-competition-2024',
                event_type='competition',
                description='''The Ministry of Earth Sciences invites entries for the National Polar Science Essay Competition, open to school and college students across India.

**Categories:**
- **Junior** (Classes 6–10): "Why do polar regions matter to India?"
- **Senior** (Classes 11–12): "Climate change and the cryosphere: What does the science tell us?"
- **Undergraduate** (B.Sc/B.Tech): "India's contributions to Antarctic science: A critical review"

**Prizes:**
- 1st Prize: ₹25,000 + Certificate + Invitation to NCPOR open day
- 2nd Prize: ₹15,000 + Certificate
- 3rd Prize: ₹10,000 + Certificate

**Submission Deadline:** 31 December 2024
**Results Announced:** January 2025

[This is demonstration content for the PolarConnect portal.]''',
                start_datetime=now + timedelta(days=35),
                is_online=False,
                organizer='Ministry of Earth Sciences',
                is_featured=True,
                registration_link='https://moes.gov.in',
            ),
            dict(
                title='Polar Science Workshop for Educators — New Delhi',
                slug='educator-workshop-polar-delhi-2024',
                event_type='workshop',
                description='''A two-day intensive workshop designed for school and college science teachers, equipping them with the knowledge and resources to teach polar science effectively.

**Day 1: Science Content**
- Introduction to polar geography and climate
- Ice sheets, glaciers and sea-level rise
- Polar biodiversity and food webs
- India's research stations and expeditions

**Day 2: Pedagogy and Resources**
- Integrating polar science into the NCERT curriculum
- Using PolarConnect in the classroom
- Interactive activities and demonstrations
- Building a polar science club at your school

**Eligibility:** Science teachers at secondary and higher secondary level.
**Venue:** India International Centre, New Delhi (demonstration venue)
**Fee:** No fee. Travel allowance available for outstation participants.

[This is demonstration content for the PolarConnect portal.]''',
                start_datetime=now + timedelta(days=22),
                is_online=False,
                organizer='NCPOR Education Outreach Division',
                is_featured=False,
                registration_link='https://ncpor.res.in',
            ),
            dict(
                title='Open Day at NCPOR Goa — Visit India\'s Polar Research Centre',
                slug='ncpor-open-day-goa-2024',
                event_type='other',
                description='''The National Centre for Polar and Ocean Research (NCPOR) in Vasco da Gama, Goa, opens its doors to students, educators and science enthusiasts for its annual Open Day.

**What You Can See:**
- Scientific instruments and equipment used at Antarctic stations
- Ice core samples and geological specimens from Antarctica
- Research vessels and logistical operations
- Interactive climate change demonstrations
- Meet scientists who have wintered in Antarctica

**Who Should Attend:**
School groups, college students, educators and the general public with an interest in science and exploration.

**[This is demonstration content for the PolarConnect portal.]**''',
                start_datetime=now + timedelta(days=45),
                is_online=False,
                organizer='National Centre for Polar and Ocean Research, Goa',
                is_featured=False,
                registration_link='https://ncpor.res.in',
            ),
            dict(
                title='Antarctic Treaty System: India\'s Role — Public Lecture',
                slug='antarctic-treaty-public-lecture-2024',
                event_type='other',
                description='''A free public lecture on India's role in the Antarctic Treaty System and international polar governance, delivered by a senior Ministry of Earth Sciences official.

**Topics:**
- History and structure of the Antarctic Treaty System
- India as a Consultative Party: rights and responsibilities
- The Madrid Protocol on Environmental Protection
- Future challenges: tourism, bioprospecting and resource governance
- Antarctica in Indian foreign policy

[This is demonstration content for the PolarConnect portal.]''',
                start_datetime=now + timedelta(days=8),
                is_online=True,
                organizer='Ministry of Earth Sciences',
                is_featured=False,
                registration_link='https://moes.gov.in',
            ),
        ]
        created = 0
        for d in events:
            if Event.objects.filter(slug=d['slug']).exists():
                continue
            reg = d.pop('registration_link', '')
            e = Event(**d, registration_link=reg)
            e.save()
            created += 1
        self.stdout.write(f'  ✓ Events: {created} created')

    # ------------------------------------------------------------- research
    def _create_research(self):
        from research.models import ResearchPublication
        from accounts.models import CustomUser
        uploader = CustomUser.objects.filter(role='researcher').first() or \
                   CustomUser.objects.filter(is_staff=True).first()

        papers = [
            dict(
                title='Mass Balance of the Antarctic Ice Sheet 1992–2023: A Multi-Sensor Assessment',
                authors='Sharma P., Kumar R., Nair S., Krishnan A.',
                institution='National Centre for Polar and Ocean Research, Goa, India',
                abstract='We present a comprehensive multi-sensor assessment of Antarctic Ice Sheet mass balance spanning three decades (1992–2023). Using a combination of satellite radar altimetry, gravimetry (GRACE/GRACE-FO) and synthetic aperture radar, we quantify ice mass changes across the East Antarctic Ice Sheet (EAIS), West Antarctic Ice Sheet (WAIS) and Antarctic Peninsula. Our results indicate a net mass loss of −150 ± 25 Gt/yr over the full period, accelerating to −220 ± 30 Gt/yr in the most recent decade. The WAIS accounts for 65% of total mass loss, driven primarily by outlet glacier acceleration at Thwaites and Pine Island glaciers. The EAIS shows regional heterogeneity, with gains in the interior offset by coastal losses. These findings have significant implications for sea-level projections. [DEMONSTRATION CONTENT — educational purpose only]',
                keywords='ice sheet, mass balance, glaciology, sea level, satellite altimetry, GRACE',
                category='glaciology',
                publication_year=2024,
                journal_name='Journal of Glaciology',
                doi='10.1017/jog.2024.DEMO',
                status='approved',
                is_featured=True,
            ),
            dict(
                title='Ozone Column Variability Over Maitri Station, Antarctica: A 15-Year Record',
                authors='Reddy V., Pillai M., Bhatt U., Sharma P.',
                institution='Indian Institute of Tropical Meteorology, Pune; NCPOR, Goa',
                abstract='Total ozone column measurements collected at India\'s Maitri station (70.77°S, 11.73°E) over a 15-year period (2008–2023) are presented and analysed for interannual variability, seasonal cycles and trends. The dataset reveals a significant Antarctic ozone hole over Maitri each austral spring (September–November), with minimum total ozone values reaching as low as 150 Dobson Units. Long-term trend analysis shows a slight positive trend of +1.2 DU/year consistent with Montreal Protocol recovery projections. Correlations with stratospheric temperature, polar vortex strength and sea surface temperature anomalies are examined. [DEMONSTRATION CONTENT]',
                keywords='ozone, Antarctic ozone hole, stratosphere, Maitri, Dobson Units, Montreal Protocol',
                category='atmospheric',
                publication_year=2023,
                journal_name='Atmospheric Chemistry and Physics',
                doi='10.5194/acp-2023-DEMO',
                status='approved',
                is_featured=True,
            ),
            dict(
                title='Southern Ocean Phytoplankton Blooms and Their Role in Carbon Sequestration',
                authors='Joshi T., Fernandes A., Kumar R., Lal S.',
                institution='National Institute of Oceanography, Goa; NCPOR, Goa',
                abstract='The Southern Ocean accounts for approximately 40% of the global oceanic uptake of anthropogenic CO2, with phytoplankton playing a central role in this carbon pump. We analyse satellite chlorophyll-a data and in-situ measurements from Indian research voyages to characterise seasonal phytoplankton bloom dynamics in the Atlantic sector of the Southern Ocean (40°S–70°S). Peak blooms occur in November–January, driven by light availability and iron fertilisation from iceberg meltwater. We estimate a net primary production of 2.1 ± 0.4 Pg C/yr for the study region. Interannual variability is significantly correlated with sea ice extent and the Southern Annular Mode index. [DEMONSTRATION CONTENT]',
                keywords='Southern Ocean, phytoplankton, carbon cycle, chlorophyll, sea ice, primary production',
                category='oceanography',
                publication_year=2023,
                journal_name='Deep-Sea Research Part I',
                doi='10.1016/j.dsr.2023.DEMO',
                status='approved',
                is_featured=False,
            ),
            dict(
                title='Permafrost Dynamics in the Svalbard Archipelago: Implications for Arctic Carbon Budgets',
                authors='Nair M., Eriksen L., Patel A.',
                institution='NCPOR Goa; University of Oslo',
                abstract='Permafrost in Svalbard has warmed by approximately 2°C over the past three decades, the most rapid permafrost warming recorded anywhere in the Arctic. We present borehole temperature profiles from four sites near Ny-Ålesund, combined with ground-penetrating radar surveys and soil carbon flux measurements, to characterise active layer deepening and thermokarst formation. Net methane flux from thawing permafrost in the study area is estimated at 12 ± 4 g CH4/m²/yr, representing a significant positive feedback to regional warming. These results suggest that Svalbard permafrost may transition from a carbon sink to a net source within two decades under current warming trajectories. [DEMONSTRATION CONTENT]',
                keywords='permafrost, Svalbard, Arctic, methane, carbon budget, thermokarst',
                category='arctic',
                publication_year=2022,
                journal_name='Nature Climate Change',
                doi='10.1038/s41558-022-DEMO',
                status='approved',
                is_featured=True,
            ),
            dict(
                title='Leopard Seals as Sentinels of Southern Ocean Health: Diet and Distribution Shifts',
                authors='Kapoor S., Rodriguez M., Bhatt K.',
                institution='Wildlife Institute of India; NCPOR, Goa',
                abstract='Leopard seals (Hydrurga leptonyx) are apex predators in the Antarctic marine ecosystem and sensitive indicators of ecosystem change. Using satellite telemetry, stable isotope analysis and stomach content data collected across five Antarctic summer seasons, we document significant northward range expansion (mean: 2.3° latitude) and dietary shifts from krill-based to fish-dominated diets in populations near the Antarctic Peninsula. These changes are strongly correlated with declining winter sea ice extent, suggesting that leopard seal ecology is tracking rapid ecosystem reorganisation driven by climate change. [DEMONSTRATION CONTENT]',
                keywords='leopard seal, Antarctic, marine ecosystem, sea ice, predator, climate change',
                category='polar_ecology',
                publication_year=2023,
                journal_name='Marine Ecology Progress Series',
                doi='10.3354/meps-2023-DEMO',
                status='approved',
                is_featured=False,
            ),
            dict(
                title='Glacial Isostatic Adjustment in Dronning Maud Land: GPS Constraints',
                authors='Singh R., Chaturvedi A., Sharma P., Bhatt U.',
                institution='Survey of India; NCPOR, Goa',
                abstract='Glacial Isostatic Adjustment (GIA) — the ongoing uplift of Earth\'s crust in response to deglaciation — is a critical correction in satellite-based ice mass balance estimates. We present horizontal and vertical GPS velocity measurements from six continuous GPS stations in Dronning Maud Land, East Antarctica, three of which are located near India\'s Maitri station. Our results show crustal uplift rates of 1.5–3.2 mm/yr at the measurement sites. Comparison with existing GIA models reveals that current models systematically underestimate uplift rates in this region, with implications for ice mass balance estimates from GRACE-FO gravimetry. [DEMONSTRATION CONTENT]',
                keywords='GIA, glacial isostatic adjustment, GPS, East Antarctica, Dronning Maud Land, GRACE',
                category='geology',
                publication_year=2024,
                journal_name='Geophysical Research Letters',
                doi='10.1029/2024GL-DEMO',
                status='approved',
                is_featured=False,
            ),
            dict(
                title='Autonomous Underwater Vehicles in Antarctic Research: Challenges and Opportunities',
                authors='Mehta V., Nair S., Krishnamurthy T.',
                institution='Indian Institute of Technology Madras; NCPOR, Goa',
                abstract='Autonomous underwater vehicles (AUVs) are transforming oceanographic research in ice-covered Antarctic waters, enabling measurements previously impossible with traditional ship-based methods. We review the state of AUV technology applied in Antarctica over the past decade and present results from two IIT Madras-developed AUV deployments in the Prydz Bay during ISEA-40 and ISEA-41. The vehicles mapped sub-ice-shelf cavities, measured temperature and salinity profiles beneath the Amery Ice Shelf, and documented benthic communities at depths exceeding 800 m. Technical challenges including acoustic communication limitations, battery management in cold water and ice avoidance are discussed. [DEMONSTRATION CONTENT]',
                keywords='AUV, autonomous underwater vehicle, Antarctica, sub-ice ocean, ice shelf, oceanography',
                category='polar_technology',
                publication_year=2023,
                journal_name='Cold Regions Science and Technology',
                doi='10.1016/j.coldregions.2023.DEMO',
                status='approved',
                is_featured=False,
            ),
            dict(
                title='Changes in Antarctic Krill Abundance and Distribution Under Climate Projections',
                authors='Patel R., Fernandez C., Lal S., Joshi T.',
                institution='NCPOR Goa; Alfred Wegener Institute',
                abstract='Antarctic krill (Euphausia superba) underpin one of the most productive marine ecosystems on Earth, supporting populations of penguins, seals, whales and seabirds. Using an ensemble of CMIP6 climate models combined with a krill habitat suitability model, we project changes in krill abundance and geographic distribution under RCP2.6 and RCP8.5 scenarios through 2100. Under RCP8.5, we project a 30–40% reduction in krill habitat in the Atlantic sector of the Southern Ocean and a 500 km southward shift in core distribution by 2100. These changes pose severe risks to dependent predator populations and have implications for the management of commercial krill fisheries under CCAMLR. [DEMONSTRATION CONTENT]',
                keywords='krill, Euphausia superba, Southern Ocean, climate projections, CMIP6, marine ecosystem',
                category='marine_biology',
                publication_year=2024,
                journal_name='Global Change Biology',
                doi='10.1111/gcb.2024-DEMO',
                status='approved',
                is_featured=False,
            ),
        ]

        created = 0
        for d in papers:
            if ResearchPublication.objects.filter(title=d['title']).exists():
                continue
            p = ResearchPublication(**d, uploaded_by=uploader)
            p.save()
            created += 1
        self.stdout.write(f'  ✓ Research papers: {created} created')

    # ----------------------------------------------------------- repository
    def _create_repository(self):
        from repository.models import KnowledgeResource
        from accounts.models import CustomUser
        uploader = CustomUser.objects.filter(is_staff=True).first()

        resources = [
            dict(
                title='A Student\'s Guide to Polar Regions — Earth\'s Frozen Frontiers',
                author='PolarConnect Education Team',
                institution='Ministry of Earth Sciences, India',
                abstract='A comprehensive introductory guide to the Arctic and Antarctic regions, written for secondary school and undergraduate students. Covers geography, climate, ecosystems, research activities and India\'s polar programme. Includes diagrams, maps, key terms and review questions. Approximately 80 pages. [DEMONSTRATION CONTENT]',
                keywords='polar regions, Antarctic, Arctic, student guide, education, glaciology, climate',
                category='antarctic', resource_type='educational', is_featured=True, is_published=True,
                publication_date=date(2024, 1, 15),
            ),
            dict(
                title='India\'s Antarctic Research Programme: Scientific Achievements 1981–2023',
                author='National Centre for Polar and Ocean Research',
                institution='NCPOR, Ministry of Earth Sciences',
                abstract='A comprehensive review of four decades of Indian scientific research in Antarctica, documenting key findings across glaciology, atmospheric science, oceanography, geology and biological sciences. This report summarises the contributions of over 1,500 Indian scientists who have participated in Antarctic expeditions. [DEMONSTRATION CONTENT — not an official NCPOR document]',
                keywords='India, Antarctica, NCPOR, research history, Maitri, Bharati, expedition',
                category='antarctic', resource_type='report', is_featured=True, is_published=True,
                publication_date=date(2023, 12, 1),
                external_url='https://www.ncpor.res.in',
            ),
            dict(
                title='Understanding Climate Change: A Polar Perspective',
                author='PolarConnect Science Team',
                institution='Ministry of Earth Sciences',
                abstract='This educational document explains climate change through the lens of polar science — using observations from Antarctica and the Arctic to illustrate the mechanisms, evidence and consequences of global warming. Suitable for CBSE Classes 9–12 and undergraduate general science courses. [DEMONSTRATION CONTENT]',
                keywords='climate change, global warming, polar regions, education, CBSE, ice sheets',
                category='climate_change', resource_type='educational', is_featured=True, is_published=True,
                publication_date=date(2024, 3, 1),
            ),
            dict(
                title='Antarctic Treaty System: A Guide for Indian Students and Researchers',
                author='Legal & Policy Division, Ministry of Earth Sciences',
                institution='Ministry of Earth Sciences, Government of India',
                abstract='An accessible guide to the Antarctic Treaty System, explaining its history, structure and India\'s role as a Consultative Party. Covers the Treaty itself, the Madrid Environmental Protocol, CCAMLR fisheries management and the Antarctic Treaty Consultative Meeting process. [DEMONSTRATION CONTENT]',
                keywords='Antarctic Treaty, international law, governance, India, ATCM, Madrid Protocol',
                category='antarctic', resource_type='educational', is_featured=False, is_published=True,
                publication_date=date(2023, 6, 15),
            ),
            dict(
                title='Polar Wildlife Field Guide: Antarctic and Sub-Antarctic Species',
                author='Wildlife Institute of India; NCPOR',
                institution='Wildlife Institute of India',
                abstract='An illustrated field guide to the marine mammals, seabirds, fish and invertebrates encountered during Indian polar expeditions. Each species account includes identification features, distribution, behaviour, diet and conservation status. Approximately 120 species covered with photographs and range maps. [DEMONSTRATION CONTENT]',
                keywords='Antarctic wildlife, penguins, seals, whales, seabirds, marine mammals, field guide',
                category='polar_ecology', resource_type='educational', is_featured=False, is_published=True,
                publication_date=date(2022, 11, 1),
            ),
            dict(
                title='Remote Sensing Applications in Polar Research: A Technical Overview',
                author='Space Applications Centre, ISRO',
                institution='Indian Space Research Organisation (ISRO)',
                abstract='An overview of remote sensing technologies and their applications in polar research, with a focus on ISRO\'s contributions to polar monitoring. Covers optical and SAR satellite imagery for ice mapping, ocean monitoring, atmospheric sounding and topographic mapping in polar regions. [DEMONSTRATION CONTENT — not an official ISRO publication]',
                keywords='remote sensing, SAR, satellite, ISRO, polar monitoring, ice mapping',
                category='polar_technology', resource_type='report', is_featured=False, is_published=True,
                publication_date=date(2023, 9, 1),
                external_url='https://www.sac.gov.in',
            ),
            dict(
                title='Southern Ocean Oceanography: Circulation, Fronts and Ecosystems',
                author='National Institute of Oceanography',
                institution='CSIR-National Institute of Oceanography, Goa',
                abstract='A technical overview of Southern Ocean physical and biological oceanography, covering the Antarctic Circumpolar Current, polar fronts, water mass formation, nutrient cycling and biological productivity. Includes data from Indian research cruises in the Southern Ocean. [DEMONSTRATION CONTENT]',
                keywords='Southern Ocean, ACC, oceanography, water masses, polar front, NIO',
                category='oceanography', resource_type='report', is_featured=True, is_published=True,
                publication_date=date(2023, 7, 1),
            ),
            dict(
                title='Glaciology Fieldwork Manual: Techniques for Ice and Snow Measurements',
                author='Himalayan Glaciology Division, NCPOR',
                institution='NCPOR, Ministry of Earth Sciences',
                abstract='A practical manual covering standard techniques for glaciological fieldwork including ice core drilling, mass balance stakes, snow pit analysis, GPS surveying on ice and ground-penetrating radar. Developed for training scientists before Antarctic deployment. [DEMONSTRATION CONTENT]',
                keywords='glaciology, fieldwork, ice core, mass balance, GPS, ground-penetrating radar',
                category='glaciology', resource_type='educational', is_featured=False, is_published=True,
                publication_date=date(2022, 8, 1),
            ),
        ]

        created = 0
        for d in resources:
            if KnowledgeResource.objects.filter(title=d['title']).exists():
                continue
            r = KnowledgeResource(**d, uploaded_by=uploader)
            r.save()
            created += 1
        self.stdout.write(f'  ✓ Repository resources: {created} created')

    # ---------------------------------------------------- learning modules
    def _create_learning_modules(self):
        from education.models import LearningCategory, LearningModule

        modules_data = [
            # Category 1 – Introduction
            dict(category_slug='introduction-polar-regions', title='Arctic vs Antarctic: Key Differences',
                 slug='arctic-vs-antarctic', difficulty='beginner', duration=20, order=2,
                 description='Learn the fundamental differences between the two polar regions — geography, climate, wildlife and human presence.',
                 content='''Many people assume the Arctic and Antarctic are essentially the same — just one at the top of the planet and one at the bottom. In fact, they are fundamentally different in almost every way.

## Geography

**The Arctic** is primarily an ocean — the Arctic Ocean — surrounded by the landmasses of North America, Europe and Asia. The sea ice that covers much of the Arctic floats on water. Greenland, the world's largest island, sits at the edge of the Arctic and contains its own massive ice sheet.

**Antarctica** is a continent — a landmass — covered by an ice sheet averaging 2.3 km in thickness. It is completely surrounded by the Southern Ocean. No other landmass lies close to it.

## Temperature

Both regions are extremely cold, but Antarctica is significantly colder:

| | Arctic | Antarctic |
|---|---|---|
| Average winter temperature | −40°C | −60°C |
| Record low temperature | −68°C (Siberia) | −89.2°C (Vostok) |
| Average summer temperature | 0°C | −20°C |

Antarctica is colder for three reasons: it sits on a high plateau (average elevation 2,300 m), it is surrounded by ocean rather than moderated by it, and cold air drains down from the high interior plateau.

## Wildlife

**Arctic wildlife** includes polar bears, Arctic foxes, lemmings, Arctic hares and reindeer on land, and walruses, narwhals and beluga whales in the ocean. The Arctic tern migrates between the Arctic and Antarctic each year.

**Antarctic wildlife** includes emperor penguins, Adélie penguins, leopard seals, Weddell seals, crabeater seals and numerous seabird species. There are no native land mammals. All Antarctic wildlife is ultimately dependent on the ocean for food.

## Human Presence

The Arctic has been inhabited by Indigenous peoples — including the Inuit, Yupik and Chukchi — for thousands of years. Several nations with Arctic territory include Canada, Russia, Norway, the United States and Denmark (Greenland).

Antarctica has no indigenous human population and no permanent civilian residents. It is governed by the Antarctic Treaty System and hosts only temporary scientific personnel at research stations.

## Why Both Matter

Both polar regions are critical regulators of Earth's climate, and both are warming rapidly — the Arctic at two to four times the global average rate. Changes in the poles affect sea levels, weather patterns and biodiversity worldwide.'''),

            dict(category_slug='introduction-polar-regions', title='India\'s Polar Research Journey',
                 slug='india-polar-research-journey', difficulty='beginner', duration=30, order=3,
                 description='Discover the history of India\'s involvement in Antarctic and Arctic research, from the first expedition in 1981 to today.',
                 content='''India's engagement with polar research began in 1981 — a relatively modest start that has grown into one of the world's most active Antarctic research programmes.

## The First Expedition (1981)

India's first Antarctic expedition was launched in December 1981, with a team of 21 scientists and support personnel. The team established a temporary base camp near the Antarctic coast and conducted the first Indian scientific surveys in the region — covering geology, glaciology and meteorology.

This expedition established India's credentials in Antarctic science and paved the way for the country's accession to the Antarctic Treaty in 1983, with Consultative Party status granted shortly thereafter.

## Dakshin Gangotri (1983)

India established its first permanent Antarctic research base, Dakshin Gangotri, in 1983. Named after the southernmost Gangotri glacier, this was India's first Antarctic station. After being damaged by encroaching ice, it was decommissioned as a research station in 1990 and now serves as a supply depot.

## Maitri Station (1989–Present)

India's current primary Antarctic station, Maitri, was established in the Schirmacher Oasis region of Queen Maud Land in 1989. The Schirmacher Oasis is a 34 km long, ice-free rocky oasis — an unusual feature in the otherwise ice-covered continent.

Maitri operates year-round and houses up to 25 scientists and support staff during summer and a smaller winter-over team. Research programmes include:
- Atmospheric and ozone research
- Geomagnetism
- Geological studies of the Schirmacher Oasis
- Meteorological observations

## Bharati Station (2012–Present)

India's most modern Antarctic station, Bharati, was established in 2012 in the Larsemann Hills of East Antarctica. Built to the highest environmental standards — it is one of the most energy-efficient Antarctic stations — Bharati focuses on oceanographic, atmospheric and geological research.

## India in the Arctic: Himadri Station (2008–Present)

India extended its polar research to the Arctic in 2007–2008, establishing the Himadri station at Ny-Ålesund, Svalbard, Norway. Himadri is used for seasonal research on Arctic atmospheric science, glaciology and marine biology.

## Key Achievements

Over four decades, Indian polar scientists have:
- Built one of the world's longest Antarctic atmospheric monitoring datasets
- Contributed to multiple IPCC assessment reports
- Mapped geology of the Schirmacher Oasis and surrounding regions
- Monitored Southern Ocean productivity from research vessels
- Collected Antarctic ice cores contributing to global climate records

India is a proud member of the Antarctic Treaty System and participates actively in the annual Antarctic Treaty Consultative Meeting (ATCM).

**[This module contains demonstration content for educational purposes.]**'''),

            # Category 4 – Ice Sheets
            dict(category_slug='ice-sheets-glaciers', title='How Do Glaciers Form and Move?',
                 slug='how-glaciers-form-move', difficulty='beginner', duration=25, order=2,
                 description='Explore the life cycle of a glacier — from snowflake to ice flow — and understand how glaciers shape landscapes.',
                 content='''Glaciers are among the most powerful geological forces on Earth. They cover about 10% of Earth's land surface and contain 70% of its fresh water.

## From Snow to Ice

A glacier begins as accumulated snowfall in an area where more snow falls each winter than melts each summer. Over years and decades, the snow compresses under its own weight:

1. **Fresh snow** (new snow crystal, hexagonal, ~90% air) → density ~100 kg/m³
2. **Firn** (rounded, partially bonded grains, ~1–3 years old) → density ~400–830 kg/m³
3. **Glacier ice** (interlocking crystals, almost no air bubbles) → density ~917 kg/m³

The transition from snow to glacier ice typically takes 100–1,000 years in the cold, dry interior of Antarctica — where snowfall is very low — but just 5–10 years in temperate glaciers with heavy snowfall.

## How Glaciers Move

Glaciers flow under gravity — from areas of accumulation (where snow adds mass) toward areas of ablation (where ice is lost through melting, calving or sublimation).

**Two mechanisms of glacier flow:**

**1. Internal deformation (creep)**
Ice crystals deform and slide over each other under the weight of overlying ice. This occurs throughout the glacier and is dominant in cold, polar ice.

**2. Basal sliding**
In temperate (warmer) glaciers, meltwater forms at the base of the glacier, lubricating the rock surface and allowing the glacier to slide. Much faster than internal deformation alone.

## Speed of Glaciers

Most glaciers move surprisingly quickly:
- Slow mountain glaciers: a few centimetres per day
- Fast Antarctic outlet glaciers: several kilometres per year
- Jakobshavn Glacier, Greenland: up to 46 metres per day — one of the fastest on Earth

## Glaciers and Climate

Glaciers are sensitive thermometers of climate. When temperatures warm, glaciers lose more mass through melting and calving than they gain through snowfall — they retreat. The vast majority of the world's glaciers are currently retreating.

**India's Himalayan glaciers** — the source of water for the Ganges, Indus and Brahmaputra — are retreating at accelerating rates, threatening long-term water security for hundreds of millions of people.

**[Demonstration content for PolarConnect.]**'''),

            # Category 5 – Climate Change
            dict(category_slug='climate-change-polar', title='The Polar Vortex and Extreme Weather',
                 slug='polar-vortex-extreme-weather', difficulty='intermediate', duration=35, order=2,
                 description='Understand the polar vortex, how Arctic warming destabilises it, and why this causes extreme cold events at lower latitudes.',
                 content='''The polar vortex is a large area of low pressure and cold air surrounding both of Earth's poles. Changes in the Arctic polar vortex have been linked to increasingly frequent extreme weather events across the Northern Hemisphere — including the extreme cold waves that periodically affect northern India.

## What is the Polar Vortex?

The polar vortex is not a storm or a weather event — it is a persistent, large-scale cyclone that sits over each pole during winter, rotating counterclockwise in the Northern Hemisphere. It is maintained by the strong temperature contrast between the cold Arctic and the warmer mid-latitudes.

**The polar vortex exists in two layers:**
- **Stratospheric polar vortex**: 15–50 km altitude; forms each autumn and breaks down each spring
- **Tropospheric polar vortex**: lower atmosphere; influences day-to-day weather more directly

## The Jet Stream Connection

The polar vortex is closely connected to the **polar jet stream** — a fast-flowing river of air at around 10 km altitude that separates cold polar air from warmer mid-latitude air. When the jet stream is strong and circular, it keeps cold Arctic air locked in the north.

## Arctic Amplification and Jet Stream Weakening

Here is the crucial climate change connection:

As the Arctic warms faster than the mid-latitudes (Arctic amplification), the temperature difference that drives the jet stream **weakens**. A weaker jet stream becomes more **wavy** — developing large meanders that allow cold Arctic air to plunge southward.

When these meanders become extreme, they can "pinch off" a pocket of cold Arctic air at mid-latitudes — the event colloquially called a **polar vortex disruption**.

## Effects at Mid-Latitudes

Polar vortex disruptions bring:
- Extreme cold waves to North America, Europe and Asia
- Heavy snowfall far south of normal limits
- Disruptions to agriculture, transport and energy systems

Research suggests that although individual cold events have become less frequent as the planet warms overall, **extreme cold intrusions linked to polar vortex disruption** may be becoming more intense as Arctic sea ice declines.

## Implications for India

Northern India — particularly the Indo-Gangetic Plain, Rajasthan and Kashmir — occasionally experiences severe cold waves linked to Arctic-sourced air masses. Understanding the polar vortex helps meteorologists improve cold wave forecasting for the region.

**[Demonstration content for PolarConnect.]**'''),

            # Category 7 – Ocean
            dict(category_slug='ocean-marine-research', title='The Southern Ocean: Earth\'s Climate Engine',
                 slug='southern-ocean-climate-engine', difficulty='intermediate', duration=40, order=1,
                 description='Discover why the Southern Ocean, surrounding Antarctica, is one of the most important and least-understood oceans on Earth.',
                 content='''The Southern Ocean — the body of water that completely encircles Antarctica — is often called the ocean that connects all oceans. It is unique, immensely powerful and critically important to Earth's climate.

## What is the Southern Ocean?

In 2000, the International Hydrographic Organization officially recognised the Southern Ocean as the world's fifth ocean, defined as the waters south of 60°S. It covers approximately 20.3 million km² and reaches depths of over 7,000 metres in places.

Unlike the Pacific, Atlantic and Indian Oceans — which are bounded by continents to their north and south — the Southern Ocean has no northern land boundary. This allows the **Antarctic Circumpolar Current (ACC)** to flow unimpeded around the globe.

## The Antarctic Circumpolar Current

The ACC is the largest and most powerful ocean current on Earth. It:
- Carries approximately 130–150 million cubic metres of water per second (the Amazon River carries about 0.2 million m³/s)
- Flows clockwise (eastward) around Antarctica
- Acts as a thermal barrier, preventing warm tropical waters from reaching Antarctica
- Connects the Atlantic, Pacific and Indian Ocean basins

## Deep Water Formation

The Southern Ocean plays a crucial role in **thermohaline circulation** — the global ocean conveyor belt that distributes heat around the planet.

In the Southern Ocean, cold, salty Antarctic water sinks to the sea floor, forming **Antarctic Bottom Water (AABW)** — the densest water mass in the ocean. This dense water flows northward along the sea floor into all three ocean basins, returning as warmer, shallower water thousands of years later.

This overturning circulation is a key mechanism for transporting heat from the tropics to the poles and for distributing oxygen and nutrients throughout the deep ocean.

## Carbon Sink

The Southern Ocean absorbs approximately **40% of all anthropogenic CO2** taken up by the world's oceans. Cold water absorbs more CO2 than warm water, and the vigorous mixing of the ACC brings CO2-rich surface water to depth.

However, as the Southern Ocean warms and freshens due to ice melt, its capacity to absorb carbon may decrease — a potentially significant positive feedback on climate change.

## India's Southern Ocean Research

India conducts regular oceanographic surveys in the Southern Ocean during annual Antarctic expeditions. Research focuses on:
- Physical oceanography: temperature, salinity, currents
- Biological productivity: phytoplankton and krill abundance
- Carbon chemistry: air-sea CO2 exchange
- Deep-sea sediments: climate records

**[Demonstration content for PolarConnect.]**'''),

            # Category 8 – Expeditions
            dict(category_slug='scientific-expeditions', title='Life at an Antarctic Research Station',
                 slug='life-at-antarctic-station', difficulty='beginner', duration=30, order=1,
                 description='What is daily life actually like at India\'s Maitri and Bharati stations? Explore the routines, challenges and rewards of wintering in Antarctica.',
                 content='''Spending time at an Antarctic research station is one of the most extraordinary experiences a scientist can have. It is also demanding, isolating and unlike anything else in human experience.

## Getting There

Scientists travelling to India's Antarctic stations typically fly from India to Cape Town, South Africa, and then take a long research vessel voyage south through the Southern Ocean — a journey of 10–15 days depending on ice conditions. The sea crossing is notoriously rough; the Southern Ocean is the stormiest on Earth.

Alternatively, some personnel fly via South Africa to a landing strip on the Antarctic ice, though this depends on the season and ice conditions.

## The Stations

**Maitri Station** in the Schirmacher Oasis houses up to 25 people in summer. The station has sleeping quarters, a laboratory building, a dining hall, a recreation room, a small library and a gym. The Oasis is an ice-free rocky area of about 34 km in length — unusual in Antarctica — and the station sits at an elevation of about 130 metres.

**Bharati Station** in the Larsemann Hills is more modern, opened in 2012. It is designed to the highest energy efficiency standards, using solar, wind and diesel power. It can house approximately 24 personnel and has fully equipped laboratories for oceanography, atmospheric science and geology.

## Daily Routine

A typical day at Maitri in summer might look like this:

- **0700**: Wake up, breakfast in the dining hall
- **0800–1200**: Scientific work — field surveys, lab analysis, instrument maintenance
- **1200–1300**: Lunch
- **1300–1800**: Continued scientific work, data processing
- **1800**: Dinner
- **1900 onwards**: Recreation, communication with family, preparation for next day

## Challenges

**Isolation**: Antarctic stations are genuinely cut off from the rest of the world for months at a time. Supply ships visit once per year. Medical emergencies must be handled on-site — every winterover team includes a doctor.

**Darkness**: In winter (May–August), the sun never rises above the horizon. This "polar night" can be psychologically demanding.

**Cold**: Outside temperatures at Maitri reach −35°C in winter. Working outdoors requires specialised clothing and strict safety protocols.

**Communication**: Modern stations have satellite internet, but bandwidth is limited. Regular calls home are possible but not always reliable.

## Rewards

Scientists describe Antarctica as profoundly humbling and transformative. The wildlife — penguins nesting metres from the station, seals sunbathing on the ice, whales breaching offshore — creates experiences unavailable anywhere else on Earth. And the science being done is genuinely important — contributing to global understanding of climate change, sea-level rise and Earth's history.

**[Demonstration content for PolarConnect.]**'''),
        ]

        created = 0
        for d in modules_data:
            if LearningModule.objects.filter(slug=d['slug']).exists():
                continue
            try:
                cat = LearningCategory.objects.get(slug=d['category_slug'])
            except LearningCategory.DoesNotExist:
                continue
            LearningModule.objects.create(
                category=cat,
                title=d['title'],
                slug=d['slug'],
                description=d['description'],
                content=d['content'],
                difficulty=d['difficulty'],
                duration_minutes=d['duration'],
                order=d['order'],
                is_published=True,
            )
            created += 1
        self.stdout.write(f'  ✓ Learning modules: {created} created')

    # --------------------------------------------------------------- quizzes
    def _create_quizzes(self):
        from education.models import LearningModule, Quiz, Question

        quiz_data = [
            dict(
                module_slug='understanding-ice-sheets',
                title='Ice Sheets and Glaciers Quiz',
                description='Test your understanding of polar ice dynamics and their role in sea-level change.',
                passing_score=60, time_limit=12,
                questions=[
                    dict(q='What is the average thickness of the Antarctic Ice Sheet?',
                         a='500 metres', b='1,000 metres', c='2,300 metres', d='5,000 metres', ans='C',
                         exp='The Antarctic Ice Sheet has an average thickness of approximately 2,300 metres, making it the largest single mass of ice on Earth.'),
                    dict(q='Which process converts snow into glacier ice?',
                         a='Sublimation', b='Compaction and recrystallisation', c='Evaporation', d='Condensation', ans='B',
                         exp='Over years and decades, accumulated snow is compacted by overlying layers and recrystallises into dense glacier ice, losing most of its air content.'),
                    dict(q='What would happen to global sea levels if all Antarctic ice melted?',
                         a='Sea levels would rise by about 1 metre', b='Sea levels would rise by about 10 metres',
                         c='Sea levels would rise by about 58 metres', d='Sea levels would not change significantly', ans='C',
                         exp='The Antarctic Ice Sheet contains enough water to raise global sea levels by approximately 58 metres if it were to melt completely.'),
                    dict(q='Which part of Antarctica is considered most vulnerable to collapse?',
                         a='East Antarctic Ice Sheet', b='West Antarctic Ice Sheet',
                         c='Antarctic Peninsula', d='Dronning Maud Land', ans='B',
                         exp='The West Antarctic Ice Sheet (WAIS) is considered most vulnerable because much of it rests on bedrock below sea level (marine ice sheet), making it susceptible to marine ice sheet instability.'),
                    dict(q='What is an ice shelf?',
                         a='Sea ice that forms in winter', b='A glacier that has stopped moving',
                         c='A floating extension of a land-based ice sheet', d='Ice that forms on the surface of the ocean', ans='C',
                         exp='An ice shelf is a floating extension of an ice sheet or glacier where the ice flows from land into the sea. The largest is the Ross Ice Shelf, roughly the size of France.'),
                ]
            ),
            dict(
                module_slug='climate-change-poles',
                title='Climate Change and Polar Regions Quiz',
                description='Test your knowledge of how climate change affects the Arctic and Antarctic.',
                passing_score=60, time_limit=15,
                questions=[
                    dict(q='What is "Arctic amplification"?',
                         a='The reflection of sunlight by Arctic sea ice', b='The process by which the Arctic warms faster than the global average',
                         c='The amplification of radio signals in the Arctic', d='The increase in Arctic biodiversity due to warming', ans='B',
                         exp='Arctic amplification refers to the observation that the Arctic warms at two to four times the global average rate, driven by feedback loops including sea-ice albedo loss.'),
                    dict(q='By approximately how much has Arctic sea ice extent declined per decade since 1979?',
                         a='3%', b='7%', c='13%', d='25%', ans='C',
                         exp='Arctic sea ice has declined at approximately 13% per decade since satellite records began in 1979 — one of the clearest signals of climate change.'),
                    dict(q='What is the "albedo effect" in the context of polar sea ice?',
                         a='Sea ice absorbs more heat than open water', b='Sea ice reflects sunlight back into space, while dark ocean absorbs it',
                         c='Melting ice causes the ocean to become more reflective', d='Clouds over ice are more reflective', ans='B',
                         exp='Sea ice is highly reflective (albedo ~0.9), reflecting most incoming solar radiation. When sea ice melts, the dark ocean beneath absorbs much more heat (albedo ~0.1), causing further warming — a positive feedback loop.'),
                    dict(q='Which global circulation system could be disrupted by melting polar ice sheets?',
                         a='The Hadley Cell', b='The Ferrel Cell', c='The Atlantic Meridional Overturning Circulation (AMOC)', d='The Walker Circulation', ans='C',
                         exp='The Atlantic Meridional Overturning Circulation (AMOC), which includes the Gulf Stream, could be weakened by the influx of cold, fresh meltwater from Greenland into the North Atlantic, potentially disrupting climate across Europe and North America.'),
                    dict(q='What gas, released by thawing Arctic permafrost, is a potent greenhouse gas?',
                         a='Carbon dioxide (CO2)', b='Nitrogen (N2)', c='Methane (CH4)', d='Ozone (O3)', ans='C',
                         exp='Thawing permafrost releases methane (CH4), a greenhouse gas approximately 80 times more potent than CO2 over a 20-year period. This represents a major potential positive feedback on climate change.'),
                    dict(q='Which international agreement designates Antarctica as a "natural reserve, devoted to peace and science"?',
                         a='The Kyoto Protocol', b='The Paris Agreement',
                         c='The Protocol on Environmental Protection to the Antarctic Treaty (Madrid Protocol)', d='The Montreal Protocol', ans='C',
                         exp='The Madrid Protocol (1991, in force 1998) designates Antarctica as a natural reserve devoted to peace and science, banning mineral resource activities and requiring environmental impact assessments.'),
                ]
            ),
            dict(
                module_slug='southern-ocean-climate-engine',
                title='Southern Ocean and Marine Science Quiz',
                description='Test your knowledge of the Southern Ocean and its role in global climate.',
                passing_score=60, time_limit=12,
                questions=[
                    dict(q='What is the Antarctic Circumpolar Current (ACC)?',
                         a='A current that flows from Antarctica to the tropics', b='The largest and most powerful ocean current, flowing eastward around Antarctica',
                         c='A cold current that flows along the South American coast', d='An underwater current beneath the Antarctic Ice Sheet', ans='B',
                         exp='The Antarctic Circumpolar Current is the largest and most powerful ocean current on Earth, flowing continuously eastward around Antarctica and connecting the Atlantic, Pacific and Indian Oceans.'),
                    dict(q='Approximately what percentage of human-emitted CO2 does the Southern Ocean absorb?',
                         a='10%', b='20%', c='40%', d='60%', ans='C',
                         exp='The Southern Ocean absorbs approximately 40% of all anthropogenic CO2 taken up by the world\'s oceans, making it a critically important carbon sink.'),
                    dict(q='What is "Antarctic Bottom Water"?',
                         a='Meltwater that flows beneath the Antarctic Ice Sheet', b='The densest water mass in the ocean, formed when cold, salty water sinks in the Southern Ocean',
                         c='Warm water that flows under Antarctic ice shelves', d='Groundwater beneath the Antarctic continent', ans='B',
                         exp='Antarctic Bottom Water (AABW) forms when surface waters in the Southern Ocean become very cold and salty, causing them to sink to the sea floor. It is the densest water in the ocean and drives a key part of global thermohaline circulation.'),
                    dict(q='Which organism is considered the foundation of the Antarctic food web?',
                         a='Leopard seals', b='Emperor penguins', c='Antarctic krill (Euphausia superba)', d='Toothfish', ans='C',
                         exp='Antarctic krill are small crustaceans that form vast swarms in the Southern Ocean. They feed on phytoplankton and are themselves the primary food source for penguins, seals, whales, fish and seabirds — making them the keystone species of the Antarctic food web.'),
                ]
            ),
        ]

        created = 0
        for qd in quiz_data:
            try:
                module = LearningModule.objects.get(slug=qd['module_slug'])
            except LearningModule.DoesNotExist:
                continue
            if Quiz.objects.filter(module=module).exists():
                continue
            quiz = Quiz.objects.create(
                module=module, title=qd['title'],
                description=qd['description'],
                passing_score=qd['passing_score'],
                time_limit_minutes=qd['time_limit'],
            )
            for i, q in enumerate(qd['questions'], 1):
                Question.objects.create(
                    quiz=quiz, question_text=q['q'],
                    option_a=q['a'], option_b=q['b'],
                    option_c=q['c'], option_d=q['d'],
                    correct_option=q['ans'], explanation=q['exp'], order=i,
                )
            created += 1
        self.stdout.write(f'  ✓ Quizzes: {created} created')

    # ---------------------------------------------------------- expeditions
    def _create_expeditions(self):
        from expeditions.models import Expedition

        exps = [
            dict(
                name='9th Indian Antarctic Expedition',
                slug='9th-indian-antarctic-expedition',
                expedition_year=1989,
                region='antarctica',
                location='Schirmacher Oasis, Queen Maud Land, Antarctica',
                participating_institutions='Department of Ocean Development\nGeological Survey of India\nSurvey of India\nIndia Meteorological Department',
                objectives='Establish India\'s permanent research station Maitri at the Schirmacher Oasis in Queen Maud Land. Conduct geological mapping of the Oasis, establish continuous meteorological and geomagentic monitoring, and begin atmospheric ozone measurements. [DEMONSTRATION DATA]',
                findings='Maitri station successfully established and commissioned. Geological surveys revealed Precambrian basement rocks with significant mineral interest. Continuous instrument records begun for meteorology, geomagnetism and upper atmosphere physics. [DEMONSTRATION DATA]',
                chief_scientist='Dr. S. Bhatt (demonstration)',
                team_size=28,
                duration_days=98,
                is_featured=True,
                is_demo_data=True,
            ),
            dict(
                name='25th Indian Antarctic Expedition',
                slug='25th-indian-antarctic-expedition',
                expedition_year=2005,
                region='antarctica',
                location='Maitri Station, Schirmacher Oasis, Antarctica',
                participating_institutions='National Centre for Antarctic and Ocean Research (NCAOR)\nIndian Institute of Tropical Meteorology\nGeological Survey of India\nBhabha Atomic Research Centre',
                objectives='Conduct long-term monitoring of atmospheric chemistry including ozone, greenhouse gases and aerosols. Geological investigation of the Wohlthat Mountains. Marine biological surveys in coastal waters adjacent to Maitri. Continuation of GPS geodetic observations. [DEMONSTRATION DATA]',
                findings='Significant ozone hole observed over Maitri with minimum total ozone of 165 DU. New geological formations identified in the Wohlthat Mountains. Marine biological data revealed high abundance of diatoms and krill in nearshore waters. GPS measurements showed 3.1 mm/yr of crustal uplift. [DEMONSTRATION DATA]',
                chief_scientist='Dr. M. Ravindran (demonstration)',
                team_size=35,
                duration_days=112,
                is_featured=False,
                is_demo_data=True,
            ),
            dict(
                name='31st Indian Scientific Expedition to Antarctica',
                slug='31st-indian-scientific-expedition-antarctica',
                expedition_year=2011,
                region='antarctica',
                location='Maitri Station & Site Survey for Bharati, East Antarctica',
                participating_institutions='National Centre for Antarctic and Ocean Research (NCAOR)\nNational Institute of Oceanography\nIIT Delhi\nIISc Bangalore',
                objectives='Final site survey and logistics preparation for Bharati station construction at Larsemann Hills. Continuation of long-term atmospheric, glaciological and oceanographic monitoring at Maitri. First deployment of autonomous underwater vehicles in Prydz Bay. [DEMONSTRATION DATA]',
                findings='Bharati station site confirmed with geological and logistical surveys completed. Prydz Bay AUV deployment successfully mapped seafloor topography and current profiles. Southern Ocean survey yielded high-resolution data on water mass properties along the voyage track. [DEMONSTRATION DATA]',
                chief_scientist='Dr. T. Krishnan (demonstration)',
                team_size=42,
                duration_days=120,
                is_featured=False,
                is_demo_data=True,
            ),
            dict(
                name='32nd Indian Scientific Expedition to Antarctica — Bharati Commissioning',
                slug='32nd-indian-scientific-expedition-bharati',
                expedition_year=2012,
                region='antarctica',
                location='Bharati Station, Larsemann Hills & Maitri Station, Schirmacher Oasis',
                participating_institutions='National Centre for Antarctic and Ocean Research (NCAOR)\nMinistry of Earth Sciences\nMECON India (station construction)',
                objectives='Commission India\'s second permanent Antarctic research station, Bharati, at the Larsemann Hills. Establish all scientific instrument programmes at Bharati. Continue research at Maitri station. [DEMONSTRATION DATA]',
                findings='Bharati station successfully commissioned and handed over to NCAOR for scientific operations. The station is designed to operate year-round with solar, wind and diesel hybrid power. First scientific data collected at the new station including oceanographic and atmospheric measurements. [DEMONSTRATION DATA]',
                chief_scientist='Dr. R. Ravindra (demonstration)',
                team_size=52,
                duration_days=130,
                is_featured=True,
                is_demo_data=True,
            ),
            dict(
                name='2nd Indian Arctic Expedition',
                slug='2nd-indian-arctic-expedition',
                expedition_year=2009,
                region='arctic',
                location='Ny-Ålesund, Svalbard, Norway',
                participating_institutions='National Centre for Antarctic and Ocean Research (NCAOR)\nIndian Institute of Tropical Meteorology, Pune\nSpace Applications Centre, ISRO',
                objectives='Conduct second season of research at Himadri station at Ny-Ålesund. Focus on atmospheric aerosol measurements, glaciological surveys of Svalbard glaciers and monitoring of Arctic sea ice from Svalbard. [DEMONSTRATION DATA]',
                findings='High-resolution aerosol optical depth dataset collected, revealing pronounced seasonal cycle. Mass balance of three Svalbard glaciers measured; all three in net negative balance. Sea ice satellite data processed at Himadri contributed to international monitoring efforts. [DEMONSTRATION DATA]',
                chief_scientist='Dr. A. Pattnaik (demonstration)',
                team_size=8,
                duration_days=45,
                is_featured=False,
                is_demo_data=True,
            ),
        ]

        created = 0
        for d in exps:
            if Expedition.objects.filter(slug=d['slug']).exists():
                continue
            Expedition.objects.create(**d)
            created += 1
        self.stdout.write(f'  ✓ Expeditions: {created} created')

    # ---------------------------------------------------------------- media
    def _create_media(self):
        from media_gallery.models import MediaAsset, MediaCategory

        # Ensure categories exist
        cat_map = {}
        for name, slug in [
            ('Antarctic Landscapes', 'antarctic-landscapes'),
            ('Arctic Landscapes',    'arctic-landscapes'),
            ('Scientific Research',  'scientific-research'),
            ('Expedition Photography','expedition-photography'),
            ('Polar Wildlife',       'polar-wildlife'),
            ('Research Stations',    'research-stations'),
        ]:
            cat, _ = MediaCategory.objects.get_or_create(slug=slug, defaults={'name': name})
            cat_map[slug] = cat

        # These are Unsplash embed URLs — illustrative images for the gallery
        # Each clearly captioned as illustrative stock photography
        assets = [
            dict(title='Antarctic Landscape — Iceberg at Sunset', category_slug='antarctic-landscapes',
                 description='A large tabular iceberg drifts in Antarctic waters at sunset. Icebergs like this calve from ice shelves and can be the size of small countries. [Illustrative stock image]',
                 embed_url='', tags='antarctica, iceberg, sunset, landscape',
                 photographer='Unsplash (Illustrative)', location='Southern Ocean',
                 media_type='image'),
            dict(title='Emperor Penguin Colony — Cape Washington', category_slug='polar-wildlife',
                 description='Emperor penguins (Aptenodytes forsteri) congregate at a nesting site. Emperor penguins are the tallest and heaviest penguin species and are uniquely adapted to breed during the Antarctic winter. [Illustrative stock image]',
                 embed_url='', tags='emperor penguin, wildlife, Antarctica, colony',
                 photographer='Unsplash (Illustrative)', location='Cape Washington, Antarctica',
                 media_type='image'),
            dict(title='Arctic Sea Ice from Above', category_slug='arctic-landscapes',
                 description='Aerial view of Arctic sea ice showing the characteristic mosaic of ice floes separated by leads of open water. Sea ice extent at the September minimum has declined by 13% per decade since 1979. [Illustrative stock image]',
                 embed_url='', tags='Arctic, sea ice, aerial, climate change',
                 photographer='Unsplash (Illustrative)', location='Arctic Ocean',
                 media_type='image'),
            dict(title='Aurora Australis Over Antarctica', category_slug='antarctic-landscapes',
                 description='The Southern Lights (Aurora Australis) illuminate the Antarctic sky in shades of green and violet. Auroras are caused by charged solar particles interacting with Earth\'s magnetic field. [Illustrative stock image]',
                 embed_url='', tags='aurora australis, southern lights, night sky, Antarctica',
                 photographer='Unsplash (Illustrative)', location='Antarctica',
                 media_type='image'),
            dict(title='Research Scientist Drilling Ice Core', category_slug='scientific-research',
                 description='A researcher extracts an ice core from the Antarctic ice sheet. Ice cores contain air bubbles that preserve ancient atmosphere, allowing scientists to reconstruct climate conditions hundreds of thousands of years ago. [Illustrative stock image]',
                 embed_url='', tags='ice core, research, glaciology, fieldwork',
                 photographer='Unsplash (Illustrative)', location='Antarctica',
                 media_type='image'),
            dict(title='Humpback Whale Breaching — Southern Ocean', category_slug='polar-wildlife',
                 description='A humpback whale (Megaptera novaeangliae) breaches in the Southern Ocean. Humpback whale populations in the Southern Ocean have recovered significantly since the end of commercial whaling. [Illustrative stock image]',
                 embed_url='', tags='humpback whale, Southern Ocean, marine mammal, wildlife',
                 photographer='Unsplash (Illustrative)', location='Southern Ocean',
                 media_type='image'),
            dict(title='Melt Pond on Arctic Sea Ice', category_slug='arctic-landscapes',
                 description='A blue melt pond sits atop Arctic sea ice in summer. Melt ponds form as surface snow melts in summer, darkening the ice surface and absorbing more solar radiation — a feedback that accelerates sea ice loss. [Illustrative stock image]',
                 embed_url='', tags='melt pond, Arctic sea ice, climate change, feedback',
                 photographer='Unsplash (Illustrative)', location='Arctic Ocean',
                 media_type='image'),
            dict(title='Research Vessel in Pack Ice', category_slug='expedition-photography',
                 description='A polar research vessel navigates through pack ice. India\'s research vessels regularly make the voyage to Antarctica through the Southern Ocean, one of the stormiest seas on Earth. [Illustrative stock image]',
                 embed_url='', tags='research vessel, pack ice, expedition, Antarctic voyage',
                 photographer='Unsplash (Illustrative)', location='Southern Ocean',
                 media_type='image'),
            dict(title='Polar Bear on Sea Ice — Arctic', category_slug='polar-wildlife',
                 description='A polar bear (Ursus maritimus) stands on Arctic sea ice. Polar bears depend on sea ice as a platform for hunting seals. Declining sea ice threatens their survival. [Illustrative stock image]',
                 embed_url='', tags='polar bear, Arctic, sea ice, wildlife, climate',
                 photographer='Unsplash (Illustrative)', location='Arctic',
                 media_type='image'),
            dict(title='Glacial Calving Event — Antarctic Ice Shelf', category_slug='antarctic-landscapes',
                 description='A large section of ice calves from an Antarctic ice shelf, sending a cascade of ice and water into the ocean. Ice calving events are a primary mechanism of ice sheet mass loss. [Illustrative stock image]',
                 embed_url='', tags='calving, ice shelf, Antarctica, glaciology',
                 photographer='Unsplash (Illustrative)', location='Antarctic Peninsula',
                 media_type='image'),
            dict(title='Atmospheric Research at a Polar Station', category_slug='research-stations',
                 description='Instruments at a polar research station measure atmospheric composition, including ozone, greenhouse gases and aerosols. Continuous monitoring at polar stations provides critical long-term datasets. [Illustrative stock image]',
                 embed_url='', tags='atmospheric research, polar station, instruments, ozone monitoring',
                 photographer='Unsplash (Illustrative)', location='Research Station',
                 media_type='image'),
            dict(title='Adélie Penguins on Ice Floe', category_slug='polar-wildlife',
                 description='A group of Adélie penguins (Pygoscelis adeliae) stand on a drifting ice floe. Adélie penguins are highly dependent on sea ice and are considered reliable indicators of changes in the Antarctic ecosystem. [Illustrative stock image]',
                 embed_url='', tags='Adélie penguin, sea ice, Antarctica, wildlife',
                 photographer='Unsplash (Illustrative)', location='Ross Sea, Antarctica',
                 media_type='image'),
        ]

        # Unsplash image URLs (free to use, illustrative stock photos)
        image_urls = [
            'https://images.unsplash.com/photo-1517783999520-f068d7431a60?w=800&q=80',
            'https://images.unsplash.com/photo-1467579424161-6bdd8ef27cfc?w=800&q=80',
            'https://images.unsplash.com/photo-1508193638397-1c4234db14d8?w=800&q=80',
            'https://images.unsplash.com/photo-1476610182048-b716b8518aae?w=800&q=80',
            'https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=800&q=80',
            'https://images.unsplash.com/photo-1551009175-15bdf9dcb580?w=800&q=80',
            'https://images.unsplash.com/photo-1534447677768-be436bb09401?w=800&q=80',
            'https://images.unsplash.com/photo-1519832979-6fa011b87667?w=800&q=80',
            'https://images.unsplash.com/photo-1562177916-8b097f2b8842?w=800&q=80',
            'https://images.unsplash.com/photo-1547471080-7cc2caa01a7e?w=800&q=80',
            'https://images.unsplash.com/photo-1504457047772-27faf1c00561?w=800&q=80',
            'https://images.unsplash.com/photo-1555021946-a568e9d4a0cb?w=800&q=80',
        ]

        created = 0
        for i, d in enumerate(assets):
            if MediaAsset.objects.filter(title=d['title']).exists():
                continue
            cat_slug = d.pop('category_slug')
            cat = cat_map.get(cat_slug)
            # Remove embed_url from d (we set it explicitly below)
            d.pop('embed_url', None)
            d['media_type'] = 'embed'   # override media_type
            asset = MediaAsset(
                category=cat,
                embed_url=image_urls[i % len(image_urls)],
                allow_download=True,
                is_featured=(i < 4),
                **d,
            )
            asset.save()
            created += 1
        self.stdout.write(f'  ✓ Media assets: {created} created')

    # ------------------------------------------------------------- stations
    def _create_stations(self):
        from stations.models import ResearchStation, MapLocation

        stations = [
            dict(name='Himadri Station (India)', slug='himadri-station',
                 region='arctic', country='India',
                 operating_institution='National Centre for Polar and Ocean Research (NCPOR)',
                 latitude=78.92, longitude=11.93, established_year=2008,
                 description='India\'s Arctic research station at Ny-Ålesund, Svalbard, Norway. Operated by NCPOR, Himadri is used for seasonal research on Arctic atmospheric science, glaciology and marine biology. The station shares the Ny-Ålesund International Arctic Research and Monitoring Facility with researchers from more than 10 other nations. [DEMONSTRATION DATA — verify details from official NCPOR sources.]',
                 research_activities='Atmospheric aerosol monitoring, ozone measurements, Arctic glacier mass balance, sea ice remote sensing, marine biology surveys.',
                 is_active=True, is_demo_data=True),
            dict(name='Dakshin Gangotri (India — Historic)', slug='dakshin-gangotri',
                 region='antarctica', country='India',
                 operating_institution='National Centre for Polar and Ocean Research (NCPOR)',
                 latitude=-70.09, longitude=11.93, established_year=1983,
                 description='India\'s first Antarctic base camp, established in 1983 during the 3rd Indian Antarctic Expedition. Located in the Dronning Maud Land region, the station was used for scientific research until 1990 when it was decommissioned after being partially buried by advancing ice. It now serves as a supply depot during annual expeditions. [DEMONSTRATION DATA]',
                 research_activities='Historical: meteorology, glaciology, upper atmosphere physics. Currently used as a supply depot.',
                 is_active=False, is_demo_data=True),
        ]

        locations = [
            dict(name='Prydz Bay', location_type='landmark', latitude=-69.0, longitude=74.0,
                 description='A large bay in East Antarctica adjacent to India\'s Bharati Station. It is an important area for oceanographic research and hosts significant populations of Antarctic krill and penguins.',
                 research_activities='Physical oceanography, marine biology, sea ice monitoring.',
                 is_demo_data=False),
            dict(name='Schirmacher Oasis', location_type='landmark', latitude=-70.77, longitude=11.73,
                 description='A 34 km long, ice-free rocky oasis in the Dronning Maud Land region of East Antarctica. India\'s Maitri station is located here. The Oasis is unusual for Antarctica in having exposed rock and even freshwater lakes.',
                 research_activities='Geological research, biology of freshwater ecosystems, glaciological boundary studies.',
                 is_demo_data=False),
            dict(name='Larsemann Hills', location_type='landmark', latitude=-69.41, longitude=76.19,
                 description='An ice-free coastal area in Prydz Bay, East Antarctica, home to India\'s Bharati Station. The Hills are a biodiversity hotspot for Antarctic mosses and invertebrates.',
                 research_activities='Oceanography, atmospheric science, biology, geology.',
                 is_demo_data=False),
            dict(name='Thwaites Glacier', location_type='landmark', latitude=-75.5, longitude=-107.0,
                 description='Nicknamed the "Doomsday Glacier", Thwaites is one of the fastest-retreating and most closely monitored glaciers in Antarctica. Its collapse could ultimately raise global sea levels by approximately 65 cm.',
                 research_activities='Glaciological surveys, basal melting studies, oceanographic measurements beneath ice shelf.',
                 is_demo_data=False),
        ]

        created_s = 0
        for d in stations:
            if ResearchStation.objects.filter(slug=d['slug']).exists():
                continue
            ResearchStation.objects.create(**d)
            created_s += 1

        created_l = 0
        for d in locations:
            if MapLocation.objects.filter(name=d['name']).exists():
                continue
            MapLocation.objects.create(**d)
            created_l += 1

        self.stdout.write(f'  ✓ Research stations: {created_s} created, map locations: {created_l} created')

    # ----------------------------------------------------------- community
    def _create_community(self):
        from community.models import DiscussionForum, Discussion, Comment
        from accounts.models import CustomUser

        users = {u.username: u for u in CustomUser.objects.all()}
        researcher = users.get('dr_sharma') or CustomUser.objects.filter(role='researcher').first()
        educator   = users.get('ananya_edu') or CustomUser.objects.filter(role='educator').first()
        student    = users.get('ravi_student') or CustomUser.objects.filter(role='student').first()
        public_u   = users.get('meera_pub') or CustomUser.objects.filter(role='general_user').first()
        admin_u    = CustomUser.objects.filter(is_staff=True).first()

        if not researcher:
            self.stdout.write('  ⚠ No users found — skipping community data')
            return

        forums = {f.slug: f for f in DiscussionForum.objects.all()}

        discussions_data = [
            dict(
                forum_slug='ask-a-scientist',
                author_obj=student or admin_u,
                title='Why does Antarctica get colder than the Arctic even though both are polar regions?',
                content='''I\'ve been reading about polar temperatures and I\'m confused. The Arctic and Antarctic are both near the poles, so shouldn\'t they be roughly the same temperature? But apparently Antarctica is much colder. Can someone explain why?

I know Antarctica has a continental ice sheet and the Arctic is mostly ocean, but I don\'t fully understand why that makes such a big difference to the temperature.''',
                is_question=True,
                comments=[
                    dict(author_obj=researcher or admin_u, is_answer=True,
                         content='''Great question! There are three main reasons Antarctica is significantly colder than the Arctic:

**1. Elevation**
Antarctica sits on a high continental plateau averaging about 2,300 metres above sea level. Temperature decreases with altitude (the lapse rate), so the high elevation makes it substantially colder. The Arctic is mostly at sea level.

**2. The ocean's moderating effect**
The Arctic Ocean, even when frozen, moderates temperatures because ocean water retains heat from summer. Antarctica is surrounded by ocean but sits atop a landmass — the continent itself has no stored heat to moderate winter temperatures.

**3. Cold air drainage**
In Antarctica, cold, dense air from the high interior plateau drains down toward the coast as katabatic winds. This constantly replaces any warmed air with fresh cold air from the interior.

The result: the South Pole averages about −49°C annually, while the North Pole averages about −18°C. The world's lowest recorded temperature — −89.2°C — was at Vostok Station, Antarctica.

For India's polar research, this difference matters because Maitri station (which sits at a relatively low elevation in the Schirmacher Oasis) is actually somewhat warmer than other Antarctic locations at the same latitude!'''),
                    dict(author_obj=educator or admin_u, is_answer=False,
                         content='''Adding to the excellent answer above — this is also why Antarctica has such different ecosystems from the Arctic.

The Arctic is warm enough for some land plants, land mammals (polar bears, Arctic foxes, lemmings) and has been inhabited by humans for thousands of years. Antarctica is so cold that virtually no land plants or animals survive on the continent itself — all Antarctic wildlife is ultimately dependent on the ocean, not the land.

This is a great topic for the classroom! I use the temperature comparison to introduce the concept of heat capacity and why oceans moderate coastal climates.'''),
                ]
            ),
            dict(
                forum_slug='research-discussions',
                author_obj=researcher or admin_u,
                title='New GRACE-FO results for WAIS — anyone working on GIA corrections?',
                content='''I\'ve been looking at the latest GRACE-FO mass balance results for the West Antarctic Ice Sheet and I\'m noticing significant spread between the different GIA model corrections. The ICE-6G_C model gives quite different results from W12 in the Amundsen Sea Embayment.

Is anyone else working on this? I\'d be interested in whether bedrock GPS data from the POLENET network is helping to constrain this — the last I checked, there was quite limited coverage in the WAIS interior.

We have GPS data from near Maitri in the EAIS which shows uplift rates slightly higher than the ICE-6G_C model predicts, but I\'m not sure how transferable that result is to the WAIS setting.''',
                is_question=True,
                comments=[
                    dict(author_obj=admin_u, is_answer=False,
                         content='''This is a really active area right now. The Thwaites Glacier region in particular has very limited bedrock GPS coverage, which is a known source of uncertainty in mass balance estimates.

The POLENET/ANET network has been expanding over the last few years and there are now a few more GPS stations in the interior, but coverage is still sparse.

One approach I\'ve seen in recent papers is to use seismic-based estimates of lithospheric thickness and viscosity to generate regionally tuned GIA models rather than relying on global models. This seems to reduce the spread between models in the WAIS considerably.

Your EAIS GPS data sounds interesting — have you tried comparing with the ANU/Whitehouse (W12a) model specifically? In my experience it performs better for EAIS than ICE-6G_C.'''),
                ]
            ),
            dict(
                forum_slug='student-zone',
                author_obj=student or admin_u,
                title='I want to work in polar science — what subjects should I study?',
                content='''I\'m in Class 12 and I\'m really passionate about climate change and polar regions after using this portal and learning about Antarctica. I want to eventually work as a polar scientist or go on an Antarctic expedition.

What subjects should I study at university? Is there a specific degree for polar science? Which universities or institutes in India are best for this?

Any advice from researchers or students who are already in this field would be really helpful!''',
                is_question=True,
                comments=[
                    dict(author_obj=researcher or admin_u, is_answer=True,
                         content='''What a great aspiration! Indian polar science needs enthusiastic young scientists. Here\'s a practical roadmap:

**Undergraduate (B.Sc/B.Tech)**
Polar science draws from many disciplines. Useful undergraduate subjects include:
- Physics, Mathematics, Earth Sciences, Oceanography → for atmospheric/glaciological science
- Biology, Zoology → for marine biology/ecology
- Geology, Geography → for geological or geophysical research
- Engineering (Mechanical, Electronics) → for instrument development and station technology

The best institutions for Earth/Ocean sciences in India include IIT Kharagpur (Ocean Engineering), IIT Madras, IISc Bangalore, University of Pune, Cochin University of Science and Technology, and BHU Varanasi.

**Postgraduate (M.Sc)**
Consider specialising in one of: Polar Oceanography, Atmospheric Science, Glaciology, Marine Biology or Geophysics.

**PhD and Research Opportunities**
NCPOR (Goa) offers PhD programmes and research fellowships specifically in polar and ocean sciences. IITM Pune, NIO Goa and WIHG Dehradun also do polar-related research.

**The Antarctic Expedition**
Participation in expeditions is typically available to PhD students and postdoctoral researchers associated with NCPOR or collaborating institutions. Building a strong research track record is key.

Good luck — the polar science community in India is welcoming and needs new talent!'''),
                    dict(author_obj=educator or admin_u, is_answer=False,
                         content='''I teach science at school and several of my students have gone into environmental and ocean science careers.

One additional tip: start engaging with polar science NOW — even as a Class 12 student. Use this portal, read accessible books like "The Ice at the End of the World" by Jon gertner, follow NCPOR on social media and try to attend public lectures at universities near you.

The essay competition listed in the Events section is a perfect opportunity to deepen your knowledge and get recognised. Some essay competition winners have gone on to receive invitations to visit NCPOR!'''),
                ]
            ),
            dict(
                forum_slug='climate-environment',
                author_obj=public_u or admin_u,
                title='If Arctic sea ice is melting, why do we still get cold winters in India?',
                content='''I keep reading that the Arctic is warming and sea ice is declining. But last winter was really cold in Delhi and there were reports of cold waves across north India.

If the Arctic is warming, shouldn\'t winters everywhere be getting warmer? I\'m confused by the apparent contradiction. Can someone explain what\'s actually happening?''',
                is_question=True,
                comments=[
                    dict(author_obj=researcher or admin_u, is_answer=True,
                         content='''This is one of the most common and important misconceptions about climate change — and it\'s a great question.

**Global warming doesn\'t mean every place gets uniformly warmer every year.** It means the average global temperature is rising, and that rising average comes with *more variability* in some regions.

Here\'s specifically what\'s happening with cold waves in South Asia:

**The Polar Vortex Connection**
When the Arctic warms rapidly (Arctic amplification), it weakens the temperature gradient between the Arctic and mid-latitudes. This weakens the polar jet stream, which normally acts like a wall keeping cold Arctic air locked in the north.

A weaker jet stream meanders more. Sometimes those meanders become so extreme that a lobe of bitterly cold Arctic air gets pushed far south — into Europe, Central Asia or northern India. This is a "polar vortex disruption."

**What the research shows**
While extreme cold events like this may happen in individual winters, the LONG-TERM trend is clearly toward:
- Warmer average winter temperatures across India
- Fewer cold days overall
- But potentially more intense cold intrusions linked to polar vortex disruption

So you can have a record cold week in Delhi AND a record warm year globally — these are not contradictory.

**The Bottom Line**
Climate change isn\'t just "everything gets uniformly warmer." It disrupts weather patterns in complex ways, some of which include more extreme events at the cold end of the spectrum in some locations, even as the global average warms.'''),
                    dict(author_obj=educator or admin_u, is_answer=False,
                         content='''This is exactly the kind of question we should be discussing more in schools. The confusion between weather (what\'s happening today, this week, this season) and climate (long-term trends over decades) is at the root of a lot of public misunderstanding.

A good analogy: imagine you have a fever of 39°C. Your average body temperature is elevated. But you might still have moments of chills and shivering. The overall trend is toward higher temperature even if individual moments feel cold.

The PolarConnect learning modules cover the polar vortex in detail — worth exploring those if you want to understand the mechanism more fully!'''),
                ]
            ),
        ]

        created_d, created_c = 0, 0
        for dd in discussions_data:
            forum = forums.get(dd['forum_slug'])
            if not forum:
                continue
            if Discussion.objects.filter(title=dd['title']).exists():
                disc = Discussion.objects.get(title=dd['title'])
            else:
                disc = Discussion.objects.create(
                    forum=forum, author=dd['author_obj'],
                    title=dd['title'], content=dd['content'],
                    is_question=dd.get('is_question', False),
                    view_count=random.randint(50, 400),
                )
                created_d += 1
            for cd in dd.get('comments', []):
                if not Comment.objects.filter(discussion=disc, content=cd['content'][:50]).exists():
                    Comment.objects.create(
                        discussion=disc, author=cd['author_obj'],
                        content=cd['content'], is_answer=cd.get('is_answer', False),
                    )
                    created_c += 1

        self.stdout.write(f'  ✓ Discussions: {created_d} created, comments: {created_c} created')
