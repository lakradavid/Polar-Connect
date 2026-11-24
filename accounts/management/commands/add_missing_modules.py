"""
Management command: python manage.py add_missing_modules
Adds full learning modules + quizzes for:
  - Antarctic Ecosystems
  - Arctic Ecosystems
  - Polar Wildlife
"""
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Add learning modules for Antarctic Ecosystems, Arctic Ecosystems and Polar Wildlife'

    def handle(self, *args, **options):
        from education.models import LearningCategory, LearningModule, Quiz, Question
        self.stdout.write('Adding missing learning modules...\n')

        created_m = 0
        created_q = 0

        # ----------------------------------------------------------------
        # DATA DEFINITIONS
        # ----------------------------------------------------------------
        modules = [

            # ============================================================
            # ANTARCTIC ECOSYSTEMS  (3 modules)
            # ============================================================
            dict(
                category_slug='antarctic-ecosystems',
                title='Life in Antarctica: An Overview',
                slug='life-in-antarctica-overview',
                description='Discover how life survives and thrives in one of the harshest environments on Earth.',
                difficulty='beginner',
                duration=25,
                order=1,
                content='''\
Antarctica is the coldest, driest and windiest continent on Earth — and yet it is teeming with life. That life, however, is concentrated almost entirely at the edges of the continent and in the surrounding Southern Ocean. The interior ice sheet is essentially barren, but the coastlines, ice shelves and open waters host rich and highly productive ecosystems.

## Why Antarctica Has Such Unique Ecosystems

Antarctic ecosystems are shaped by four extreme conditions:

**1. Cold**
Temperatures in coastal Antarctica range from about 0°C in summer to −40°C in winter. The surrounding Southern Ocean stays between −1.8°C and +2°C year-round. These cold temperatures slow down biological processes but also allow seawater to hold large amounts of dissolved oxygen, supporting rich marine life.

**2. Light Seasonality**
Antarctica experiences extreme seasonal light cycles. In summer (November–February), the sun never sets. In winter, there is complete darkness for months. This creates intense seasonal booms in biological productivity — particularly phytoplankton blooms that form the base of the food web.

**3. Sea Ice**
Sea ice forms each winter, roughly doubling Antarctica's area, and melts each summer. It is a critical habitat — the underside of sea ice is colonised by ice algae, which is the primary food source for krill, which in turn feeds almost everything else.

**4. Isolation**
Antarctica has been isolated from other continents for about 30 million years. This has created highly endemic species — animals found nowhere else on Earth — and an ecosystem with relatively few species but enormous populations of those that do exist.

## The Trophic Structure: Who Eats Whom

The Antarctic food web is remarkably simple and linear:

**Phytoplankton** (microscopic algae) → **Krill** → **Penguins, seals, whales, fish, seabirds**

Antarctic krill (*Euphausia superba*) is the keystone species — the linchpin of the entire ecosystem. It is estimated that there are 300–500 million tonnes of krill in the Southern Ocean. Almost every large animal in Antarctica depends on krill, directly or indirectly.

## Life on Land

The continent itself supports very little life. There are no land mammals, no reptiles, no amphibians and almost no land plants. What exists includes:

- **Mosses and liverworts**: Found on rocky outcrops near the coast. Some mosses can survive at temperatures as low as −15°C.
- **Lichens**: The most widespread land organisms in Antarctica; over 400 species survive here.
- **Bacteria and algae**: Microorganisms colonise rocks, soils and even the interior of translucent rocks (endolithic organisms), where they absorb enough light to survive.
- **Mites and springtails**: Tiny invertebrates — the largest purely land animals in Antarctica. The Antarctic midge (*Belgica antarctica*) is the continent's largest land animal at just 6 mm long.

## Life in the Sea

The Southern Ocean is extraordinarily productive. Key groups include:

- **Phytoplankton**: Diatoms are the dominant group, blooming spectacularly in spring and summer
- **Zooplankton**: Dominated by Antarctic krill and copepods
- **Fish**: About 320 species, including the Antarctic toothfish (*Dissostichus mawsoni*), prized for its antifreeze proteins
- **Marine mammals**: 6 species of seal, baleen whales, sperm whales and orcas
- **Seabirds**: 46 species breed in Antarctica or on sub-Antarctic islands, including 5 species of penguin

## Why This Ecosystem Matters Globally

The Southern Ocean biological pump — the process by which phytoplankton absorb CO₂ at the surface and sink carbon to the deep ocean when they die — sequesters an estimated 0.3 billion tonnes of carbon per year. Changes in Antarctic ecosystems thus have global implications for the carbon cycle and climate regulation.

**[This module contains demonstration content for educational purposes. PolarConnect, Ministry of Earth Sciences, India.]**
''',
                quiz=dict(
                    title='Antarctic Ecosystems Quiz',
                    description='Test your understanding of life in Antarctic environments.',
                    passing_score=60,
                    time_limit=12,
                    questions=[
                        dict(q='What is the keystone species of the Antarctic food web?',
                             a='Emperor penguin', b='Antarctic krill (Euphausia superba)',
                             c='Leopard seal', d='Antarctic toothfish',
                             ans='B',
                             exp='Antarctic krill is the keystone species — almost every large animal in Antarctica depends on it, directly or indirectly. There are an estimated 300–500 million tonnes of krill in the Southern Ocean.'),
                        dict(q='What is the largest purely terrestrial animal found on the Antarctic continent?',
                             a='A species of beetle', b='The Antarctic wolf spider',
                             c='The Antarctic midge (Belgica antarctica)', d='A species of earthworm',
                             ans='C',
                             exp='The Antarctic midge (Belgica antarctica) is just 6 mm long and is the largest animal that lives its entire life cycle on the Antarctic continent itself.'),
                        dict(q='Why is sea ice critically important to the Antarctic ecosystem?',
                             a='It reflects sunlight, keeping Antarctica cold', b='It provides a breeding platform for all Antarctic penguins',
                             c='Its underside is colonised by ice algae that feed krill', d='It prevents warm ocean water from reaching the continent',
                             ans='C',
                             exp='The underside of Antarctic sea ice is colonised by ice algae, which forms the primary food source for Antarctic krill, particularly in winter when open-water phytoplankton is scarce.'),
                        dict(q='Approximately how many species of seabird breed in Antarctica or on sub-Antarctic islands?',
                             a='8', b='20', c='46', d='120',
                             ans='C',
                             exp='About 46 species of seabird breed in Antarctica or on sub-Antarctic islands, including penguins, albatrosses, petrels, skuas and terns.'),
                        dict(q='Which group of microscopic organisms forms the base of the Antarctic marine food web?',
                             a='Bacteria', b='Phytoplankton (especially diatoms)', c='Zooplankton', d='Lichens',
                             ans='B',
                             exp='Phytoplankton — microscopic algae dominated by diatoms — form the base of the Antarctic marine food web. They undergo spectacular blooms in spring and summer when sea ice retreats and sunlight returns.'),
                    ]
                )
            ),

            dict(
                category_slug='antarctic-ecosystems',
                title='Penguins: Masters of the Frozen South',
                slug='penguins-masters-frozen-south',
                description='A deep dive into the biology, behaviour and ecology of Antarctica\'s most iconic birds.',
                difficulty='beginner',
                duration=30,
                order=2,
                content='''\
Penguins are arguably the most recognisable animals on Earth. Five species breed in Antarctica itself, while another 13 species are found on sub-Antarctic islands and other southern landmasses. Far from being clumsy creatures, penguins are superbly adapted to one of the planet's harshest environments.

## Penguin Species in Antarctica

**Emperor Penguin** (*Aptenodytes forsteri*)
The largest penguin — up to 1.2 m tall and 40 kg. The only penguin that breeds during the Antarctic winter, in temperatures as low as −60°C with wind speeds exceeding 200 km/h. The male incubates the single egg on his feet for 65 days, surviving without food. Huddles of thousands of males rotate from the exposed outer edge to the warm centre of the huddle, maintaining a core temperature of 37°C even in extreme cold.

**Adélie Penguin** (*Pygoscelis adeliae*)
One of the most studied and abundant Antarctic penguins. Breeds in large coastal colonies in spring and summer. A classic indicator species — changes in Adélie population size and distribution are closely correlated with sea ice extent and krill availability.

**Chinstrap Penguin** (*Pygoscelis antarcticus*)
Named for the thin black line under the chin. Breeds primarily on the Antarctic Peninsula and sub-Antarctic islands. Population trends show significant regional variation linked to changing sea ice conditions.

**Gentoo Penguin** (*Pygoscelis papua*)
The fastest swimming penguin — clocked at up to 36 km/h underwater. Currently expanding its range southward as the Antarctic Peninsula warms.

**Macaroni Penguin** (*Eudyptes chrysolophus*)
The most numerous penguin species; about 18 million breeding pairs worldwide, primarily on sub-Antarctic islands.

## Adaptations to Extreme Cold

**Feathers**: Penguins have the highest feather density of any bird — about 100 feathers per square centimetre. These create a waterproof, windproof outer layer and an insulating inner layer.

**Counter-current heat exchange**: Warm arterial blood flowing to the flippers runs alongside cold venous blood returning from them. Heat is transferred from outgoing to returning blood, minimising heat loss to the environment.

**Body shape**: The compact, streamlined body minimises surface area exposed to cold and reduces drag in water.

**Subcutaneous fat**: A thick layer of fat beneath the skin provides insulation and an energy reserve during fasting periods (which can last months in emperor penguins).

## Penguin Diving Abilities

Emperor penguins are remarkable divers:
- Maximum recorded depth: **565 metres**
- Maximum dive duration: **22 minutes**
- Routine dives: 150–300 metres for 5–8 minutes

Their bones are denser than other birds (reducing buoyancy), and they can tolerate very low blood oxygen levels by slowing their heart rate and redirecting blood away from non-essential organs.

## Penguins as Climate Indicators

Penguin populations are sensitive indicators of environmental change. Their prey (primarily krill and fish) is closely linked to sea ice extent and ocean temperature. Studies of penguin colonies over decades have revealed:

- Adélie penguin colonies near the Antarctic Peninsula have declined by up to 65% in some areas as sea ice retreats
- Emperor penguin colonies in some regions are threatened as sea ice — where they breed — forms later and breaks up earlier each year
- Gentoo penguins, which prefer ice-free water, are expanding southward as conditions warm

India's polar scientists have contributed to global penguin monitoring during Antarctic expeditions, collecting population data and tracking colony health near Indian research stations.

**[Demonstration content for PolarConnect educational portal, Ministry of Earth Sciences, India.]**
''',
                quiz=None
            ),

            dict(
                category_slug='antarctic-ecosystems',
                title='Seals and Whales of the Southern Ocean',
                slug='seals-whales-southern-ocean',
                description='Explore the marine mammals that make the Southern Ocean one of the richest ecosystems on Earth.',
                difficulty='intermediate',
                duration=35,
                order=3,
                content='''\
The Southern Ocean surrounding Antarctica supports six species of seal and a diverse array of cetaceans — whales and dolphins — that together represent some of the most spectacular marine wildlife on Earth. Understanding these animals gives us deep insight into how polar ecosystems function.

## Antarctic Seals

**Weddell Seal** (*Leptonychotes weddellii*)
The world's most southerly mammal. Lives further south than any other seal, beneath fast ice near the Antarctic continent. Maintains breathing holes by rasping the ice with its teeth — a habit that wears teeth down over time, eventually limiting lifespan. Can dive to 600 metres for up to 80 minutes. Weddell seals are considered an important indicator of Southern Ocean health.

**Crabeater Seal** (*Lobodon carcinophaga*)
Despite the name, it eats almost exclusively Antarctic krill — using specialised sieve-like teeth to filter them from water. The most abundant seal in the world, with an estimated population of 15–40 million. The crabeater seal's extraordinary abundance is a direct result of the explosion in krill availability following the near-extinction of baleen whales last century.

**Leopard Seal** (*Hydrurga leptonyx*)
An apex predator of the Antarctic marine ecosystem. Feeds on penguins, fish, squid and other seals. The second-largest seal in Antarctica. Known for waiting below penguin colonies as birds enter or exit the water, timing strikes with remarkable precision. Also feeds heavily on krill and fish outside the breeding season.

**Ross Seal** (*Ommatophoca rossii*)
The rarest and least-studied Antarctic seal. Lives in heavy pack ice, making it extremely difficult to observe. Known from relatively few specimens.

**Antarctic Fur Seal** (*Arctocephalus gazella*)
Unlike the true seals above, the fur seal has visible external ears and can rotate its hind flippers to walk on land. Was hunted almost to extinction for its dense, soft underfur in the 18th and 19th centuries. Now recovered to approximately 4 million individuals, primarily breeding on South Georgia Island.

**Southern Elephant Seal** (*Mirounga leonina*)
The world's largest seal — males can reach 4 metres and 2,200 kg. Can dive to 1,500 metres for up to 2 hours, making it one of the deepest-diving mammals. Breeds on sub-Antarctic islands; feeds on squid and fish in deep Southern Ocean waters.

## Whales of the Southern Ocean

**Blue Whale** (*Balaenoptera musculus*)
The largest animal ever to have lived on Earth — up to 30 metres and 150 tonnes. The Antarctic blue whale (*B. m. intermedia*) feeds almost exclusively on krill in summer. Was hunted to near extinction — population fell from an estimated 200,000–300,000 to fewer than 400 by the mid-20th century. Now slowly recovering but remains endangered.

**Humpback Whale** (*Megaptera novaeangliae*)
Famous for its complex songs and spectacular breaching behaviour. Migrates from tropical breeding grounds to Antarctic feeding grounds each summer, consuming up to 1.4 tonnes of krill per day. Population has recovered significantly since the end of commercial whaling.

**Minke Whale** (*Balaenoptera bonaerensis*)
The Antarctic minke whale is the most numerous baleen whale in the Southern Ocean. Much smaller than other baleen whales — 7–10 metres. The subject of ongoing scientific research by Japan and international bodies. Population estimated at 500,000–750,000.

**Orca (Killer Whale)** (*Orcinus orca*)
Not technically a whale but the largest dolphin. The Southern Ocean hosts several genetically distinct orca populations (ecotypes) that specialise in different prey: Type A orcas hunt minke whales; Type B hunt seals and penguins; Type C (the smallest) eat fish; Type D are enigmatic deep-water hunters. This specialisation is unique among mammals.

## Why These Animals Matter to Science

Marine mammals are long-lived, wide-ranging predators that integrate ecological information across vast areas of ocean. Their population trends, body condition and reproductive success reflect the health of the entire Southern Ocean ecosystem. India's Antarctic expeditions include regular surveys of marine mammal populations in the waters near Maitri and Bharati stations.

**[Demonstration content for PolarConnect educational portal, Ministry of Earth Sciences, India.]**
''',
                quiz=None
            ),

            # ============================================================
            # ARCTIC ECOSYSTEMS  (3 modules)
            # ============================================================
            dict(
                category_slug='arctic-ecosystems',
                title='The Arctic Ecosystem: Land, Ice and Sea',
                slug='arctic-ecosystem-land-ice-sea',
                description='Explore the interconnected land, sea ice and ocean ecosystems of the Arctic region.',
                difficulty='beginner',
                duration=30,
                order=1,
                content='''\
The Arctic is fundamentally different from Antarctica. Where Antarctica is a continent surrounded by ocean, the Arctic is an ocean surrounded by land. This seemingly simple difference has enormous consequences for its ecosystems — the Arctic is warmer, more biodiverse and has been home to human communities for thousands of years.

## The Arctic Defined

The Arctic can be defined in several ways:
- **The Arctic Circle** (66.5°N): The latitude above which the sun stays up for at least 24 hours in summer and stays down for at least 24 hours in winter
- **The 10°C July isotherm**: The boundary where average July temperatures stay below 10°C — roughly coinciding with the treeline
- **The sea ice boundary**: The region covered by sea ice for at least part of the year

The Arctic Ocean covers about 14 million km² and is permanently ice-covered at its centre but seasonally ice-free at its margins.

## Arctic Marine Ecosystem

**The Productive Ocean**
Unlike the deep, isolated Southern Ocean, the Arctic Ocean receives substantial inputs of nutrients from surrounding rivers and continental shelves, making it highly productive in summer. The Arctic shelf seas — the Barents Sea, Chukchi Sea and Beaufort Sea — are among the most productive marine ecosystems on Earth.

**Arctic Phytoplankton**
When sea ice retreats in spring, light penetrates the ocean and triggers massive phytoplankton blooms. Recent research has discovered that phytoplankton blooms can also occur underneath sea ice when it is thin enough to transmit sufficient light — previously unrecognised productivity.

**Arctic Cod** (*Boreogadus saida*)
The Arctic cod plays a role in the Arctic equivalent to krill in the Antarctic — it is the critical link between zooplankton and larger predators. Almost everything in the Arctic marine ecosystem eats Arctic cod: seabirds, seals, beluga whales, narwhals and polar bears.

## Arctic Sea Ice as Habitat

Sea ice is not simply frozen ocean — it is a complex, three-dimensional habitat. The ice surface hosts polar bears and seals; the underside is colonised by ice algae; brine channels within the ice host bacteria and protists; and the ice-water interface is a critical hunting and breeding zone for numerous species.

**Ringed Seal** (*Pusa hispida*): The most common Arctic seal and the primary prey of polar bears. Creates and maintains breathing holes in sea ice. Gives birth in snow lairs on top of sea ice, hidden from aerial predators.

**Polar Bear** (*Ursus maritimus*): The world's largest terrestrial predator. Almost entirely dependent on sea ice for access to ringed seals. Has the longest fasting period of any bear — females in some populations go without food for up to 8 months.

## Arctic Tundra

Beyond the coastline lies the tundra — a treeless, permafrost-underlain landscape that covers about 5.5 million km². Despite its austere appearance, the tundra is surprisingly biodiverse in summer:

**Plants**: Dwarf willows, sedges, grasses, mosses, lichens and cotton grass. All grow low to the ground to avoid desiccating wind.

**Mammals**: Arctic fox, Arctic hare, Arctic wolf, musk ox, lemmings, ground squirrels, caribou/reindeer and wolverine.

**Birds**: Over 200 species migrate to the Arctic in summer to breed, taking advantage of the explosion of insect life and long days. Arctic terns make the longest migration of any animal — from the Arctic to Antarctica and back each year.

**Insects**: Mosquitoes, blackflies, bumblebees and beetles are present in remarkable numbers during the brief Arctic summer.

## The Arctic Food Web

**Land**: Vegetation → Lemmings/hares/caribou → Arctic foxes/wolves/snowy owls/peregrine falcons

**Sea**: Phytoplankton → Zooplankton/Arctic cod → Seabirds/seals/beluga whales/narwhals → Polar bears/orcas

## Connections to India

India monitors Arctic ecosystems through its Himadri station at Ny-Ålesund, Svalbard. Research focuses on how Arctic changes — particularly sea ice decline and permafrost thaw — affect global weather patterns, including the Indian monsoon. Indian scientists have documented correlations between Arctic sea ice extent in autumn and the subsequent strength of the winter monsoon over India.

**[Demonstration content for PolarConnect educational portal, Ministry of Earth Sciences, India.]**
''',
                quiz=dict(
                    title='Arctic Ecosystems Quiz',
                    description='Test your knowledge of Arctic land, ice and marine ecosystems.',
                    passing_score=60,
                    time_limit=12,
                    questions=[
                        dict(q='What is the Arctic equivalent of Antarctic krill in terms of ecological role?',
                             a='Ringed seal', b='Arctic cod (Boreogadus saida)', c='Copepods', d='Arctic char',
                             ans='B',
                             exp='Arctic cod plays the same critical "middle link" role in the Arctic food web that krill plays in the Antarctic — connecting zooplankton to seabirds, seals, whales and polar bears.'),
                        dict(q='Why can the Arctic Ocean be more productive than expected despite being ice-covered?',
                             a='Warm Atlantic currents carry nutrients northward', b='Phytoplankton can bloom underneath thin sea ice',
                             c='Arctic rivers deposit large amounts of minerals', d='Deep volcanic vents supply nutrients',
                             ans='B',
                             exp='Recent research has discovered that phytoplankton blooms can occur underneath sea ice when it is thin enough to transmit sufficient light — a previously unrecognised source of Arctic productivity.'),
                        dict(q='What is the primary food source of polar bears?',
                             a='Arctic char fish', b='Caribou', c='Ringed seals', d='Beluga whales',
                             ans='C',
                             exp='Polar bears are almost entirely dependent on ringed seals, which they catch by waiting at breathing holes in sea ice. As sea ice declines, polar bears have fewer opportunities to hunt, threatening their survival.'),
                        dict(q='Which animal makes the longest migration of any living creature?',
                             a='Humpback whale', b='Arctic tern', c='Monarch butterfly', d='Caribou',
                             ans='B',
                             exp='The Arctic tern migrates from its Arctic breeding grounds to Antarctic waters and back every year — a round trip of approximately 70,000–90,000 km, the longest migration of any animal.'),
                        dict(q='Why is India\'s Himadri station in the Arctic scientifically important for India?',
                             a='India is building a shipping route through the Arctic', b='Arctic ice contains mineral resources India is claiming',
                             c='Arctic changes affect Indian monsoon patterns', d='Himadri monitors volcanic activity',
                             ans='C',
                             exp='Indian scientists have documented correlations between Arctic sea ice extent in autumn and the strength of the subsequent Indian monsoon. Monitoring Arctic changes at Himadri helps improve monsoon forecasting — directly relevant to India\'s agriculture and water security.'),
                    ]
                )
            ),

            dict(
                category_slug='arctic-ecosystems',
                title='Permafrost: The Frozen Ground Beneath Our Feet',
                slug='permafrost-frozen-ground',
                description='Understand what permafrost is, where it exists, and why its thawing poses a major climate risk.',
                difficulty='intermediate',
                duration=35,
                order=2,
                content='''\
Beneath the tundra and boreal forests of the Arctic lies a layer of permanently frozen ground called permafrost. It covers about 25% of the Northern Hemisphere's land surface and plays a critically important role in the global carbon cycle — one that is now under severe threat from climate change.

## What is Permafrost?

Permafrost is defined as ground (soil, rock or sediment) that remains at or below 0°C for at least two consecutive years. The top layer — the **active layer** — thaws each summer and refreezes each winter. Below this, the permafrost can extend to hundreds of metres depth.

**Continuous permafrost**: Covers >90% of the landscape; found in the high Arctic (Siberia, northern Canada, Greenland)
**Discontinuous permafrost**: Patches of permafrost separated by unfrozen ground; found at mid-Arctic latitudes
**Sporadic permafrost**: Isolated patches; found near the southern limit of permafrost

## What is Stored in Permafrost?

Permafrost is essentially a freezer — it has preserved organic material for thousands of years. This includes:
- **Dead plant material** accumulated over millennia in cold, waterlogged conditions (particularly in peatlands)
- Intact mammoth carcasses, ancient bacteria and even viable seeds up to 30,000 years old
- Methane gas trapped in ice crystals (**methane clathrates** or hydrates)

Scientists estimate that permafrost contains approximately **1,500 billion tonnes of organic carbon** — roughly twice the amount currently in the atmosphere. This is one of the most significant carbon stores on Earth.

## Why Permafrost Matters for Climate

When permafrost thaws, the organic matter it contains is exposed to microbial decomposition. This releases:
- **Carbon dioxide (CO₂)**: Produced when oxygen is present (aerobic decomposition)
- **Methane (CH₄)**: Produced in waterlogged, oxygen-free conditions (anaerobic decomposition); 80× more potent than CO₂ over 20 years

This creates a **positive feedback loop**: warming → permafrost thaw → greenhouse gas release → more warming → more permafrost thaw.

## Observed Changes

The Arctic has warmed by approximately 3–4°C since the 1970s — roughly three times faster than the global average. As a result:

- Permafrost temperatures have increased by 0.3–0.5°C per decade in many regions
- The active layer is deepening, exposing more organic material to decomposition
- **Thermokarst** features are spreading — terrain collapses as ice within permafrost melts, creating sinkholes, ponds and slumping hillsides
- Methane emissions from Arctic lakes and wetlands are measurably increasing
- Infrastructure in permafrost regions is failing: buildings tilt, roads buckle, pipelines break

## India's Role in Arctic Research

India monitors permafrost dynamics at the Himadri station at Ny-Ålesund, Svalbard, where permafrost warming has been particularly well documented. Indian researchers measure active layer depth, soil temperature profiles and greenhouse gas fluxes from thawing permafrost. This data contributes to international databases used in IPCC climate assessments.

Svalbard is warming at twice the rate of the broader Arctic — about 7°C since 1970 — making it a bellwether for permafrost change globally.

## Impacts Beyond Climate

Permafrost thaw has profound practical consequences:
- **Siberia**: Tens of thousands of buildings and hundreds of kilometres of pipelines are at risk
- **Alaska and Canada**: Communities built on permafrost are facing existential threats as the ground beneath them collapses
- **Ancient pathogens**: There are documented cases of anthrax spores released from thawing permafrost killing reindeer in Siberia

Understanding and monitoring permafrost is thus not just a scientific priority but a matter of human security.

**[Demonstration content for PolarConnect educational portal, Ministry of Earth Sciences, India.]**
''',
                quiz=None
            ),

            dict(
                category_slug='arctic-ecosystems',
                title='Indigenous Communities and Arctic Knowledge',
                slug='indigenous-arctic-knowledge',
                description='Learn how Indigenous peoples have lived in the Arctic for thousands of years and what their knowledge tells us about environmental change.',
                difficulty='beginner',
                duration=25,
                order=3,
                content='''\
The Arctic has been home to human communities for more than 15,000 years. The Indigenous peoples of the Arctic — including the Inuit, Yupik, Chukchi, Sami, Nenets and many other groups — have developed extraordinary knowledge systems, technologies and cultural practices that have enabled them to thrive in one of the world's most demanding environments.

## Who Are the Arctic's Indigenous Peoples?

**Inuit**: The largest and most geographically dispersed Arctic Indigenous group, living across Arctic Canada, Greenland, Alaska and northeastern Russia. The word "Inuit" means "the people" in Inuktitut. The language group is remarkably uniform across thousands of kilometres.

**Yupik**: Living in Alaska and the Russian Far East; linguistically and culturally related to but distinct from the Inuit.

**Chukchi and Siberian Yupik**: The Indigenous peoples of the Chukotka Peninsula in northeastern Russia; skilled sea mammal hunters and reindeer herders.

**Sami**: The Indigenous peoples of northern Scandinavia and the Kola Peninsula of Russia; traditionally reindeer herders, fishers and hunters, with a territory called Sápmi.

**Nenets and Nganasan**: Reindeer herding peoples of Siberia who maintain one of the world's most extraordinary nomadic traditions, moving reindeer herds across the Arctic tundra through all seasons.

## Traditional Ecological Knowledge

Indigenous Arctic peoples have accumulated thousands of years of detailed observation of their environment. This Traditional Ecological Knowledge (TEK) includes:

- Detailed understanding of sea ice types, stability and behaviour
- Intricate knowledge of weather prediction, wind patterns and storm warning signs
- Understanding of animal behaviour, migration routes and breeding cycles
- Knowledge of sustainable hunting and fishing practices developed over millennia
- Plant knowledge — identifying which species are edible, medicinal or useful as materials

Crucially, TEK represents a continuous, long-term record of environmental change that scientific instruments cannot replicate. Indigenous communities have documented changes in sea ice thickness, the arrival of new species, shifts in migration routes and unpredictable weather as climate change accelerates — often decades before systematic scientific data was available.

## Traditional Technologies

Inuit and other Arctic peoples developed remarkable technologies for living with cold:

**Clothing**: Multi-layered garments of seal, caribou and fox skin, designed to allow moisture to escape while blocking cold. The principle of layering for insulation was later adopted by modern outdoor clothing technology.

**Qajaq (Kayak)**: The original sea kayak, designed for hunting in Arctic waters. Each kayak was custom-built for its owner, tailored to body proportions. Modern kayaking and sea kayaking directly descend from this technology.

**Iglu (Igloo)**: A temporary shelter built from snow blocks, exploiting snow's excellent insulating properties. Interior temperature can be −5°C even when outside temperatures drop to −40°C. The dome structure distributes weight evenly and is structurally extremely strong.

**Qamutik (Sled)**: Dog sled technology that enabled travel across sea ice and tundra with heavy loads in ways that wheeled vehicles could not achieve.

## TEK and Climate Change Science

Combining Indigenous knowledge with scientific data is increasingly recognised as essential for understanding Arctic change. Some examples:

- Inuit hunters have documented thinning sea ice, unpredictable ice conditions and new hazards over decades — consistent with and enriching satellite data
- Sami reindeer herders report changes in the timing of snow-cover melt affecting reindeer access to food
- Communities across the Arctic have noted the arrival of previously unknown species — from fish to insects — as the region warms

The Arctic Council — the inter-governmental forum for Arctic nations — formally recognises Indigenous peoples as Permanent Participants, giving them a voice in Arctic governance. India, as an observer state to the Arctic Council through its Himadri research activities, engages with this framework.

**[Demonstration content for PolarConnect educational portal, Ministry of Earth Sciences, India.]**
''',
                quiz=None
            ),

            # ============================================================
            # POLAR WILDLIFE  (3 modules)
            # ============================================================
            dict(
                category_slug='polar-wildlife',
                title='Polar Bear: King of the Arctic',
                slug='polar-bear-king-arctic',
                description='An in-depth look at the biology, behaviour and conservation of the polar bear — Earth\'s largest terrestrial predator.',
                difficulty='beginner',
                duration=28,
                order=1,
                content='''\
The polar bear (*Ursus maritimus*) is one of the most iconic animals on Earth and the living symbol of the Arctic. It is the world's largest terrestrial predator and one of the most specialised carnivores ever to have evolved — an animal so perfectly adapted to the Arctic marine environment that some scientists argue it should be classified as a marine mammal.

## Basic Facts

- **Size**: Males 350–700 kg, 2.4–3 m long; females 150–250 kg. The largest recorded polar bear weighed 1,002 kg.
- **Lifespan**: 20–30 years in the wild; older in captivity
- **Range**: Circumpolar Arctic, primarily the sea ice zone
- **Population**: Approximately 20,000–31,000 (various estimates; 19 recognised subpopulations)
- **Conservation status**: Vulnerable (IUCN Red List)

## Adaptations to Arctic Life

**Fur and skin**: Polar bear fur appears white but is actually transparent and hollow — it scatters light and may help channel solar energy to dark skin beneath. The black skin absorbs heat. The dense undercoat and coarse guard hairs together provide extraordinary insulation.

**Body fat**: A thick layer of blubber (up to 11 cm) provides additional insulation and an energy reserve for the extended fasting periods that are a normal part of polar bear life.

**Paws**: Large, flat paws act as snowshoes and paddles. The pads have small papillae (bumps) that increase grip on ice. The polar bear is an excellent swimmer and has been observed swimming continuously for up to 10 days across open water.

**Sense of smell**: The most acute of any bear — a polar bear can smell a seal breathing hole under 1 metre of snow from up to 1 km away.

**Metabolism**: Polar bears can enter a state called "walking hibernation" during food-scarce periods — lowering their metabolic rate and surviving on fat reserves without entering full dormancy.

## Hunting Strategy

Polar bears are **still hunters** — the most patient of predators. Their primary technique is called **still hunting**:

1. The bear locates a ringed seal's breathing hole in sea ice using its nose
2. It waits motionless beside the hole, sometimes for hours
3. When the seal surfaces to breathe, the bear strikes with its forelegs
4. It drags the seal out of the water and kills it with a bite to the head

Polar bears may also stalk seals resting on ice, swim beneath ice floes to surprise basking seals, and excavate dens where female seals give birth beneath snow. Cubs are the most vulnerable to predation.

## Reproduction

Polar bears have one of the lowest reproductive rates of any mammal. Females give birth to 1–3 cubs (usually 2) every 3 years. The female enters a snow den in autumn, gives birth in December–January, and emerges in March–April with the cubs, who weigh only 500–700g at birth. Cubs stay with their mother for 2–2.5 years, learning to hunt sea ice. This long intergenerational dependence means that population recovery from declines is very slow.

## Polar Bears and Climate Change

Sea ice is the platform on which polar bears hunt seals — their almost exclusive prey. As the Arctic warms and sea ice declines, polar bears face a triple threat:

**1. Reduced hunting time**: The sea ice season is shortening. In Hudson Bay, Canada, sea ice now forms several weeks later and melts earlier than in the 1970s. This means fewer weeks for bears to build up fat reserves.

**2. Longer fasting periods**: Bears must survive longer on land without food, burning fat reserves and sometimes resulting in starvation — particularly in older individuals and females with cubs.

**3. Increased drowning risk**: Longer swims in ice-free waters can be fatal for cubs and exhausted adults.

Models project that if greenhouse gas emissions continue on a high trajectory, polar bears could be functionally extinct in most of their range by 2100.

## Polar Bears and Indigenous Peoples

For the Inuit, the polar bear (*Nanuk* in Inuktitut) is a central figure in culture, spirituality and subsistence. Polar bear hunting has been practised sustainably by Inuit communities for thousands of years. The Inuit Circumpolar Council and Indigenous communities are important voices in polar bear conservation discussions, emphasising the need to integrate Traditional Ecological Knowledge with scientific data.

**[Demonstration content for PolarConnect educational portal, Ministry of Earth Sciences, India.]**
''',
                quiz=dict(
                    title='Polar Wildlife Quiz',
                    description='Test your knowledge of polar bears, Arctic and Antarctic wildlife.',
                    passing_score=60,
                    time_limit=15,
                    questions=[
                        dict(q='What is the primary hunting method of polar bears?',
                             a='Chasing seals across ice', b='Still hunting at breathing holes in sea ice',
                             c='Diving underwater to catch fish', d='Ambushing seals from beneath ice floes',
                             ans='B',
                             exp='Still hunting is the primary technique — a polar bear waits motionless beside a seal\'s breathing hole in sea ice, sometimes for hours, and strikes when the seal surfaces to breathe.'),
                        dict(q='Why is polar bear fur white?',
                             a='It is white to blend in with snow (camouflage)', b='The fur is transparent and hollow, scattering light to appear white',
                             c='A pigment called ursocanine makes it white', d='The fur bleaches in UV radiation',
                             ans='B',
                             exp='Polar bear fur is actually transparent and hollow — it scatters light in the same way that snow does, making it appear white. The skin beneath is black, absorbing solar heat.'),
                        dict(q='What is the main threat to polar bear survival from climate change?',
                             a='Ocean acidification killing their fish prey', b='Increased competition from grizzly bears moving north',
                             c='Sea ice decline reducing hunting opportunities and extending fasting periods', d='Toxic algal blooms poisoning seals',
                             ans='C',
                             exp='Polar bears hunt almost exclusively on sea ice, which is declining rapidly. Shorter ice seasons mean fewer weeks to build fat reserves and longer, potentially fatal fasting periods on land.'),
                        dict(q='Approximately how many polar bears are estimated to exist in the wild?',
                             a='5,000–10,000', b='20,000–31,000', c='50,000–80,000', d='100,000+',
                             ans='B',
                             exp='Current estimates put the global polar bear population at approximately 20,000–31,000 individuals across 19 recognised subpopulations. The species is listed as Vulnerable on the IUCN Red List.'),
                        dict(q='How long can polar bear cubs remain with their mother?',
                             a='6 months', b='1 year', c='2–2.5 years', d='5 years',
                             ans='C',
                             exp='Polar bear cubs stay with their mother for 2–2.5 years, learning to hunt on sea ice. This extended dependence, combined with the 3-year gap between litters, means polar bear populations recover very slowly from declines.'),
                        dict(q='Which indigenous word for polar bear reflects its cultural significance to Arctic peoples?',
                             a='Isbjørn', b='Nanuk', c='Qilak', d='Umiak',
                             ans='B',
                             exp='Nanuk is the Inuktitut word for polar bear. The polar bear is a central figure in Inuit culture, spirituality and subsistence, and Indigenous knowledge of polar bear behaviour and population trends is an important complement to scientific research.'),
                    ]
                )
            ),

            dict(
                category_slug='polar-wildlife',
                title='Migration: Epic Journeys Across the Polar World',
                slug='migration-polar-world',
                description='Follow the extraordinary migrations of Arctic terns, caribou, whales and other animals that connect the poles to the rest of the planet.',
                difficulty='beginner',
                duration=25,
                order=2,
                content='''\
Migration is one of the most spectacular phenomena in the natural world, and the polar regions are connected to the rest of the planet through some of the most extraordinary migrations ever documented.

## Arctic Tern: The Ultimate Migrant

The Arctic tern (*Sterna paradisaea*) holds the record for the longest migration of any animal. Each year, it makes a round trip from its Arctic breeding grounds to the Antarctic and back — a journey of approximately **70,000–90,000 km**.

A GPS-tracking study of Arctic terns breeding in Greenland and Iceland revealed that individual birds were covering up to 90,000 km per round trip, following an S-shaped route that exploited prevailing wind systems. Over a lifetime of 30 years, an Arctic tern may travel the equivalent of **three trips to the Moon and back**.

Why go this far? The Arctic tern exploits **two summers per year** — the Arctic summer in June–August and the Antarctic summer in November–January. At both ends of its journey, it feeds on fish and invertebrates in highly productive polar seas during their most productive periods.

## Caribou and Reindeer: The Great Land Migration

The porcupine caribou herd of North America — about 200,000 animals — undertakes what is considered the **longest land migration of any terrestrial mammal** in the Western Hemisphere. Each year, the herd travels up to **5,000 km** between their winter range in boreal forest and their summer calving grounds on the Arctic coastal plain of Alaska and the Yukon.

They face:
- River crossings, sometimes swimming across rivers with swift currents
- Attacks from wolves, bears and Golden eagles
- Biting insects (mosquitoes and bot flies) in vast numbers
- Unpredictable Arctic weather

The timing of migration is tightly synchronised with plant growth on the calving grounds. If Arctic warming causes plants to bloom earlier, calves born too late may miss the peak of vegetation — a phenomenon called trophic mismatch.

## Humpback Whales: Ocean Highways

Humpback whales migrate between cold, productive polar feeding grounds and warm tropical breeding grounds — one of the longest migrations of any mammal.

- **Feeding grounds**: Antarctic waters (Southern Ocean) in summer; Arctic/sub-Arctic waters in Northern Hemisphere summer
- **Breeding grounds**: Warm tropical waters (e.g., the coasts of Hawaii, Mexico, Brazil, the Caribbean)
- **Distance**: Up to 8,500 km each way in some populations

During migration and in tropical breeding areas, humpbacks eat almost nothing — surviving entirely on fat reserves built up during polar summer feeding frenzies. A single humpback can consume up to 1.4 tonnes of krill per day in Antarctic waters.

## Polar Wildlife and India

India's geographic position and large coastline mean that many migratory species connect Indian seas to the polar oceans. Humpback whales feeding in the Southern Ocean may eventually enter the Indian Ocean. Arctic terns photographed in India's coastal waters have been tracked to Arctic breeding sites. Indian oceanographers study the Southern Ocean ecosystem that sustains these animals during their polar stays.

## Why Understanding Migration Matters

Migratory species are exceptional indicators of environmental change because their survival depends on conditions at multiple, geographically separated locations. A change in timing at one end of the migration route — triggered by climate change — can cascade through the entire life cycle. Understanding migration routes also guides conservation: protecting a species' Arctic breeding ground is futile if its tropical wintering habitat is destroyed.

**[Demonstration content for PolarConnect educational portal, Ministry of Earth Sciences, India.]**
''',
                quiz=None
            ),

            dict(
                category_slug='polar-wildlife',
                title='Adaptation to Extreme Cold: Nature\'s Engineering Marvels',
                slug='adaptation-extreme-cold',
                description='Discover the remarkable biological solutions that animals have evolved to survive at the extremes of temperature on Earth.',
                difficulty='intermediate',
                duration=32,
                order=3,
                content='''\
Survival at the poles requires solutions to problems that no other environment presents: temperatures that can kill unprotected tissue in minutes, prolonged darkness, food scarcity and the mechanical challenges of ice. Evolution has produced astonishing engineering in polar animals.

## Maintaining Body Temperature

Most polar mammals and birds are **endotherms** (warm-blooded) — they maintain a constant internal body temperature regardless of external conditions. The challenge is not generating heat, but retaining it.

**Counter-current heat exchange** is used by virtually every polar animal to prevent heat loss to extremities. In Arctic foxes, penguins, seals and whales, arterial blood flowing to the flippers/feet/tail runs alongside venous blood returning from them. Heat transfers from the warm outgoing blood to the cooler returning blood. By the time blood reaches the flipper tip, it is barely above freezing — minimising heat loss to the water or air.

**Fur and feathers** create insulating dead-air layers. Arctic mammals have guard hairs (long, coarse, water-repellent) over dense underfur (fine, crimped, trapping air). Emperor penguins achieve 100 feathers per cm² — the densest feather coverage of any bird.

**Blubber** in marine mammals (seals, whales, walruses) provides insulation, buoyancy and an energy store. Blue whale blubber can be 50 cm thick.

## Antifreeze

Some polar animals face a different problem: their blood would freeze solid. Fish living in Antarctic and Arctic waters have evolved **antifreeze proteins (AFPs)** — molecules that bind to ice crystals and prevent them from growing.

The Antarctic toothfish (*Dissostichus mawsoni*) survives in water at −1.9°C — the freezing point of seawater — using AFPs that are among the most effective biological antifreezes known. The proteins are so effective that they can depress the freezing point of water well below −5°C.

**Wood frogs** (*Rana sylvatica*) in the Arctic take a completely different approach: they allow themselves to freeze solid. Up to 70% of body water converts to ice. Heart stops. Brain activity ceases. In spring, they thaw and hop away. They survive by flooding their cells with glucose, which acts as a cryoprotectant preventing cell damage during freezing.

## Surviving Without Food

Extended food scarcity is a reality for most polar animals. Solutions include:

**Hibernation and torpor**: Arctic ground squirrels can lower their body temperature to below 0°C (without freezing) during winter torpor, reducing metabolic demands by 99%. Their hibernation lasts 6–9 months. Brown bears enter full hibernation, surviving 5–7 months without food, water or defecation.

**Fat reserves**: Polar bears and seal pups accumulate enormous fat reserves before food-scarce seasons. Emperor penguin males fast for 65 days while incubating eggs, losing up to 40% of their body weight. Female elephant seals fast for 11 months per year — the longest fasting period of any mammal.

**Rumen fermentation in reindeer**: Reindeer (*Rangifer tarandus*) can digest lichens — which contain compounds toxic to most mammals — using specialised gut bacteria. In winter, when other food sources are buried under snow, lichens are often the only available food.

## Colour Change

Many Arctic animals change colour with the seasons — white in winter (camouflage against snow) and brown/grey in summer (camouflage against tundra).

Species that change: Arctic fox, Arctic hare, stoat (ermine), ptarmigan (a bird)

This is controlled by photoperiod (day length) rather than temperature — the same molecular signalling pathway (involving melatonin) that controls seasonal reproduction and migration in many animals.

**Climate change problem**: As snow cover decreases and arrives later, white Arctic animals are increasingly visible against brown ground — increasing predation pressure in a process called **phenological mismatch**.

## Echolocation Under Ice

Beluga whales and narwhals use sophisticated echolocation to navigate under sea ice, find fish and avoid becoming trapped in ice. The beluga's forehead — the "melon" — is a specialised fatty organ that focuses sound. Belugas can modulate the shape of the melon to steer sound beams, giving them extraordinary sonar precision. Their vocalisations are so diverse (whistles, clicks, clangs, chirps) that sailors historically called them "the canaries of the sea."

**[Demonstration content for PolarConnect educational portal, Ministry of Earth Sciences, India.]**
''',
                quiz=None
            ),
        ]

        # ----------------------------------------------------------------
        # CREATE MODULES AND QUIZZES
        # ----------------------------------------------------------------
        for md in modules:
            cat_slug = md.pop('category_slug')
            quiz_data = md.pop('quiz')

            try:
                cat = LearningCategory.objects.get(slug=cat_slug)
            except LearningCategory.DoesNotExist:
                self.stdout.write(self.style.WARNING(f'  Category not found: {cat_slug}'))
                continue

            if LearningModule.objects.filter(slug=md['slug']).exists():
                self.stdout.write(f'  - Skipping (exists): {md["title"]}')
                continue

            module = LearningModule.objects.create(
                category=cat,
                title=md['title'],
                slug=md['slug'],
                description=md['description'],
                content=md['content'],
                difficulty=md['difficulty'],
                duration_minutes=md['duration'],
                order=md['order'],
                is_published=True,
            )
            created_m += 1
            self.stdout.write(f'  + Created module: {module.title}')

            if quiz_data:
                quiz = Quiz.objects.create(
                    module=module,
                    title=quiz_data['title'],
                    description=quiz_data['description'],
                    passing_score=quiz_data['passing_score'],
                    time_limit_minutes=quiz_data['time_limit'],
                )
                for i, q in enumerate(quiz_data['questions'], 1):
                    Question.objects.create(
                        quiz=quiz,
                        question_text=q['q'],
                        option_a=q['a'], option_b=q['b'],
                        option_c=q['c'], option_d=q['d'],
                        correct_option=q['ans'],
                        explanation=q['exp'],
                        order=i,
                    )
                created_q += 1
                self.stdout.write(f'    + Quiz: {quiz.title} ({len(quiz_data["questions"])} questions)')

        self.stdout.write(self.style.SUCCESS(
            f'\n✓ Done — {created_m} modules created, {created_q} quizzes created'
        ))
