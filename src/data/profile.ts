// ─────────────────────────────────────────────────────────────
// Single source of truth for the facts on the About page.
// ─────────────────────────────────────────────────────────────

import type { DirectionId } from './direction-ids';

export const PROFILE = {
	name: 'Kristie Hu',
	nameZh: '静祎',
	pronounce: '/jing-yee hoo/',
	// Shown under the name on the About page, one per line as "role · place". The place is the link.
	identity: [
		{
			role: 'PhD student',
			org: 'GIM Lab, University of Waterloo',
			href: 'https://uwaterloo.ca/geospatial-intelligence/profiles/kristie-j-hu', // her GIM Lab profile
		},
		{
			role: 'Application Data Analyst',
			org: 'Beanfield Metroconnect',
			href: 'https://www.linkedin.com/company/beanfieldcanada/', // Beanfield's LinkedIn page
		},
		{
			role: 'Vice President, Graduate Student Association',
			org: 'CE²GA',
			href: 'https://www.linkedin.com/company/civil-and-environmental-engineering-graduate-student-association-ce2ga/',
		},
		{
			role: 'Ambassador, Event Organizing Team',
			org: 'ISPRS STEP',
			href: 'https://sc.isprs.org/about/the-isprs-step/',
		},
	],
	supervisors: 'Prof. Shunde Yin and Prof. Jonathan Li', // not shown on the site since Oct 2026 (listed on the CV)
	links: {
		github: 'https://github.com/Kristiehu',
		linkedin: 'https://www.linkedin.com/in/kristiehu/',
		lab: 'https://uwaterloo.ca/geospatial-intelligence/', // GIM Lab homepage (her own lab profile is linked from the first identity line)
		email: 'mailto:kristieyet@gmail.com',
	},
	motto: '不坠青云志，常怀赤子心。',
};

export type Entry = {
	title: string; // degree or role
	org: string;
	dates: string;
	note?: string;
	href?: string;
};

export const EDUCATION: Entry[] = [
	{
		title: 'PhD, Civil and Environmental Engineering',
		org: 'University of Waterloo',
		dates: 'May 2026 – present',
	},
	{
		title: 'MSc, Geomatics',
		org: 'University of Waterloo',
		dates: '2022 – 2024',
		note: 'Thesis: Semantic Modelling of an Indoor Parking Garage Using Hand-held GeoSLAM LiDAR Point Clouds',
		href: 'https://uwspace.uwaterloo.ca/items/dcb172d9-cec1-487b-8b18-1226c0156061',
	},
	{
		title: 'BES, Honours Geospatial Data Science (Computing Minor, Co-op)',
		org: 'University of Waterloo',
		dates: '2017 – 2022',
		note: 'Diploma in Excellence in GIS',
	},
];

export const EXPERIENCE: Entry[] = [
	{
		title: 'Application Data Analyst',
		org: 'Beanfield Metroconnect, Toronto',
		dates: 'Apr 2025 – present',
		note: 'Automated geospatial ETL (450+ files/month), validation tools, dashboards and APIs for a fibre network.',
	},
	{
		title: 'Research Associate',
		org: 'Vision and Image Processing (VIP) Lab, University of Waterloo',
		dates: 'Sep 2024 – Apr 2025',
		note: 'PRISMA hyperspectral crop mapping; Arctic seal detection for Fisheries and Oceans Canada.',
	},
	{
		title: 'Research Associate',
		org: 'Geospatial Intelligence and Mapping (GIM) Lab, University of Waterloo',
		dates: 'May 2022 – Jun 2024',
		note: 'Indoor LiDAR-SLAM datasets, point-cloud segmentation and 3D reconstruction.',
	},
];

export type Publication = {
	authors: string;
	year: number | string;
	title: string;
	venue: string;
	url?: string;
	post?: string; // slug of the matching post in src/content/blog (link shows only once the post is published)
	status?: string; // e.g. "under review"
	direction?: DirectionId; // lists the paper on that Lab direction page (src/data/directions.ts)
};

