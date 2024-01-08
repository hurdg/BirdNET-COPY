// Project data entries consist of the following fields:
// - Project name
// - Organization/Project lead
// - Target species
// - Country
// - Region/Location
// - Latitude
// - Longitude
// - Contact
// - Website
// - Paper
// - Species Image
// - Species Image Credit
// - Species Icon (feather, paw, frog, water, bug, fish, leaf, cog)

// If a field is not applicable, enter null
// If latitude and longitude are missing, no marker will be placed on the map

var projects_data = [
    {
        "Project name": "Mid-western Bird Monitoring",
        "Organization/Project lead": "Irina Tolkova",
        "Target species": "Birds",
        "Country": "USA",
        "Region/Location": "Montana",
        "Latitude": 46.8796822,
        "Longitude": -110.3625658,
        "Contact": null,
        "Website": null,
        "Paper": null,
        "Species Icon": "feather"
    },
    {
        "Project name": "SE Asia Research Program",
        "Organization/Project lead": "Dena Clink",
        "Target species": "Gibbons",
        "Country": "Malaysia",
        "Region/Location": "Kenyir State Park",
        "Latitude": 5.0039622,
        "Longitude": 102.6388451,
        "Contact": null,
        "Website": null,
        "Paper": null,
        "Species Image": "https://upload.wikimedia.org/wikipedia/commons/2/25/Gibbon_collage.png",
        "Species Image Credit": "PaleoMatt, CC BY-SA 4.0, via Wikimedia Commons",
        "Species Icon": "paw"
    },
    {
        "Project name": "SE Asia Research Program",
        "Organization/Project lead": "Dena Clink",
        "Target species": "Gibbons",
        "Country": "Cambodia",
        "Region/Location": "Keo Seima Wildlife Sanctuary",
        "Latitude": 12.3356366,
        "Longitude": 106.8421363,
        "Contact": null,
        "Website": null,
        "Paper": null,
        "Species Image": "https://upload.wikimedia.org/wikipedia/commons/2/25/Gibbon_collage.png",
        "Species Image Credit": "PaleoMatt via Wikimedia Commons",
        "Species Icon": "paw"
    },
    {
        "Project name": "Ribbons Seals Monitoring",
        "Organization/Project lead": "Shiho Furumaki / University of Kyoto",
        "Target species": "Ribbon Seals",
        "Country": "Japan",
        "Region/Location": "Japan",
        "Latitude": 36.204824,
        "Longitude": 138.252924,
        "Contact": null,
        "Website": null,
        "Paper": null,
        "Species Image": "https://upload.wikimedia.org/wikipedia/commons/c/c6/Male_Ribbon_Sea_Ozernoy_Gulf_Russia.jpg",
        "Species Image Credit": "Michael Cameron via Wikimedia Commons",
        "Species Icon": "water"
    },
    {
        "Project name": "Sierra Nevada acoustic monitoring project",
        "Organization/Project lead": "Connor Wood, Zach Peery, US Forest Service",
        "Target species": "Birds",
        "Country": "USA",
        "Region/Location": "California",
        "Latitude": 36.778261,
        "Longitude": -119.4179324,
        "Contact": null,
        "Website": null,
        "Paper": null,
        "Species Image": "https://upload.wikimedia.org/wikipedia/commons/8/88/California_Spotted_Owl%2C_Stanislaus_National_Forest_%288427894580%29.jpg",
        "Species Image Credit": "Pacific Southwest Region 5 via Wikimedia Commons",
        "Species Icon": "feather"
    },
    {
        "Project name": "Cape Parrot Project",
        "Organization/Project lead": "Wild Bird Trust",
        "Target species": "Cape Parrots",
        "Country": "South Africa",
        "Region/Location": "Amathole forest complex",
        "Latitude": -32.585389,
        "Longitude": 27.206551,
        "Contact": null,
        "Website": "https://www.wildbirdtrust.com/projects/cape-parrot-project",
        "Paper": null,
        "Species Image": "https://upload.wikimedia.org/wikipedia/commons/2/26/Poicephalus_robustus_104453705.jpg",
        "Species Image Credit": "Dave Brown via Wikimedia Commons",
        "Species Icon": "feather"
    },
    {
        "Project name": "Difficult Bird Group Monitoring",
        "Organization/Project lead": "Difficult Bird Group",
        "Target species": "Birds",
        "Country": "Australia",
        "Region/Location": "Tasmania",
        "Latitude": -42.0409059,
        "Longitude": 146.8087322,
        "Contact": null,
        "Website": "https://www.difficultbirds.com",
        "Paper": null,
        "Species Image": "assets/img/dummy_birds_image.png",
        "Species Image Credit": "ChatGPT",
        "Species Icon": "feather"
    },
    {
        "Project name": "Endangered Species Monitoring",
        "Organization/Project lead": "Cristina Gomes, Florida international university",
        "Target species": "St. Vincent Parrot",
        "Country": "Saint Vincent and the Grenadines",
        "Region/Location": "Caribbean island of Saint Vincent",
        "Latitude": 13.2509747,
        "Longitude": -61.1863473,
        "Contact": null,
        "Website": null,
        "Paper": null,
        "Species Image": "https://upload.wikimedia.org/wikipedia/commons/9/9d/Amazona_guildingii-4_%28cropped%29.jpg",
        "Species Image Credit": "Beralpo via Wikimedia Commons",
        "Species Icon": "feather"
    },
    {
        "Project name": "Endangered Species Monitoring",
        "Organization/Project lead": null,
        "Target species": "Regent Honeyeater",
        "Country": "Australia",
        "Region/Location": "Taronga Zoo",
        "Latitude": -33.8435473,
        "Longitude": 151.2413418,
        "Contact": null,
        "Website": null,
        "Paper": null,
        "Species Image": "https://upload.wikimedia.org/wikipedia/commons/7/75/Regent_honeyeater%2C_Xanthomyza_phrygia%2C_Sydney%2C_Australia._Not_the_best_picture_on_a_cloudy_day_with_crappy_camera%2C_but_quite_a_striking_bird._%2816445299203%29.jpg",
        "Species Image Credit": "Derek Keats via Wikimedia Commons",
        "Species Icon": "feather"
    },
    {
        "Project name": "Mentorship program",
        "Organization/Project lead": "Kristen Morrow",
        "Target species": "Red langurs, oranguants, gibbons",
        "Country": "Indonesia",
        "Region/Location": "Central Borneo",
        "Latitude": -1.6814878,
        "Longitude": 113.3823545,
        "Contact": null,
        "Website": null,
        "Paper": null,
        "Species Image": "https://upload.wikimedia.org/wikipedia/commons/8/83/Red_leaf_monkey_%28Presbytis_rubicunda%29.jpg",
        "Species Image Credit": "Charles J. Sharp via Wikimedia Commons",
        "Species Icon": "paw"
    },
    {
        "Project name": "Endangered Species Monitoring",
        "Organization/Project lead": "Christy Hand",
        "Target species": "Black Rail",
        "Country": "USA",
        "Region/Location": "Ashepoo, Combahee, and Edisto basin",
        "Latitude": 32.5503474,
        "Longitude": -80.2971369,
        "Contact": null,
        "Website": null,
        "Paper": null,
        "Species Image": "https://upload.wikimedia.org/wikipedia/commons/1/10/Laterallus_jamaicensis_-_Black_Rail%3B_Arari%2C_Maranh%C3%A3o%2C_Brazil.jpg",
        "Species Image Credit": "Hector Bottai via Wikimedia Commons",
        "Species Icon": "feather"
    },
    {
        "Project name": "California's wolf recolonization",
        "Organization/Project lead": "UC-Davis + Connor Wood",
        "Target species": "Gray Wolf",
        "Country": "USA",
        "Region/Location": "Northeastern CA",
        "Latitude": 38.8375215,
        "Longitude": -120.8958242,
        "Contact": null,
        "Website": null,
        "Paper": null,
        "Species Image": "https://upload.wikimedia.org/wikipedia/commons/c/c3/Canis_lupus_Ernstbrunn.jpg",
        "Species Image Credit": "Mariofan13 via Wikimedia Commons",
        "Species Icon": "paw"
    },
    {
        "Project name": "Rubber farm ecology",
        "Organization/Project lead": "Charlie Tebbutt",
        "Target species": "Birds",
        "Country": "Colombia",
        "Region/Location": "Colombia",
        "Latitude": 4.570868,
        "Longitude": -74.297333,
        "Contact": null,
        "Website": null,
        "Paper": null,
        "Species Image": "assets/img/dummy_birds_image.png",
        "Species Image Credit": "ChatGPT",
        "Species Icon": "feather"
    },
    {
        "Project name": "Amphibian monitoring",
        "Organization/Project lead": "Alyssa Killingsworth",
        "Target species": "Mid-elevation frogs",
        "Country": "Ecuador",
        "Region/Location": "Ecuador",
        "Latitude": -1.831239,
        "Longitude": -78.183406,
        "Contact": null,
        "Website": null,
        "Paper": null,
        "Species Image": "assets/img/dummy_frogs_image.png",
        "Species Image Credit": "ChatGPT",
        "Species Icon": "frog"
    },
    {
        "Project name": "National Park Service",
        "Organization/Project lead": "Laurel Syems",
        "Target species": "Birds",
        "Country": "USA",
        "Region/Location": "New England",
        "Latitude": 43.9653889,
        "Longitude": -70.8226541,
        "Contact": null,
        "Website": null,
        "Paper": null,
        "Species Image": "assets/img/dummy_birds_image.png",
        "Species Image Credit": "ChatGPT",
        "Species Icon": "feather"
    },
    {
        "Project name": "Mentorship program",
        "Organization/Project lead": "Pramana Yuda",
        "Target species": "Bali Myna",
        "Country": "Indonesia",
        "Region/Location": "Indonesia",
        "Latitude": -0.789275,
        "Longitude": 113.921327,
        "Contact": null,
        "Website": null,
        "Paper": null,
        "Species Image": "https://upload.wikimedia.org/wikipedia/commons/3/31/Bali_Myna_0A2A9443.jpg",
        "Species Image Credit": "JJ Harrison via Wikimedia Commons",
        "Species Icon": "feather"
    },
    {
        "Project name": "Mentorship program",
        "Organization/Project lead": "Sikundur Manmal",
        "Target species": "Siamang, Lars Gibbon, and Chainsaws",
        "Country": "Indonesia",
        "Region/Location": "Indonesia",
        "Latitude": -0.789275,
        "Longitude": 113.921327,
        "Contact": null,
        "Website": null,
        "Paper": null,
        "Species Image": "https://upload.wikimedia.org/wikipedia/commons/d/de/Symphalangus_syndactylus%2C_Chiba_Zoo%2C_Japan.jpg",
        "Species Image Credit": "suneko via Wikimedia Commons",
        "Species Icon": "paw"
    },
    {
        "Project name": "Amphibian monitoring",
        "Organization/Project lead": "UFMS",
        "Target species": "Pantanal frogs",
        "Country": "Brazil",
        "Region/Location": "Brazil",
        "Latitude": -14.235004,
        "Longitude": -51.92528,
        "Contact": null,
        "Website": null,
        "Paper": null,
        "Species Image": "assets/img/dummy_frogs_image.png",
        "Species Image Credit": "ChatGPT",
        "Species Icon": "frog"
    },
    {
        "Project name": "Endangered Species Monitoring",
        "Organization/Project lead": "Viral Joshi",
        "Target species": "Birds, Asiatic Lion",
        "Country": "India",
        "Region/Location": "Western Ghats",
        "Latitude": 10.166667,
        "Longitude": 77.066667,
        "Contact": null,
        "Website": null,
        "Paper": null,
        "Species Image": "https://upload.wikimedia.org/wikipedia/commons/f/f9/Panthera_leo_persica_M.jpg",
        "Species Image Credit": "I, Chrumps",
        "Species Icon": "paw"
    },
    {
        "Project name": "Rungan Biodiversity ",
        "Organization/Project lead": "Kristen Morrow",
        "Target species": "Hornbills, frogs, gecko, red langurs, orangutans, gibbons, long tailed macaques, anthropogenic noise ",
        "Country": "Indonesia",
        "Region/Location": "Central Borneo",
        "Latitude": -1.8814878,
        "Longitude": 113.3823545,
        "Contact": "Kristen Morrow; ksmorrow@uga.edu",
        "Website": null,
        "Paper": null,
        "Species Image": "https://upload.wikimedia.org/wikipedia/commons/3/34/Buceros_rhinoceros_-Kuala_Lumpur_Bird_Park%2C_Malaysia-8a_%282%29.jpg",
        "Species Image Credit": "AbZahri AbAzizis via Wikimedia Commons",
        "Species Icon": "feather"
    },
    {
        "Project name": "Yosemite toad monitoring",
        "Organization/Project lead": "Connor Wood/US Forest Service",
        "Target species": "Yosemite toad, Pacific chorus frog",
        "Country": "USA",
        "Region/Location": "John Muir Wilderness, California",
        "Latitude": 36.9757749,
        "Longitude": -118.8120504,
        "Contact": null,
        "Website": null,
        "Paper": null,
        "Species Image": "https://upload.wikimedia.org/wikipedia/commons/3/33/Bufo_canorus05.jpg",
        "Species Image Credit": "Pierre Fidenci via Wikimedia Commons",
        "Species Icon": "frog"
    },
    {
        "Project name": "Kenyan rangeland restoration",
        "Organization/Project lead": "Natural State & Connor Wood",
        "Target species": "Birds",
        "Country": "Kenya",
        "Region/Location": "Lewa wildlife conservancy",
        "Latitude": 0.2253854,
        "Longitude": 37.4408517,
        "Contact": null,
        "Website": null,
        "Paper": null,
        "Species Image": "assets/img/dummy_birds_image.png",
        "Species Image Credit": "ChatGPT",
        "Species Icon": "feather"
    },
    {
        "Project name": "Endangered Species Monitoring",
        "Organization/Project lead": "Frowin Becker + Connor Wood",
        "Target species": "Birds",
        "Country": "Namibia",
        "Region/Location": "Etosha National Park",
        "Latitude": -18.8555909,
        "Longitude": 16.3293197,
        "Contact": null,
        "Website": null,
        "Paper": null,
        "Species Image": "assets/img/dummy_birds_image.png",
        "Species Image Credit": "ChatGPT",
        "Species Icon": "feather"
    },
    {
        "Project name": "Dhole monitoring",
        "Organization/Project lead": "Holger Klinck, Namitha Suresh",
        "Target species": "Dholes",
        "Country": "Nepal, India",
        "Region/Location": "Nepal, India",
        "Latitude": 28.394857,
        "Longitude": 84.124008,
        "Contact": null,
        "Website": null,
        "Paper": null,
        "Species Image": "https://upload.wikimedia.org/wikipedia/commons/7/7c/Cuon.alpinus-cut.jpg",
        "Species Image Credit": "Kalyanvarma via Wikimedia Commons",
        "Species Icon": "paw"
    },
    {
        "Project name": "Bavarian Forest National Park Monitoring",
        "Organization/Project lead": "Bavarian Forest National Park Service",
        "Target species": "Bird communities, Western Capercaillie",
        "Country": "Germany",
        "Region/Location": "Bavarian Forest National Park",
        "Latitude": 48.9596919,
        "Longitude": 13.39492,
        "Contact": null,
        "Website": null,
        "Paper": null,
        "Species Image": "https://upload.wikimedia.org/wikipedia/commons/5/59/Tetrao_urogallus%2C_Glenfeshie%2C_Scotland_1.jpg",
        "Species Image Credit": "sighmanb via Wikimedia Commons",
        "Species Icon": "feather"
    },
    {
        "Project name": "High elevation bird monitoring",
        "Organization/Project lead": "Vogelwarte Sempach",
        "Target species": "Rock Ptarmigan",
        "Country": "Switzerland",
        "Region/Location": "Swiss Alpes",
        "Latitude": 46.5601061,
        "Longitude": 8.5610781,
        "Contact": null,
        "Website": null,
        "Paper": null,
        "Species Image": "https://upload.wikimedia.org/wikipedia/commons/1/1f/Rock_Ptarmigan_%28Lagopus_Muta%29.jpg",
        "Species Image Credit": "Jan Frode Haugseth via Wikimedia Commons",
        "Species Icon": "feather"
    }
];