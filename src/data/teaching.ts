// ─────────────────────────────────────────────────────────────
// Data for the Teaching & Service page (src/pages/teaching.astro).
// Add a term, a course or a role here; the page layout updates itself.
// Empty sections are hidden automatically.
// ─────────────────────────────────────────────────────────────

export type Role = {
	role: string;
	org: string; // [text](https://…) makes a link
	start: string;
	end?: string; // leave out for a one-off role; use 'present' for ongoing
	points?: string[]; // [text](https://…) makes a link
};

// Shown under the heading "Leadership & Service" (set in src/pages/teaching.astro).
// LEADERSHIP is a name used in the code: no spaces or & allowed.
export const LEADERSHIP: Role[] = [
	{
		role: 'Program Committee',
		org: '[AAAI-27 SA](https://aaai.org/conference/aaai/aaai-27/), Association for the Advancement of Artificial Intelligence (AAAI), Montréal, Canada',
		start: 'Oct 2026',
		end: 'present',
	},
	{
		role: 'Vice President',
		org: 'Civil & Environmental Engineering Graduate Association (CE²GA), University of Waterloo',
		start: 'Sep 2026',
		end: 'present',
		points: [
			'Plan academic, social and student-support events with the executive team through biweekly meetings.',
			'Created and run the [CE²GA LinkedIn page](https://www.linkedin.com/company/civil-and-environmental-engineering-graduate-student-association-ce2ga/) to promote events and connect graduate students with industry.',
		],
	},
	{
		role: 'Ambassador',
		org: 'ISPRS Student and Early Professionals (ISPRS STEP)',
		start: 'Sep 2026',
		end: 'present',
		points: ['Support the organisation of ISPRS conferences, congresses and symposia.'],
	},
];

export type Course = {
	code: string;
	title: string;
	roles?: string[]; // e.g. ['Teaching Assistant', 'Guest lecture']
	tasks?: string[]; // e.g. ['Labs', 'Grading']
	terms?: string[]; // e.g. ['F22', 'W23'] (shown when filled in)
};

export type Institution = {
	institution: string;
	role?: string;
	courses: Course[];
};

// TODO(Kristie): add terms to each course. The old page showed "1.0 / 2.5"
// next to some courses without a unit; add them back as terms or leave them out.
export const TEACHING: Institution[] = [
	{
		institution: 'University of Waterloo',
		role: 'Teaching Assistant',
		courses: [
			{ code: 'GEOG 101', title: 'Human Geography' },
			{ code: 'GEOG 310', title: 'Geodesy & Land Surveying', },
			// roles: ['Guest lecture'] },
			{ code: 'GEOG 316', title: 'Multivariate Statistics' },
		],
	},
	{
		institution: 'University of Toronto',
		role: 'Part-time Tutor',
		courses: [
			{ code: 'GGRA30H3', title: 'Geographic Information Systems and Empirical Reasoning' },
			{ code: 'MGEA06H3', title: 'Advanced Geographic Information Systems' },
			{ code: 'GGR210H5S', title: 'Social Geographies' },
			{ code: 'GGR209H5S', title: 'Economic Geography' },
		],
	},
];

// Courses you have taken (PhD coursework). Leave empty to hide the section.
// Example: { code: 'CIVE 700', title: 'Course title', term: 'F26' }
export const COURSEWORK: { code: string; title: string; term?: string }[] = [
	// Hidden since Oct 2026. Uncomment a line to show the section again.
	// { code: 'GEOG 600', title: 'Foundations in Spatial Data Handling', term: 'Fall 2022' },
	// { code: 'GEOG 675', title: 'Selected Topics in Geography: LiDAR Remote Sensing', term: 'Fall 2022' },
	// { code: 'GEOG 700', title: 'Professional Skills Development for Master Students', term: 'Fall 2022' },
	// { code: 'SYDE 770', title: 'Selected Topics in Communication and Information: Remote Sensing Systems', term: 'Winter 2023' },
	// { code: 'CIVE 705', title: 'Subsurface Energy Storage Review', term: 'Fall 2026' },
];