// Grouped in the order they appear on the page.
export const PUBLICATIONS: { group: string; items: Publication[] }[] = [
	{
		group: 'Journal articles',
		items: [
			{
				authors: 'Hu, K. J., Chai, Y., Asgarpour, S., Boudreault, R., Li, J., & Yin, S.',
				year: 2026,
				title: 'Methane detection of super-emitters by remote sensing and investigation of wind-driven bias in complex terrain: A multi-instrument analysis',
				direction: 'earth-observation',
				venue: 'Mining, 6(2), 35',
				url: 'https://doi.org/10.3390/mining6020035',
				post: '13_methane-super-emitters-mining',
			},
			{
				authors: 'Fatholahi, S. N., Yin, S., Hu, K., He, H., Yao, K. Y., Zhang, D., Lu, D., Li, J., & Teng, J.',
				year: 2026,
				title: 'Comparative evaluation of deep-learning models for point cloud upsampling: Insights from indoor parking lot data set',
				direction: 'lidar',
				venue: 'Photogrammetric Engineering & Remote Sensing, 92(6)',
				url: 'https://doi.org/10.14358/PERS.25-00083R3',
			},
		],
	},
	{
		group: 'Workshop papers & preprints',
		items: [
			{
				authors: 'Hu, K., Knezevic, J., Zhang, P., Yin, S., Li, J., & Gao, K.',
				year: 2026,
				title: 'What or where? Class–site geometry and geographic transfer in geospatial embeddings',
				direction: 'earth-observation',
				venue: 'NeurIPS 2026 Workshop on Advances in Representation Learning for Earth Observation (REO-2)',
				post: '9_geofm-what-or-where',
			},
			{
				authors: 'Zhang, P., Hu, K., Knezevic, J., Yin, S., & Gao, K.',
				year: 2026,
				title: 'Recoverable geographic location information in Earth-observation embeddings',
				direction: 'earth-observation',
				venue: 'arXiv:2609.29151',
				url: 'https://arxiv.org/abs/2609.29151',
			},
		],
	},
	{
		group: 'Conference papers & presentations',
		items: [
			{
				authors: 'Hu, K. J., Shpir, M., Clausi, D., & Xu, L.',
				year: 2025,
				title: 'Unlocking the potential of PRISMA hyperspectral imagery for precision agriculture mapping',
				direction: 'earth-observation',
				venue: '46th Canadian Symposium on Remote Sensing (CSRS 2025)',
				post: '6_hsi-crop-mapping',
			},
			{
				authors: 'Hu, K. J., Clausi, D., & Xu, L.',
				year: 2025,
				title: 'Enhancing seal detection in Arctic regions through fine-tuning of Faster R-CNN: A case study using NOAA and DFO datasets',
				direction: 'earth-observation',
				venue: '46th Canadian Symposium on Remote Sensing (CSRS 2025)',
				post: '5_seal-detection',
			},
			{
				authors: 'Hu, K., Du, J., Gong, X., Ma, L., & Li, J.',
				year: 2023,
				title: 'A comparative study of semantic segmentation using deep neural networks in a GNSS-denied underground parking lot',
				direction: 'lidar',
				venue: 'Advances in Cartography and GIScience of the ICA, 4, 18 (ICC 2023)',
				url: 'https://doi.org/10.5194/ica-adv-4-18-2023',
				post: '4_semantic-segmentation-1',
			},
			{
				authors: 'Hu, K., & Li, J.',
				year: 2023,
				title: 'Using least cost path analysis to plan a new bypass route on Highway 401 to mitigate traffic congestion and impacts in the City of Toronto, Ontario',
				venue: 'Abstracts of the ICA, 6, 94 (ICC 2023)',
				url: 'https://doi.org/10.5194/ica-abs-6-94-2023',
				post: '3b_lcp-analsysi-for-hwy-401',
			},
			{
				authors: 'Hu, K. J., Mahboubi, M., Chen, Y., & Fatholahi, S.',
				year: 2022,
				title: 'Indirect detection of permafrost degradation in eastern Alaska using MODIS and Landsat data',
				direction: 'earth-observation',
				venue: 'XXVII FIG Congress, Warsaw, Poland',
				post: '3c_alaska-permaforst',
			},
		],
	},
	{
		group: 'Thesis',
		items: [
			{
				authors: 'Hu, K. J.',
				year: 2024,
				title: 'Semantic modelling of an indoor parking garage using hand-held GeoSLAM LiDAR point clouds',
				direction: 'lidar',
				venue: 'MSc thesis, University of Waterloo',
				url: 'https://uwspace.uwaterloo.ca/items/dcb172d9-cec1-487b-8b18-1226c0156061',
				post: '4_semantic-segmentation-2',
			},
		],
	},
];

export const AWARDS: Entry[] = [
	{ title: 'Caivan Future Cities Graduate Scholarship', org: 'University of Waterloo', dates: '2022' },
	{ title: 'International Master’s Award of Excellence (IMAE)', org: 'University of Waterloo', dates: '2022' },
];

export const TRAINING: Entry[] = [
	{
		title: 'i2I Skills Training',
		org: 'Invention to Innovation Research & Innovation Institute, SFU (NSERC)',
		dates: 'Fall 2026 cohort',
		href: 'https://inventiontoinnovation.ca/', // links the title
	},
	{
		title: 'RPAS Pilot Certificate - Basic Operations',
		org: 'Transport Canada',
		dates: '2026',
	},
];
