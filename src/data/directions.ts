import type { ImageMetadata } from 'astro';
import lidarCover from '../assets/covers/lidar.jpg';
import lidarCoverLight from '../assets/covers/lidar-light.jpg';
import eoCover from '../assets/covers/earth-observation.jpg';
import eoCoverLight from '../assets/covers/earth-observation-light.jpg';
import systemsCover from '../assets/covers/data-systems.jpg';
import systemsCoverLight from '../assets/covers/data-systems-light.jpg';
import type { DirectionId } from './direction-ids';

// Lab directions, in display order. The Lab page and each /blog/<id>/ page are built from this list.
// Posts and papers are attached automatically: posts by `direction:` in their frontmatter,
// papers by `direction` in PUBLICATIONS (src/data/profile.ts).
export type Direction = {
	id: DirectionId;
	kicker: string; // short label: Lab filter chips, card badges and the back-link on its posts
	title: string;
	line: string; // one sentence on the Lab card
	intro: string[]; // paragraphs at the top of the direction page; [text](https://…) makes a link
	cover: ImageMetadata; // dark theme
	coverLight: ImageMetadata; // light theme: same scene, lightness flipped (`python scripts/render-covers.py light`)
	coverAlt: string;
	// Tag colour (r, g, b) for this direction's badge on project cards and filter chips.
	accent: string;
};

export const DIRECTIONS: Direction[] = [
	{
		id: 'lidar',
		accent: '86, 156, 190',
		kicker: 'LiDAR & 3D',
		title: 'Point clouds & 3D scenes',
		line: 'Enclosed spaces GPS can’t reach, from handheld scans to labelled 3D models.',
		intro: [
			'I use LiDAR to capture and model 3D spaces, indoors and out. I’m especially interested in enclosed spaces, where GPS is unavailable and scans can be difficult to interpret. My master’s thesis focused on handheld scans of an underground parking garage, identifying walls, pillars, vehicles and ground, point by point.',
			'I’m continuing this work with public indoor datasets and scenes I collect myself. I also study how evaluation choices affect the results, including how dataset splits can change which model appears to perform best.',
		],
		cover: lidarCover,
		coverLight: lidarCoverLight,
		coverAlt:
			'Isometric point cloud of a room drawn as grey dots, with a table and two chairs picked out in red, blue and green.',
	},
	{
		id: 'earth-observation',
		accent: '76, 158, 120',
		kicker: 'Earth observation',
		title: 'Earth observation AI',
		line: 'Arctic seals (recall 52% → 87.7% after fine-tuning), PRISMA crop maps, and now satellite foundation models.',
		intro: [
			'My PhD asks what Earth-observation foundation models learn from satellite imagery, and how reliably they work in new regions.',
			'I came to this through the data. At the [Vision and Image Processing (VIP)](https://vip.uwaterloo.ca/) Lab, I used hyperspectral imagery to study vegetation and trained models to detect objects in satellite and aerial images. I have also measured methane plumes with airborne and satellite instruments. Working that close to the sensors shapes how I approach AI for Earth observation.',
		],
		cover: eoCover,
		coverLight: eoCoverLight,
		coverAlt:
			'Isometric terrain drawn as a grid of dots: a red plume drifts from a site on a ridge, with a blue river and green crop fields on the plain below.',
	},
	{
		id: 'data-systems',
		accent: '216, 58, 31',
		kicker: 'Data systems',
		title: 'Spatial data in production',
		line: 'What runs behind a Toronto fibre network every month: 450+ files in, capacity reports in under half a day instead of two.',
		intro: [
			'I build data systems that support infrastructure networks, connecting the data behind the scenes with the tools people use every day. My work spans pipelines, validation checks, web maps, APIs, and views that bring 2D and 3D data together.',
			'I enjoy untangling complex problems and turning them into straightforward tools, so people spend less time working around the data and more time using it.',
		],
		cover: systemsCover,
		coverLight: systemsCoverLight,
		coverAlt:
			'Isometric city blocks drawn as grey dots, with a red fibre route running along the streets from a blue hub building to three green buildings.',
	},
];

export const directionById = (id?: string) => DIRECTIONS.find((d) => d.id === id);
